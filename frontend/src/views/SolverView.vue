<template>
  <div class="container">
    <h1>魔方求解演示</h1>

    <!-- 模型区 -->
    <div class="cube3d-wrapper">
      <Cube3DView ref="cube3dRef" :cubeState="cubeState" />
    </div>

     <!-- 3D R 面旋转测试按钮 -->
    <button class="test3d-btn" @click="test3DMove" :disabled="loading">
      3D旋转测试公式
    </button>

    <div class="cube-net">
      <div class="row">
        <Face2DView :face="cubeState.faces.U" />
      </div>

      <div class="row middle-row">
        <Face2DView :face="cubeState.faces.L" />
        <Face2DView :face="cubeState.faces.F" />
        <Face2DView :face="cubeState.faces.R" />
        <Face2DView :face="cubeState.faces.B" />
      </div>

      <div class="row">
        <Face2DView :face="cubeState.faces.D" />
      </div>
    </div>

    <!-- 控制区 -->
    <div class="controls">
      <button @click="fetchSolution" :disabled="loading">
        {{ loading ? "求解中..." : "开始求解" }}
      </button>

      <div class="step-buttons">
        <button @click="prevStep" :disabled="currentStep === 0">
          上一步
        </button>

        <button @click="nextStep" :disabled="currentStep >= steps.length">
          下一步
        </button>
      </div>

      <button class="reset-btn" @click="resetCube">
        重置
      </button>
    </div>

    <!-- 测试公式按钮 -->
    <button class="test-btn" @click="testMoves" :disabled="loading">
      2D旋转测试公式
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
import Face2DView from "../components/Face2DView.vue";
import Cube3DView from "../components/Cube3DView.vue";

// 状态
const loading = ref(false);
const hasSolved = ref(false);
const steps = ref([]);
const currentStep = ref(0);
const testStep = ref(0);
const test3DStep = ref(0);
const cubeState = ref(createCubeFromJson());
const cube3dRef = ref(null);
const solutionMoves = ref([]);
const testMovesArray = ref([
  "R", "U", "R'", "U'",
  "R", "U", "R'", "U'",
  "R", "U", "R'", "U'",
  "R", "U", "R'", "U'",
  "R", "U", "R'", "U'",
  "R", "U", "R'", "U'"
]);
const test3DMovesArray = ref([
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
    const stateRes = await getCubeState();
    if (stateRes.data.success) {
      const newCube = createCubeFromJson(stateRes.data.data);
      cubeState.value.cubies = newCube.cubies;
      cubeState.value.faces = newCube.faces;
    } else {
      alert("获取魔方状态失败");
      return;
    }

    const res = await solveCube();
    const data = res.data.data;

    // 对后端返回的数据再次进行校验
    if (data?.raw_solution && data.raw_solution.startsWith("Error")) {
      alert(
        "魔方状态不合法：可能有某个面拍摄时方向旋转了 90° 或 180°。\n" +
        "请按照拍摄顺序重新拍摄，或在 2D 展开图中手动修正。"
      )
      hasSolved.value = false;
      return;
    }

    // 校验通过后才开始赋值
    steps.value = data.readable_solution;
    solutionMoves.value = data.moves;
    currentStep.value = 0;
    hasSolved.value = true;

  } catch (e) {
    console.error(e);
    alert("请求失败，请检查后端");
    hasSolved.value = false;
  } finally {
    loading.value = false;
  }
}

// 控制步骤
function nextStep() {
  if (!hasSolved.value) return;

  if (currentStep.value < solutionMoves.value.length) {
    const move = solutionMoves.value[currentStep.value];
    applyMove(cubeState.value, move);      // 数据层更新 cubies
    cube3dRef.value.playMove(move);        // 播放 3D 动画
    currentStep.value++;
  }
}

function prevStep() {
  if (!hasSolved.value) return;

  if (currentStep.value > 0) {
    currentStep.value--;
    const move = solutionMoves.value[currentStep.value];
    const reverseMove = invertMove(move);  // 反向 move
    applyMove(cubeState.value, reverseMove);
    cube3dRef.value.playMove(reverseMove); // 播放反向动画
  }
}

