from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date as DateType  # Rename the import to avoid conflict


# --- Input Model: What the API expects to receive ---
class ReviewInput(BaseModel):
    """Schema for the raw customer review input."""

    review_id: str = Field(..., description="The unique identifier for the review.")
    date: DateType = Field(..., description="The date the review was posted.")
    rating: str = Field(..., description="The star rating provided by the customer.")
    text: str = Field(..., description="The full text of the customer review.")

    # Example for the OpenAPI docs
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "review_id": "R12345",
                    "date": "2025-01-01",
                    "rating": "★★★★☆ (4 stars)",
                    "text": "I love the discount program in this app - saved 30% on my last order! However, the search functionality is really frustrating. Results are rarely relevant.",
                }
            ]
        }
    }


# --- Output Model: What the API promises to return ---
class InsightOutput(BaseModel):
    """Schema for a single structured insight extracted from the review."""

    sentiment: str = Field(
        ...,
        description="The overall sentiment for this specific topic/issue. Must be 'positive', 'negative', or 'neutral'.",
        examples=["negative"],
    )
    topic: str = Field(
        ...,
        description="The specific product feature or topic this insight is about.",
        examples=["search functionality"],
    )
    problem: Optional[str] = Field(
        None,
        description="The specific problem or pain point described by the customer, if any.",
        examples=["Results are rarely relevant"],
    )
    suggestion: Optional[str] = Field(
        None,
        description="The specific improvement or solution suggested by the customer, if any.",
        examples=["improve their search algorithm"],
    )


class AnalysisResult(BaseModel):
    """Schema for the full analysis response."""

    review_id: str
    review_date: DateType
    rating: str
    original_text: str
    overall_sentiment: str = Field(
        ...,
        description="The overall sentiment of the entire review. Must be 'positive', 'negative', or 'neutral'.",
        examples=["neutral"],
    )
    insights: List[InsightOutput] = Field(
        ..., description="A list of structured insights extracted from the review."
    )
