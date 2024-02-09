from flask import Blueprint
from flask_login import current_user, login_required

from project.game_controller import gforui, rforui, uforui

from project.models import Game, Round, User
from sqlalchemy import update

from flask import request
from project import db

from flask_socketio import SocketIO, join_room, leave_room, send
from .round_controller import RoundController, rounds
from datetime import datetime


def addGame(app, socketio:SocketIO):
    testing=True
    game = Blueprint('game', __name__)

    def now():
        nowt = datetime.now()
        time = nowt.strftime("%m/%d/%Y, %H:%M:%S")
        return time


    @game.route("/user/<id>")
    #@login_required
    def getUser(id):
        result = User.query.filter_by(id=int(id)).first()

        return result.name

    @game.route("/game/all")
    def allGames():
        return [gforui(-1, g) for g in  Game.query.all()]

    @game.route("/round/all")
    def allRounds():
        return [rforui(-1, r) for r in  Round.query.all()]


    @game.route("/game/new")
    #@login_required
    def newg():
        new_game = Game(np = request.args.get("np"), players ="", name="", rounds="", time=now() )
        # add the new user to the database
        db.session.add(new_game)
        db.session.commit()
        return str(new_game.id)

    @game.route("/game/<game_id>/round/new")
    #@login_required
    def newr(game_id):
        new_round = Round(np = request.args.get("np"), players ="", name="", game_id=game_id, state="CREATED", time=now() )
        gameq = Game.query.filter(Game.id == game_id).first()
        db.session.add(new_round)
        db.session.commit()
        #update(Game).where(Game.id == game_id).values(Game.rounds = Game.rounds + ","+ new_round.id)
        gameq.rounds=str(new_round.id) if (len(gameq.rounds) == 0) else (gameq.rounds + ","+str(new_round.id))
        # add the new user to the database

        db.session.commit()

        return str(new_round.id)

    @game.route("/game/<game_id>/join")
    #@login_required
    def joing(game_id):
        user_id = str(current_user.id) if current_user.is_authenticated  else request.args.get("user_id")
        game = Game.query.filter_by(id=int(game_id)).first()
        
        players = game.players
        users = [p.split(':')[0] for p in players.split(",") if p!=""]
        if(user_id not in users ):
            game.players = f"{players}{ ',' if len(players)>0 else ''}{user_id}:0"
        db.session.commit()
        # add the new user to the database
        return str(game.id)

    @game.route("/round/<round_id>/join")
    #@login_required
    def joinr(round_id):
        user_id = str(current_user.id) if current_user.is_authenticated  else request.args.get("user_id")
        round = Round.query.filter_by(id=int(round_id)).first()
        players = round.players
        users = [p.split(':')[0] for p in players.split(",") if p!=""]
        if(round.state == "CREATED" and user_id not in users and len(users)<4 ):
            round.players = f"{players}{ ',' if len(players)>0 else ''}{user_id}:0"
        db.session.commit()
        # add the new user to the database
        return str(round.id)


    @game.route("/round/<round_id>/finish")
    #@login_required
    def finish(round_id):
        user_id = str(current_user.id) if current_user.is_authenticated  else request.args.get("user_id")
        round = Round.query.filter_by(id=round_id).first()
        if(round.state == "PLAYING"):
            round.state = "FINISHED"


        if (int(round_id) in rounds):
            rc = rounds[int(round_id)]
            finished = rc.finish(int(user_id))
            if(finished):
                round.players = ",".join([ f"{p.id}:{p.score}" for p in rc.players])
                db.session.commit()
                socketio.emit("update", f"finish:{user_id}", to="round"+str(round_id) )
        # add the new user to the database
        return rforui(round_id, round)

    @game.route("/round/<round_id>/abondon")
    #@login_required
    def abondon(round_id):
        user_id = str(current_user.id) if current_user.is_authenticated  else request.args.get("user_id")
        round = Round.query.filter_by(id=round_id).first()
        if(round.state != "PLAYING"):
            return rforui(round_id, round)


        if (int(round_id) in rounds):
            rc = rounds[int(round_id)]
            abondoned = rc.abondon(int(user_id))
            socketio.emit("update", "abondon:{user_id}", to="round"+str(round_id) )
            if(abondoned):
                round.state = "ABONDONED"
                db.session.commit()
                socketio.emit("update", f"abondonconfirmed", to="round"+str(round_id) )


        # add the new user to the database
        return rforui(round_id, round)
    


    @game.route("/round/<round_id>/init")
    #@login_required
    def initr(round_id):
        #email = current_user.email
        rounds
        round = Round.query.filter_by(id=round_id).first()
        if(round.state == "CREATED"):
            round.state = "PLAYING"

            rc = RoundController(round.id)

            players = round.players.split(",")
            for p in players:
                rc.join(uforui(p))
            

            rc.initRoundController()
            socketio.emit("init", f"", to="round"+str(round_id) )

        db.session.commit()
        # add the new user to the database
        return rforui(-1, round)


    @game.route("/round/<round_id>/move")
    #@login_required
    def mover(round_id):
        user_id = str(current_user.id) if current_user.is_authenticated  else request.args.get("user_id")
        ip1 = request.args.get("ip1")
        ip2 = request.args.get("ip2")
        ics1 = request.args.get("ics1")
        ics2 = request.args.get("ics2")
        idc1 = request.args.get("idc1")
        idc2 = request.args.get("idc2")

        if (int(round_id) in rounds):
            round = rounds[int(round_id)]
            moveResult = round.move(int(ip1), int(ip2), int(ics1),int(ics2), int(idc1), int(idc2) )
            if (ip1 == ip2 and ics1 == ics2 and ics1 == "0"  ):
                pass
            else:
                socketio.emit("move", f"{moveResult[0]}{str(moveResult[1])}{str(moveResult[2])}", to="round"+str(round_id) )
            return round.tojson(int(user_id))
        

    @game.route("/round/<round_id>/details")
    #@login_required
    def detailsr(round_id):
        version =  request.args.get("version")
        user_id = str(current_user.id) if current_user.is_authenticated  else request.args.get("user_id")
        if (int(round_id) in rounds):
            rc = rounds[int(round_id)]
            #if(rc.version>int(version)):
            return rounds[int(round_id)].tojson(int(user_id))

        return {}
    
    @game.route("/round/<round_id>/nextp")
    #@login_required
    def setNextP(round_id):
        user_id = str(current_user.id) if current_user.is_authenticated  else request.args.get("user_id")
        if (int(round_id) in rounds):
            rc = rounds[int(round_id)]
            rc.nextPlayer = int(request.args.get("nextp"))
            #if(rc.version>int(version)):
            socketio.emit("update", f"nextp", to="round"+str(round_id) )
            return {}
            

        return {}
    
    @socketio.on('join')
    def on_join(data):
        username = data['user_id']
        room = data['room']
        join_room(room)
        send(str(username) + ' has entered the room.', to=room)
    
    @socketio.on('leave')
    def on_leave(data):
        username = data['username']
        room = data['room']
        leave_room(room)
        send(username + ' has left the room.', to=room)
        
    return game
