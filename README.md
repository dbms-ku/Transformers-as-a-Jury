# Transformers-as-a-Jury (TaaJ)
Transformers-as-a-Jury: Mimicking LLM-as-a-Judge Text Evaluation on Edge Devices

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)  
[![PyTorch](https://img.shields.io/badge/pytorch-2.x-red.svg)](https://pytorch.org/)  
[![Edge AI](https://img.shields.io/badge/edge-AI-green.svg)]()  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

The **Transformers-as-a-Jury (TaaJ)** project provides a lightweight, on-device alternative to **LLM-as-a-Judge** systems.  
Instead of relying on large, cloud-hosted models for automated text evaluation, TaaJ leverages compact transformer architectures fine-tuned on **LLM-labelled datasets** to enable **local, low-latency, and privacy-preserving text evaluation**.

This approach is particularly suited for **edge deployments** where bandwidth, compute power, and energy are constrained.  

**Key innovation**: TaaJ mimics the evaluation capabilities of cloud-based judges while running efficiently on devices such as the **Raspberry Pi 5**.

---

## Features

-  **On-device evaluation**: Run locally without cloud calls.  
-  **LLM-mimicking scoring**: Compact transformers replicate the judgment of large LLMs.  
-  **Agricultural use case demo**: Evaluate generated farm advisory text on a Raspberry Pi 5.  
-  **Privacy-first**: Keeps all text and evaluation on-device.  
-  **Open-source PyTorch & Ollama integration**: Easy to extend and adapt.  

---

## Methodology
Domain-agnostic 5-step methodology for TaaJ.

```text
  ┌─────────────────────────────┐
 │  Step 1: On-device Text Gen │
 │  • Prompts + IoT (Sobol)    │
 │  • Compact Ollama Models    │
 └─────────────────────────────┘
               │
               ▼
 ┌─────────────────────────────┐
 │  Step 2: Dataset Labelling  │
 │  • Candidate Texts          │
 │  • LLM-as-a-Judge (70B)     │
 │  • Criteria: clarity, etc.  │
 └─────────────────────────────┘
               │
               ▼
 ┌─────────────────────────────┐
 │ Step 3: Training of TaaJ    │
 │  • DistilBERT per criterion │
 │  • Weighted focal loss       │
 │  • Early stopping            │
 └─────────────────────────────┘
               │
               ▼
 ┌─────────────────────────────┐
 │ Step 4: Deployment          │
 │  • Transfer to RPi 5        │
 │  • Memory-fit optimization  │
 │  • Ollama runtime ready     │
 └─────────────────────────────┘
               │
               ▼
 ┌─────────────────────────────┐
 │ Step 5: System Testing      │
 │  • Evaluate new texts       │
 │  • Compare with LLM-Judge   │
 │  • Regenerate if < threshold│
 │  • Collect metrics          │
 └─────────────────────────────┘
```

## Installation
```bash
git clone https://github.com/<your-username>/taaj.git
cd taaj
pip install -r requirements.txt
```
