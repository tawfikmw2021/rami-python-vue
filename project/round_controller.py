import random
import uuid
 
colors = ['hearts', 'diamonds', 'clubs', 'spades']
Card = list[int] #id,owner,icards,order
def rCards() -> list[Card]:
    initialCards = [[i%13+1, colors[int(i/26)], i] for i in range(104)] + [[0, '', 104], [0, '', 105],[0, '', 106],[0, '', 107]]
    random.seed()
    return sorted([[card[-1], -1, 0, idx] for idx, card in enumerate(initialCards)], key=lambda c : random.random())


class Player:

    cards : list[list[Card]] = []
    order:int = -1
    id:int
    score:int
    STATE_PLAYING = "PLAYING"
    STATE_HABET = "HABET"

    def __init__(self, id, order, name, round) -> None:
        self.round = round
        self.taken = False
        self.order = order
        self.cards = [[]]
        self.name = name
        self.id = id
        self.score = 100
        self.state = Player.STATE_PLAYING

    def tojson(self, verbose:bool) -> dict:
        dic = {"order":self.order, "name":self.name, "id":self.id, "score":self.score}
        dic["ncards"] = len(self.cards[0])
        dic["ncards2"] = self.round.getNCards(self.order)

        if(verbose):
            dic["cards"] =self.cards
        else:
            dic["cards"] = [[]] + self.cards[1:]

        return dic 

