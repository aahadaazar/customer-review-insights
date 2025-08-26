import logging
from supabase import create_client, Client
from config import Config
from models import ReviewInput, AnalysisResult

logger = logging.getLogger(__name__)


class DatabaseService:
    def __init__(self):
        self.client: Client = create_client(
            Config.SUPABASE_URL, Config.SUPABASE_SERVICE_KEY
        )
        self.table_name = "review_insights"

    async def save_analysis(
        self, review_input: ReviewInput, analysis_result: AnalysisResult
    ) -> dict:
        """Save analysis results to Supabase."""
        try:
            data = {
                "review_id": review_input.review_id,
                "review_date": review_input.date.isoformat(),
                "rating": review_input.rating,
                "original_text": review_input.text,
                "overall_sentiment": analysis_result.overall_sentiment,
                "insights": [
                    insight.model_dump() for insight in analysis_result.insights
                ],
            }

            # Upsert to handle duplicate review_ids
            result = self.client.table(self.table_name).upsert(data).execute()

            logger.info(
                f"Saved analysis for review {review_input.review_id} to database"
            )
            return result.data[0] if result.data else None

        except Exception as e:
            logger.error(f"Failed to save analysis to database: {e}")
            raise

    async def get_analysis(self, review_id: str) -> dict:
        """Retrieve analysis results by review_id."""
        try:
            result = (
                self.client.table(self.table_name)
                .select("*")
                .eq("review_id", review_id)
                .execute()
            )
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Failed to fetch analysis from database: {e}")
            raise

    async def get_all_analyses(self, limit: int = 100) -> list:
        """Retrieve all analyses for dashboard."""
        try:
            result = (
                self.client.table(self.table_name)
                .select("*")
                .order("review_date", desc=True)
                .limit(limit)
                .execute()
            )
            return result.data
        except Exception as e:
            logger.error(f"Failed to fetch analyses from database: {e}")
            raise


# Create a singleton instance
database_service = DatabaseService()
