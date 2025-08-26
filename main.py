from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from models import ReviewInput, AnalysisResult
from services.llm_gateway import llm_gateway
from services.database import database_service
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Customer Review Insights API",
    description="AI-powered analysis of customer reviews",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config.FRONT_END_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Customer Review Insights API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/analyze", response_model=AnalysisResult)
async def analyze_review(review_input: ReviewInput):
    """
    Analyze a customer review and return structured insights.
    """
    try:
        # Step 1: Analyze review with LLM
        analysis_result = await llm_gateway.analyze_review(
            review_id=review_input.review_id,
            review_text=review_input.text,
            review_date=review_input.date.isoformat(),
            rating=review_input.rating,
        )

        # Step 2: Save results to database
        await database_service.save_analysis(review_input, analysis_result)

        return analysis_result

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/reviews/{review_id}")
async def get_review_analysis(review_id: str):
    """Get analysis results for a specific review."""
    try:
        analysis = await database_service.get_analysis(review_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Review analysis not found")
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reviews")
async def get_all_reviews(limit: int = 100):
    """Get all analyses for dashboard."""
    try:
        analyses = await database_service.get_all_analyses(limit)
        return analyses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    print("Hello from backend!")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