// 2D测试按钮
function testMoves() {
  if (testStep.value < testMovesArray.value.length) {
    applyMove(cubeState.value, testMovesArray.value[testStep.value]);
    testStep.value++;
  } else {
    alert("2D公式已执行完毕");
  }
}

// 3D测试按钮
function test3DMove() {
  if (test3DMovesArray.value.length > test3DStep.value) {
    const move = test3DMovesArray.value[test3DStep.value];
    applyMove(cubeState.value, move); // 更新状态
    cube3dRef.value.playMove(move);   // 播放动画
    test3DStep.value++;
  } else {
    alert("3D公式已执行完毕");
  }
}

// 重置状态函数
function resetCube() {
  cubeState.value = createCubeFromJson();
  steps.value = [];
  solutionMoves.value = [];
  currentStep.value = 0;
  testStep.value = 0;
  test3DStep.value = 0;
  hasSolved.value = false;
}
</script>

<style scoped>
/* 页面整体 */
.container {
  max-width: 680px;
  margin: 40px auto;
  padding: 24px;

  font-family: "Segoe UI", Arial, sans-serif;

  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(8px);
  border-radius: 16px;

  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
}

/* 标题 */
h1 {
  text-align: center;
  font-size: 28px;
  margin-bottom: 24px;

  color: #4db8ff; /* 浅蓝色 */
  font-weight: 700;
}

/* 魔方区域 */
.cube-net {
  display: flex;
  flex-direction: column;
  align-items: center;

  padding: 20px;
  margin-bottom: 24px;

  background: #f7f8fc;
  border-radius: 14px;

  box-shadow: inset 0 0 0 1px rgba(0,0,0,0.05),
              0 6px 16px rgba(0,0,0,0.15);
}

.row {
  display: flex;
}

.middle-row {
  margin-left: 130px;
}

/* 控制区 */
.controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.step-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
}

/* 控制区按钮 */
button {
  padding: 10px 18px;
  border: none;
  border-radius: 10px;

  font-size: 14px;
  font-weight: 600;
  color: #fff;

  cursor: pointer;
  background: linear-gradient(135deg, #4facfe, #00f2fe); /* 主按钮渐变色 */
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

button:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}

button:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

button:disabled {
  background: #bfc2d9;
  cursor: not-allowed;
  box-shadow: none;
}

/* 重置按钮 */
.reset-btn {
  background: linear-gradient(135deg, #ff5f6d, #ffc371);
  box-shadow: 0 6px 15px rgba(255, 95, 109, 0.35);
  padding: 10px 18px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.reset-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 10px 22px rgba(255, 95, 109, 0.45);
}

.reset-btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 6px 15px rgba(255, 95, 109, 0.25);
}

/* 2D测试按钮 */
.test-btn {
  margin-top: 16px;
  display: block;
  background: linear-gradient(135deg, #ff9f43, #ff6f00);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.25);
}

.test-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.35);
}

.test-btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.25);
}

/* 3D测试按钮 */
.test3d-btn {
  margin-top: 12px;
  display: block;
  background: linear-gradient(135deg, #20c997, #0ca678);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.25);
}

.test3d-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.35);
}

.test3d-btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.25);
}

/* 上一步/下一步按钮 */
.step-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  width: 100%;
}

/* 进度 */
.progress {
  text-align: center;
  margin-bottom: 12px;
  font-weight: 600;
  color: #333;
}

/* 步骤列表 */
.steps {
  list-style: none;
  padding: 0;
  margin: 0;
}

.steps li {
  padding: 8px 12px;
  margin-bottom: 6px;

  border-radius: 6px;
  background: #f1f2f6;

  transition: all 0.25s ease;
  font-size: 14px;
}

.steps li.active {
  background: linear-gradient(90deg, #6c63ff, #4b45d2);
  color: #fff;
  font-weight: 700;
  transform: translateX(6px);
}

.cube3d-wrapper {
  width: 400px;
  height: 400px;
  margin: 20px auto;
}
</style>
