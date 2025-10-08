from evaluation_questions import evaluation_questions

prompt = f"""
You are an impartial domain expert evaluating the quality of AI-generated {domain} advice intended for {target}. 
Your task is to carefully assess the response **only** based on the specified evaluation criterion.

Use the 0–5 scale described below, where 0 is the lowest and 5 is the highest quality. 
Provide your result strictly in valid JSON format with exactly two fields:
- "Score": an integer from 0 to 5.
- "Justification": a brief, specific reason supporting the assigned score.

Do not include any text outside the JSON object.

---

**Evaluation Context**
Question:
{question}

Answer:
{answer}

---

**Evaluation Criterion**
{evaluation_criteria}

---

Now, based on the criterion above, rate the *Answer* and output your evaluation in this JSON format:
{{
  "Score": <integer>,
  "Justification": "<one-sentence justification>"
}}
"""
