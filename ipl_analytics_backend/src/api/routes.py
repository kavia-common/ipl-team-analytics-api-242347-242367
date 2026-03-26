from __future__ import annotations

from fastapi import APIRouter, HTTPException, Path

from src.api.analytics import AnalyticsEngine
from src.api.models import (
    BoundaryAnalysisResponse,
    DotBallStatsResponse,
    HeadToHeadResponse,
    RunRateBreakdownResponse,
    TeamListResponse,
    TeamOverviewResponse,
    TopBattersResponse,
    TopBowlersResponse,
    WicketTypesResponse,
)

router = APIRouter(tags=["IPL Team Analytics"])
_engine = AnalyticsEngine()


def _not_found(team_code: str) -> HTTPException:
    return HTTPException(status_code=404, detail=f"Unknown team_code '{team_code}'. Use GET /teams to list valid codes.")


@router.get(
    "/teams",
    response_model=TeamListResponse,
    summary="List teams",
    description="Return all IPL teams available for analytics. The frontend can use this to render team logos or filters.",
    operation_id="list_teams",
)
def list_teams() -> TeamListResponse:
    """List all IPL teams supported by the analytics API."""
    teams = [
        {"code": t.code, "name": t.name, "colors": {"primary": t.colors[0], "secondary": t.colors[1]}}
        for t in _engine.list_teams()
    ]
    return TeamListResponse(teams=teams)


@router.get(
    "/teams/{team_code}",
    response_model=TeamOverviewResponse,
    summary="Team overview KPIs",
    description=(
        "Return team metadata and high-level KPIs for summary cards, including wins/losses, run rate, "
        "boundaries, dot-ball percentage and wickets lost."
    ),
    operation_id="get_team_overview",
)
def get_team_overview(
    team_code: str = Path(..., description="Team code (e.g., CSK, MI)."),
) -> TeamOverviewResponse:
    """Get a team's overview KPIs for dashboard summary tiles."""
    try:
        data = _engine.get_team_overview(team_code)
        return TeamOverviewResponse.model_validate(data)
    except KeyError:
        raise _not_found(team_code)


@router.get(
    "/teams/{team_code}/top-batters",
    response_model=TopBattersResponse,
    summary="Top batters",
    description="Return top batters for a team to power leaderboards and bar charts.",
    operation_id="get_team_top_batters",
)
def get_team_top_batters(
    team_code: str = Path(..., description="Team code (e.g., CSK, MI)."),
) -> TopBattersResponse:
    """Return top batters for the specified team."""
    try:
        rows = _engine.get_top_batters(team_code)
        return TopBattersResponse(team_code=team_code.upper(), top_batters=rows)
    except KeyError:
        raise _not_found(team_code)


@router.get(
    "/teams/{team_code}/top-bowlers",
    response_model=TopBowlersResponse,
    summary="Top bowlers",
    description="Return top bowlers for a team to power leaderboards and bar charts.",
    operation_id="get_team_top_bowlers",
)
def get_team_top_bowlers(
    team_code: str = Path(..., description="Team code (e.g., CSK, MI)."),
) -> TopBowlersResponse:
    """Return top bowlers for the specified team."""
    try:
        rows = _engine.get_top_bowlers(team_code)
        return TopBowlersResponse(team_code=team_code.upper(), top_bowlers=rows)
    except KeyError:
        raise _not_found(team_code)


@router.get(
    "/teams/{team_code}/boundaries",
    response_model=BoundaryAnalysisResponse,
    summary="Boundary analysis",
    description="Return fours/sixes totals and a per-over boundary series for visualization.",
    operation_id="get_team_boundary_analysis",
)
def get_team_boundary_analysis(
    team_code: str = Path(..., description="Team code (e.g., CSK, MI)."),
) -> BoundaryAnalysisResponse:
    """Get boundary totals and per-over boundary counts for the specified team."""
    try:
        payload = _engine.get_team_boundary_analysis(team_code)
        return BoundaryAnalysisResponse.model_validate(payload)
    except KeyError:
        raise _not_found(team_code)


@router.get(
    "/teams/{team_code}/run-rates",
    response_model=RunRateBreakdownResponse,
    summary="Run-rate breakdown",
    description="Return phase-wise and over-by-over run-rate series (powerplay/middle/death).",
    operation_id="get_team_run_rate_breakdown",
)
def get_team_run_rate_breakdown(
    team_code: str = Path(..., description="Team code (e.g., CSK, MI)."),
) -> RunRateBreakdownResponse:
    """Get phase-wise run rate and over-by-over run rate series."""
    try:
        payload = _engine.get_team_run_rate_breakdown(team_code)
        return RunRateBreakdownResponse.model_validate(payload)
    except KeyError:
        raise _not_found(team_code)


@router.get(
    "/teams/{team_code}/wickets",
    response_model=WicketTypesResponse,
    summary="Wicket type breakdown",
    description="Return wicket type percentages (caught/bowled/lbw/run out/stumped/other).",
    operation_id="get_team_wicket_types",
)
def get_team_wicket_types(
    team_code: str = Path(..., description="Team code (e.g., CSK, MI)."),
) -> WicketTypesResponse:
    """Get wicket type distribution for the specified team."""
    try:
        payload = _engine.get_team_wicket_types(team_code)
        return WicketTypesResponse.model_validate(payload)
    except KeyError:
        raise _not_found(team_code)


@router.get(
    "/teams/{team_code}/dot-balls",
    response_model=DotBallStatsResponse,
    summary="Dot ball stats",
    description="Return dot ball count/percentage and a yearly dot-ball percentage series.",
    operation_id="get_team_dot_ball_stats",
)
def get_team_dot_ball_stats(
    team_code: str = Path(..., description="Team code (e.g., CSK, MI)."),
) -> DotBallStatsResponse:
    """Get dot-ball KPI and yearly dot-ball percentage series for the specified team."""
    try:
        payload = _engine.get_team_dot_ball_stats(team_code)
        return DotBallStatsResponse.model_validate(payload)
    except KeyError:
        raise _not_found(team_code)


@router.get(
    "/teams/{team_code}/yearly",
    response_model=dict,
    summary="Yearly performance",
    description="Return year-by-year performance (matches/wins/losses/NRR/position).",
    operation_id="get_team_yearly_performance",
)
def get_team_yearly_performance(
    team_code: str = Path(..., description="Team code (e.g., CSK, MI)."),
) -> dict:
    """Get a year-by-year performance table for the specified team."""
    try:
        payload = _engine.get_team_yearly_performance(team_code)
        # Pydantic model exists but a dict response keeps this endpoint flexible for future expansion.
        return payload
    except KeyError:
        raise _not_found(team_code)


@router.get(
    "/teams/{team_code}/head-to-head",
    response_model=HeadToHeadResponse,
    summary="Head-to-head records",
    description="Return head-to-head summary (played/wins/losses) vs all other teams.",
    operation_id="get_team_head_to_head",
)
def get_team_head_to_head(
    team_code: str = Path(..., description="Team code (e.g., CSK, MI)."),
) -> HeadToHeadResponse:
    """Get head-to-head record table for the specified team."""
    try:
        payload = _engine.get_team_head_to_head(team_code)
        return HeadToHeadResponse.model_validate(payload)
    except KeyError:
        raise _not_found(team_code)
