data_preamble = """Farm data:
- Type: {{farm_type}}
- Days since stocking: {{days_since_stocking}}
- Water temperature (°C): {{water_temperature}}
- Dissolved oxygen (mg/L): {{dissolved_oxygen}}
- pH of pond water: {{water_ph}}
- Electrical conductivity (µS/cm): {{water_ec}}
- Turbidity (NTU): {{turbidity}}
- Ammonia concentration (mg/L): {{ammonia_level}}
- Nitrate concentration (mg/L): {{nitrate_level}}
- Nitrite concentration (mg/L): {{nitrite_level}}
- Water level (cm): {{water_level}}
- Feed rate (grams per fish per day): {{feed_rate}}
- Fish average weight (grams): {{avg_fish_weight}}
- Air temperature (°C): {{air_temperature}}
- Air humidity (%): {{air_humidity}}
- Rainfall: {{rainfall_state}}
- Sunshine intensity: {{sunshine_intensity}}
"""

PROMPT_TEMPLATES = {
    1: data_preamble + """
You are an experienced aquaculture extension officer specializing in freshwater fish farming.
Write a short instructional message (under 200 words) to help the farmer maintain healthy fish growth, improve yield, and protect the pond environment.

Guidelines:
- Speak in a friendly, natural tone, as if talking directly to the farmer.
- Avoid symbols, bullet points, and special characters that may sound awkward when spoken.
- Refer naturally to the provided data where relevant.
- Keep sentences clear, concise, and easy to read aloud.
- Begin with: "Hello Watanabe-san,"

Example style:
"Hello Watanabe-san, the water temperature is a bit high today, which can lower oxygen levels. Try adding some fresh water or increasing aeration to keep the fish comfortable..."

Now, write the complete instructional message.
""",
    2: """
""",
    3: """
""",
    4: """
"""
}
