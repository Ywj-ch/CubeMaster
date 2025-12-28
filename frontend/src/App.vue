<template>
  <div id="app">
    <div class="bg-layer"></div>
    <SolverView />
  </div>
</template>

<script setup>
import SolverView from "./views/SolverView.vue";
</script>

<style>
#app {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
}

/* 背景图层固定在底部 */
.bg-layer {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: url('./assets/deerlet.png') no-repeat center center fixed;
  background-size: cover;
  z-index: -1; /* 保证内容在上层 */
}
</style>