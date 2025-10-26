# ----------------------------------------
# 1️⃣ Setup the prompt dynamically
# ----------------------------------------

def build_fewshot_prompt(data_preamble: str) -> str:
    """
    Builds an efficient few-shot prompt for Ollama text generation on Raspberry Pi 5.
    Designed to ensure consistent outputs, natural flow, and minimal token overhead.
    Adapted for the environmental monitoring domain (air quality context).
    """

    # Define few-shot examples (concise but realistic)
    examples = [
    {
        "iot_data": """Location: Urban residential area
PM2.5 (µg/m³): 45
PM10 (µg/m³): 70
CO₂ (ppm): 850
NO₂ (ppm): 0.03
O₃ (ppm): 0.045
SO₂ (ppm): 0.006
Temperature (°C): 27
Humidity (%): 65
Wind speed (m/s): 2.1
Air Quality Index (AQI): 92
Time of day: Morning""",
        "response": """Hello Watanabe-san,
The morning air quality is moderate (AQI 92). PM2.5 at 45 µg/m³ means sensitive individuals should limit outdoor activities. CO₂ is slightly elevated (850 ppm), suggesting limited ventilation. Keep indoor windows open for cross-ventilation and avoid burning solid fuels. Temperature and humidity are comfortable, and mild winds help disperse pollutants. If you jog in the morning, prefer areas with more trees or near parks."""
    },
    {
        "iot_data": """Location: City center
PM2.5 (µg/m³): 120
PM10 (µg/m³): 160
CO₂ (ppm): 1100
NO₂ (ppm): 0.06
O₃ (ppm): 0.072
SO₂ (ppm): 0.008
Temperature (°C): 31
Humidity (%): 55
Wind speed (m/s): 0.8
Air Quality Index (AQI): 165
Time of day: Afternoon""",
        "response": """Hello Watanabe-san,
The air quality is unhealthy (AQI 165). PM2.5 and PM10 levels are high due to traffic and heat buildup. Limit prolonged outdoor exposure, especially for children or the elderly. Indoor CO₂ levels are also high—use air purifiers if available and increase ventilation at cooler times. Avoid using sprays or incense. When outdoors, wear a mask rated for particulate filtration. Conditions should improve after sunset as temperatures drop and winds increase."""
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
        "for an environmental officer providing practical air quality guidance "
        "for public health and pollution awareness. "
        "Avoid using special characters that may disrupt speech synthesis. "
        'Demonstrate clear understanding of air quality monitoring and start with "Hello Watanabe-san,".'
    )

    # Combine everything into one optimized prompt
    return (
        "You are an experienced environmental monitoring officer specializing in air quality and public health.\n\n"
        f"{fewshot_section}\n\n"
        f"New data:\n{data_preamble}\n\n"
        f"{generation_instruction}"
    )
