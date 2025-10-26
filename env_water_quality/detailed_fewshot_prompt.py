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
        "iot_data": """Water type: River water
pH: 7.2
Water temperature: 21°C
Electrical conductivity: 350 µS/cm
Turbidity: 8 NTU
Dissolved oxygen: 7.8 mg/L
Total dissolved solids: 180 ppm
Oxidation-reduction potential: 280 mV
Nitrate level: 2.1 mg/L
Phosphate level: 0.4 mg/L
Ammonia level: 0.1 mg/L
Chlorine residual: 0.0 mg/L
Water hardness: 120 mg/L CaCO3
Ambient temperature: 26°C
Atmospheric humidity: 58%""",
        "response": """Hello Tanaka-san,
Your river water quality looks fairly healthy. The pH of 7.2 and conductivity around 350 microSiemens show good mineral balance. Dissolved oxygen at 7.8 milligrams per liter means the water is well aerated, supporting aquatic life. Turbidity of 8 NTU is slightly high, possibly due to runoff after rain. Regularly check for upstream soil disturbance or urban discharge. The low nitrate and phosphate levels show limited nutrient pollution, which is great. Keep monitoring weekly and clear any debris around the sampling point to maintain flow and prevent buildup."""
    },
    {
        "iot_data": """Water type: Underground water
pH: 6.9
Water temperature: 18°C
Electrical conductivity: 410 µS/cm
Turbidity: 2 NTU
Dissolved oxygen: 5.5 mg/L
Total dissolved solids: 210 ppm
Oxidation-reduction potential: 240 mV
Nitrate level: 4.2 mg/L
Phosphate level: 0.3 mg/L
Ammonia level: 0.05 mg/L
Chlorine residual: 0.0 mg/L
Water hardness: 140 mg/L CaCO3
Ambient temperature: 20°C
Atmospheric humidity: 62%""",
        "response": """Hello Tanaka-san,
Your underground water sample looks stable overall. The pH near neutral and low turbidity indicate good clarity and balance. However, nitrate levels around 4.2 milligrams per liter are slightly elevated, possibly from nearby fertilizer use or septic leakage. Keep checking surrounding land use and ensure no direct contamination sources. Dissolved oxygen is moderate at 5.5, which is normal for underground water. Conductivity and hardness values are safe for general use. Continue monitoring monthly to detect any slow changes in quality and keep records to track long-term trends."""
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
        "Write a conversational advisory script (max 200 words) "
        "for an environmental officer explaining water quality findings "
        "and providing clear, practical recommendations. "
        "Avoid using special characters that may disrupt speech synthesis. "
        'Demonstrate clear understanding of water quality monitoring and start with "Hello Tanaka-san,".'
    )

    # Combine everything into one optimized prompt
    return (
        "You are an experienced environmental monitoring officer specializing in water quality assessment.\n\n"
        f"{fewshot_section}\n\n"
        f"New data:\n{data_preamble}\n\n"
        f"{generation_instruction}"
    )
