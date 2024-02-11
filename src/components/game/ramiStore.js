import { reactive } from 'vue'
import { userStore, socket, ax } from '../userStore';

const colors = ["clubs", "diamonds", "hearts", "spades"]






let query = document.location.search;
const urlParams = new URLSearchParams(query);

export const store = reactive({
  colors: [
    "rgba(255,0,0,0.7)",
    "rgba(100,150,0,0.7)",
    "rgba(0,150,100,0.7)",
    "rgba(0,0,255,0.7)",
  ],
  order : -1,
  round_id: urlParams.get("round_id") || localStorage.getItem("round_id") || -1,
  game_id: urlParams.get("game_id") || localStorage.getItem("game_id") || -1,
  user_id : userStore.user_id,

  currentPlayer : 0,
  heavy : false,
  count: 0,
  ncards:0,
  added:{},
  removed:{},
  version:-1,
  nversion : -1,
  myCards : [[1, 0,0,1]],
  droppedCards : [[-1, -1,1,1]],
  json : "",
  ref_round :"",
  players : [
     {
      ncards:5,
      ncards2:10,
      name:"name1",
      cards : []
    }
  ],

  scores:[0,0,0],
  notifs:[],

  selected:[],

  down(){


  },




  getimage(id, quality=true){
    var n = 0
    if(id>=104){
      return `red_joker.svg`
    }
    let naux = id%13 + 1
    let color = colors[Math.floor(id / 26)]
    switch (naux){
      case 11 : n = quality ?  `jack_of_${color}2.svg` :  `jack_of_${color}.svg` ; break
      case 12 : n = quality ?  `queen_of_${color}2.svg` :  `queen_of_${color}.svg` ; break
      case 13 : n = quality ? `king_of_${color}2.svg` :  `king_of_${color}.svg` ; break
      case 1 : n = quality ?  `ace_of_${color}.svg` :  `ace_of_${color}.svg` ; break
      case 0 : n = "Card_back_01.svg";break
      default : n = `${naux}_of_${color}.svg`
    }
    
    return n
  },

  move2(ip1, ip2, ics1, ics2, idc1, idc2, vm){
    console.log("moved1", ip1, ip2, ics1, ics2, idc1, idc2)
    console.log("moved", ip1, ip2, ics1, ics2, idc1%3+1, idc2%3+1)
    let selected = this.selected //.sort((a,b)=> b.id-a.id)
    this.selected = []
    if(selected.length>1 && selected.find(el => el == "card-"+idc1))
    selected.reverse().map(el=> {
      this.move(ip1, ip2, ics1, ics2, el.split("-")[1], idc2)
      vm.dbclicked2(el)
    })
    else
      this.move(ip1, ip2, ics1, ics2, idc1, idc2)
  },

  move(ip1, ip2, ics1, ics2, idc1, idc2){

    //console.log(ip1, ip2, ics1, ics2, idc1, idc2)
      

      ax.get(`/round/${this.round_id}/move?user_id=${this.user_id}&ip1=${ip1}&ip2=${ip2}&ics1=${ics1}&ics2=${ics2}&idc1=${idc1}&idc2=${idc2}&user_id=${userStore.user_id}`)
      .then(() => {
        return this.refresh()
      })
      .catch(() => console.log("error move api"))
      

  },

  forcer(){
    ax.get(`/round/${this.round_id}/forcer?user_id=${userStore.user_id}&ref_round=${this.ref_round}`).then(v => console.log(v))
  },


  refresh(){
    ax.get(`/round/${this.round_id}/details?user_id=${userStore.user_id}&version=${this.version}`)
      .then(r => {
        
        let round = JSON.parse(r.data)
        if(round.change) return 

        this.order = round.players.map(v=> Number(v.id)).indexOf(Number(round.user_id))
        
        this.version = round.version
        this.players = round.players
        this.droppedCards = round.droppedCards.length>0? round.droppedCards : [[-1,-1,1,0]]
        //console.log("droppedCards",this.droppedCards)
        this.myCards = round.players[this.order].cards[0]
        this.ncards = round.ncards
        this.scores = round.scores
        this.state = "R"+this.round_id+" "+round.state
        this.currentPlayer = round.currentPlayer

        let roundj = JSON.parse(r.data)
        roundj.players == roundj.players.map(v => {v.cards = []; return v})
        roundj.droppedCards = undefined
        this.json = JSON.stringify(roundj)
        this.user_id = round.user_id
        //console.log("ncards",this.myCards.length)
        
        
      })
      .catch(() => console.log("error move api"))
  },

  heavyChange(){
    this.heavy = !this.heavy
    this.refresh()
  },

  setNextPlayerToMe(){
    ax.get(`/round/${this.round_id}/nextp?nextp=${this.order}&user_id=${userStore.user_id}`)
  },

  init(){
    ax.get(`/round/${this.round_id}/init?user_id=${userStore.user_id}`)
      .then(() => {
        return this.refresh()
      })
      .catch(() => console.log("error init api"))
  },

  goToNext(){
    ax.get(`/round/${this.round_id}/gotonext?user_id=${userStore.user_id}`)
  },

  initFromStats(round, callback){
    ax.get(`/round/${round.id}/init?user_id=${userStore.user_id}&players=${round.players.map(v=> v.id+":"+0).join(",")}`)
      .then(() => {
        return callback()
      })
      .catch(() => console.log("error init api"))
  },

  finish(){
    ax.get(`/round/${this.round_id}/finish?user_id=${userStore.user_id}`)
      .then(() => {
        return this.refresh()
      })
      .catch(() => console.log("error finish api"))
  },
  abondon(){
    ax.get(`/round/${this.round_id}/abondon?user_id=${userStore.user_id}`)
      .then(() => {
        return this.refresh()
      })
      .catch(() => console.log("error finish api"))
  },
})

socket.emit("join", {user_id:store.user_id, room:"round"+store.round_id})

socket.on("message", (...args) => {
  store.nversion += 1;
  store.notifs.unshift({id:store.nversion,message:args[0]})
  //console.log("message", args)
})

socket.on("move", (...args) => {
  store.nversion += 1;
  store.notifs.unshift({id:store.nversion,message:args[0]})
  store.refresh()
})

socket.on("update", (...args) => {
  store.nversion += 1;
  store.notifs.unshift({id:store.nversion,message:args[0]})
  store.refresh()
})



socket.on("init", (...args) => {
  store.nversion += 1;
  store.notifs.unshift({id:store.nversion,message:args[0]})
  store.refresh()
})

socket.on("nextp", (...args) => {
  args
  store.refresh()
})

socket.on("forcer", (...args) => {
  document.location.href = document.location.origin+`?round_id=${args[0]}`  
})

function refresh() {
  // make Ajax call here, inside the callback call:
  //setTimeout(refresh, 500);
  store.refresh()
}

// initial call, or just call refresh directly
setTimeout(refresh, 500);