class RoundController:
    players:list[Player]
    def __init__(self, id:int) -> None:
        rounds[id] = self 
        self.id = id
        self.cards = [rCards(), []]
        self.players = []
        self.uid = str(uuid.uuid4())
        self.actions = []
        self.abondoned = set()
        self.nextPlayer = 0

        self.version = -1

        self.currentPlayer = int(0)
    
    def goToNextPlayer(self, user_id):
        actionnerOrder = [u for u in self.players if u.id == int(user_id)][0].order
        if(self.currentPlayer != actionnerOrder): return False
        self.currentPlayer = (self.currentPlayer+1)%len(self.players)
        return True

    def join(self, p):
        self.players.append(Player(int(p['id']), len(self.players), p['name'], self))


    def initRoundController(self):
        self.version += 1
        if(len(self.players[0].cards[0])>0) :return False 
        for i in range(7):
            if( i == 0):
                self.giveToPlayer(self.players[0].order)
            for p in self.players:
                self.giveToPlayer(p.order, 2)
    
    def giveToPlayer(self, ip:int, ct:int = 1):
        for i in range(ct):
            self.move(self.players[self.currentPlayer].id,  -1, ip, 0, 0, None, None, bypass=True)

    
    def finish(self, pid):
        finished = False

        for p in self.players:
            if(len(p.cards[0]) == 0):
                p.score = -10
                finished = True
            else :
                if(len(p.cards[0]) < 10) :
                    score = sum([ (number if (number>1 and number<10) else 10)
                                  for number in  
                                  [(card[0] %13 + 1 if card[0]<104 else 0) for card in p.cards[0]]
                                  ] )
                    p.score = score
        return finished
    
    def abondon(self, pid)->bool:
        self.abondoned.add(pid)
        if(len(self.abondoned)  == len(self.players)):
            return True
        return False
    
    def getNCards(self, ip:int):
        result = 0
        for i in range(len(self.players)):
            p = self.players[i]
            for cs in p.cards:
                result += len([1 for c in cs if c[1] == ip])
        return result
    
    ACTION_REORDER = "REORDER"
    ACTION_DROP = "DROP"
    ACTION_BUY = "BUY"
    ACTION_FASKEL = "FASKEL"
    ACTION_HBOUT = "HBOUT"
    ACTION_RAKKEB = "RAKKEB"

    def checkMove(self, iPlayer1:int, iPlayer2:int, iCards1:int, iCards2:int, idCard1:int, idCard2:int) -> tuple[str, bool]:
        # reordering
        case1 = iPlayer1 == iPlayer2 and iCards1 == iCards2 
        if(case1) : return RoundController.ACTION_REORDER, True

        # drop
        case2 = iPlayer1>=0 and iPlayer2 == -1 and iCards1 == 0 and iCards2 == 1 and self.getNCards(iPlayer1) == 15
        if(case2) : return RoundController.ACTION_DROP, True

        # get card
        case3 = iPlayer1==-1 and iPlayer2 >=0 and iCards1 == 0 and iCards2 == 0 and self.getNCards(iPlayer2) == 14
        if(case3) : return RoundController.ACTION_BUY, self.nextPlayer == iPlayer2

        #faskel
        case4 = iPlayer1==-1 and iPlayer2 >=0 and iCards1 == 1 and iCards2 == 0 and self.getNCards(iPlayer2) == 14
        if(case4): return RoundController.ACTION_FASKEL, self.nextPlayer == iPlayer2

        #hbout
        case5 = iPlayer1>=0 and iPlayer2 ==iPlayer1 and iCards1 == 0 and iCards2 >= 1 and self.getNCards(iPlayer1) == 15 \
            and self.players[iPlayer1].state == Player.STATE_PLAYING
        if(case5): return RoundController.ACTION_HBOUT, self.nextPlayer == (iPlayer1 + 1)%len(self.players)
        
        #rakkeb
        case5 = iPlayer1>=0 and iPlayer2 >=0 and iCards1 == 0 and iCards2 >= 1 and self.getNCards(iPlayer1) == 15
        if(case5): return RoundController.ACTION_RAKKEB, self.nextPlayer == (iPlayer1 + 1)%len(self.players)

        return "UNKNOWN", False
    
    def checkMoveDeep(self, iPlayer1:int, iPlayer2:int, iCards1:int, iCards2:int, idCard1:int, idCard2:int):
        action, alllowed = self.checkMove(iPlayer1, iPlayer2, iCards1, iCards2, idCard1, idCard2) 
        if(action == RoundController.ACTION_DROP and len(self.cards)<10) : return action, self.checkHbout(iPlayer1), "hbout"
        return action, alllowed, "simple"

    def checkHbout(self, iPlayer1):
        return True

    
    def postMove(self, moved, action, iPlayer1, iPlayer2, iCards1, iCards2, idCard1, idCard2 ):
        if(action == RoundController.ACTION_BUY and moved ):
            self.nextPlayer = (self.nextPlayer +1) % len(self.players)
        if(action == RoundController.ACTION_FASKEL and moved ): self.nextPlayer = (self.nextPlayer +1) % len(self.players)



    def move(self,user_id, iPlayer1:int, iPlayer2:int, iCards1:int, iCards2:int, idCard1:int, idCard2:int, bypass=False) -> tuple[str, bool, bool]:
         action, isallowed, reason =  self.checkMoveDeep(iPlayer1, iPlayer2, iCards1, iCards2, idCard1, idCard2) 
         self.version += 1
         self.abondoned.clear()
         actionnerOrder = [u for u in self.players if u.id == int(user_id)][0].order
         if(not bypass and action != RoundController.ACTION_REORDER and self.currentPlayer != actionnerOrder) : return "UNOTHORIZED", False, False
         moved = self.moveInternal(iPlayer1, iPlayer2, iCards1, iCards2, idCard1, idCard2)
         self.postMove(moved ,action, iPlayer1, iPlayer2, iCards1, iCards2, idCard1, idCard2)
         return action, isallowed, moved 
    
    def moveInternal(self, iPlayer1:int, iPlayer2:int, iCards1:int, iCards2:int, idCard1:int, idCard2:int) -> bool:
        
        # cas 1 : jebt
        if(iPlayer1 == -1 and iCards1 == 0):
            # cas cartes finis
            if(len(self.cards[0]) == 0) :
                droppedCards = self.cards[1]
                self.cards[0] = sorted(droppedCards[0:len(droppedCards) - 4], key = lambda x:random.random())
                self.cards[1] = droppedCards[len(droppedCards) - 4::]
                for card in self.cards[0]:
                    card[2] = 0

            card = self.cards[0].pop()
            card[1] = iPlayer2
            card[3] = len(self.players[iPlayer2].cards[0] )
            self.players[iPlayer2].cards[0].append(card)
            
            return True
        
        # cas tayech
        if(iPlayer2 == -1 and iCards2 == 0):
            cards1 = self.cards[iCards1] if(iPlayer1 == -1) else self.players[iPlayer1].cards[iCards1]
            cards2 = self.cards[iCards2] if(iPlayer2 == -1) else self.players[iPlayer2].cards[iCards2]
            index1 = -1
            for i in range(len(cards1)):
                if (cards1[i][0] == idCard1): index1 = i

            cards2.append(cards1[index1])
            cards1.remove(cards1[index1])

            return True

        
        
        if(iPlayer2>=len(self.players) or iPlayer1>=len(self.players)): return False

        # cas ahbet bacou jdid 
        if(iPlayer2 == iPlayer1  and iCards2 == len(self.players[iPlayer2].cards)):
            self.players[iPlayer2].cards.append([])
        
        #if( iCards2 >= len(self.players[iPlayer2].cards)):
        #    return False

        # terkib

        cards1 = self.cards[iCards1] if(iPlayer1 == -1) else self.players[iPlayer1].cards[iCards1]
        cards2 = self.cards[iCards2] if(iPlayer2 == -1) else self.players[iPlayer2].cards[iCards2]

        index1 = -1
        for i in range(len(cards1)):
            if (cards1[i][0] == idCard1): index1 = i
        
        index2 = -1
        for i in range(len(cards2)):
            if (cards2[i][0] == idCard2): index2 = i
        
        if (iPlayer1 == iPlayer2 and iCards1 == iCards2):
            ncard = cards1[index1]
            cards1.remove(ncard)
            if(index2>index1):
                cards2.insert(index2, ncard)
            else:
                cards2.insert(index2+1, ncard)
        
        else:
            ncard = cards1[index1]
            cards1.remove(ncard)
            cards2.insert(index2+1, ncard)
        return True
    

                



        
            




    def tojson(self, pid):
        result = { "id":self.id, "ncards":len(self.cards[0]), "droppedCards":self.cards[1][max(len(self.cards[1]) - 4, 0):], 
                  "players":[ p.tojson(p.id == pid) for p in self.players],
                  "user_id":pid,
                  "version":self.version,
                  "nextPlayer" : self.nextPlayer,
                  "currentPlayer" : self.currentPlayer
                  }
        return result
    

    def reorderCards():{

    }

