import unittest
from unittest.mock import patch

from player_reader import PlayerReader


class StubResponse:
    def __init__(self, players):
        self.players = players

    def json(self):
        return self.players


class TestPlayerReader(unittest.TestCase):
    def test_get_players_uses_response_data_without_network(self):
        response_data = [
            {
                "name": "Test Player",
                "nationality": "FIN",
                "assists": 4,
                "goals": 3,
                "team": "AAA",
                "games": 10,
                "id": 1,
            }
        ]

        with patch(
            "player_reader.requests.get",
            return_value=StubResponse(response_data),
        ) as get:
            players = PlayerReader("https://example.invalid/players").get_players()

        get.assert_called_once_with(
            "https://example.invalid/players",
            timeout=10,
        )
        self.assertEqual(1, len(players))
        self.assertEqual("Test Player", players[0].name)
        self.assertEqual(7, players[0].points)


if __name__ == "__main__":
    unittest.main()
