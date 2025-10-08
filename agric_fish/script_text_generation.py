import csv
import time
import random
import datetime
import subprocess
import re
import signal
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
from scipy.stats.qmc import Sobol
from ollama import Client
from text_generation_prompt import PROMPT_TEMPLATES  # ensure you have fish pond templates here too

# -------------------------------
# Configuration
# -------------------------------
NUM_RESPONSES = 1001
CSV_WRITE_INTERVAL = 20
SEED = 42
FARM_TYPES = ["Fish Pond"]
RAIN_STATES = ["No Rain", "Dew", "Light Rain", "Heavy Rain"]
SUNSHINE_INTENSITIES = ["Low", "Moderate", "High"]
CSV_FILE_PATH = f"data/agric_fish/exp%%experiment%%-responses%%NUM_RESPONSES%%-%%model_name%%.csv"

# -------------------------------
# Timeout setup
# -------------------------------
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Operation timed out")

TIMEOUT = 2 * 60 * 60  # 2 hours

# -------------------------------
# Ollama model client
# -------------------------------
client = Client()

# -------------------------------
# Sobol setup
# d = 14 → number of IoT parameters
# -------------------------------
sobol = Sobol(d=14, scramble=True, seed=SEED)

def scale_sobol_vector(vector: List[float]) -> Dict[str, Any]:
    return {
        "water_temperature": round(20 + vector[0] * 15, 2),     # 20–35°C
        "dissolved_oxygen": round(3 + vector[1] * 7, 2),        # 3–10 mg/L
        "water_ph": round(6 + vector[2] * 3, 2),                # 6–9
        "water_ec": round(200 + vector[3] * 1800, 2),           # 200–2000 µS/cm
        "turbidity": round(10 + vector[4] * 100, 2),            # 10–110 NTU
        "ammonia_level": round(vector[5] * 2, 3),               # 0–2 mg/L
        "nitrate_level": round(vector[6] * 100, 2),             # 0–100 mg/L
        "nitrite_level": round(vector[7] * 5, 2),               # 0–5 mg/L
        "water_level": round(50 + vector[8] * 100, 2),          # 50–150 cm
        "feed_rate": round(1 + vector[9] * 9, 2),               # 1–10 g/fish/day
        "avg_fish_weight": round(5 + vector[10] * 995, 2),      # 5–1000 g
        "air_temperature": round(15 + vector[11] * 25, 2),      # 15–40°C
        "air_humidity": round(vector[12] * 100, 2),             # 0–100%
        "days_since_stocking": int(1 + vector[13] * 179),       # 1–180 days
    }

def random_choice(seq):
    return random.choice(seq)

# -------------------------------
# Prompt Assembly
# -------------------------------
def make_prompt(pcp: Dict[str, Any], experiment: int) -> str:
    replacements = {
        "farm_type": random_choice(FARM_TYPES),
        "days_since_stocking": pcp["days_since_stocking"],
        "water_temperature": pcp["water_temperature"],
        "dissolved_oxygen": pcp["dissolved_oxygen"],
        "water_ph": pcp["water_ph"],
        "water_ec": pcp["water_ec"],
        "turbidity": pcp["turbidity"],
        "ammonia_level": pcp["ammonia_level"],
        "nitrate_level": pcp["nitrate_level"],
        "nitrite_level": pcp["nitrite_level"],
        "water_level": pcp["water_level"],
        "feed_rate": pcp["feed_rate"],
        "avg_fish_weight": pcp["avg_fish_weight"],
        "air_temperature": pcp["air_temperature"],
        "air_humidity": pcp["air_humidity"],
        "rainfall_state": random_choice(RAIN_STATES),
        "sunshine_intensity": random_choice(SUNSHINE_INTENSITIES),
    }
    prompt = PROMPT_TEMPLATES[experiment]
    for key, val in replacements.items():
        prompt = prompt.replace(f"{{{{{key}}}}}", str(val))
    return prompt, replacements

# -------------------------------
# CSV Writing
# -------------------------------
def write_to_csv(file_path: str, rows: List[Dict[str, Any]], header_written: bool = False):
    with open(file_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        if not header_written and f.tell() == 0:
            writer.writeheader()
        writer.writerows(rows)

# -------------------------------
# Ollama Model Management
# -------------------------------
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

# -------------------------------
# Experiment Runner
# -------------------------------
def run_experiment(model_name: str, experiment: int):
    csv_file_path = CSV_FILE_PATH.replace("%%experiment%%", str(experiment)) \
                                 .replace("%%model_name%%", model_name) \
                                 .replace("%%NUM_RESPONSES%%", str(NUM_RESPONSES))

    print(f"Starting agric_fish data generation at {datetime.datetime.now()}")
    print(f"Experiment number: {experiment}")
    print(f"Using model: {model_name}")
    print(f"Number of responses to generate: {NUM_RESPONSES}")
    print(f"CSV file path: {csv_file_path}")

    header_written = Path(csv_file_path).exists()
    results = []

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

# -------------------------------
# Main Execution
# -------------------------------
if __name__ == "__main__":
    model_names = ["tinydolphin", "falcon:7b", "vicuna:7b", "phi3:3.8b", "openchat:7b", "mistral", "llama3.2"]
    experiments = [1, 2, 3, 4]

    for model_name in model_names:
        uninstall_all_ollama_models(model_names)
        install_ollama_model(model_name)
        for experiment in experiments:
            run_experiment(model_name, experiment)
