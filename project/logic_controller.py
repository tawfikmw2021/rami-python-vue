class CardGroup:
    cards : list[list[int]]
    def __init__(self, cards) -> None:
        self.cards = cards
    
    def isOrdered(self) -> bool : 
        cards = self.cards
        cnot  = [c[0] for c in cards if c[0] != 0]
        if(max(cnot) == min(cnot)): return True

        currenti = 0
        while cards[currenti][0] == 0:
            currenti += 1
         
        for i in range(currenti+1, len(cards)):
            if(cards[i-1][0] == 1 and i>1): return i == len(cards) - 1
            if(cards[i][0] * cards[i-1][0] == 0) : continue
            if cards[i][0] != cards[i-1][0] +1: return False
        return True

    def isvalidGroup(self) -> int:
        cards = self.cards
        if( not self.isOrdered()): return 0
        if len(cards) < 3 : return 0
        
        cnot  = [c[0] for c in cards if c[0] != 0]
        if(max(cnot) == min(cnot)): return 0 if len(cards)>4 else (10 if cnot[0] == 1 or cnot[0]>=10 else cnot[0] ) * len(cards)
        
        currenti = 0
        while cards[currenti][0] == 0:
            currenti += 1
        
        beg = cards[currenti][0]  - currenti
        return beg  * ( beg + len(cards) -1) * len(cards) / 2
    
    def sum(self):
        cards = self.cards
        result = 0
        for card in cards:
            result += 10 if card[0] <= 1  else  card[0]%10 
        return result
   
if(__name__=="__main__"):
    cards = [[0],[1],[2],[3]]
    grp = CardGroup(cards)

    print(grp.isOrdered(cards))
    #print(grp.)
