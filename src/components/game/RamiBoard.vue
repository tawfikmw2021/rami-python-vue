<template>
  <div>
    <div
      style="height: 10px"
      class="col-12 showmenu"
      @click="showmenu = !showmenu"
    ></div>
    <div class="row m-0" :style="{ display: showmenu ? '' : 'none' }">
      <a class="rami-btn col-4 col-md-2" href="/">home</a>
      <button class="rami-btn col-4 col-md-2" @click="store.heavyChange()">
        heavy
      </button>
      <button class="rami-btn col-4 col-md-2" @click="store.init()">
        init
      </button>
      <button
        style="display: none"
        class="rami-btn col-4 col-md-2"
        @click="store.setNextPlayerToMe()"
      >
        douri
      </button>
      <button class="rami-btn col-6 col-md-3" @click="store.finish()">
        rami
      </button>
      <button class="rami-btn col-6 col-md-3" @click="store.abondon()">
        frish
      </button>

      <button class="rami-btn col-6" @click="store.goToNext()">next</button>

      <button
        class="rami-btn col-3"
        @click="store.forcer()"
        :style="{ display: store.ref_round.startsWith('round') }"
      >
        forcer
      </button>
      <input
        style="border: solid 1px"
        class="rami-btn col-3"
        v-model="store.ref_round"
      />
    </div>
  </div>
  <div class="d-flex">
    <div style="position: relative">
      <button
        style="
          position: absolute;
          background-color: transparent;
          border: none;
          font-size: small;
          font-weight: bold;

          left: 2vh;
          top: 10vh;
        "
        @click="store.move(-1, store.order, 0, 0, -1, -1)"
      >
        echri
      </button>
      <span style="font-size: small; padding-left: 2vh"
        >current : {{ store.players[store.currentPlayer].name }}</span
      >
      <div style="font-size: small; padding-left: 2vh">
        {{ "round" + store.round_id }}
      </div>
      <div style="opacity: 0.5">
        <RamiCards
          :cstyle="{ 'card-width': 0, 'img-width': 5 }"
          :cards="[
            [-1, -1, 0, 1],
            [-1, -1, 0, 1],
          ]"
          :type="'-1::0'"
          :cclass="'full-card'"
        />
      </div>
    </div>

    <RamiCards
      :cstyle="{ 'card-width': 3, 'img-width': 10 }"
      :cards="store.droppedCards"
      :type="'-1::1'"
    />
    <div class="px-3">
      <div
        class="alert alert-primary"
        role="alert"
        :style="{
          display:
            store.players[store.currentPlayer].order == store.order
              ? ''
              : 'none',
        }"
      >
        Your turn! ({{ store.state }})
      </div>
    </div>
    <div>
      <div
        v-for="notif in store.notifs.slice(0, 4)"
        :key="notif.id"
        style="display: none"
      >
        {{ notif.message }}
      </div>
    </div>
  </div>
  <div class="d-flex align-items-center">
    <div class="down-head-container">
      <div
        class="down-head"
        :style="{ backgroundColor: store.colors[store.order] }"
      >
        {{ store.players[store.order] && store.players[store.order].name }}
      </div>
    </div>
    <RamiCards
      :cstyle="{ 'card-width': 3, 'img-width': 10 }"
      :cards="store.myCards"
      :type="store.order + '::0'"
    />
  </div>
  <template v-for="(player, ip) in store.players" :key="ip">
    <div
      class="down"
      :class="{
        nextp: store.currentPlayer == ip,
        focusp: player.id == store.user_id,
      }"
    >
      <div class="down-head-container">
        <div
          class="down-head"
          :style="{ backgroundColor: store.colors[ip] }"
          :class="{ focusp: player.id == store.user_id }"
        >
          {{ `${player.name} (${player.ncards2}-${player.ncards})` }}
        </div>
      </div>
      <RamiCards
        :cstyle="{ 'card-width': 3, 'img-width': 10 }"
        :cards="[[-1, ip, player.cards.length, 1]]"
        :type="ip + '::' + player.cards.length"
      />
      <template v-for="(cards, ics) in player.cards.toReversed()" :key="ics">
        <RamiCards
          :cstyle="{ 'card-width': 3, 'img-width': 10 }"
          v-if="(player.cards && player.cards.length - ics - 1) > 0"
          :cards="cards"
          :type="ip + '::' + (player.cards && player.cards.length - ics - 1)"
        />
      </template>
    </div>
  </template>
  <div style="display: none">
    <textarea
      class="w-100"
      style="height: 20vh"
      v-model="store.json"
      disabled
    ></textarea>
    <div>
      <div v-for="notif in store.notifs.slice(0, 4)" :key="notif.id">
        {{ notif.message }}
      </div>
    </div>
  </div>
