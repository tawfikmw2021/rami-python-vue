<template>
  <div class="cards">
    <template v-for="card in $props.cards" :key="card[0]">
      <div
        class="rami-card"
        :style="{ width: $props.cstyle && $props.cstyle['card-width'] + 'vh' }"
      >
        <div
          :id="card[0]"
          @dragstart="dragstartHandler($event)"
          @drop="dropHandler($event)"
          @dragover="dragoverHandler($event)"
          draggable="true"
          @dblclick="dbclicked($event)"
        >
          <img
            :id="card[0]"
            :style="{
              width: $props.cstyle && $props.cstyle['img-width'] + 'vh',
              height: $props.cstyle && $props.cstyle['img-width'] * 1.5 + 'vh',
            }"
            draggable="false"
            class="card-img"
            v-bind:src="
              require('../../assets/cards/' + getimage(card[0], store.heavy)) +
              ''
            "
          />
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { store } from "./ramiStore";
export default {
  name: "HelloWorld",
  props: {
    cards: [],
    cclass: String,
    type: String,
    cstyle: {},
  },
  created() {
    //console.log(store);
  },
  data: function () {
    return {
      store: store,
    };
  },

  methods: {
    getimage(id) {
      return store.getimage(id);
    },
    dbclicked2: function (element) {
      let isSelected = element.classList.contains("selected");
      if (isSelected) {
        element.classList.remove("selected");

        this.store.selected = this.store.selected.filter(
          (v) => v.id != element.id
        );
      } else {
        element.classList.add("selected");
        this.store.selected.push(element);
      }
    },

    dbclicked: function (ev) {
      this.dbclicked2(ev.target);
    },

    dragstartHandler: function (ev) {
      //console.log(ev.target.id);
      ev.dataTransfer.setData(
        "text/plain",
        ev.target.id + ">>" + this.$props.type
      );
      ev.dataTransfer.effectAllowed = "move";
    },
    dragoverHandler: function (ev) {
      ev.preventDefault();
      ev.target.classList.add("drop-active");
      ev.dataTransfer.dropEffect = "move";
    },
    dragleaveHandler: function (ev) {
      ev.target.classList.remove("drop-active");
    },
    dropHandler: function (ev) {
      ev.preventDefault();
      // Get the id of the target and add the moved element to the target's DOM
      const datao = ev.dataTransfer.getData("text/plain");

      let typeo = datao.split(">>")[1];

      let ip1 = typeo.split("::")[0];
      let ip2 = this.$props.type.split("::")[0];
      let ics1 = typeo.split("::")[1];
      let ics2 = this.$props.type.split("::")[1];
      let idc1 = datao.split(">>")[0];
      let idc2 = ev.target.id;

      store.move2(ip1, ip2, ics1, ics2, idc1, idc2, this);

      //console.log(i1, "moved to ", i2);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.drop-active {
  width: 50px;
}
.rami-card {
  /*border: solid 1px;*/
  width: 4vh;
  /*height: 20vh;*/
  overflow: hidden;

  /*user-select: none;*/
}

.full-card {
  width: fit-content;
}

.rami-card:last-child {
  width: fit-content !important;
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
  border: solid 1px;
  width: 5vh;
  transform: rotate(0.25turn);
}

.card-img {
  pointer-events: none;
  width: 13vh;
  height: 20vh;
}

.card-img2 {
  position: absolute;
  clip: rect(0px, 60px, 200px, 0px);
}

.card2 {
  border: solid 1px;
}

.selected {
  border-radius: 5%;
  background-color: rgb(44, 52, 58, 0.1);
}

.card-content {
  overflow: hidden;
}
</style>
./state ./ramiStore
