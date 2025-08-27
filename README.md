# AI-Powered Customer Review Insights API

A FastAPI backend that analyzes customer reviews using OpenAI's GPT-4 to extract structured insights, sentiments, topics, problems, and suggestions. Perfect for e-commerce platforms drowning in unstructured customer feedback.

## 🚀 Features

- **AI-Powered Analysis**: Uses GPT-4 to extract insights from unstructured review text
- **Structured Output**: Returns sentiment, topics, problems, and suggestions in JSON format
- **Supabase Integration**: Automatically stores analyzed reviews in PostgreSQL
- **RESTful API**: Clean FastAPI endpoints with automatic OpenAPI documentation
- **Real-time Processing**: Async processing for efficient review analysis


<img width="600" height="3840" alt="deepseek_mermaid_20250827_b6f345" src="https://github.com/user-attachments/assets/3360cc61-ee31-4a29-bd2a-fc01ff1184ff" />


## 📦 API Endpoints

### POST `/analyze`

Analyze a customer review and return structured insights.

**Request:**

```json
{
  "review_id": "R-12345678",
  "date": "2024-03-15",
  "rating": "★★★★☆ (4 stars)",
  "text": "I love the discount program but the search functionality is frustrating."
}
```

**Response:**

```json
{
  "review_id": "R-12345678",
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
      "problem": "search is frustrating",
      "suggestion": null
    }
  ]
}
```

### GET `/reviews`

Get all analyzed reviews (optional limit parameter).

### GET `/reviews/{review_id}`

Get analysis for a specific review.

### GET `/health`

Health check endpoint.

## Tech Stack

- **Framework**: FastAPI (Python 3.8+)
- **AI Processing**: OpenAI GPT-4-turbo
- **Database**: Supabase (PostgreSQL)
- **API Documentation**: Auto-generated Swagger/OpenAPI
- **Environment Management**: python-dotenv

## Installation & Setup

### Prerequisites

- Python 3.8+
- OpenAI API account
- Supabase account
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd customer-review-insights
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a .env file in the root directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_SERVICE_KEY=your_supabase_service_key_here
```

### 4. Database Setup

Run this SQL in your Supabase SQL editor:

```bash
CREATE TABLE review_insights (
    id BIGSERIAL PRIMARY KEY,
    review_id TEXT NOT NULL UNIQUE,
    review_date DATE NOT NULL,
    rating TEXT NOT NULL,
    original_text TEXT NOT NULL,
    overall_sentiment TEXT NOT NULL,
    insights JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_review_insights_date ON review_insights (review_date);
CREATE INDEX idx_review_insights_sentiment ON review_insights (overall_sentiment);
```

### 5. Run the Application (built with UV)

```bash
uv run main.py
```

The API will be available at:
API: http://localhost:8000
Interactive Docs: http://localhost:8000/docs

## Project Structure

src/
├── main.py # FastAPI application and routes
├── models.py # Pydantic models for request/response
├── config.py # Environment configuration
├── services/
│ ├── llm_gateway.py # OpenAI API integration
│ └── database.py # Supabase database operations
├── prompts.py # LLM prompt engineering templates
└── **init**.py

## API Configuration

- Port: 8000 (configurable)
- Host: 0.0.0.0 (accepts external connections)
- CORS: Enabled for localhost:3000 (React dev server)
