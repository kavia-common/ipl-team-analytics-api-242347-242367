from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class TeamInfo:
    """Represents a team metadata record used by the API."""

    code: str
    name: str
    colors: Tuple[str, str]


def _round2(value: float) -> float:
    return float(f"{value:.2f}")


class AnalyticsEngine:
    """
    Simple analytics engine.

    Notes:
    - This implementation intentionally uses deterministic in-memory sample data so the API is fully functional
      without requiring a dataset in this template repository.
    - The public methods are structured to be easily replaced with real computations from ball-by-ball data later.
    """

    def __init__(self) -> None:
        self._teams: List[TeamInfo] = [
            TeamInfo(code="CSK", name="Chennai Super Kings", colors=("#FBBF24", "#1F2937")),
            TeamInfo(code="MI", name="Mumbai Indians", colors=("#2563EB", "#F59E0B")),
            TeamInfo(code="RCB", name="Royal Challengers Bangalore", colors=("#EF4444", "#111827")),
            TeamInfo(code="KKR", name="Kolkata Knight Riders", colors=("#7C3AED", "#F59E0B")),
            TeamInfo(code="RR", name="Rajasthan Royals", colors=("#EC4899", "#1F2937")),
            TeamInfo(code="DC", name="Delhi Capitals", colors=("#2563EB", "#EF4444")),
            TeamInfo(code="SRH", name="Sunrisers Hyderabad", colors=("#F97316", "#111827")),
            TeamInfo(code="PBKS", name="Punjab Kings", colors=("#EF4444", "#F9FAFB")),
            TeamInfo(code="GT", name="Gujarat Titans", colors=("#111827", "#F59E0B")),
            TeamInfo(code="LSG", name="Lucknow Super Giants", colors=("#2563EB", "#F59E0B")),
        ]
        self._team_by_code: Dict[str, TeamInfo] = {t.code: t for t in self._teams}

        # Precomputed sample metrics for charting. All values are template/demo numbers.
        self._team_kpis: Dict[str, dict] = {}
        for idx, t in enumerate(self._teams):
            base = 1500 + idx * 60
            balls = 1200 + idx * 50
            runs = base * 10 + idx * 123
            boundaries_4 = 320 + idx * 7
            boundaries_6 = 140 + idx * 4
            dots = 380 + idx * 5
            wickets_lost = 220 + idx * 3
            overs = balls / 6.0

            self._team_kpis[t.code] = {
                "matches": 200 - (idx % 7) * 8,
                "wins": 120 - (idx % 5) * 9,
                "losses": 70 - (idx % 4) * 7,
                "no_results": 10 + (idx % 3),
                "runs_scored": runs,
                "balls_faced": balls,
                "overs_faced": _round2(overs),
                "run_rate": _round2(runs / overs),
                "boundaries": {
                    "fours": boundaries_4,
                    "sixes": boundaries_6,
                    "total": boundaries_4 + boundaries_6,
                },
                "dot_balls": {"count": dots, "percentage": _round2((dots / balls) * 100.0)},
                "wickets_lost": wickets_lost,
            }

        # Example top performers; structure designed for frontend tables.
        self._top_batters: Dict[str, List[dict]] = {}
        self._top_bowlers: Dict[str, List[dict]] = {}
        for idx, t in enumerate(self._teams):
            self._top_batters[t.code] = [
                {
                    "player": f"{t.code} Batter {i}",
                    "runs": 3400 - i * 210 + idx * 35,
                    "balls": 2600 - i * 160 + idx * 22,
                    "strike_rate": _round2((3400 - i * 210 + idx * 35) / (2600 - i * 160 + idx * 22) * 100),
                    "fours": 360 - i * 25 + idx * 2,
                    "sixes": 140 - i * 12 + idx * 1,
                    "matches": 110 - i * 6,
                }
                for i in range(1, 6)
            ]
            self._top_bowlers[t.code] = [
                {
                    "player": f"{t.code} Bowler {i}",
                    "wickets": 140 - i * 9 + idx * 2,
                    "overs": _round2(420 - i * 18 + idx * 3),
                    "economy": _round2(7.9 + (i * 0.18) - (idx * 0.03)),
                    "dot_ball_percentage": _round2(39.0 + i * 1.2 - idx * 0.5),
                    "matches": 120 - i * 5,
                }
                for i in range(1, 6)
            ]

    def get_team(self, team_code: str) -> Optional[TeamInfo]:
        return self._team_by_code.get(team_code.upper())

    def list_teams(self) -> List[TeamInfo]:
        return list(self._teams)

    def get_team_overview(self, team_code: str) -> dict:
        team_code = team_code.upper()
        info = self._require_team(team_code)
        kpi = self._team_kpis[team_code]

        wins = int(kpi["wins"])
        matches = int(kpi["matches"])
        win_pct = _round2((wins / matches) * 100.0) if matches > 0 else 0.0

        return {
            "team": {"code": info.code, "name": info.name, "colors": {"primary": info.colors[0], "secondary": info.colors[1]}},
            "kpis": {
                **kpi,
                "win_percentage": win_pct,
            },
        }

    def get_team_boundary_analysis(self, team_code: str) -> dict:
        team_code = team_code.upper()
        self._require_team(team_code)
        boundaries = self._team_kpis[team_code]["boundaries"]
        balls = int(self._team_kpis[team_code]["balls_faced"])

        fours = int(boundaries["fours"])
        sixes = int(boundaries["sixes"])
        boundary_balls = fours + sixes

        return {
            "team_code": team_code,
            "boundaries": {
                "fours": fours,
                "sixes": sixes,
                "total": int(boundaries["total"]),
                "boundary_ball_percentage": _round2((boundary_balls / balls) * 100.0) if balls > 0 else 0.0,
            },
            "by_over": [
                # 20-over breakdown for a common T20 innings (template numbers).
                {"over": o, "fours": max(0, (o + len(team_code)) % 4 - 1), "sixes": max(0, (o + len(team_code)) % 5 - 3)}
                for o in range(1, 21)
            ],
        }

    def get_team_run_rate_breakdown(self, team_code: str) -> dict:
        team_code = team_code.upper()
        self._require_team(team_code)

        # Typical T20 phases: powerplay(1-6), middle(7-15), death(16-20)
        # Template values are stable but distinct by team.
        seed = sum(ord(c) for c in team_code)
        pp = 8.1 + (seed % 7) * 0.12
        mid = 7.4 + (seed % 5) * 0.10
        death = 9.6 + (seed % 6) * 0.14

        return {
            "team_code": team_code,
            "phases": [
                {"phase": "Powerplay (1-6)", "overs": 6, "run_rate": _round2(pp)},
                {"phase": "Middle (7-15)", "overs": 9, "run_rate": _round2(mid)},
                {"phase": "Death (16-20)", "overs": 5, "run_rate": _round2(death)},
            ],
            "runs_per_over": [{"over": o, "run_rate": _round2(6.2 + ((seed + o) % 10) * 0.35)} for o in range(1, 21)],
        }

    def get_team_wicket_types(self, team_code: str) -> dict:
        team_code = team_code.upper()
        self._require_team(team_code)

        # Common wicket types; template share sums to 100.
        seed = (sum(ord(c) for c in team_code) % 11) + 1
        caught = 46 + (seed % 7)
        bowled = 18 + (seed % 5)
        lbw = 10 + (seed % 4)
        run_out = 9 + (seed % 3)
        stumped = 6 + (seed % 2)
        other = max(0, 100 - (caught + bowled + lbw + run_out + stumped))

        return {
            "team_code": team_code,
            "wicket_types": [
                {"type": "Caught", "percentage": caught},
                {"type": "Bowled", "percentage": bowled},
                {"type": "LBW", "percentage": lbw},
                {"type": "Run Out", "percentage": run_out},
                {"type": "Stumped", "percentage": stumped},
                {"type": "Other", "percentage": other},
            ],
        }

    def get_team_dot_ball_stats(self, team_code: str) -> dict:
        team_code = team_code.upper()
        self._require_team(team_code)
        dd = self._team_kpis[team_code]["dot_balls"]
        return {
            "team_code": team_code,
            "dot_balls": {"count": int(dd["count"]), "percentage": float(dd["percentage"])},
            "dot_ball_percentage_by_year": self._year_series(team_code, base=38.0, jitter=3.0),
        }

    def get_team_yearly_performance(self, team_code: str) -> dict:
        team_code = team_code.upper()
        self._require_team(team_code)
        seed = sum(ord(c) for c in team_code)

        years = list(range(2008, 2023))
        rows = []
        for y in years:
            w = 6 + ((seed + y) % 9)
            l = 3 + ((seed + 2 * y) % 7)
            nrr = _round2(-0.25 + ((seed + 3 * y) % 100) / 100.0 * 0.9)
            rows.append(
                {
                    "year": y,
                    "matches": w + l,
                    "wins": w,
                    "losses": l,
                    "net_run_rate": nrr,
                    "position": 1 + ((seed + y) % 10),
                }
            )
        return {"team_code": team_code, "yearly": rows}

    def get_team_head_to_head(self, team_code: str) -> dict:
        team_code = team_code.upper()
        self._require_team(team_code)
        seed = sum(ord(c) for c in team_code)

        rows = []
        for opp in self._teams:
            if opp.code == team_code:
                continue
            played = 24 - ((seed + sum(ord(c) for c in opp.code)) % 8)
            wins = max(0, (played // 2) + ((seed - len(opp.code)) % 5) - 2)
            losses = max(0, played - wins)
            rows.append(
                {
                    "opponent_code": opp.code,
                    "opponent_name": opp.name,
                    "played": played,
                    "wins": wins,
                    "losses": losses,
                    "win_percentage": _round2((wins / played) * 100.0) if played > 0 else 0.0,
                }
            )
        rows.sort(key=lambda r: (-r["played"], -r["wins"], r["opponent_code"]))
        return {"team_code": team_code, "head_to_head": rows}

    def get_top_batters(self, team_code: str) -> List[dict]:
        team_code = team_code.upper()
        self._require_team(team_code)
        return list(self._top_batters[team_code])

    def get_top_bowlers(self, team_code: str) -> List[dict]:
        team_code = team_code.upper()
        self._require_team(team_code)
        return list(self._top_bowlers[team_code])

    def _require_team(self, team_code: str) -> TeamInfo:
        team = self.get_team(team_code)
        if team is None:
            raise KeyError(f"Unknown team_code '{team_code}'")
        return team

    def _year_series(self, team_code: str, base: float, jitter: float) -> List[dict]:
        seed = sum(ord(c) for c in team_code)
        out = []
        for y in range(2008, 2023):
            v = base + (((seed + y) % 100) / 100.0) * jitter - jitter / 2.0
            out.append({"year": y, "value": _round2(v)})
        return out
