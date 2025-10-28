# ----------------------------------------
# 🩺 1️⃣ Setup the prompt dynamically (Healthcare / Fitness version)
# ----------------------------------------

def build_fewshot_prompt(data_preamble: str) -> str:
    """
    Builds an efficient few-shot prompt for Ollama text generation on Raspberry Pi 5.
    Designed to generate personalized, natural, and health-coaching-style messages 
    based on IoT or wearable sensor data.
    """

    # Define few-shot examples (realistic wearable fitness data)
    examples = [
        {
            "iot_data": """User profile: Fitness monitoring
Steps today: 8420
Heart rate (bpm): 74
Sleep duration (hours): 6.2
Body temperature (°C): 36.7
Blood oxygen (SpO2): 97
Respiratory rate (breaths/min): 16
Stress level: Moderate
Calories burned (kcal): 420
Hydration level: Slightly low
Activity duration (minutes): 45
""",
            "response": """Hello Watanabe-san,
You’re doing well today! You’ve walked about 8400 steps and stayed active for 45 minutes—great progress toward your daily goal. Your heart rate of 74 beats per minute and oxygen level of 97 percent show healthy circulation. Try to get at least 7 hours of sleep tonight since you had only 6.2 hours, to support recovery and mental focus. Your hydration level is slightly low, so sip water regularly during the afternoon. A few gentle stretches can also help reduce your moderate stress. Keep up the good balance between activity and rest."""
        },
        {
            "iot_data": """User profile: Fitness monitoring
Steps today: 3200
Heart rate (bpm): 88
Sleep duration (hours): 5.1
Body temperature (°C): 37.2
Blood oxygen (SpO2): 94
Respiratory rate (breaths/min): 19
Stress level: High
Calories burned (kcal): 210
Hydration level: Low
Activity duration (minutes): 20
""",
            "response": """Hello Watanabe-san,
It looks like you had a tiring day. Your heart rate is a bit high at 88 beats per minute, and your oxygen level is slightly low at 94 percent. Try to rest more and take slow, deep breaths to calm your system. You’ve had only 5 hours of sleep, which may increase stress and reduce recovery. Aim for 7 to 8 hours tonight if possible. Drink plenty of water and take a short walk or stretch break—it will help relax your muscles and lower tension. Remember, consistency is better than intensity when it comes to long-term health."""
        }
    ]

    # Construct few-shot prompt examples
    fewshot_section = "\n\n".join(
        [
            f"Scenario {i+1}:\n{ex['iot_data']}\nResponse:\n{ex['response']}"
            for i, ex in enumerate(examples)
        ]
    )

    # Instruction for generating the next response
    generation_instruction = (
        "Now, based on the examples above, use the following new data.\n"
        "Write a friendly, spoken-style message (under 200 words) "
        "as if you are a personal health coach guiding the user "
        "based on their IoT and wearable fitness data.\n"
        "Avoid symbols, bullet points, and technical jargon. "
        "Refer naturally to the provided data. "
        "Start with 'Hello Watanabe-san,' and maintain a calm, supportive, and informative tone."
    )

    # Final assembly
    return (
        "You are an experienced fitness and wellness coach specializing in interpreting IoT health and wearable data.\n\n"
        f"{fewshot_section}\n\n"
        f"New data:\n{data_preamble}\n\n"
        f"{generation_instruction}"
    )
