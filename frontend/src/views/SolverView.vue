<template>
  <div>
    <h2>魔方求解</h2>

    <button @click="handleSolve" :disabled="loading">
      {{ loading ? "求解中..." : "开始求解" }}
    </button>

    <pre v-if="result">{{ result }}</pre>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { solveCube } from "../api/cube";

const loading = ref(false);
const result = ref(null);

async function handleSolve() {
  loading.value = true;
  try {
    const res = await solveCube();
    result.value = JSON.stringify(res.data, null, 2);
  } catch (err) {
    result.value = "请求失败";
  } finally {
    loading.value = false;
  }
}
</script>