rounds:dict[str, RoundController] = {}



"""
colors = ['hearts', 'diamonds', 'clubs', 'spades']
import uuid



class Card:
    def __init__(self, number, color, id) -> None:
        self.number = number
        self.color = color
        self.id = id
    
    def __eq__(self, __value: object) -> bool:
        return __value and __value.id == self.id

class Player:

    cards : list[Card] = []
    downCards :list[list[Card]] = []
    order:int = -1
    uid:str
    def __init__(self) -> None:
        self.taken = False
        self.order = -1
        self.cards = []
        self.downCards = []
        self.uid = str(uuid.uuid4())
        self.name = ""

    def tojson(self, verbose:bool) -> dict:
        dic = {"downCards":self.downCards, "order":self.order, "name":self.name}
        if(verbose):
            dic["cards"] =self.cards
            dic["uid"] = self.uid
        else:
            dic["cards"] = [[] for i in self.cards]
            dic["uid"] = self.uid[0:8]
        return dic
    


class RoundController:
    players : list[Player]
    cards : list[Card] 
    droppedCards : list[Card]

    def getDownCard(self, ip:int, ic, ip2:int, id2:int, ic2:int):
        p1 = self.players[ip]

        p2 = self.players[ip2]
        card = [c for c in p1.cards if c.id == ic][0]
        down2 = p2.downCards[id2]
        self.players[ip].cards.remove(card)
        down2.append(card)
        self.actions.append(["downcard", ip, ic, ip2, id2])

    def revertDownCard(self, ip, ic, ip2, id2):
        p2 = self.players[ip2]
        card = [c for c in p2.downCards[id2] if c.id == ic][0]
        p2.downCards[id2].remove(card)
        self.players[ip].cards.append(card)

    def tojson(self, puid):
        result = { "uid":self.uid, "cards":len(self.cards), "droppedCards":self.droppedCards[max(len(self.droppedCards) - 4, 0):], 
                  "players":[ p.tojson(p.uid == puid) for p in self.players],
                  "nremaining" : len(self.cards),
                  "scores" : self.scores
                  }
        return result
    

    def __init__(self) -> str:
        initialCards = [[i%13+1, colors[int(i/26)], i] for i in range(104)] + [[0, '', 104], [0, '', 105],[0, '', 106],[0, '', 107]]
        random.seed()
        initialCards = sorted(initialCards, key=lambda c : random.random())
        #random.shuffle(initialCards)
        self.cards = [Card(c[0], c[1], c[2]) for c in initialCards]
        self.players = []
        self.droppedCards = []
        self.uid = str(uuid.uuid4())
        self.actions = []
        self.scores = []


    def revert(self):
        if(len(self.actions) == 0):
            return 
        else:
            action = self.actions[len(self.actions)-1]
            match action[0]:
                case "give" : self.returnCard(action[1], action[2])
                case "givethrown" :  self.throwCard(action[1], action[2], False)
                case "throw": self.giveToPlayerFromThrown(action[1], False)
                case "down": self.revertDown(action[1])
                case "downcard": self.revertDownCard(action[1], action[2], action[3], action[4])
            self.actions.pop()
            
    def revertDown(self, ip:int):
        cards = self.players[ip].downCards.pop()
        for c in cards:
            self.players[ip].cards.append(c)
    
    def giveToPlayer(self, ip:int, c:int = 1, history = True):
        for j in range(c):
            if(len(self.cards) == 0) :
                self.cards = sorted(self.droppedCards[0:len(self.droppedCards) - 4], key = lambda x:random.random())
                self.droppedCards = self.droppedCards[len(self.droppedCards) - 4::]


            card = self.cards.pop()
            self.players[ip].cards.append(card)
            if(history):
                self.actions.append(["give", ip, card.id])
    
    def returnCard(self, ip:int, ic:int):
        cards = self.players[ip].cards
        for card in  cards:
            if(card.id == ic):
                self.cards.append(card)
                self.players[ip].cards.remove(card)
                #self.actions.append[["throw", ip, card.id]]
                return card
    
    def giveToPlayerFromThrown(self, ip:int, history=True):

            card = self.droppedCards.pop()
            self.players[ip].cards.append(card)
            if(history):
                self.actions.append(["givethrown", ip, card.id])
            return card
    
    def throwCard(self, ip:int, ic:int, history=True) -> Card:
        cards = self.players[ip].cards
        for card in  cards:
            if(card.id == ic):
                self.droppedCards.append(card)
                self.players[ip].cards.remove(card)
                if(history):
                    self.actions.append(["throw", ip, card.id])
                return card

    def getDown(self, ip:int, ics:list[int], target:int):
        nd = []
        if(target == -1):
            self.players[ip].downCards.append(nd)
        else:
            toappend = [d for p in self.players for d in p.downCards if Card(-1,-1,target) in d ]
            if(len(toappend != 1)):return ""
            nd = toappend[0]
        
        
        self.actions.append(["down", ip, ics[0]])
        cards = self.players[ip].cards
        for ic in ics:
            for card in  cards:
                if(card.id == ic):
                    nd.append(card)
                    self.players[ip].cards.remove(card)
        
    def sort(self, ip:int, ics:list[int], tp):

        nd = []
        if(tp == 100):
            cards = self.players[ip].cards
        else:
            cards = self.players[ip].downCards[tp]
        for ic in ics:
            for card in  cards:
                if(card.id == ic):
                    nd.append(card)
        if(tp == 100):
            self.players[ip].cards = nd
        else:
            self.players[ip].downCards[tp] = nd
      
    
    def initRoundController(self):
        if(len(self.players[0].cards)>0) :return False 
        for i in range(7):
            if( i == 0):
                self.giveToPlayer(self.players[0].order, history=False)
            for p in self.players:
                self.giveToPlayer(p.order, 2, history=False)
        self.scores = []
        for p in self.players:
            self.scores.append(100) 
    def end(self):
        for i in range(len(self.players)):
            p = self.players[i]
            if(len(p.cards) == 0):
                self.scores[i] == -10
            else :
                if(len(p.downCards) > 0) :
                    score = sum([ (card.number if (card.number>1 and card.number<10) else 10) for card in  p.cards] )
                    self.scores[i] = score

        
"""