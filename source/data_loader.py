import requests
import pandas as pd
from datetime import datetime
import os
import time
import re

def limpiar_pgn(pgn_raw):
    """
    Recibe un PGN crudo (con \n, relojes, etc.) y devuelve un PGN limpio y legible.
    """
    if not pgn_raw:
        return ""

    # 1. Reemplazar secuencias \n por saltos de línea reales
    pgn = pgn_raw.replace("\\n", "\n")

    # 2. Quitar anotaciones de reloj {[%clk ...]}
    pgn = re.sub(r"\{.*?\}", "", pgn)

    # 3. Quitar espacios dobles y limpiar
    pgn = re.sub(r"\s+", " ", pgn)
    pgn = pgn.replace(" ]", "]")

    # 4. Asegurar headers en líneas separadas
    pgn = pgn.replace("] [", "]\n[")

    # 5. Doble salto antes de las jugadas
    if "1." in pgn:
        pgn = pgn.replace("] 1.", "]\n\n1.")

    return pgn.strip()

class ChessDownloader:
    def __init__(self, output_dir="../data"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_leaderboard_page(self, game_type="live", page=1):
        url = f"https://www.chess.com/callback/leaderboard/{game_type}?gameType={game_type}&page={page}&totalPage=10000"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            return []
        leaders = r.json().get("leaders", [])
        return [
            {
                "rank": l.get("rank"),
                "username": l["user"].get("username"),
                "title": l["user"].get("chess_title"),
                "country": l["user"].get("country_name"),
                "rating": l.get("score"),
                "games_played": l.get("totalGameCount"),
                "wins": l.get("totalWinCount"),
                "losses": l.get("totalLossCount"),
                "draws": l.get("totalDrawCount")
            }
            for l in leaders
        ]

    def get_leaderboard(self, pages=5, game_type="live", save=True):
        all_players = []
        for page in range(1, pages + 1):
            all_players.extend(self.get_leaderboard_page(game_type, page))
        df = pd.DataFrame(all_players)
        if save:
            path = os.path.join(self.output_dir, "chess_ratings.csv")
            df.to_csv(path, index=False, encoding="utf-8")
        return df

    def get_month_games(self, username, year, month):
        url = f"https://api.chess.com/pub/player/{username.lower()}/games/{year}/{month:02d}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)

        if r.status_code != 200:
            return pd.DataFrame()

        games = r.json().get("games", [])
        clean = []

        for g in games:
            pgn_raw = g.get("pgn", "")
            pgn = limpiar_pgn(pgn_raw)  # ✅ aplicar limpieza aquí

            # extraer código ECO desde el PGN
            match_code = re.search(r'\[ECO "([A-E]\d{2})"\]', pgn)
            eco_code = match_code.group(1) if match_code else None
            eco_name = self.ECO_DICT.get(eco_code, None)

            clean.append({
                "url": g.get("url"),
                "pgn": pgn,
                "time_control": g.get("time_control"),
                "time_class": g.get("time_class"),
                "accuracies_white": g.get("accuracies", {}).get("white"),
                "accuracies_black": g.get("accuracies", {}).get("black"),
                "white_username": g["white"]["username"],
                "white_rating": g["white"]["rating"],
                "white_result": g["white"]["result"],
                "black_username": g["black"]["username"],
                "black_rating": g["black"]["rating"],
                "black_result": g["black"]["result"],
                "eco": eco_code,
                "eco_name": eco_name,
                "rules": g.get("rules"),
            })

        return pd.DataFrame(clean)

    def get_last_n_months_games(self, usernames, n=3, delay=1):
        today = datetime.today()
        months = [(today.year, today.month - i) for i in range(n)]
        months = [(y if m > 0 else y-1, (m-1) % 12 + 1) for (y, m) in months]

        all_games = []
        for user in usernames:
            for y, m in months:
                df = self.get_month_games(user, y, m)
                if not df.empty:
                    all_games.append(df)
            time.sleep(delay)

        if not all_games:
            return pd.DataFrame()

        games = pd.concat(all_games, ignore_index=True).drop_duplicates()
        games = games[(games["time_class"] == "blitz") & (games["rules"] == "chess")]
        games.reset_index(drop=True, inplace=True)
        games["score_white"] = games["white_result"].apply(lambda r: self.map_result("white", r))
        games["score_black"] = games["black_result"].apply(lambda r: self.map_result("black", r))

        path = os.path.join(self.output_dir, "chess_games.csv")
        games.to_csv(path, index=False, encoding="utf-8")
        return games

    import requests
import pandas as pd
from datetime import datetime
import os
import time


class ChessDownloader:
    def __init__(self, output_dir="../data"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_leaderboard_page(self, game_type="live", page=1):
        url = f"https://www.chess.com/callback/leaderboard/{game_type}?gameType={game_type}&page={page}&totalPage=10000"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            return []
        leaders = r.json().get("leaders", [])
        return [
            {
                "rank": l.get("rank"),
                "username": l["user"].get("username"),
                "title": l["user"].get("chess_title"),
                "country": l["user"].get("country_name"),
                "rating": l.get("score"),
                "games_played": l.get("totalGameCount"),
                "wins": l.get("totalWinCount"),
                "losses": l.get("totalLossCount"),
                "draws": l.get("totalDrawCount"),
            }
            for l in leaders
        ]

    def get_leaderboard(self, pages=5, game_type="live", save=True):
        all_players = []
        for page in range(1, pages + 1):
            all_players.extend(self.get_leaderboard_page(game_type, page))
        df = pd.DataFrame(all_players)
        if save:
            path = os.path.join(self.output_dir, "chess_ratings.csv")
            df.to_csv(path, index=False, encoding="utf-8")
        return df

    def get_month_games(self, username, year, month):
        url = f"https://api.chess.com/pub/player/{username.lower()}/games/{year}/{month:02d}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            return pd.DataFrame()
        games = r.json().get("games", [])
        clean = []
        for g in games:
            pgn = g.get("pgn", "")
            
            # extraer código ECO desde el PGN
            match_code = re.search(r'\[ECO "([A-E]\d{2})"\]', pgn)
            eco_code = match_code.group(1) if match_code else None
            eco_name = ECO_DICT.get(eco_code, None) 
            
            clean.append({
                "url": g.get("url"),
                "pgn": pgn,
                "time_control": g.get("time_control"),
                "time_class": g.get("time_class"),
                "accuracies_white": g.get("accuracies", {}).get("white"),
                "accuracies_black": g.get("accuracies", {}).get("black"),
                "white_username": g["white"]["username"],
                "white_rating": g["white"]["rating"],
                "white_result": g["white"]["result"],
                "black_username": g["black"]["username"],
                "black_rating": g["black"]["rating"],
                "black_result": g["black"]["result"],
                "eco": eco_code,
                "eco_name": eco_name,   
                "rules": g.get("rules"),
            })
        return pd.DataFrame(clean)

    def get_last_n_months_games(self, usernames, n=3, delay=1):
        today = datetime.today()
        months = [(today.year, today.month - i) for i in range(n)]
        months = [(y if m > 0 else y - 1, (m - 1) % 12 + 1) for (y, m) in months]

        all_games = []
        for user in usernames:
            for y, m in months:
                df = self.get_month_games(user, y, m)
                if not df.empty:
                    all_games.append(df)
            time.sleep(delay)

        if not all_games:
            return pd.DataFrame()

        games = pd.concat(all_games, ignore_index=True).drop_duplicates()
        games = games[(games["time_class"] == "blitz") & (games["rules"] == "chess")]
        games.reset_index(drop=True, inplace=True)
        games["score_white"] = games["white_result"].apply(lambda r: self.map_result("white", r))
        games["score_black"] = games["black_result"].apply(lambda r: self.map_result("black", r))

        path = os.path.join(self.output_dir, "chess_games.csv")
        games.to_csv(path, index=False, encoding="utf-8")
        return games

    def get_player_info(self, username):
        """Devuelve nombre y avatar de un jugador de Chess.com"""
        url = f"https://api.chess.com/pub/player/{username}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        time.sleep(0.5)  # para no saturar la API
        if r.status_code == 200:
            data = r.json()
            return {
                "name": data.get("name"),
                "avatar": data.get("avatar"),
            }
        return {"name": None, "avatar": None}

    def build_players_table(self, games, leaderboard):
        # --- stats recientes ---
        players = pd.concat([
            games[["white_username", "white_rating", "score_white"]]
                .rename(columns={"white_username": "player",
                                 "white_rating": "rating",
                                 "score_white": "score"}),
            games[["black_username", "black_rating", "score_black"]]
                .rename(columns={"black_username": "player",
                                 "black_rating": "rating",
                                 "score_black": "score"})
        ])

        stats = players.groupby("player").agg(
            games_played=("score", "count"),
            avg_score=("score", "mean"),
            wins=("score", lambda x: (x == 1).sum()),
            draws=("score", lambda x: (x == 0.5).sum()),
            losses=("score", lambda x: (x == 0).sum()),
        ).reset_index()

        # --- merge con leaderboard (stats globales) ---
        players_table = stats.merge(
            leaderboard[["username", "rank", "title", "country", "rating",
                         "games_played", "wins", "losses", "draws"]],
            left_on="player", right_on="username", how="inner"
        ).drop(columns="username")

        players_table = players_table.rename(columns={
            "games_played_x": "games_played_recent",
            "wins_x": "wins_recent",
            "draws_x": "draws_recent",
            "losses_x": "losses_recent",
            "games_played_y": "games_played_total",
            "wins_y": "wins_total",
            "draws_y": "draws_total",
            "losses_y": "losses_total",
            "rating": "rating"   # rating global
        })

        # --- añadir nombre y avatar ---
        players_table[["name", "avatar"]] = players_table["player"].apply(
            lambda u: pd.Series(self.get_player_info(u))
        )

        # --- ordenar columnas ---
        players_table = players_table[
            ["player", "name", "avatar", "rank", "title", "country", "rating",
             "games_played_recent", "wins_recent", "draws_recent", "losses_recent",
             "games_played_total", "wins_total", "draws_total", "losses_total",
             "avg_score"]
        ]

        players_table = self.add_flag_url(players)


        path = os.path.join(self.output_dir, "players_stats.csv")
        players_table.to_csv(path, index=False, encoding="utf-8")
        return players_table

    def map_result(self, color, result):
        if result == "win":
            return 1 if color == "white" else 0
        elif result in {"resigned", "checkmated", "timeout", "abandoned"}:
            return 0 if color == "white" else 1
        elif result in {"repetition", "insufficient", "agreed", "timevsinsufficient", "stalemate", "50move"}:
            return 0.5
        return None
    
    def add_flag_url(self,df):
        df["country_code"] = df["country"].str.split("/").str[-1].str.lower()
        df["flag_url"] = "https://flagcdn.com/h20/" + df["country_code"] + ".png"
        return df


if __name__ == "__main__":
    ECO_DICT = pd.read_csv("./data/eco_dict.csv").set_index("eco")["name"].to_dict()
    downloader = ChessDownloader(output_dir="../data")
    leaders = downloader.get_leaderboard(pages=5)
    usernames = leaders["username"].tolist()
    games = downloader.get_last_n_months_games(usernames, n=3)
    players = downloader.build_players_table(games, leaders)
    print(leaders.shape, games.shape, players.shape)
