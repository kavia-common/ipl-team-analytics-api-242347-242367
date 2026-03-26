from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class TeamColors(BaseModel):
    primary: str = Field(..., description="Primary team color hex code.")
    secondary: str = Field(..., description="Secondary team color hex code.")


class Team(BaseModel):
    code: str = Field(..., description="Short team code (e.g., CSK, MI).")
    name: str = Field(..., description="Display name of the IPL team.")
    colors: TeamColors = Field(..., description="Brand colors for UI theming.")


class TeamListResponse(BaseModel):
    teams: List[Team] = Field(..., description="List of all teams available in the system.")


class TeamKpisBoundaries(BaseModel):
    fours: int = Field(..., description="Total fours hit by the team.")
    sixes: int = Field(..., description="Total sixes hit by the team.")
    total: int = Field(..., description="Total boundaries (fours+sixes).")


class DotBallKpi(BaseModel):
    count: int = Field(..., description="Number of dot balls.")
    percentage: float = Field(..., description="Dot ball percentage over all balls faced.")


class TeamKpis(BaseModel):
    matches: int = Field(..., description="Total matches included in the aggregation.")
    wins: int = Field(..., description="Total wins.")
    losses: int = Field(..., description="Total losses.")
    no_results: int = Field(..., description="No result / abandoned matches.")
    runs_scored: int = Field(..., description="Total runs scored by the team.")
    balls_faced: int = Field(..., description="Total balls faced.")
    overs_faced: float = Field(..., description="Total overs faced (balls/6).")
    run_rate: float = Field(..., description="Overall run rate (runs per over).")
    win_percentage: float = Field(..., description="Win percentage (wins/matches*100).")
    boundaries: TeamKpisBoundaries = Field(..., description="Boundary totals.")
    dot_balls: DotBallKpi = Field(..., description="Dot-ball KPI values.")
    wickets_lost: int = Field(..., description="Total wickets lost while batting.")


class TeamOverviewResponse(BaseModel):
    team: Team = Field(..., description="Team metadata.")
    kpis: TeamKpis = Field(..., description="High-level KPIs for summary cards.")


class TopBatter(BaseModel):
    player: str = Field(..., description="Player name.")
    runs: int = Field(..., description="Total runs scored.")
    balls: int = Field(..., description="Total balls faced.")
    strike_rate: float = Field(..., description="Strike rate (runs/balls*100).")
    fours: int = Field(..., description="Fours hit.")
    sixes: int = Field(..., description="Sixes hit.")
    matches: int = Field(..., description="Matches played.")


class TopBowler(BaseModel):
    player: str = Field(..., description="Player name.")
    wickets: int = Field(..., description="Total wickets taken.")
    overs: float = Field(..., description="Overs bowled.")
    economy: float = Field(..., description="Economy rate (runs conceded per over).")
    dot_ball_percentage: float = Field(..., description="Percentage of dot balls delivered.")
    matches: int = Field(..., description="Matches played.")


class TopBattersResponse(BaseModel):
    team_code: str = Field(..., description="Team code for which the ranking is returned.")
    top_batters: List[TopBatter] = Field(..., description="Top batters for the team.")


class TopBowlersResponse(BaseModel):
    team_code: str = Field(..., description="Team code for which the ranking is returned.")
    top_bowlers: List[TopBowler] = Field(..., description="Top bowlers for the team.")


class BoundaryByOver(BaseModel):
    over: int = Field(..., description="Over number (1-based).")
    fours: int = Field(..., description="Fours hit in this over.")
    sixes: int = Field(..., description="Sixes hit in this over.")


class BoundaryAnalysis(BaseModel):
    fours: int = Field(..., description="Total fours.")
    sixes: int = Field(..., description="Total sixes.")
    total: int = Field(..., description="Total boundaries.")
    boundary_ball_percentage: float = Field(..., description="Boundary-ball percentage over all balls faced.")


class BoundaryAnalysisResponse(BaseModel):
    team_code: str = Field(..., description="Team code.")
    boundaries: BoundaryAnalysis = Field(..., description="Boundary summary.")
    by_over: List[BoundaryByOver] = Field(..., description="Per-over boundary counts for charting.")


class PhaseRunRate(BaseModel):
    phase: str = Field(..., description="Phase label.")
    overs: int = Field(..., description="Number of overs in this phase.")
    run_rate: float = Field(..., description="Run rate in this phase.")


class RunRatePerOver(BaseModel):
    over: int = Field(..., description="Over number (1-based).")
    run_rate: float = Field(..., description="Run rate for that over (runs/over).")


class RunRateBreakdownResponse(BaseModel):
    team_code: str = Field(..., description="Team code.")
    phases: List[PhaseRunRate] = Field(..., description="Phase-wise run rate breakdown.")
    runs_per_over: List[RunRatePerOver] = Field(..., description="Over-by-over run rate series for line charts.")


class WicketTypeRow(BaseModel):
    type: str = Field(..., description="Wicket type.")
    percentage: int = Field(..., description="Percentage share for this wicket type (sums ~100).")


class WicketTypesResponse(BaseModel):
    team_code: str = Field(..., description="Team code.")
    wicket_types: List[WicketTypeRow] = Field(..., description="Wicket type breakdown.")


class YearValue(BaseModel):
    year: int = Field(..., description="Season year.")
    value: float = Field(..., description="Value for the metric in that year.")


class DotBallStatsResponse(BaseModel):
    team_code: str = Field(..., description="Team code.")
    dot_balls: DotBallKpi = Field(..., description="Dot ball KPI.")
    dot_ball_percentage_by_year: List[YearValue] = Field(..., description="Yearly dot-ball percentage series.")


class YearlyPerformanceRow(BaseModel):
    year: int = Field(..., description="Season year.")
    matches: int = Field(..., description="Matches played in the season.")
    wins: int = Field(..., description="Wins in the season.")
    losses: int = Field(..., description="Losses in the season.")
    net_run_rate: float = Field(..., description="Net run rate (NRR) for the season.")
    position: int = Field(..., description="Final league/season position (template/demo value).")


class YearlyPerformanceResponse(BaseModel):
    team_code: str = Field(..., description="Team code.")
    yearly: List[YearlyPerformanceRow] = Field(..., description="Year-by-year performance table.")


class HeadToHeadRow(BaseModel):
    opponent_code: str = Field(..., description="Opponent team code.")
    opponent_name: str = Field(..., description="Opponent team display name.")
    played: int = Field(..., description="Matches played vs opponent.")
    wins: int = Field(..., description="Wins vs opponent.")
    losses: int = Field(..., description="Losses vs opponent.")
    win_percentage: float = Field(..., description="Win percentage vs opponent.")


class HeadToHeadResponse(BaseModel):
    team_code: str = Field(..., description="Team code.")
    head_to_head: List[HeadToHeadRow] = Field(..., description="Head-to-head table vs all other teams.")
