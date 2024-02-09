<template>
  <HelloWorld msg="Welcome to Your Vue.js App" />
  <div v-if="!isplaying">
    <input
      type="checkbox"
      :checked="userStore.enableEdit"
      @change="enableEdit($event)"
    />
    <a v-if="!isplaying" href="/">home</a>
  </div>
  <div :style="{ display: userStore.enableEdit ? '' : 'none' }">
    <input v-model="userStore.user_id" @change="uchange()" />
  </div>
  <StatsBoard v-if="!isplaying" />
  <RamiBoard v-if="isplaying" />
</template>

<script>
//import HelloWorld from "./components/HelloWorld.vue";
import StatsBoard from "./components/StatsBoard.vue";
import RamiBoard from "./components/game/RamiBoard.vue";
import { userStore } from "./components/userStore";
let query = document.location.search;
const urlParams = new URLSearchParams(query);

export default {
  name: "App",
  components: {
    StatsBoard,
    RamiBoard,
  },
  data: function () {
    return {
      userStore: userStore,
      isplaying: urlParams.get("round_id") != undefined,
    };
  },

  methods: {
    enableEdit: function (ev) {
      this.userStore.enableEdit = ev.target.checked;
    },
    uchange: function () {
      console.log("user_id", userStore.user_id);
      localStorage.setItem("user_id", userStore.user_id);
    },
  },
};
</script>

<style></style>
