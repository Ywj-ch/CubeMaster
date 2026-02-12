<template>
  <div class="about-page">
    <h1>关于 CubeMaster</h1>
    <p>这是一个基于 Vue 3 和 Three.js 的项目...</p>

    <div class="model-display">
      <TechCore />
    </div>
  </div>
</template>

<script setup>
import TechCore from "../components/TechCore.vue";
</script>

<style>
.model-display {
  width: 1000px;
  height: 1200px;
  margin: 0 auto;
}
</style>
