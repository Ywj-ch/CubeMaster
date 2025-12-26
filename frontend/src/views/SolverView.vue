<template>
  <div class="container">
    <h1>魔方求解演示</h1>
    <pre>{{ cubeState }}</pre>
    <!-- 控制区 -->
    <div class="controls">
      <button @click="fetchSolution" :disabled="loading">
        {{ loading ? "求解中..." : "开始求解" }}
      </button>

      <button @click="prevStep" :disabled="currentStep === 0">
        上一步
      </button>

      <button
        @click="nextStep"
        :disabled="currentStep >= steps.length - 1"
      >
        下一步
      </button>
    </div>

    <!-- 进度 -->
    <div v-if="steps.length" class="progress">
      当前步骤：{{ currentStep + 1 }} / {{ steps.length }}
    </div>

    <!-- 步骤列表 -->
    <ul class="steps">
      <li
        v-for="(step, index) in steps"
        :key="index"
        :class="{ active: index === currentStep }"
      >
        {{ index + 1 }}. {{ step }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { solveCube } from "../api/cube";
import { createInitialCube } from "../utils/cubeState";
import { applyMove } from "../utils/cubeMoves";

// 状态
const loading = ref(false);
const steps = ref([]);
const currentStep = ref(0);
const cubeState = ref(createInitialCube());
const moves = ref(["U", "U'", "U2"]); // 临时测试

// 请求后端
async function fetchSolution() {
  loading.value = true;
  try {
    const res = await solveCube();
    console.log("后端返回：", res.data);

    const payload = res.data;
    steps.value = payload.data?.readable_solution || [];
    currentStep.value = 0;
  } catch (e) {
    console.error(e);
    alert("请求失败，请检查后端");
  } finally {
    loading.value = false;
  }
}

// 控制步骤
function nextStep() {
  if (currentStep.value < moves.value.length) {
    applyMove(cubeState.value, moves.value[currentStep.value]);
    currentStep.value++;
  }
}

function prevStep() {
  if (currentStep.value > 0) {
    currentStep.value--;
  }
}
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 40px auto;
  font-family: Arial, sans-serif;
}

.controls {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

button {
  padding: 6px 12px;
  cursor: pointer;
}

.progress {
  margin-bottom: 10px;
  font-weight: bold;
}

.steps {
  list-style: none;
  padding: 0;
}

.steps li {
  padding: 6px;
  border-bottom: 1px solid #ddd;
}

.steps li.active {
  background-color: #d0ebff;
  font-weight: bold;
}
</style>
