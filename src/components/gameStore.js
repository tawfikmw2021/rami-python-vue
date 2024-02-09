import { reactive } from 'vue'
import {userStore, ax} from "./userStore"


let query = document.location.search;
const urlParams = new URLSearchParams(query);

export const gameStore = reactive({
    game_id : urlParams.get("game_id") || localStorage.getItem("game_id") || -1,
    games : [],

    roundStates: [{value:"CREATED", text:"CREA"},
    {value:"PLAYING", text:"PLAY"},{value:"FINISHED", text:"FINI"},{value:"ABONDONED", text:"ABON"}],
    refresh(){
      ax.get("/game/all").then (r => {
        let gs =  JSON.parse(r.data)
        gs.forEach(element => {
          if(element.rounds)
          element.rounds = element.rounds.reverse()
        });
        this.games = gs.reverse()
      })
    },
    newg(){
      ax.get("/game/new").then (() => {
        this.refresh()
      })
    },
    newr(){
      ax.get(`/game/${this.game_id}/round/new`).then (() => {
        this.refresh()
      })
    },
    joinr(game_id, round_id){
      this.joing(game_id).then(() =>{
  
        ax.get(`/round/${round_id}/join?user_id=${userStore.user_id}`).then ((r) => {
          localStorage.setItem("round_id", r.data)
          location.href = location.origin + "/index.html?round_id="+r.data
        })
      }) 
    },
  
    joing(game_id){
      return ax.get(`/game/${game_id}/join?user_id=${userStore.user_id}`).then((g) => {
        this.game_id = g.data
        localStorage.setItem("game_id", g.data)
      })
    }
  })