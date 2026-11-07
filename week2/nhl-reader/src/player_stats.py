class PlayerStats:
    def __init__(self, reader):
        self.reader = reader

    def top_scorers_by_nationality(self, nationality):
        players = self.reader.get_players()
        national_players = [player for player in players
                            if player.nationality == nationality]
        return sorted(national_players, key=lambda player: player.points,
                      reverse=True)
