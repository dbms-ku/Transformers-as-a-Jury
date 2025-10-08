from detailed_fewshot_prompt import build_fewshot_prompt

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
    2: data_preamble + """You are an experienced aquaculture extension officer specializing in freshwater fish farming. 
Using the data above, write a short spoken script (about 180–200 words) for another extension officer to read directly to the farmer. 
The style should be warm, conversational, and natural — as if speaking kindly to the farmer in person. 
Avoid all special characters, symbols, numbered lists, or bullet points. 
Use complete sentences and smooth transitions. 
Demonstrate expert understanding of pond-based fish farming and relate your advice to the actual data provided. 
Maintain focus on fish health, water quality, feed efficiency, and environmental safety. 
Start your response exactly with: Hello Watanabe-san, 

Example responses (for reference only — do not copy or reuse):
Example 1:
Hello Watanabe-san, based on the recent readings from your fish pond, there are a few things to pay attention to. 
The water temperature is around twenty six degrees, which is quite good for most freshwater fish. 
However, the dissolved oxygen is slightly below the ideal range, so gentle aeration will help your fish stay active and healthy. 
The pH is a bit on the alkaline side, so check for lime use or runoff that may raise it. 
Ammonia and nitrite levels are moderate, meaning the pond is still stable, but continue partial water changes to prevent buildup. 
The turbidity looks a little high, so avoid overfeeding to reduce waste. 
Overall, your pond is in good condition, and with small adjustments in aeration and feeding, you can expect steady growth and good survival rates.

Example 2:
Hello Watanabe-san, your pond readings show generally healthy conditions, but a few points need care. 
The temperature and oxygen are within the safe range, so the fish should be feeding well. 
The ammonia level has increased slightly, likely from uneaten feed or organic matter. 
Try reducing the feeding rate a little and monitor the water clarity each day. 
The pH is slightly acidic, which can stress the fish, so adding a bit of agricultural lime will stabilize it. 
Keep aeration running during warm afternoons when oxygen drops fastest. 
Your consistent care is keeping the pond balanced, and these small steps will help maintain healthy growth and strong yields.
""",
    3: build_fewshot_prompt(data_preamble),
    4: data_preamble + """
You are an experienced aquaculture extension officer specializing in pond-based fish farming. 
Produce a single plain-text paragraph (maximum 200 words) that an extension officer can read aloud without changes.

Output constraints (must follow exactly):
- Start with: Hello Watanabe-san,
- Use a casual, instructional tone.
- Use short sentences (preferably under 25 words each).
- Do NOT use parentheses, percent signs, degree symbols, slashes, bullets, emojis, or other special characters. Spell units out: write "percent" and "degrees Celsius" and "milligrams per liter".
- No headings, no lists, no numbered steps, no markdown, and no extra commentary.
- Reference sensor values explicitly (for example, "water temperature is 27.5 degrees Celsius" or "dissolved oxygen is 4.8 milligrams per liter"). If a value is missing, state "value not provided."
- Avoid unexplained acronyms; if necessary, spell the phrase once (for example, "dissolved oxygen").
- Provide a concise, stage-aware assessment that follows this order in short sentences:
  1) growth-stage assessment based on days since stocking (early, mid, or nearing harvest),
  2) brief water quality assessment linking pH, dissolved oxygen, temperature, and nutrients to fish behavior and health,
  3) brief atmospheric assessment,
  4) 2–4 practical, stage-appropriate recommendations (each with its reason),
  5) a final single-sentence reminder about safety, feed management, and environmental care.
- Do not include internal chain-of-thought, model reasoning, or meta commentary.

Deliver a polished, farmer-facing instructional script that is immediately suitable for TTS.
"""
}
