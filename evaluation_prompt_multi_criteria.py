prompt = f"""
You are an impartial domain expert evaluating the quality of AI-generated {domain} advice intended for {target}. 
Your task is to assess the response based on **seven criteria** that capture overall quality, clarity, and contextual appropriateness.

Use the 0–5 scale defined for each criterion (0 = lowest, 5 = highest). 
For each criterion, provide:
- "Score": an integer from 0 to 5.
- "Justification": a brief, specific one-sentence reason supporting the score.

Respond **only** with a single valid JSON object structured exactly as shown below.
Do not include explanations, markdown formatting, or extra commentary outside the JSON.

---

**Evaluation Context**
Question:
{question}

Answer:
{answer}

---

**Evaluation Criteria**
{evaluation_criteria}

---

Now evaluate the *Answer* according to all seven criteria above, and return your output in this format:

{{
  "Relevance and Accuracy": {{
    "Score": <integer>,
    "Justification": "<one-sentence justification>"
  }},
  "Clarity and Coherence": {{
    "Score": <integer>,
    "Justification": "<one-sentence justification>"
  }},
  "Practicality and Usefulness": {{
    "Score": <integer>,
    "Justification": "<one-sentence justification>"
  }},
  "Safety and Environmental Sustainability": {{
    "Score": <integer>,
    "Justification": "<one-sentence justification>"
  }},
  "Cultural and Contextual Fit": {{
    "Score": <integer>,
    "Justification": "<one-sentence justification>"
  }},
  "Creativity and Innovation": {{
    "Score": <integer>,
    "Justification": "<one-sentence justification>"
  }},
  "Conciseness and Natural Flow": {{
    "Score": <integer>,
    "Justification": "<one-sentence justification>"
  }}
}}
"""
