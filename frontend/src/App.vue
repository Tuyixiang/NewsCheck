<template>
  <div id="app">
    <HelloWorld />
  </div>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import HelloWorld from "./components/HelloWorld.vue";

Vue.prototype.$http = axios
Vue.prototype.$backend = 'http://127.0.0.1:8000'

export default {
  name: "App",
  components: {
    HelloWorld
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
