import csv
import time
import random
import datetime
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Any
from text_generation_prompt import PROMPT_TEMPLATES

import numpy as np
from scipy.stats.qmc import Sobol
from ollama import Client
import signal

# ----------------------------------------
# Configuration
# ----------------------------------------
NUM_RESPONSES = 1001
CSV_WRITE_INTERVAL = 20
SEED = 42
LOCATIONS = ["Urban Residential", "City Center", "Industrial Area", "Suburban", "Rural"]
TIMES_OF_DAY = ["Morning", "Afternoon", "Evening", "Night"]
CSV_FILE_PATH = f"data/exp%%experiment%%-responses%%NUM_RESPONSES%%-%%model_name%%.csv"

# ----------------------------------------
# Timeout handler
# ----------------------------------------
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Operation timed out")

TIMEOUT = 2 * 60 * 60  # 2 hours
client = Client()

# ----------------------------------------
# Sobol sequence setup
# ----------------------------------------
sobol = Sobol(d=12, scramble=True, seed=SEED)


def scale_sobol_vector(vector: List[float]) -> Dict[str, Any]:
    """
    Maps Sobol-generated random numbers to realistic air quality sensor parameters.
    """
    return {
        "pm2_5": round(vector[0] * 200, 2),              # µg/m³
        "pm10": round(vector[1] * 250, 2),               # µg/m³
        "co2": round(350 + vector[2] * 2000, 2),         # ppm
        "no2": round(vector[3] * 0.2, 3),                # ppm
        "o3": round(vector[4] * 0.15, 3),                # ppm
        "so2": round(vector[5] * 0.05, 3),               # ppm
        "temperature": round(5 + vector[6] * 35, 2),     # °C
        "humidity": round(vector[7] * 100, 2),           # %
        "wind_speed": round(vector[8] * 10, 2),          # m/s
        "aqi": int(20 + vector[9] * 300),                # Air Quality Index
        "ambient_pressure": round(980 + vector[10] * 40, 2), # hPa
        "visibility": round(1 + vector[11] * 9, 2),      # km
    }


def random_choice(seq):
    return random.choice(seq)


def make_prompt(pcp: Dict[str, Any], experiment: int) -> str:
    """
    Build the textual prompt for the Ollama model using environmental parameters.
    """
    replacements = {
        "location": random_choice(LOCATIONS),
        "time_of_day": random_choice(TIMES_OF_DAY),
        "pm2_5": pcp["pm2_5"],
        "pm10": pcp["pm10"],
        "co2": pcp["co2"],
        "no2": pcp["no2"],
        "o3": pcp["o3"],
        "so2": pcp["so2"],
        "temperature": pcp["temperature"],
        "humidity": pcp["humidity"],
        "wind_speed": pcp["wind_speed"],
        "aqi": pcp["aqi"],
        "ambient_pressure": pcp["ambient_pressure"],
        "visibility": pcp["visibility"]
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
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e.stderr.strip()}")
        return None


def parse_model_list(output):
    models = []
    lines = output.splitlines()
    for line in lines:
        match = re.match(r"^\s*([\w\-]+:[\w\-]+)", line)
        if match:
            models.append(match.group(1))
    return models


def uninstall_all_ollama_models(model_names):
    print("Fetching installed Ollama models...")
    for model_name in model_names:
        print(f"Uninstalling model: {model_name}")
        uninstall_command = f"ollama rm {model_name}"
        run_command(uninstall_command)
        print(f"Model {model_name} uninstalled.")


def install_ollama_model(model_name):
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
    print(f"Locations: {LOCATIONS}")

    header_written = Path(csv_file_path).exists()
    results = []

    print("Generating data...")

    for i in range(NUM_RESPONSES):
        pcp = scale_sobol_vector(sobol.random()[0])
        prompt, pcp_values = make_prompt(pcp, experiment)

        print(f"Model: {model_name} - Experiment: {experiment} - Generating response {i + 1}/{NUM_RESPONSES}...")
        start_time = time.time()

        try:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(TIMEOUT)
            response = client.chat(model=model_name, messages=[{"role": "user", "content": prompt}])

        except TimeoutException as e:
            print(f"⚠️ Timeout on response {i + 1}: {e}")
            response = {"message": {"content": "Timeout occurred"}, "eval_count": "N/A"}

        except Exception as e:
            print(f"⚠️ Error on response {i + 1}: {e}")
            response = {"message": {"content": f"Error: {e}"}, "eval_count": "N/A"}

        finally:
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

        if (i + 1) % CSV_WRITE_INTERVAL == 0:
            write_to_csv(csv_file_path, results, header_written)
            header_written = True
            results.clear()

    if results:
        write_to_csv(csv_file_path, results, header_written)


if __name__ == "__main__":
    model_names = ["tinydolphin", "falcon:7b", "vicuna:7b", "phi3:3.8b", "openchat:7b", "mistral", "llama3.2"]
    experiments = [1, 2, 3, 4]

    for model_name in model_names:
        uninstall_all_ollama_models(model_names)
        install_ollama_model(model_name)

        for experiment in experiments:
            run_experiment(model_name, experiment)
