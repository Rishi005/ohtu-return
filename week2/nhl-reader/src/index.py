from rich.console import Console
from rich.table import Table

from player_reader import PlayerReader
from player_stats import PlayerStats


def get_players_by_nationality():
    season = input("Season (e.g. 2024-25): ").strip()
    nationality = input("Nationality (e.g. FIN): ").strip().upper()
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    return season, nationality, stats.top_scorers_by_nationality(nationality)


def create_table(season, nationality, players):
    table = Table(title=f"Players from {nationality}, season {season}")
    table.add_column("Player")
    table.add_column("Team")
    table.add_column("Goals", justify="right")
    table.add_column("Assists", justify="right")
    table.add_column("Points", justify="right")
    table.add_column("Games", justify="right")

    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.points),
            str(player.games),
        )
    return table


def main():
    season, nationality, players = get_players_by_nationality()
    table = create_table(season, nationality, players)
    Console().print(table)


if __name__ == "__main__":
    main()
