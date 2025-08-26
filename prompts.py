# This is the system prompt that defines the AI's role and task.
SYSTEM_PROMPT = """You are an expert AI analyst specialized in extracting structured insights from customer reviews.
Your task is to analyze the given review and output a JSON object with an overall sentiment and a list of insights.

CRITICAL INSTRUCTIONS:
1. Be precise and objective. Do not hallucinate or add information not present in the review.
2. For the overall_sentiment, consider the entire review holistically.
3. Break down the review into distinct insights. Each insight must be about a single specific topic (e.g., 'discount', 'delivery', 'app UI').
4. For each insight, you MUST populate the 'sentiment' (positive/negative/neutral), 'topic', 'problem', and 'suggestion'.
5. If a 'problem' or 'suggestion' is not explicitly stated, you MUST set that field to null.
6. Your final output MUST be a valid JSON object that matches this exact schema:
{
  "overall_sentiment": "string",
  "insights": [
    {
      "sentiment": "string",
      "topic": "string",
      "problem": "string | null",
      "suggestion": "string | null"
    }
  ]
}
"""

# These user/assistant examples guide the LLM to the desired output format and logic.
FEW_SHOT_EXAMPLES = [
    {
        "user": """review_id: "R12345"
        text: "I love the discount program in this app - saved 30% on my last order! However, the search functionality is really frustrating. Results are rarely relevant to what I'm looking for. They should implement category filters and improve their search algorithm.\"""",
        "assistant": """{
  "overall_sentiment": "neutral",
  "insights": [
    {
      "sentiment": "positive",
      "topic": "discount program",
      "problem": null,
      "suggestion": null
    },
    {
      "sentiment": "negative",
      "topic": "search functionality",
      "problem": "Results are rarely relevant",
      "suggestion": "implement category filters and improve their search algorithm"
    }
  ]
}""",
    },
    {
        "user": """review_id: "R67890"
        text: "Delivery was super fast and the rider was polite. The food was hot and fresh. Best experience so far!\"""",
        "assistant": """{
  "overall_sentiment": "positive",
  "insights": [
    {
      "sentiment": "positive",
      "topic": "delivery speed",
      "problem": null,
      "suggestion": null
    },
    {
      "sentiment": "positive",
      "topic": "rider politeness",
      "problem": null,
      "suggestion": null
    },
    {
      "sentiment": "positive",
      "topic": "food quality",
      "problem": null,
      "suggestion": null
    }
  ]
}""",
    },
]


def build_prompt(review_text: str) -> list:
    """
    Constructs the conversation payload for the OpenAI API using few-shot learning.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for example in FEW_SHOT_EXAMPLES:
        messages.append({"role": "user", "content": example["user"]})
        messages.append({"role": "assistant", "content": example["assistant"]})

    messages.append(
        {"role": "user", "content": f'review_id: "TODO"\ntext: "{review_text}"'}
    )

    return messages
