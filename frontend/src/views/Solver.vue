<template>
  <div class="cube-solver-page">
    <div class="solver-header">
      <div class="title-group">
        <h2 class="main-title">Kociemba 智能求解演示</h2>
        <p class="sub-title">算法层级：二阶段缩减算法 | 最优解步数：{{ steps.length }}</p>
      </div>
      <div class="header-actions">
        <el-button
          type="primary"
          size="large"
          @click="fetchSolution"
          :loading="loading"
          :icon="Search"
          round
        >
          {{ loading ? "正在分析状态..." : "智能求解" }}
        </el-button>
        <el-button
          type="danger"
          size="large"
          plain
          @click="resetCube"
          :icon="RefreshLeft"
          round
        >
          重置
        </el-button>
      </div>
    </div>

    <div class="solver-main-content">
      <div class="view-3d-box">
        <Cube3DView ref="cube3dRef" :cubeState="cubeState" />
        <div class="step-counter" v-if="steps.length">
          <span class="curr">{{ currentStep }}</span>
          <span class="total">/ {{ steps.length }}</span>
        </div>
      </div>

      <div class="view-2d-box">
        <div class="box-label">2D 状态映射</div>
        <div class="mini-net">
          <div class="net-row"><Face2DView :face="cubeState.faces.U" /></div>
          <div class="net-row mid">
            <Face2DView :face="cubeState.faces.L" />
            <Face2DView :face="cubeState.faces.F" />
            <Face2DView :face="cubeState.faces.R" />
            <Face2DView :face="cubeState.faces.B" />
          </div>
          <div class="net-row"><Face2DView :face="cubeState.faces.D" /></div>
        </div>
      </div>
    </div>

    <div class="solver-footer">
      <div class="playback-controls">
        <el-button-group>
          <el-button
            type="info"
            size="large"
            :icon="ArrowLeft"
            @click="prevStep"
            :disabled="currentStep === 0 || is3DBusy"
          >
            上一步
          </el-button>
          <el-button
            type="success"
            size="large"
            :icon="ArrowRight"
            @click="nextStep"
            :disabled="currentStep >= steps.length || !hasSolved || is3DBusy"
          >
            下一步
          </el-button>
        </el-button-group>
      </div>

      <div class="steps-progress-bar" v-if="steps.length">
        <el-scrollbar ref="scrollRef">
          <div class="steps-flex">
            <div
              v-for="(step, index) in steps"
              :key="index"
              class="step-node"
              :class="{
                'is-active': index === currentStep - 1,
                'is-past': index < currentStep - 1
              }"
            >
              <div class="node-idx">{{ index + 1 }}</div>
              <div class="node-move">{{ step }}</div>
            </div>
          </div>
        </el-scrollbar>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue";
import {getCubeState, solveCube} from "../api/cube";
import { createCubeFromJson } from "../utils/cubeState";
import {applyMove, invertMove} from "../utils/cubeMoves";
import Face2DView from "../components/Face2DView.vue";
import Cube3DView from "../components/Cube3DView.vue";
import {
  Search, RefreshLeft, ArrowLeft, ArrowRight
} from "@element-plus/icons-vue";

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
const is3DBusy = ref(false);

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
  if (!hasSolved.value || is3DBusy.value) return;

  if (currentStep.value < solutionMoves.value.length) {
    const move = solutionMoves.value[currentStep.value];
    is3DBusy.value = true;                 // 魔方旋转式暂时锁定按钮
    applyMove(cubeState.value, move);      // 数据层更新 cubies
    cube3dRef.value.playMove(move);        // 播放 3D 动画
    currentStep.value++;

    setTimeout(() => {
      is3DBusy.value = false;
    }, 350); // 动画时长 300ms，预留 50ms 缓冲

    // 自动滚动到底部步骤条
    nextTick(() => {
      const activeNode = document.querySelector('.step-node.is-active');
      if (activeNode) activeNode.scrollIntoView({ behavior: 'smooth', inline: 'center' });
    });
  }
}

