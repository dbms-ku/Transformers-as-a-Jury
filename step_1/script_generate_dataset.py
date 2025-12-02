import csv
import time
import random
import datetime
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Any
from prompt_text import PROMPT_TEMPLATES
from pathlib import Path

import numpy as np
from scipy.stats.qmc import Sobol
from ollama import Client

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Configuration
NUM_RESPONSES = 5
CSV_WRITE_INTERVAL = 2
SEED = 42
FARM_TYPES = ["Paddy Rice"]
RAINFALL_STATES = ["No Rain", "Dew", "Light Rain", "Heavy Rain"]
SUNSHINE_INTENSITIES = ["Low", "Moderate", "High"]

DATA_DIR = "data"
taaj_model_dir = "../trained_taaj_models"


evaluation_criteria_cols = [
    'relevance_score','clarity_score', 'fluency_score', 'visual_score', 'cultural_score',
    'innovation_score', 'safety_score', 'environmental_score', 'costeffectiveness_score', 
    'scalability_score', 'gender_score'
]

# Initialize
client = Client()
sobol = Sobol(d=12, scramble=True, seed=SEED)

def predict_taaj(text: str, taaj_model, taaj_tokenizer, taaj_device) -> Dict[str, Any]:
    inputs = taaj_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    inputs = {k: v.to(taaj_device) for k, v in inputs.items()}
    start_time = time.time()
    with torch.no_grad():
        outputs = taaj_model(**inputs)
    duration = time.time() - start_time
    logits = outputs.logits
    prediction = torch.argmax(logits, dim=-1).item()
    return {
        "prediction": prediction,
        "response_time": round(duration, 2)
    }

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
        "water_level": round(5 + vector[11] * 25, 2),
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

def run_experiment(model_name: str, experiment: int, taaj_model=None, taaj_tokenizer=None, taaj_device=None, criteria_model=None):
    CSV_FILE_PATH = f"{DATA_DIR}/cry{criteria_model}_exp{experiment}-responses-{model_name}-{NUM_RESPONSES}.csv"
    print(f"Starting data generation at {datetime.datetime.now()}")
    print(f"Experiment number: {experiment}")
    print(f"Using model: {model_name}")
    print(f"Number of responses to generate: {NUM_RESPONSES}")
    print(f"CSV file path: {CSV_FILE_PATH}")
    header_written = Path(CSV_FILE_PATH).exists()
    results = []

    for i in range(NUM_RESPONSES):
        pcp = scale_sobol_vector(sobol.random()[0])
        prompt, pcp_values = make_prompt(pcp, experiment)

        print(f"Generating response {i + 1}/{NUM_RESPONSES}...")
        start_time = time.time()
        response = client.chat(model=model_name, messages=[{"role": "user", "content": prompt}])
        # response = {"message": {"content": f"Mock response for {prompt}"}}
        duration = time.time() - start_time

        if taaj_model and taaj_tokenizer and taaj_device:
            taaj_result = predict_taaj(response['message']['content'], taaj_model, taaj_tokenizer, taaj_device)
        else:
            taaj_result = {"prediction": "", "response_time": ""}

        result = {
            "#": str(1 + i),
            "prompt": prompt,
            "response": response['message']['content'],
            "duration_sec": round(duration, 2),
            "token_count": response.get("eval_count", "N/A"),
            "taaj_prediction": taaj_result["prediction"],
            "taaj_response_time_sec": taaj_result["response_time"],
            **dict(pcp_values),
        }

        results.append(result)

        if (i + 1) % CSV_WRITE_INTERVAL == 0:
            write_to_csv(CSV_FILE_PATH, results, header_written)
            header_written = True
            results.clear()

    if results:
        write_to_csv(CSV_FILE_PATH, results, header_written)

if __name__ == "__main__":
    use_taaj_model = True  # Set to True to run with TAAJ model
    model_names = ["falcon:7b", "phi3:3.8b", "tinydolphin", "llama3.2", "mistral", "openchat:7b", "vicuna:7b"]
    experiments = [1, 2, 3, 4]
    criteria_models = [0, 1, 2, 6]

    if use_taaj_model:
        for model_name in model_names:
            uninstall_all_ollama_models(model_names)
            install_ollama_model(model_name)

            for criteria_model in criteria_models:
                TAAJ_MODEL_NAME = f"fine_tuned_taaj_model_{evaluation_criteria_cols[criteria_model]}"
                TAAJ_MODEL_PATH = Path(f"{taaj_model_dir}/{TAAJ_MODEL_NAME}/final_model").resolve()
                TAAJ_TOKENIZER_PATH = Path(f"{taaj_model_dir}/{TAAJ_MODEL_NAME}/tokenizer").resolve()

                print(TAAJ_MODEL_PATH)
                print(TAAJ_TOKENIZER_PATH)

                # Load TAAJ model and tokenizer
                taaj_tokenizer = AutoTokenizer.from_pretrained(str(TAAJ_TOKENIZER_PATH), local_files_only=True)
                taaj_model = AutoModelForSequenceClassification.from_pretrained(str(TAAJ_MODEL_PATH), local_files_only=True)
                taaj_model.eval()
                taaj_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                taaj_model.to(taaj_device)

                for experiment in experiments:
                    run_experiment(model_name, experiment, taaj_model, taaj_tokenizer, taaj_device, criteria_model)
    else:
        for model_name in model_names:
            uninstall_all_ollama_models(model_names)
            install_ollama_model(model_name)

            for experiment in experiments:
                run_experiment(model_name, experiment)