</template>

<script>
import { store } from "./ramiStore";
import RamiCards from "./RamiCards.vue";

export default {
  name: "HelloWorld",
  props: {
    cards: [],
  },
  components: {
    RamiCards,
  },
  created() {
    //console.log(store);
    store.refresh();
  },
  data: function () {
    return {
      store: store,
      showmenu: false,
    };
  },

  methods: {
    goToNext: function () {
      store.goToNext();
    },
    setNextPlayerToMe: function () {
      store.setNextPlayerToMe();
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.drop-active {
  width: 50px;
}
.card {
  /*border: solid 1px;*/
  width: 5vh;
  height: 20vh;

  /*user-select: none;*/
}

.cards {
  display: flex;
  margin-top: 1rem;
  margin-left: 1rem;
}

.down {
  display: flex;
  align-items: center;
}

.down-head {
  border: solid 1px rgb(255, 150, 50, 0.3);
  border-radius: 5%;
  width: 10vh;
  transform: translate(5vh, -2vh) rotate(0.25turn);
  transform-origin: top left;
  font-size: small;
  color: rgb(255, 250, 250, 1);
}
.down-head-container {
  width: 5vh;
}

.card-img {
  width: 13vh;
  height: 20vh;
}

.nextp {
  border: solid 0.1px;
  border-radius: 5px;
  border-color: rgb(0, 0, 0, 0.3);
}

.focusp {
  border-width: 3px;
  background-color: rgb(255, 250, 200, 0.1);
}

.card-img2 {
  position: absolute;
  clip: rect(0px, 60px, 200px, 0px);
}

.card2 {
  border: solid 1px;
}

.rami-btn:first-child {
}
.rami-btn {
  border: none;
  border-left: solid 1px rgba(96, 88, 84, 0.5);
  border-bottom: solid 1px rgba(96, 88, 84, 0.5);
}

.rami-btn:first-child {
  border-left: none;
}
a.rami-btn {
  background-color: buttonface;
  text-align: center;
}

.rami-btn:active {
  background-color: rgba(96, 88, 84, 1);
}
.rami-btn:hover {
  background-color: rgba(96, 88, 84, 0.4);
}

.card-content {
  overflow: hidden;
}

.button {
  position: relative;
  background-color: black;
  border-radius: 4em;
  font-size: 16px;
  color: white;
  padding: 0.8em 1.8em;
  cursor: pointer;
  user-select: none;
  text-align: center;
  text-decoration: none;
  cursor: pointer;
  transition-duration: 0.4s;
  -webkit-transition-duration: 0.4s; /* Safari */
}

.showmenu {
  background-color: rgb(174, 193, 193, 0.8);
  cursor: pointer;
}

.showmenu:active {
  background-color: rgb(174, 193, 193);
}

.showmenu2:hover:after {
  position: absolute;
  left: 50vw;
  background-color: aqua;
  content: ">";
  transform: rotate(00.25turn);
  color: red;
}

.button:hover {
  transition-duration: 0.1s;
  background-color: #3a3a3a;
}

.button:after {
  content: "";
  display: block;
  position: absolute;
  border-radius: 4em;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: all 0.5s;
  box-shadow: 0 0 10px 40px white;
}

.button:active:after {
  box-shadow: 0 0 0 0 white;
  position: absolute;
  border-radius: 4em;
  left: 0;
  top: 0;
  opacity: 1;
  transition: 0s;
}

.button:active {
  top: 1px;
}
</style>
./state ./ramiStore
