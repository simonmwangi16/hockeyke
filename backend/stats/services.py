from matches.models import Match


def empty_row(team):
    return {
        "team": team,
        "played": 0,
        "won": 0,
        "drawn": 0,
        "lost": 0,
        "goals_for": 0,
        "goals_against": 0,
        "goal_difference": 0,
        "points": 0,
        "form": [],
    }


def calculate_standings(league_season):
    table = {}

    all_matches = Match.objects.filter(
        league_season=league_season,
    ).select_related("home_team", "away_team")

    # Add all teams from fixtures first
    for match in all_matches:
        table.setdefault(match.home_team.id, empty_row(match.home_team))
        table.setdefault(match.away_team.id, empty_row(match.away_team))

    # Apply only completed results
    completed_matches = all_matches.filter(status="FT")

    for match in completed_matches:
        home_row = table[match.home_team.id]
        away_row = table[match.away_team.id]

        home_score = match.home_score
        away_score = match.away_score

        home_row["played"] += 1
        away_row["played"] += 1

        home_row["goals_for"] += home_score
        home_row["goals_against"] += away_score

        away_row["goals_for"] += away_score
        away_row["goals_against"] += home_score

        if home_score > away_score:
            home_row["won"] += 1
            away_row["lost"] += 1
            home_row["points"] += 3
            home_row["form"].append("W")
            away_row["form"].append("L")
        elif home_score < away_score:
            away_row["won"] += 1
            home_row["lost"] += 1
            away_row["points"] += 3
            home_row["form"].append("L")
            away_row["form"].append("W")
        else:
            home_row["drawn"] += 1
            away_row["drawn"] += 1
            home_row["points"] += 1
            away_row["points"] += 1
            home_row["form"].append("D")
            away_row["form"].append("D")

    for row in table.values():
        row["form"] = row["form"][-5:]
        row["goal_difference"] = row["goals_for"] - row["goals_against"]

    return sorted(
        table.values(),
        key=lambda row: (
            -row["points"],
            -row["goal_difference"],
            -row["goals_for"],
            row["team"].name,
        )
    )


def calculate_team_stats(league_season):
    table = {}

    matches = Match.objects.filter(
        league_season=league_season,
        status="FT",
    ).select_related(
        "home_team",
        "away_team",
    ).order_by("match_date", "match_time")

    for match in matches:
        for team in [match.home_team, match.away_team]:
            if team.id not in table:
                table[team.id] = {
                    "team": team,
                    "goals_scored": 0,
                    "goals_conceded": 0,
                    "clean_sheets": 0,
                    "current_winning_streak": 0,
                    "longest_winning_streak": 0,
                    "current_losing_streak": 0,
                    "longest_losing_streak": 0,
                }

        home_stats = table[match.home_team_id]
        away_stats = table[match.away_team_id]

        home_goals = match.home_score
        away_goals = match.away_score

        home_stats["goals_scored"] += home_goals
        home_stats["goals_conceded"] += away_goals

        away_stats["goals_scored"] += away_goals
        away_stats["goals_conceded"] += home_goals

        if away_goals == 0:
            home_stats["clean_sheets"] += 1

        if home_goals == 0:
            away_stats["clean_sheets"] += 1

        if home_goals > away_goals:
            home_stats["current_winning_streak"] += 1
            home_stats["longest_winning_streak"] = max(
                home_stats["longest_winning_streak"],
                home_stats["current_winning_streak"],
            )
            home_stats["current_losing_streak"] = 0

            away_stats["current_losing_streak"] += 1
            away_stats["longest_losing_streak"] = max(
                away_stats["longest_losing_streak"],
                away_stats["current_losing_streak"],
            )
            away_stats["current_winning_streak"] = 0

        elif home_goals < away_goals:
            away_stats["current_winning_streak"] += 1
            away_stats["longest_winning_streak"] = max(
                away_stats["longest_winning_streak"],
                away_stats["current_winning_streak"],
            )
            away_stats["current_losing_streak"] = 0

            home_stats["current_losing_streak"] += 1
            home_stats["longest_losing_streak"] = max(
                home_stats["longest_losing_streak"],
                home_stats["current_losing_streak"],
            )
            home_stats["current_winning_streak"] = 0

        else:
            home_stats["current_winning_streak"] = 0
            home_stats["current_losing_streak"] = 0
            away_stats["current_winning_streak"] = 0
            away_stats["current_losing_streak"] = 0

    return sorted(
        table.values(),
        key=lambda row: (-row["goals_scored"], row["team"].name),
    )