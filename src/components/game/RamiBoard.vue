<template>
  <div class="row m-0">
    <a class="rami-btn col-4 col-md-2" href="/">home</a>
    <button class="rami-btn col-4 col-md-2" @click="store.heavyChange()">
      heavy
    </button>
    <button class="rami-btn col-4 col-md-2" @click="store.init()">init</button>
    <button class="rami-btn col-4 col-md-2" @click="store.setNextPlayerToMe()">
      douri
    </button>
    <button class="rami-btn col-4 col-md-2" @click="store.finish()">
      rami
    </button>
    <button class="rami-btn col-4 col-md-2" @click="store.abondon()">
      frish
    </button>
  </div>
  <div class="d-flex align-items-center">
    <RamiCards
      :cstyle="{ 'card-width': 0, 'img-width': 10 }"
      :cards="[
        [-1, -1, 0, 1],
        [-1, -1, 0, 1],
      ]"
      :type="'-1::0'"
      :cclass="'full-card'"
    />
    <RamiCards
      :cstyle="{ 'card-width': 3, 'img-width': 10 }"
      :cards="store.droppedCards"
      :type="'-1::1'"
    />
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
        nextp: store.nextPlayer == ip,
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
  <textarea
    class="w-100"
    style="height: 20vh"
    v-model="store.json"
    disabled
  ></textarea>
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
    };
  },

  methods: {
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
  color: rgb(255, 50, 50, 0.7);
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
}

.rami-btn:first-child {
  border: none;
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
</style>
./state ./ramiStore
