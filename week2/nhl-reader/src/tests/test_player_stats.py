import unittest

from player import Player
from player_stats import PlayerStats


class StubPlayerReader:
    def __init__(self, players):
        self.players = players

    def get_players(self):
        return self.players


class TestPlayerStats(unittest.TestCase):
    def setUp(self):
        players = [
            Player({
                "name": "Finn",
                "nationality": "FIN",
                "assists": 10,
                "goals": 5,
                "team": "AAA",
                "games": 20,
                "id": 1,
            }),
            Player({
                "name": "Swede",
                "nationality": "SWE",
                "assists": 2,
                "goals": 8,
                "team": "AAA",
                "games": 20,
                "id": 2,
            }),
            Player({
                "name": "Other Finn",
                "nationality": "FIN",
                "assists": 4,
                "goals": 6,
                "team": "BBB",
                "games": 20,
                "id": 3,
            }),
        ]
        self.stats = PlayerStats(StubPlayerReader(players))

    def test_top_scorers_by_nationality(self):
        players = self.stats.top_scorers_by_nationality("FIN")

        self.assertEqual(["Finn", "Other Finn"],
                         [player.name for player in players])

    def test_top_scorers_by_team(self):
        players = self.stats.top_scorers_by_team("AAA")

        self.assertEqual(["Finn", "Swede"],
                         [player.name for player in players])

    def test_top_goal_scorers(self):
        players = self.stats.top_goal_scorers(2)

        self.assertEqual(["Swede", "Other Finn"],
                         [player.name for player in players])


if __name__ == "__main__":
    unittest.main()
