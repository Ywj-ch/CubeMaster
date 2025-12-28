<template>
  <div class="container">
    <h1>魔方求解演示</h1>
    <!-- 模型区 -->
    <div class="cube-net">
      <div class="row">
        <FaceView :face="cubeState.U" />
      </div>

      <div class="row middle-row">
        <FaceView :face="cubeState.L" />
        <FaceView :face="cubeState.F" />
        <FaceView :face="cubeState.R" />
        <FaceView :face="cubeState.B" />
      </div>

      <div class="row">
        <FaceView :face="cubeState.D" />
      </div>
    </div>
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
        :disabled="currentStep >= steps.length"
      >
        下一步
      </button>
    </div>

    <!-- 测试公式按钮 -->
    <button @click="testMoves" :disabled="loading">
      测试公式
    </button>

    <!-- 进度 -->
    <div v-if="steps.length" class="progress">
      已执行步骤：{{ currentStep }} / {{ steps.length }}
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
import {getCubeState, solveCube} from "../api/cube";
import { createCubeFromJson } from "../utils/cubeState";
import {applyMove, invertMove} from "../utils/cubeMoves";
import FaceView from "../components/FaceView.vue";

// 状态
const loading = ref(false);
const steps = ref([]);
const currentStep = ref(0);
const testStep = ref(0);
const cubeState = ref(createCubeFromJson());
const solutionMoves = ref([]);
const testMovesArray = ref([
  "R", "U", "R'", "U'",
  "R", "U", "R'", "U'",
  "R", "U", "R'", "U'",
  "R", "U", "R'", "U'",
  "R", "U", "R'", "U'",
  "R", "U", "R'", "U'"
]);

// 请求后端
async function fetchSolution() {
  loading.value = true;
  try {
    // 先获取当前魔方状态 JSON
    const stateRes = await getCubeState();
    if (stateRes.data.success) {
      // 初始化 cubeState
      cubeState.value = createCubeFromJson(stateRes.data.data);
    } else {
      console.error("获取魔方状态失败:", stateRes.data.error);
      alert("获取魔方状态失败");
      return;
    }
    // 再请求求解步骤
    const res = await solveCube();
    console.log("后端返回：", res.data);

    const payload = res.data;
    steps.value = payload.data?.readable_solution || [];
    solutionMoves.value = payload.data?.moves || [];
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
  if (currentStep.value < solutionMoves.value.length) {
    applyMove(cubeState.value, solutionMoves.value[currentStep.value]);
    currentStep.value++;
  }
}

function prevStep() {
  if (currentStep.value > 0) {
    currentStep.value--;
    const move = solutionMoves.value[currentStep.value];
    const reverseMove = invertMove(move);
    applyMove(cubeState.value, reverseMove);
  }
}

// 测试按钮的控制步骤
function testMoves() {
  if (testStep.value < testMovesArray.value.length) {
    applyMove(cubeState.value, testMovesArray.value[testStep.value]);
    testStep.value++;
  } else {
    alert("公式已执行完毕");
  }
}
</script>

<style scoped>
.cube-net {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.row {
  display: flex;
}

.middle-row {
  margin-left: 130px;
}

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
