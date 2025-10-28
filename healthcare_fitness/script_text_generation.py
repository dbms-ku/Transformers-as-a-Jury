import csv
import time
import random
import datetime
import subprocess
from pathlib import Path
from typing import List, Dict, Any
from text_generation_prompt import PROMPT_TEMPLATES  # now includes fitness prompts

import numpy as np
from scipy.stats.qmc import Sobol
from ollama import Client
import signal
import re

# Configuration
NUM_RESPONSES = 1001
CSV_WRITE_INTERVAL = 20
SEED = 42
USER_PROFILES = ["Fitness Monitoring"]
USER_TYPES = ["Athlete", "Office Worker", "Elderly", "Student", "Manual Laborer"]
USER_GENDERS = ["Male", "Female", "Non-binary"]
USER_PROFILES = ["beginner", "intermediate", "advanced"]
ACTIVITY_TYPES = ["running", "walking", "cycling", "resting", "strength training", "swimming"]
STRESS_LEVELS = ["low", "moderate", "high"]
CSV_FILE_PATH = f"data/exp%%experiment%%-responses%%NUM_RESPONSES%%-%%model_name%%.csv"


# Timeout handling
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Operation timed out")

TIMEOUT = 2 * 60 * 60  # 2 hours

client = Client()
sobol = Sobol(d=15, scramble=True, seed=SEED)


def scale_sobol_vector(vector: List[float]) -> Dict[str, Any]:
    """
    Map Sobol-generated random numbers to realistic IoT/wearable fitness parameters.
    Values are derived from ranges observed in fitness trackers and medical devices.
    """
    return {
        "age": int(18 + vector[0] * 52),  # 18–70 years
        "heart_rate": int(50 + vector[1] * 100),  # 50–150 bpm
        "hrv": round(20 + vector[2] * 120, 2),  # 20–140 ms
        "spo2": round(90 + vector[3] * 10, 2),  # 90–100%
        "body_temperature": round(36.0 + vector[4] * 2.0, 2),  # 36–38°C
        "skin_temperature": round(32.0 + vector[5] * 5.0, 2),  # 32–37°C
        "respiratory_rate": int(10 + vector[6] * 12),  # 10–22 breaths/min
        "step_count": int(500 + vector[7] * 19500),  # 500–20,000 steps
        "activity_duration": int(5 + vector[8] * 175),  # 5–180 minutes
        "calories_burned": int(100 + vector[9] * 1200),  # 100–1300 kcal
        "stress_level": round(vector[10] * 100, 2),  # 0–100
        "sleep_duration": round(3 + vector[11] * 7, 2),  # 3–10 hours
        "sleep_quality": round(vector[12] * 100, 2),  # 0–100
        "ambient_temperature": round(18 + vector[13] * 12, 2),  # 18–30°C
        "ambient_humidity": round(30 + vector[14] * 60, 2),  # 30–90%
    }


def random_choice(seq):
    return random.choice(seq)


def make_prompt(pcp: Dict[str, Any], experiment: int) -> str:
    """
    Creates a natural-language prompt by filling in wearable/IoT fitness parameters.
    Suitable for generative AI health coaching tasks.
    """
    replacements = {
        "user_type": random_choice(USER_TYPES),
        "age": pcp["age"],
        "gender": random_choice(USER_GENDERS),
        "heart_rate": pcp["heart_rate"],
        "hrv": pcp["hrv"],
        "spo2": pcp["spo2"],
        "body_temperature": pcp["body_temperature"],
        "skin_temperature": pcp["skin_temperature"],
        "respiratory_rate": pcp["respiratory_rate"],
        "step_count": pcp["step_count"],
        "activity_duration": pcp["activity_duration"],
        "calories_burned": pcp["calories_burned"],
        "stress_level": pcp["stress_level"],
        "sleep_duration": pcp["sleep_duration"],
        "sleep_quality": pcp["sleep_quality"],
        "ambient_temperature": pcp["ambient_temperature"],
        "ambient_humidity": pcp["ambient_humidity"],
        "activity_type": random_choice(ACTIVITY_TYPES),
        "user_profile": random_choice(USER_PROFILES),
        "stress_state": random_choice(STRESS_LEVELS),
    }

    # Example prompt template (replace PROMPT_TEMPLATES with your actual list)
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

    print(f"Starting fitness data generation at {datetime.datetime.now()}")
    print(f"Experiment number: {experiment}")
    print(f"Using model: {model_name}")
    print(f"Number of responses to generate: {NUM_RESPONSES}")
    print(f"CSV file path: {csv_file_path}")
    print(f"CSV write interval: {CSV_WRITE_INTERVAL}")
    print(f"Seed for Sobol sequence: {SEED}")
    print(f"User profiles: {USER_PROFILES}")

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
