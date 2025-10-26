from detailed_fewshot_prompt import build_fewshot_prompt


data_preamble = """Environmental data:
- Location type: {{environment_type}}
- Air temperature (°C): {{air_temperature}}
- Air humidity (%): {{air_humidity}}
- Atmospheric pressure (hPa): {{air_pressure}}
- Carbon dioxide (CO₂ ppm): {{co2}}
- Carbon monoxide (CO ppm): {{co}}
- Nitrogen dioxide (NO₂ ppm): {{no2}}
- Sulfur dioxide (SO₂ ppm): {{so2}}
- Ozone (O₃ ppm): {{o3}}
- Particulate matter PM1.0 (µg/m³): {{pm1}}
- Particulate matter PM2.5 (µg/m³): {{pm25}}
- Particulate matter PM10 (µg/m³): {{pm10}}
- Volatile organic compounds (VOC ppm): {{voc}}
- Hydrogen sulfide (H₂S ppm): {{h2s}}
- Noise level (dB): {{noise_level}}
- Ambient light (lux): {{ambient_light}}
- Wind speed (m/s): {{wind_speed}}
- Wind direction (°): {{wind_direction}}
- Timestamp: {{timestamp}}
"""

PROMPT_TEMPLATES = {
    1: data_preamble + """
You are an experienced environmental monitoring officer specializing in air quality assessment.
Write a short instructional message (under 200 words) to help a local operator or technician understand the current air quality conditions and possible actions to improve or maintain healthy air.

Guidelines:
- Speak in a friendly, natural tone, as if talking directly to the operator.
- Avoid symbols, bullet points, and special characters that may sound awkward when spoken.
- Refer naturally to the provided data where relevant.
- Keep sentences clear, concise, and easy to read aloud.
- Begin with: "Hello Tanaka-san,"

Example style:
"Hello Tanaka-san, the air quality readings show elevated CO₂ and PM2.5 levels indoors. Please increase ventilation by opening windows or activating the air purifier for better airflow..."

Now, write the complete instructional message.
""",
2: data_preamble + """You are an experienced environmental monitoring officer specializing in air quality management. 
Using the data above, write a short spoken script (about 180–200 words) for another environmental officer to read directly to a site manager. 
The style should be warm, conversational, and natural — as if speaking kindly to the person in charge. 
Avoid all special characters, symbols, numbered lists, or bullet points. 
Use complete sentences and smooth transitions. 
Demonstrate expert understanding of air quality parameters and relate your advice to the actual data provided. 
Maintain focus on health, safety, and environmental quality. 
Start your response exactly with: Hello Tanaka-san, 

Example responses (for reference only — do not copy or reuse):
Example 1:
Hello Tanaka-san, based on the current air quality data from your urban monitoring station, CO₂ levels are slightly elevated around 950 ppm, which suggests limited ventilation. PM2.5 and PM10 values are moderate but rising, possibly due to nearby traffic. Ozone and nitrogen dioxide remain within safe limits. Increasing airflow and checking your air filters could help stabilize these values. Keep an eye on VOC levels during peak traffic hours.

Example 2:
Hello Tanaka-san, your indoor factory readings show good air temperature and humidity control, but carbon monoxide is slightly above the healthy range. Please inspect machinery ventilation systems and ensure exhaust fans are operating efficiently. The PM2.5 level is acceptable, but maintaining clean filters will prevent future buildup. Continue to monitor sulfur dioxide and nitrogen dioxide, especially near heavy equipment, to protect worker health.
""",
3: build_fewshot_prompt(data_preamble),
4: data_preamble + """
You are an experienced environmental monitoring officer specializing in air quality.
Produce a single plain-text paragraph (max 200 words) that another officer can read aloud without changes.

Output constraints (must follow exactly):
- Start with: Hello Tanaka-san,
- Use a casual, instructional tone.
- Use short sentences (preferably under 25 words each).
- Do NOT use parentheses, percent signs, degree symbols, slashes, bullets, emojis, or other special characters. Spell units out: write "percent" and "degrees Celsius".
- No headings, no lists, no numbered steps, no markdown, and no extra commentary.
- Reference sensor values explicitly (e.g., "carbon dioxide is 870 parts per million" or "humidity is 72 percent"). If a value is missing, state "value not provided."
- Avoid unexplained acronyms; if necessary, spell the phrase once (for example, "particulate matter").
- Provide a concise, stagewise-style assessment that follows this order in short sentences:
  1) Identify the monitoring environment type (domestic, industrial, urban, or volcanic area),
  2) Briefly describe the key air quality readings and what they imply,
  3) Relate these readings to comfort, safety, or compliance levels,
  4) Offer 2–4 clear recommendations for maintaining or improving air quality,
  5) End with a one-sentence reminder about health and environmental safety.
- Do not include internal chain-of-thought, model reasoning, or meta commentary.

Deliver a polished, operator-facing instructional script that is immediately suitable for TTS.
"""}
