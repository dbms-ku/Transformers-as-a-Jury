evaluation_questions = {
    "relevance_score": """Relevance and Accuracy
0: Completely irrelevant or inaccurate information.
1: Mostly inaccurate or unrelated to the topic.
2: Somewhat relevant but with major factual issues.
3: Generally accurate and related, though minor errors exist.
4: Mostly accurate and well-aligned with the topic or user needs.
5: Fully accurate, reliable, and directly relevant to the intended audience.""",

    "clarity_score": """Clarity and Coherence
0: Incomprehensible or disorganized text.
1: Very confusing, with poor sentence flow and structure.
2: Understandable in parts but overly complex or awkward.
3: Reasonably clear but may require effort to follow.
4: Clear, well-structured, and easy to understand when spoken.
5: Exceptionally clear, natural, and pleasant to hear when read aloud.""",

    "practicality_score": """Practicality and Usefulness
0: No actionable advice or practical value.
1: Very limited applicability or unrealistic guidance.
2: Some practical ideas but lacking clear instructions or affordability.
3: Practical and moderately detailed; generally applicable.
4: Clear, actionable, and cost-effective recommendations.
5: Highly useful, innovative, and immediately applicable in real-world farming contexts.""",

    "safety_sustainability_score": """Safety and Environmental Sustainability
0: Encourages unsafe or environmentally harmful practices.
1: Minimal mention of safety or sustainability.
2: Addresses safety or sustainability superficially.
3: Moderately promotes safe and sustainable methods.
4: Strong focus on protecting people and the environment.
5: Comprehensive integration of safe, healthy, and eco-friendly practices.""",

    "cultural_context_score": """Cultural and Contextual Fit
0: Completely ignores local context or regional realities.
1: Minimal adaptation to local conditions.
2: Some regional awareness but lacks practical connection.
3: Moderately tailored to cultural and local needs.
4: Effectively adapted to regional realities and easily replicable.
5: Deeply contextualized, scalable, and well-suited for the target region.""",

    "creativity_score": """Creativity and Innovation
0: Entirely unoriginal or outdated content.
1: Very minimal novelty or creativity.
2: Some new ideas but poorly integrated.
3: Moderately creative with fresh perspectives.
4: Original and thoughtfully presented ideas.
5: Highly innovative, inspiring, and forward-thinking content.""",

    "conciseness_score": """Conciseness and Natural Flow
0: Extremely verbose or incoherent; difficult to follow.
1: Overly wordy, repetitive, or fragmented.
2: Contains unnecessary detail that hinders comprehension.
3: Adequately concise but could be smoother in pacing.
4: Well-balanced length with smooth and natural rhythm for audio.
5: Exceptionally concise, fluid, and natural-sounding when spoken aloud.""",
}


# 🧠 Why This Version Works Better
# Clear structure and consistent separation between context, criterion, and expected output.
# Reduced ambiguity → models like Ollama’s Mistral or Phi variants often misinterpret nested instructions, so this linear structure prevents that.
# JSON safety → guarantees you’ll get clean key-value pairs for CSV export.
# One-sentence justification → keeps evaluation concise and usable for downstream analysis or fine-tuning.
 