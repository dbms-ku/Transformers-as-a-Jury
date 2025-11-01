import csv
import time
import random
import datetime
import subprocess
from pathlib import Path
from typing import List, Dict, Any
from text_generation_prompt import PROMPT_TEMPLATES

import numpy as np
from scipy.stats.qmc import Sobol
from ollama import Client
import signal

# Configuration
NUM_RESPONSES = 1001
CSV_WRITE_INTERVAL = 20
SEED = 42
FARM_TYPES = ["Paddy Rice"]
# FARM_TYPES = ["Paddy Rice", "Maize", "Soybean", "Wheat"]
RAINFALL_STATES = ["No Rain", "Dew", "Light Rain", "Heavy Rain"]
SUNSHINE_INTENSITIES = ["Low", "Moderate", "High"]
CSV_FILE_PATH = f"data/exp%%experiment%%-responses%%NUM_RESPONSES%%-%%model_name%%.csv"


# Define a custom timeout exception
class TimeoutException(Exception):
    pass

# Define a handler for the alarm signal
def timeout_handler(signum, frame):
    raise TimeoutException("Operation timed out")

# Set the timeout duration (in seconds)
TIMEOUT = 2*60*60 # 2 hours 

# Initialize model client
client = Client()

# Generate Sobol sequence
sobol = Sobol(d=12, scramble=True, seed=SEED)


def scale_sobol_vector(vector: List[float]) -> Dict[str, Any]:
    return {
        "soil_nitrogen": round(vector[0] * 2000, 2),
        "soil_potassium": round(vector[1] * 2000, 2),
        "soil_phosphorous": round(vector[2] * 2000, 2),
        "soil_ec": round(vector[3] * 10000, 2),
        "ph": round(vector[4] * 14, 2),
        "soil_temperature": round(10 + vector[5] * 30, 2),
        "soil_moisture": round(20 + vector[6] * 60, 2),
        "ambient_temperature": round(10 + vector[7] * 30, 2),
        "atmospheric_humidity": round(vector[8] * 100, 2),
        "days_since_planting": int(1 + vector[9] * 199),
        "summary_hours": int(1 + vector[10] * 999),
        "water_level": round(vector[11] * 50, 2),
    }


def random_choice(seq):
    return random.choice(seq)


def make_prompt(pcp: Dict[str, Any], experiment: int) -> str:
    replacements = {
        "farm_type": random_choice(FARM_TYPES),
        "days_since_planting": pcp["days_since_planting"],
        "ph": pcp["ph"],
        "soil_temperatute": pcp["soil_temperature"],
        "soil_moisture": pcp["soil_moisture"],
        "soil_nitrogen": pcp["soil_nitrogen"],
        "soil_potassium": pcp["soil_potassium"],
        "soil_phosphorous": pcp["soil_phosphorous"],
        "soil_ec": pcp["soil_ec"],
        "water_level": pcp["water_level"],
        "ambient_temperature": pcp["ambient_temperature"],
        "atmospheric_humidity": pcp["atmospheric_humidity"],
        "rainfall_state": random_choice(RAINFALL_STATES),
        "sunshine_intensity": random_choice(SUNSHINE_INTENSITIES)
    }
    prompt = PROMPT_TEMPLATES[experiment]
    for key, val in replacements.items():
        prompt = prompt.replace(f"%%{key}%%", str(val))
    return prompt, replacements


def write_to_csv(file_path: str, rows: List[Dict[str, Any]], header_written: bool = False):
    with open(file_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        if not header_written and f.tell() == 0:
            writer.writeheader()
        writer.writerows(rows)

def run_command(command):
    """
    Run a shell command and return the output and error if any.
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e.stderr.strip()}")
        return None

def parse_model_list(output):
    """
    Parse the output of 'ollama list' to extract valid model names.
    """
    models = []
    lines = output.splitlines()
    for line in lines:
        # Match only lines that look like "model_name:tag    id    size    modified"
        match = re.match(r"^\s*([\w\-]+:[\w\-]+)", line)
        if match:
            models.append(match.group(1))
    return models
    
def uninstall_all_ollama_models(model_names):
    """
    Uninstall all Ollama models.
    """
    print("Fetching installed Ollama models...")
    
    for model_name in model_names:
        print(f"Uninstalling model: {model_name}")
        uninstall_command = f"ollama rm {model_name}"
        run_command(uninstall_command)
        print(f"Model {model_name} uninstalled.")


def install_ollama_model(model_name):
    """
    Install a specified Ollama model.
    """
    print(f"Installing Ollama model: {model_name}")
    install_command = f"ollama pull {model_name}"
    run_command(install_command)
    print(f"Model {model_name} installed.")



def run_experiment(model_name: str, experiment: int):
    csv_file_path = CSV_FILE_PATH.replace("%%experiment%%", str(experiment)) \
                                 .replace("%%model_name%%", model_name) \
                                 .replace("%%NUM_RESPONSES%%", str(NUM_RESPONSES))

    print(f"Starting data generation at {datetime.datetime.now()}")
    print(f"Experiment number: {experiment}")
    print(f"Using model: {model_name}")
    print(f"Number of responses to generate: {NUM_RESPONSES}")
    print(f"CSV file path: {csv_file_path}")
    print(f"CSV write interval: {CSV_WRITE_INTERVAL}")
    print(f"Seed for Sobol sequence: {SEED}")
    print(f"Farm types: {FARM_TYPES}")

    header_written = Path(csv_file_path).exists()
    results = []

    print("Generating data...")

    for i in range(NUM_RESPONSES):
        pcp = scale_sobol_vector(sobol.random()[0])
        prompt, pcp_values = make_prompt(pcp, experiment)

        print(f"Model: {model_name} - Experiment: {experiment} - Generating response {i + 1}/{NUM_RESPONSES}...")
        start_time = time.time()

        try:
            # Register signal handler
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(TIMEOUT)

            # Attempt model call
            response = client.chat(model=model_name, messages=[{"role": "user", "content": prompt}])

        except TimeoutException as e:
            print(f"⚠️ Timeout on response {i + 1}: {e}")
            response = {"message": {"content": "Timeout occurred"}, "eval_count": "N/A"}

        except Exception as e:
            print(f"⚠️ Error on response {i + 1}: {e}")
            response = {"message": {"content": f"Error: {e}"}, "eval_count": "N/A"}

        finally:
            # Always disable alarm to avoid affecting next iteration
            signal.alarm(0)

        duration = time.time() - start_time

        result = {
            "#": str(i + 1),
            "prompt": prompt,
            "response": response['message']['content'],
            "duration_sec": round(duration, 6),
            "token_count": response.get("eval_count", "N/A"),
            **dict(pcp_values),
        }

        results.append(result)

        # Periodic CSV writing
        if (i + 1) % CSV_WRITE_INTERVAL == 0:
            write_to_csv(csv_file_path, results, header_written)
            header_written = True
            results.clear()

    # Write any remaining results
    if results:
        write_to_csv(csv_file_path, results, header_written)


if __name__ == "__main__":
    model_names = [
        # "tinydolphin", "falcon:7b", 
        "vicuna:7b", "phi3:3.8b", "openchat:7b", "mistral", "llama3.2"]
    experiments = [1, 2, 3, 4]

    for model_name in model_names:
        
        uninstall_all_ollama_models(model_names)
        install_ollama_model(model_name)

        for experiment in experiments:
            run_experiment(model_name, experiment)