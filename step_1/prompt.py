prompt = """
Below are current data points from a farm. 
Farm type: %%farm_type%%
Days since planting: %%days_since_planting%%
Soil pH: %%soil_ph%%
Soil temperature: %%soil_temperature%%
Soil moisture: %%soil_moisture%%
Soil nitrogen: %%soil_nitrogen%%
Soil potassium: %%soil_potassium%%
Soil phosphorous: %%soil_phosphorous%%
Soil electrical conductivity: %%soil_electrical_conductivity%%
Atmospheric temperature: %%atmospheric_temperature%%
Atmospheric humidity: %%atmospheric_humidity%%
Atmospheric rainfall state: %%atmospheric_rainfall_state%%
Atmospheric sunshine intensity: %%atmospheric_sunshine_intensity%%

You are an experinced agricultural extension officer, with extensive experience in and passion for %%farm_type%%. In conversational style, write an instructional script (maximum 200 words) to be read without modificatons by an agricultural extension officer teaching the farmer best practices for good yield and environmental safty. Demonstrate good knowledge of %%farm_type%%, and the specific data collected. Start with "Hello Watanabe-san,..."
"""

detailed_fewshot_prompt = """
You are an experinced agricultural extension officer, with extensive experience in and passion for Paddy-rice farming. 

For the following data scenarios, you gave the responses indicated.
--Scenario 1: %%iot_data_1%%
--Response: %%agent_response_1%%

--Scenario 2: %%iot_data_2%%
--Response: %%agent_response_2%%

Below are current data points from the farm. 
Farm type: Paddy-rice farming
Days since planting: 73
Soil pH: 5.7
Soil temperature: 19 degrees Celsius
Soil moisture: 72
Soil nitrogen: 27
Soil potassium: 68
Soil phosphorous: 42
Soil electrical conductivity: 1.13
Atmospheric temperature: 28 degrees Celsius
Atmospheric humidity: 38
Atmospheric rainfall state: Not raining
Atmospheric sunshine intensity: High 

In conversational style, write an instructional script (maximum 200 words) to be read without modificatons by an agricultural extension officer teaching the farmer best practices for good yield and environmental safty. Demonstrate good knowledge of Paddy-rice farming, and the specific data collected. Start with "Hello Watanabe-san,..."
"""

examples_data = [
    {"iot_data": """Farm type: Paddy-rice farming
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

I see your paddy field is coming along well! At 20 days since planting, your young rice plants are in the early vegetative stage, where strong root development and healthy leaf growth are key. Let’s go over some best practices to ensure a good yield while keeping the environment safe.  

Your soil pH is 5.8, which is within the ideal range for rice, but keep an eye on it—if it drops below 5.5, iron toxicity could become a problem. Your soil nitrogen (30) is good for now, supporting leaf and stem growth, but avoid over-fertilizing, as excess nitrogen can weaken plants and harm water quality. Your soil moisture (78) is excellent, especially with the light rain, but make sure there’s no prolonged flooding at this stage—too much water can hinder root oxygen intake.  

Your atmospheric temperature (18°C) is on the lower side, so be mindful of growth slowdowns. With moderate sunshine, your plants should still photosynthesize well. If cold weather continues, consider adjusting your water depth slightly to regulate soil temperature.  

Overall, your farm is on track! Keep monitoring these conditions, and you’ll be on your way to a strong, healthy crop."""},

    {"iot_data": """Farm type: Paddy-rice farming
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

Your paddy field is now at 120 days since planting, which means harvest time is approaching! From the data, I see your soil moisture is at 65%, which is good, but as you prepare for harvesting, you should start gradually draining the field. This will allow the grains to dry properly, improving quality and reducing lodging risks. Aim to stop irrigation about two weeks before harvest.  

Your soil nitrogen levels have dropped to 12, which is expected at this stage. Avoid applying additional nitrogen now, as it can delay maturity and affect grain quality. Your potassium and phosphorus levels look stable, which is good for grain filling.  

With moderate to high sunshine intensity and a soil temperature of 17°C, your crop is in a favorable condition for ripening. However, keep an eye on the weather forecast. If strong winds or storms are expected, consider an earlier harvest to prevent losses.  

Finally, when harvesting, ensure grains are at the correct moisture level—around 20% for mechanical harvesting. Afterward, dry them to 14% moisture for safe storage.  

You're almost there, Watanabe-san! With careful management, you’ll have a great yield. Ganbatte!"""}
]


chain_of_thought_prompt = """You are an experienced agricultural extension officer specializing in paddy rice farming. Your task is to analyze sensor data from a paddy rice field and provide a detailed yet casual instructional script for a farmer, using Chain of Thought reasoning to break down your assessment step by step.

Instructions:
1. Start by greeting the farmer personally, using their name (e.g., "Hello Watanabe-san").
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