from detailed_fewshot_prompt import detailed_fewshot_prompt

data_preamble = """Below are current data points from a farm.
Farm type: %%farm_type%%
Days since planting: %%days_since_planting%%
Soil pH: %%ph%%
Soil temperature: %%soil_temperatute%%
Soil moisture: %%soil_moisture%%
Soil nitrogen: %%soil_nitrogen%%
Soil potassium: %%soil_potassium%%
Soil phosphorous: %%soil_phosphorous%%
Soil electrical conductivity: %%soil_ec%%
Atmospheric temperature: %%ambient_temperature%%
Atmospheric humidity: %%atmospheric_humidity%%
Atmospheric rainfall state: %%rainfall_state%%
Atmospheric sunshine intensity: %%sunshine_intensity%%

"""

PROMPT_TEMPLATES = {
    1: data_preamble+"""You are an experienced agricultural extension officer, with extensive experience in and passion for Paddy-rice farming. In a casual tone, write an instructional script (maximum 200 words) to be read without modifications by an agricultural extension officer teaching the farmer best practices for good yield and environmental safety. Demonstrate good knowledge of Paddy-rice farming, and the specific data collected.  Start with "Hello Watanabe-san,...""",

    2: data_preamble+"""You are an experienced agricultural extension officer, with extensive experience in and passion for Paddy-rice farming. In a casual tone, write an instructional script (maximum 200 words) to be read without modifications by an agricultural extension officer teaching the farmer best practices for good yield and environmental safety. Demonstrate good knowledge of Paddy-rice farming, and the specific data collected. Avoid using bullet points, lists and special characters. Start with "Hello Watanabe-san,..."

Below are an examples of your response (do not repeat the same):
## Example 1:
# Hello Watanabe-san,
Based on the data from your paddy field, here are some critical observations and recommendations:
Soil pH: At 5.2, your soil is slightly acidic. Consider applying lime to gradually raise the pH, ensuring optimal nutrient availability.
Soil Nutrients:
Nitrogen (27): Slightly low. Supplement with urea or a nitrogen-rich fertilizer to boost growth.
Potassium (68) and Phosphorus (42): Adequate but monitor regularly to avoid deficiencies.
Soil Moisture and Drainage: At 72, the soil moisture is good. Maintain consistent water levels but ensure no water logging occurs.
Temperature and Weather: With 19°C soil temperature and high sunshine intensity, conditions are favorable. Utilize this period to encourage tillering by weeding and applying fertilizers effectively.
Atmospheric Conditions: Humidity (38) is on the lower side. Irrigation should compensate to maintain adequate microclimate conditions.
Follow these steps to maintain your crop health and productivity.

## Example 2:
Hello Watanabe-san,  
Your paddy field is showing promising conditions, but there are some areas where adjustments could help maximize your yield. The soil pH at 5.4 indicates slight acidity. To improve nutrient availability for the plants, consider applying a small amount of lime to gradually bring the pH closer to neutral.  
The nitrogen level is just below optimal, so introducing a nitrogen-rich fertilizer, like urea, would give your plants the boost they need for vigorous growth. Potassium and phosphorus levels appear sufficient for now, but it’s a good idea to keep monitoring them to ensure no deficiencies arise as the plants mature.  
The soil moisture at 70% is excellent for paddy cultivation. Be sure to maintain consistent irrigation while avoiding waterlogging, as this can hinder root health. The soil temperature of 20°C combined with high sunshine intensity creates ideal growing conditions. Take advantage of this favorable period by focusing on weeding and applying fertilizers strategically to promote tillering.  
However, the atmospheric humidity at 35% is on the lower side. Light irrigation or maintaining water in the field can help create a more humid environment, which will support plant growth. With these adjustments, your crop is well-positioned for a healthy yield. Keep monitoring the field closely! """,

    3: detailed_fewshot_prompt.replace("%%data_preamble%%", data_preamble),

    4: data_preamble+"""You are an experienced agricultural extension officer specializing in paddy rice farming. Your task is to analyze sensor data from a paddy rice field and provide a detailed yet casual instructions for a farmer, using Chain of Thought reasoning to break down your assessment step by step.

Instructions:
1. Start by greeting the farmer personally, using their name "Hello Watanabe-san".
2. Analyze the growth stage based on the "Days since planting" value and explain whether the crop is in early growth, mid-season, or nearing harvest.
3. Assess soil conditions (moisture, temperature, pH, nitrogen, phosphorus, potassium, electrical conductivity) and explain how they affect crop health at this stage.
4. Evaluate atmospheric conditions (temperature, humidity, rainfall, sunshine intensity) and how they influence plant growth.
5. Provide tailored recommendations:
    - If in early growth, focus on nutrient management and weed control.
    - If in mid-season, discuss tillering, pest monitoring, and irrigation balance.
    - If approaching harvest, explain proper drainage, grain drying, and harvesting techniques.
6. Explain why each observation leads to a specific recommendation. For example:
    - "The soil moisture is 78%, which is high. At this stage, excess water can cause root rot, so controlled drainage is necessary to prevent disease."
    - "The soil nitrogen has dropped to 12, which is expected before harvest. Applying more nitrogen now would delay ripening, so it's best to avoid fertilization."
7. Conclude with encouragement and a reminder to prioritize personal and environmental safety, and to monitor key conditions.

"""
}