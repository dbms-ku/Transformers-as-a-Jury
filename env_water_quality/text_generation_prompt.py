from detailed_fewshot_prompt import build_fewshot_prompt


data_preamble = """Water quality data:
- Type: {{water_type}}
- pH: {{ph}}
- Temperature (°C): {{water_temperature}}
- Electrical conductivity (µS/cm): {{water_ec}}
- Turbidity (NTU): {{turbidity}}
- Dissolved oxygen (mg/L): {{dissolved_oxygen}}
- Total dissolved solids (ppm): {{tds}}
- Oxidation-reduction potential (mV): {{orp}}
- Nitrate level (mg/L): {{nitrate}}
- Phosphate level (mg/L): {{phosphate}}
- Ammonia level (mg/L): {{ammonia}}
- Chlorine residual (mg/L): {{chlorine}}
- Water hardness (mg/L CaCO3): {{hardness}}
- Temperature of surrounding air (°C): {{ambient_temperature}}
- Humidity of surrounding air (%): {{atmospheric_humidity}}
"""

PROMPT_TEMPLATES = {
    1: data_preamble + """
You are an experienced environmental monitoring officer specializing in water quality assessment.
Write a short advisory message (under 200 words) to help the community or facility maintain clean and safe water conditions.

Guidelines:
- Speak in a friendly, natural tone, as if talking directly to the caretaker or facility manager.
- Avoid symbols, bullet points, and special characters that may sound awkward when spoken.
- Refer naturally to the provided data where relevant.
- Keep sentences clear, concise, and easy to read aloud.
- Begin with: "Hello Tanaka-san,"

Example style:
"Hello Tanaka-san, your river water looks generally good but the turbidity is a bit high. It might be due to surface runoff after the rain. Regular cleaning of the inlet filter and checking for sediment sources nearby will help maintain clarity..."

Now, write the complete advisory message.
""",
2: data_preamble + """You are an experienced environmental officer specializing in water quality monitoring.
Using the data above, write a short spoken script (about 180–200 words) for another officer to read to a facility caretaker or community leader.
The style should be warm, conversational, and natural — as if speaking kindly to them in person.
Avoid all special characters, symbols, numbered lists, or bullet points.
Use complete sentences and smooth transitions.
Demonstrate expert understanding of water quality and relate your advice to the actual data provided.
Maintain focus on human safety, environmental health, and pollution prevention.
Start your response exactly with: Hello Tanaka-san,

Example 1:
Hello Tanaka-san, based on your surface water data, I see that the pH is neutral, which is good, but turbidity is slightly high. This may mean soil or organic particles have entered after rain. The dissolved oxygen is healthy, which suggests good aeration. Conductivity and hardness look balanced, indicating moderate mineral content. Continue monitoring after rainfall and clean the sampling inlet weekly to maintain stability.

Example 2:
Hello Tanaka-san, your underground water sample shows good clarity and stable temperature. However, the nitrate level is slightly elevated, possibly from nearby fertilizer use. If this persists, consider testing nearby wells to confirm the source. The oxygen level is acceptable, and the pH near 7.2 indicates neutral balance. Keeping vegetation buffers and avoiding waste dumping near the borehole will improve long-term quality.
""",
3: build_fewshot_prompt(data_preamble),
4: data_preamble + """
You are an environmental monitoring officer specializing in water quality.
Produce a single plain-text paragraph (max 200 words) suitable for direct spoken delivery.

Output constraints (must follow exactly):
- Start with: Hello Tanaka-san,
- Use a natural, conversational tone.
- Use short sentences (preferably under 25 words each).
- Do NOT use parentheses, percent signs, degree symbols, slashes, bullets, emojis, or other special characters. Spell units out: write "microSiemens per centimeter" or "milligrams per liter".
- No headings, no lists, no numbered steps, no markdown, and no extra commentary.
- Reference sensor values explicitly (e.g., "pH is 7 point 2" or "dissolved oxygen is 8 point 4 milligrams per liter"). If a value is missing, state "value not provided."
- Avoid unexplained acronyms; if necessary, spell the phrase once (for example, "oxidation-reduction potential").
- Provide a concise assessment that follows this order in short sentences:
  1) water type and general condition summary,
  2) pH and chemical balance interpretation,
  3) clarity and oxygen status,
  4) contamination or pollutant indicators (e.g., nitrates, turbidity, conductivity),
  5) two to four actionable recommendations with reasons,
  6) a final single-sentence safety reminder and encouragement.
- Do not include internal chain-of-thought, model reasoning, or meta commentary.

Deliver a polished, community-facing advisory script immediately suitable for TTS.
"""}
