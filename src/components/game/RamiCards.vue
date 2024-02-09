<template>
  <div class="cards">
    <draggable
      group="people"
      :list="$props.cards"
      :disabled="false"
      :item-key="getkey"
      class="list-group2 d-flex"
      ghost-class="ghost"
      @end="onDrageEnd"
      @change="dropHandler($event, $props.type)"
    >
      <template #item="{ element }">
        <div
          :id="'card-' + element[0]"
          @dblclick="dbclicked('card-' + element[0])"
          class="rami-card"
          :style="{
            'background-color':
              $props.type.split('::')[0] != element[1]
                ? store.colors[element[1]]
                : '',
            width: $props.cstyle && $props.cstyle['card-width'] + 'vh',
          }"
        >
          <div class="img-container">
            <img
              :style="{
                width: $props.cstyle && $props.cstyle['img-width'] + 'vh',
                height:
                  $props.cstyle && $props.cstyle['img-width'] * 1.5 + 'vh',
              }"
              class="card-img"
              v-bind:src="
                require('../../assets/cards/' + getimage(element[0])) + ''
              "
            />
          </div>
        </div>
      </template>
    </draggable>
  </div>
</template>

<script>
//import draggable from "vuedraggable";
import { store } from "./ramiStore";
//import SimpleVue from "./simpleVue.vue";
import draggable from "vuedraggable";

export default {
  name: "HelloWorld",
  components: {
    draggable,
    //SimpleVue,
  },
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
      dragging: false,
      store: store,
      added: {},
    };
  },

  methods: {
    getimage(id) {
      return store.getimage(id, store.heavy);
    },
    dbclicked2: function (idCard) {
      let element = document.getElementById(idCard);

      if (!element) {
        let id = Number.parseInt(idCard.split("-")[1]);
        console.log((id % 13) + 1, store.colors[Math.floor(id / 26)]);
        return;
      }
      let isSelected = element.classList.contains("selected");
      if (isSelected) {
        element.classList.remove("selected");

        this.store.selected = this.store.selected.filter((v) => v != idCard);
      } else {
        element.classList.add("selected");
        this.store.selected.push(idCard);
      }
    },

    dbclicked: function (idCard) {
      this.dbclicked2(idCard);
    },

    dropHandler: function (item, type) {
      console.log(item, type);
      if (item.added) {
        let elm = item.added;
        let ip2 = type.split("::")[0];
        let ics2 = type.split("::")[1];
        let idc2 =
          elm.newIndex > 0 ? this.$props.cards[elm.newIndex - 1][0] : -100;

        store.added = { ip2, ics2, idc2 };
      }

      if (item.removed) {
        let ip1 = type.split("::")[0];
        let ics1 = type.split("::")[1];
        let idc1 = item.removed.element[0];
        const { ip2, ics2, idc2 } = store.added;
        store.added = {};
        store.move2(ip1, ip2, ics1, ics2, idc1, idc2, this);
      }
      let elm = item.moved;
      if (elm) {
        console.log(elm);
        let ip1 = type.split("::")[0];
        let ip2 = type.split("::")[0];
        let ics1 = type.split("::")[1];
        let ics2 = type.split("::")[1];
        let idc1 = elm.element[0];
        let idc2 =
          elm.newIndex > 0 ? this.$props.cards[elm.newIndex - 1][0] : -100;
        store.move2(ip1, ip2, ics1, ics2, idc1, idc2, this);
      } else return;
    },
    dropHandler2: function (item) {
      //ev.preventDefault();
      // Get the id of the target and add the moved element to the target's DOM
      //const datao = ev.dataTransfer.getData("text/plain");
      let datao = item.moved.element[0] + ">>" + this.$props.type;

      let typeo = datao.split(">>")[1];

      let ip1 = typeo.split("::")[0];
      let ip2 = this.$props.type.split("::")[0];
      let ics1 = typeo.split("::")[1];
      let ics2 = this.$props.type.split("::")[1];
      let idc1 = datao.split(">>")[0];
      let idc2 = 0; //ev.target.id;

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

.img-container {
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
  padding: 3px;
}

.card-content {
  overflow: hidden;
}
</style>
./state ./ramiStore
