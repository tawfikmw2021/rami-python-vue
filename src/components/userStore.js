import { reactive } from 'vue'
import * as axios from "axios"

import { io } from "socket.io-client";


export const userStore = reactive({
    user_id: localStorage.getItem("user_id") || 2,
    enableEdit :  false
})


const burl =
  process.env.NODE_ENV === "production" ? "" : "http://192.168.1.188:8087";

export const socket = io(burl);
export const ax = new axios.Axios({
  baseURL:burl
});

