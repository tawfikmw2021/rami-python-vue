<template>
  <div class="stats-board">
    <button @click="getGames">get games</button>
    <div :style="{ display: userStore.enableEdit ? '' : 'none' }">
      <button v-if="key == 'enable'" @click="newGame">new game</button>

      <input
        v-model="key"
        placeholder="key"
        style="background-color: rgba(255, 255, 255, 0.1)"
      />
    </div>

    <div
      :class="{ focus: focus(game) }"
      class="border m-2 p-2"
      v-for="game in gameStore.games"
      :key="game.id"
    >
      <div class="d-flex justify-content-around">
        <button
          v-if="key == 'enable'"
          @click="newRound(game)"
          :disabled="!focus(game)"
        >
          new Round
        </button>
        <a href="javascript:void(0)" @click="joinGame(game.id)">{{
          game.id
        }}</a>
        <div class="uid">{{ game.time }}</div>
      </div>

      <div
        class="gameb"
        :style="{
          'grid-template-columns':
            'repeat(' + (game.players.length + 1) + ',1fr)',
          'grid-template-rows': 'repeat(' + (game.rounds.length + 1) + ',1fr)',
        }"
      >
        <div
          v-for="(player, index) in game.players"
          :key="player.id"
          :class="{ focusu: focusu(player) }"
          :style="{
            'grid-row': 1,
            'grid-column': index + 2,
          }"
        >
          {{ `${player.name || player.id} (${player.score})` }}
        </div>

        <div
          :style="{
            'grid-row': 1,
            'grid-column': game.players.length + 2,
          }"
        >
          {{ "state" }}
        </div>

        <template v-for="(round, index) in game.rounds" :key="round.id">
          <div
            :class="{ focusr: focusr(round) }"
            :style="{
              'grid-row': index + 2,
              'grid-column': 1,
            }"
            class="px-2"
          >
            <a
              :title="round.id"
              href="javascript:void(0)"
              @click="joinRound(game.id, round.id)"
              >{{ round.id }}</a
            >
            <button
              style="line-height: 1em"
              v-if="round.state == 'CREATED'"
              @click="
                roundStore.initFromStats(round, () => gameStore.refresh())
              "
            >
              init
            </button>
          </div>
          <div
            :style="{
              'grid-row': index + 2,
              'grid-column': pindex + 2,
            }"
            v-for="(player, pindex) in game.players"
            :key="player.id"
            :class="{ focusu: focusu(player) }"
          >
            <input
              type="checkbox"
              :checked="getIndex(player, round.players) != -1"
              @change="checkChange($event, round, player)"
              v-if="round.state == 'CREATED'"
            />
            <span v-else> {{ getScore(player, round.players) }} </span>
            ({{ getIndex(player, round.players) }})
          </div>

          <select
            disabled
            v-model="round.state"
            :style="{
              'font-size': 'x-small',
              'grid-row': index + 2,
              'grid-column': game.players.length + 2,
            }"
          >
            <option
              v-for="option in gameStore.roundStates"
              :key="option.value"
              :value="option.value"
            >
              {{ option.text }}
            </option>
          </select>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { store as roundStore } from "./game/ramiStore";
import { gameStore } from "./gameStore";
import { userStore } from "./userStore";

export default {
  name: "StatsBoard",
  components: {},
  emits: ["join"],
  data: function () {
    return {
      gameStore: gameStore,
      userStore: userStore,
      roundStore: roundStore,
      key: "enable",
    };
  },
  created: function () {
    gameStore.refresh();
  },
  methods: {
    checkChange(ev, round, player) {
      console.log(ev, round, player);
      round.players = round.players || [];
      let pe = round.players.find((p) => p.id == player.id);
      if (pe) round.players = round.players.filter((p) => p.id != player.id);
      else round.players.push(player);
    },
    focus(game) {
      return game.id == gameStore.game_id;
    },
    focusr(round) {
      return !round || false;
      //return round.id == store.round_id;
    },
    focusu(player) {
      return !player || false; //&& player.id == store.user_id;
    },
    getScore: function (player, rplayers) {
      let pl = rplayers && rplayers.find((p) => p.id == player.id);
      return pl ? pl["score"] : "n";
    },
    getIndex: function (player, rplayers) {
      return rplayers ? rplayers.map((v) => v.id).indexOf(player.id) : -1;
    },
    getGames: function () {
      this.gameStore.refresh();
    },

    newGame() {
      this.gameStore.newg();
    },
    newRound(game) {
      if (!this.focus(game)) return;
      this.gameStore.newr();
    },

    joinGame(game_id) {
      this.gameStore.joing(game_id);
    },

    joinRound(game_id, round_id) {
      this.gameStore.joinr(game_id, round_id);
    },
  },
};
</script>

<style scoped>
.focus {
  background-color: rgba(150, 50, 0, 0.1);
}

.stats-board {
  font-size: small;
}

.gameb {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
}

.focusr {
  background-color: rgba(150, 50, 0, 0.2);
}

.focusu {
  background-color: rgba(150, 50, 0, 0.2);
}
.uid {
  overflow: hidden;
  height: 30px;
}
</style>
./game/state
