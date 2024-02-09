
from project.models import Game, Round, User

row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

def decriptPlayers(o):
    if("players" in o and len(o["players"])>0):
        players = [uforui(id) for id in o["players"].split(",") if id != ""]
        o["players"] = players
    return o

def decriptGame(o):
    if("rounds" in o and len(o["rounds"])>0):
        rounds = [rforui(int(id)) for id in o["rounds"].split(",") if id != ""]
        o["rounds"] = rounds

    result = decriptPlayers(o)
    for ug in o["players"]:
        for r in o["rounds"]:
            if r["state"]=="FINISHED":
                for ur in r["players"]:
                    if(ug["id"] == ur["id"]):
                        ug["score"] += ur["score"]

    return result

def rforui(id:int, round=None):
    if(round == None):
        round = Round.query.filter_by(id=int(id)).first()
    return decriptPlayers(row2dict(round))

def gforui(id:int, game=None):
    if(game == None):
        game = Game.query.filter_by(id=int(id)).first()
    return decriptGame(row2dict(game))

def uforui(id:str):
    p = User.query.filter_by(id=int(id.split(":")[0])).first()
    return {"id": p.id, "name":p.name, "score":int(id.split(":")[1])}