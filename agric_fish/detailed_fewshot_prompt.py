def build_fewshot_prompt(data_preamble: str) -> str:
    """
    Builds an efficient few-shot prompt for Ollama text generation on Raspberry Pi 5.
    Tailored for fish farming (pond aquaculture). Ensures consistent outputs,
    natural flow, and minimal token overhead for speech synthesis.
    """

    # Define few-shot examples (concise but realistic)
    examples = [
        {
            "iot_data": """Farm type: Fish pond (Tilapia)
Days since stocking: 15
Water temperature: 27°C
Dissolved oxygen: 5.8 mg/L
pH of pond water: 7.2
Electrical conductivity: 520 µS/cm
Turbidity: 18 NTU
Ammonia concentration: 0.05 mg/L
Nitrate concentration: 2.5 mg/L
Nitrite concentration: 0.1 mg/L
Water level: 95 cm
Feed rate: 3 grams per fish per day
Average fish weight: 10 grams
Air temperature: 29°C
Air humidity: 72%
Rainfall: Light rain
Sunshine intensity: Moderate""",
            "response": """Hello Watanabe-san,
Your pond looks healthy! The water temperature at 27°C is perfect for young tilapia. Keep dissolved oxygen above 5 mg/L by running aerators early morning and evening. The pH of 7.2 is ideal—stable and safe for fish. Light rain helps maintain the water level, but check turbidity (18 NTU) so sunlight still reaches the pond bottom. Ammonia is low, which means your feeding rate is just right. Keep daily observation to catch early signs of stress."""
        },
        {
            "iot_data": """Farm type: Fish pond (Tilapia)
Days since stocking: 90
Water temperature: 31°C
Dissolved oxygen: 4.2 mg/L
pH of pond water: 8.0
Electrical conductivity: 720 µS/cm
Turbidity: 25 NTU
Ammonia concentration: 0.18 mg/L
Nitrate concentration: 4.0 mg/L
Nitrite concentration: 0.2 mg/L
Water level: 80 cm
Feed rate: 6 grams per fish per day
Average fish weight: 200 grams
Air temperature: 33°C
Air humidity: 55%
Rainfall: No rain
Sunshine intensity: Strong""",
            "response": """Hello Watanabe-san,
The fish are growing well at 90 days! However, water temperature (31°C) and low oxygen (4.2 mg/L) could stress them. Run aerators longer, especially before sunrise. Reduce feeding slightly during hot afternoons to prevent ammonia buildup (now 0.18 mg/L). The pH of 8.0 is acceptable but watch for sharp swings after heavy feeding. With strong sunshine, algae growth may increase—partial water exchange can help maintain clarity. Great job keeping the pond balanced!"""
        }
    ]

    # Construct the few-shot section with minimal formatting overhead
    fewshot_section = "\n\n".join(
        [
            f"Scenario {i+1}:\n{ex['iot_data']}\nResponse:\n{ex['response']}"
            for i, ex in enumerate(examples)
        ]
    )

    # Main generation instruction
    generation_instruction = (
        "Now, based on the pattern above, use the following new data.\n"
        "Write a conversational instructional script (maximum 200 words) "
        "for an aquaculture extension officer advising a fish farmer "
        "on maintaining fish health, growth, and water quality. "
        "Avoid using special characters that could disrupt speech synthesis. "
        "Demonstrate sound understanding of pond aquaculture practices, "
        'and begin with "Hello Watanabe-san,".'
    )

    # Combine everything into one optimized prompt
    return (
        "You are an experienced aquaculture extension officer specializing in pond-based fish farming.\n\n"
        f"{fewshot_section}\n\n"
        f"New data:\n{data_preamble}\n\n"
        f"{generation_instruction}"
    )
