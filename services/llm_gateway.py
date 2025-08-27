import json
import logging
from openai import AsyncOpenAI, APIError
from config import Config
from prompts import build_prompt
from models import AnalysisResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMAnalysisError(Exception):
    """Custom exception for LLM analysis failures."""

    pass


class LLMGateway:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = "gpt-3.5-turbo-0125"

    async def analyze_review(
        self, review_id: str, review_date: str, rating: str, review_text: str
    ) -> AnalysisResult:
        """
        Main method: Takes review text, sends to LLM,
        returns structured AnalysisResult.
        """
        try:
            # 1. Construct the prompt using our template
            messages = build_prompt(review_text)
            logger.info(f"Analyzing review {review_id} with model {self.model}")

            # 2. Call the OpenAI API
            response = await self._make_async_api_call(messages)

            # 3. Extract the JSON content from the response
            json_str = self._extract_json_response(response)

            # 4. Parse, validate, and add the review_id
            analysis_result = self._parse_and_validate_response(
                json_str, review_id, review_date, rating, review_text
            )

            logger.info(f"Successfully analyzed review {review_id}")
            print(analysis_result)
            return analysis_result

        except (APIError, json.JSONDecodeError, ValueError) as e:
            logger.error(f"LLM analysis failed for review {review_id}: {str(e)}")
            raise LLMAnalysisError(f"Failed to analyze review: {str(e)}")

    async def _make_async_api_call(self, messages: list) -> str:
        """Make the actual API call to OpenAI."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,
                max_tokens=1000,
                response_format={"type": "json_object"},
            )
            return response.choices[0].message.content
        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    def _extract_json_response(self, response_content: str) -> str:
        """Extract and clean JSON string from response."""
        if response_content.strip().startswith("```json"):
            lines = response_content.strip().split("\n")
            json_str = "\n".join(lines[1:-1])
            return json_str
        return response_content

    def _parse_and_validate_response(
        self,
        json_str: str,
        review_id: str,
        review_date: str,
        rating: str,
        review_text: str,
    ) -> AnalysisResult:
        """Parse JSON string and validate against our Pydantic model."""
        try:
            data = json.loads(json_str)
            data["review_id"] = review_id
            data["review_date"] = review_date
            data["rating"] = rating
            data["original_text"] = review_text
            return AnalysisResult(**data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {json_str}")
            raise ValueError(f"Invalid JSON received from LLM: {e}")
        except Exception as e:
            logger.error(f"Validation failed for LLM response: {e}")
            raise ValueError(f"LLM response validation failed: {e}")


# Create a singleton instance for easy import
llm_gateway = LLMGateway()
