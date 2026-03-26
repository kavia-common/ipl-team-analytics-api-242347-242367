from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router as analytics_router

openapi_tags = [
    {
        "name": "System",
        "description": "Service health and developer help endpoints.",
    },
    {
        "name": "IPL Team Analytics",
        "description": "Team-level KPIs and chart-friendly series for IPL analytics dashboards.",
    },
]

app = FastAPI(
    title="IPL Team Analytics API",
    description=(
        "Backend API that serves IPL team analytics and KPIs suitable for frontend visualizations.\n\n"
        "Primary usage:\n"
        "- Call `GET /teams` to list team codes.\n"
        "- Call `GET /teams/{team_code}` and related sub-resources for KPIs and chart series.\n\n"
        "Note: This template ships with deterministic sample data so the API works without a dataset. "
        "Swap `AnalyticsEngine` with real ball-by-ball computations when data is added."
    ),
    version="1.0.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    tags=["System"],
    summary="Health check",
    description="Simple health check endpoint used by hosting/preview environments.",
    operation_id="health_check",
)
def health_check() -> dict:
    """Return a basic health response for uptime checks."""
    return {"message": "Healthy"}


@app.get(
    "/docs/usage",
    tags=["System"],
    summary="API usage help",
    description="Quick help for frontend developers on which endpoints to call for dashboards.",
    operation_id="api_usage_help",
)
def api_usage_help() -> dict:
    """Return a brief guide describing the intended API flow."""
    return {
        "flow": [
            {"step": 1, "call": "GET /teams", "purpose": "Get list of teams (codes/names/colors)."},
            {"step": 2, "call": "GET /teams/{team_code}", "purpose": "Overview KPIs for selected team."},
            {"step": 3, "call": "GET /teams/{team_code}/top-batters", "purpose": "Leaderboard for batters."},
            {"step": 4, "call": "GET /teams/{team_code}/top-bowlers", "purpose": "Leaderboard for bowlers."},
            {"step": 5, "call": "GET /teams/{team_code}/boundaries", "purpose": "Boundary totals + per-over series."},
            {"step": 6, "call": "GET /teams/{team_code}/run-rates", "purpose": "Phase + over-by-over run rate series."},
            {"step": 7, "call": "GET /teams/{team_code}/wickets", "purpose": "Wicket type breakdown."},
            {"step": 8, "call": "GET /teams/{team_code}/dot-balls", "purpose": "Dot ball KPI + yearly series."},
            {"step": 9, "call": "GET /teams/{team_code}/yearly", "purpose": "Season-by-season performance table."},
            {"step": 10, "call": "GET /teams/{team_code}/head-to-head", "purpose": "Opponent comparison table."},
        ]
    }


app.include_router(analytics_router)