function prevStep() {
  if (!hasSolved.value || is3DBusy.value) return;

  if (currentStep.value > 0) {
    is3DBusy.value = true;
    currentStep.value--;
    const move = solutionMoves.value[currentStep.value];
    const reverseMove = invertMove(move);  // 反向 move
    applyMove(cubeState.value, reverseMove);
    cube3dRef.value.playMove(reverseMove); // 播放反向动画
    setTimeout(() => {
      is3DBusy.value = false;
    }, 350); // 动画时长 300ms，预留 50ms 缓冲
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
/* 1. 整体页面背景优化 */
.cube-solver-page {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  background: radial-gradient(circle at 50% 50%, #f8fafc 0%, #f1f5f9 100%);
  padding: 0 40px;
  box-sizing: border-box;
  overflow: hidden; /* 禁止页面滚动 */
}

/* 2. 顶部标题美化 */
.solver-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px 0;
  flex-shrink: 0; /* 防止顶部被压缩 */
}
.main-title {
  font-size: 24px;
  letter-spacing: -0.5px;
  background: linear-gradient(120deg, #1e293b, #334155);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
}
.sub-title { color: #94a3b8; font-size: 13px; margin-top: 4px; font-weight: 500; }

/* 3. 中间展示区：解决溢出与比例 */
.solver-main-content {
  flex: 1;
  display: flex;
  gap: 24px;
  min-height: 0; /* 核心：允许子元素收缩 */
  padding-bottom: 20px; /* 为下方留出呼吸感 */
}

/* 3D 区域卡片化 */
.view-3d-box {
  flex: 3.5;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 28px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0,0,0,0.03), 0 1px 2px rgba(0,0,0,0.02);
  border: 1px solid rgba(255,255,255,0.8);
}

.step-counter {
  position: absolute;
  top: 20px;
  left: 20px; /* 移到左边，更符合 UI 逻辑 */
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(4px);
  padding: 8px 16px;
  border-radius: 12px;
  border: 1px solid #f1f5f9;
}
.curr { font-size: 20px; font-weight: 800; color: #3b82f6; }
.total { color: #94a3b8; font-size: 14px; margin-left: 4px; }

/* 2D 状态概览 */
.view-2d-box {
  flex: 1;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(12px);
  border-radius: 28px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid rgba(255,255,255,0.7);
  box-shadow: 0 4px 20px rgba(0,0,0,0.02);
}
.box-label {
  font-size: 15px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 30px;
  font-weight: 700;
}
.mini-net { transform: scale(0.8); transform-origin: top center; }

/* 4. 底部操作区：修复挡住问题 */
.solver-footer {
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 30px 30px 0 0;
  padding: 24px 40px 35px; /* 底部增加 padding 确保不贴边 */
  box-shadow: 0 -15px 50px rgba(0,0,0,0.04);
  z-index: 10;
}

.playback-controls {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

/* 5. 步骤条“轨道感”美化 */
.steps-progress-bar {
  background: #f8fafc;
  padding: 12px;
  border-radius: 20px;
  border: 1px inset rgba(0,0,0,0.01);
}

.steps-flex {
  display: flex;
  gap: 12px;
  padding: 10px 5px;
  align-items: center;
}

.step-node {
  min-width: 70px;
  background: white;
  border-radius: 14px;
  padding: 12px 8px;
  text-align: center;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid #f1f5f9;
  cursor: pointer;
}

/* 高亮当前步骤 */
.step-node.is-active {
  background: #3b82f6;
  border-color: #3b82f6;
  box-shadow: 0 10px 20px rgba(59, 130, 246, 0.2);
  transform: translateY(-5px);
}
.step-node.is-active .node-move { color: white; }
.step-node.is-active .node-idx { color: rgba(255,255,255,0.7); }

/* 已完成步骤变淡 */
.step-node.is-past {
  opacity: 0.4;
  filter: grayscale(0.8);
}

.node-idx { font-size: 10px; color: #cbd5e1; font-weight: 700; margin-bottom: 4px; }
.node-move { font-size: 17px; font-weight: 800; color: #334155; }

/* 滚动条美化 (适配 Element Plus) */
:deep(.el-scrollbar__bar) {
  bottom: 0px;
}
</style>
