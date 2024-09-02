import Supplements
from Module import Module
import pickle
import requests
f = open("SportsKey.qrs", "r")
key = f.read()
f.close()
#TODO: Fix misassociation bug (fixed? needs full names, but nicknames can be added manually)

class Sports(Module):
    def __init__(self, env):
        super().__init__("Sports", ["game", "standings"])
        self.env = env
        with open('team_ids.pkl', 'rb') as f:
            try:
                self.ids = pickle.load(f)
                env.log("ID's loaded")
            except EOFError:
                self.ids = {"la galaxy": 1605}
                env.flag("Warning: No File Found")
            env.log(self.ids)

    def saveDict(self):
        with open('team_ids.pkl', 'wb') as f:
            self.env.log("team ids saved")
            pickle.dump(self.ids, f)

    def process(self, text: str):
        text = text.split(" ")
        if "standings" in text:
            pass
        if "when" in text or "when's" in text:
            team = " ".join(text[text.index("next")+1:text.index("game")])
            self.env.log("Finding next game for: " + team)
            if team in self.ids:
                id = self.ids[team]
            else:
                self.env.flag(f"{team} not found in ids, searching for team")
                r = requests.get("https://v3.football.api-sports.io/teams", headers={
                    'x-rapidapi-host': "https://v3.football.api-sports.io",
                    'x-rapidapi-key': key
                }, params={
                    'search': team
                    # BUG: may lead to incorrect IDs in rare cases THE CASES ARE NOT RARE
                })
                if r.status_code == 200:
                    self.ids[team] = r.json()["response"][0]["team"]["id"]
                    self.saveDict()
                    id = self.ids[team]
                else:
                    self.env.throw(f"{team} not found")
                    return "error: team not located", None

            r = requests.get("https://v3.football.api-sports.io/fixtures", headers={
                    'x-rapidapi-host': "https://v3.football.api-sports.io",
                    'x-rapidapi-key': key
                }, params={
                'team': id,
                'timezone': 'America/New_York',
                'next': '1'
            })
            if r.status_code == 200:
                r = r.json()["response"][0]
                status = r["fixture"]["status"]["short"]
                if status not in "NS TBD PST CANC ABD":
                    return team + " is currently playing", None
                home, away = r["teams"]["home"]["name"], r["teams"]["away"]["name"]
                if status == "TBD":
                    return f"{home} will play {away} at an unknown date", None
                if status == "PST":
                    return f"the match between {home} and {away} has been postponed", None
                if status == "CANC" or status == "ABD":
                    return f"the match between {home} and {away} has been cancelled or abandoned", None
                else:
                    timeString = Supplements.dsToText(r["fixture"]["date"])
                    return f"{home} will play {away} {timeString}", None
            else:
                return "error: match not found", None
