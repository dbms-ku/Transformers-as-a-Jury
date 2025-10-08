# ----------------------------------------
# 1️⃣ Setup the prompt dynamically
# ----------------------------------------

def build_fewshot_prompt(data_preamble: str) -> str:
    """
    Builds an efficient few-shot prompt for Ollama text generation on Raspberry Pi 5.
    Designed to ensure consistent outputs, natural flow, and minimal token overhead.
    """

    # Define few-shot examples (concise but realistic)
    examples = [
        {
            "iot_data": """Farm type: Paddy-rice farming
Days since planting: 20
Soil pH: 5.8
Soil temperature: 14°C
Soil moisture: 78
Soil nitrogen: 30
Soil potassium: 65
Soil phosphorus: 40
Soil electrical conductivity: 1.05
Atmospheric temperature: 18°C
Atmospheric humidity: 60
Atmospheric rainfall state: Light rain
Atmospheric sunshine intensity: Moderate""",
            "response": """Hello Watanabe-san,
Your paddy field is doing well! At 20 days since planting, strong roots and leaves are developing. Keep your soil pH around 5.8—below 5.5 may cause iron toxicity. Soil nitrogen (30) is good; avoid adding more to protect water quality. Soil moisture (78) is excellent; light rain helps, but prevent over-flooding. The temperature (18°C) is slightly low, so maintain water depth to stabilize soil warmth. Your plants look on track for healthy growth."""
        },
        {
            "iot_data": """Farm type: Paddy-rice farming
Days since planting: 120
Soil pH: 5.6
Soil temperature: 17°C
Soil moisture: 65
Soil nitrogen: 12
Soil potassium: 58
Soil phosphorus: 35
Soil electrical conductivity: 0.95
Atmospheric temperature: 22°C
Atmospheric humidity: 45
Atmospheric rainfall state: No rain
Atmospheric sunshine intensity: Moderate to high""",
            "response": """Hello Watanabe-san,
You are near harvest time! With soil moisture at 65%, begin draining the field gradually to dry the grains. Stop irrigation two weeks before harvest. Nitrogen is low (12), which is normal—don’t add more. Potassium and phosphorus are stable, supporting grain filling. With 22°C and good sunlight, ripening should go smoothly. If storms are forecast, harvest early. Dry grains to 14% for storage—great work so far!"""
        }
    ]

    # Construct the few-shot prompt with minimal formatting overhead
    fewshot_section = "\n\n".join(
        [
            f"Scenario {i+1}:\n{ex['iot_data']}\nResponse:\n{ex['response']}"
            for i, ex in enumerate(examples)
        ]
    )

    # Main generation instruction
    generation_instruction = (
        "Now, based on the pattern above, use the following new data.\n"
        "Write a conversational instructional script (max 200 words) "
        "for an agricultural extension officer teaching best practices "
        "for good yield and environmental safety. "
        "Avoid using special characters that may disrupt speech synthesis. "
        'Demonstrate clear understanding of paddy-rice farming and start with "Hello Watanabe-san,".'
    )

    # Combine everything into one optimized prompt
    return (
        "You are an experienced agricultural extension officer specializing in paddy-rice farming.\n\n"
        f"{fewshot_section}\n\n"
        f"New data:\n{data_preamble}\n\n"
        f"{generation_instruction}"
    )
