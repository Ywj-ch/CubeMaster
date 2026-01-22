<template>
  <div class="cube-solver-page">
    <div class="solver-header">
      <div class="title-group">
        <h2 class="main-title">Kociemba 智能求解演示</h2>
        <p class="sub-title">算法层级：二阶段缩减算法 | 最优解步数：{{ steps.length }}</p>
      </div>
      <div class="header-actions">
        <el-button
          type="success"
          size="large"
          @click="openScanner"
          :icon="Camera"
          round
        >
          扫描识别
        </el-button>
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
          重置魔方
        </el-button>
      </div>
    </div>

    <div class="solver-main-content">
      <div class="view-3d-box">
        <Cube3DView
          ref="cube3dRef"
          :cubeState="cubeState"
          :interactive="!hasSolved"
          :enableControls="true"
        />
        <div class="step-counter" v-if="steps.length">
          <span class="curr">{{ currentStep }}</span>
          <span class="total">/ {{ steps.length }}</span>
        </div>
      </div>

      <div class="view-2d-box" :class="{ 'is-solved-locked': hasSolved }">
        <div class="box-label">2D 状态校准</div>

        <div class="vertical-net">
          <div class="face-group">
            <div class="face-wrapper">
              <span class="face-id">U (顶面)</span>
              <Face2DView :face="cubeState.faces.U" @cell-click="idx => toggleColor('U', idx)" />
            </div>
          </div>

          <div class="face-grid">
            <div class="face-wrapper">
              <span class="face-id">L (左)</span>
              <Face2DView :face="cubeState.faces.L" @cell-click="idx => toggleColor('L', idx)" />
            </div>
            <div class="face-wrapper">
              <span class="face-id">F (前)</span>
              <Face2DView :face="cubeState.faces.F" @cell-click="idx => toggleColor('F', idx)" />
            </div>
            <div class="face-wrapper">
              <span class="face-id">R (右)</span>
              <Face2DView :face="cubeState.faces.R" @cell-click="idx => toggleColor('R', idx)" />
            </div>
            <div class="face-wrapper">
              <span class="face-id">B (后)</span>
              <Face2DView :face="cubeState.faces.B" @cell-click="idx => toggleColor('B', idx)" />
            </div>
          </div>

          <div class="face-group">
            <div class="face-wrapper">
              <span class="face-id">D (底面)</span>
              <Face2DView :face="cubeState.faces.D" @cell-click="idx => toggleColor('D', idx)" />
            </div>
          </div>
        </div>

        <p class="hint-text"><el-icon><InfoFilled /></el-icon> 点击方块修正识别错误</p>
      </div>
    </div>

    <div class="solver-footer">
      <!-- 优化后的播放控制栏 -->
      <div class="playback-controls">
        <el-tooltip content="上一步" placement="top">
          <el-button
            circle
            size="large"
            :icon="ArrowLeft"
            @click="prevStep"
            :disabled="currentStep === 0 || is3DBusy"
            class="nav-btn"
          />
        </el-tooltip>

        <el-button
          type="primary"
          size="large"
          class="play-btn"
          @click="toggleAutoPlay"
          :disabled="!hasSolved || currentStep >= steps.length"
          round
        >
          <el-icon class="el-icon--left">
            <component :is="isAutoPlaying ? VideoPause : VideoPlay" />
          </el-icon>
          {{ isAutoPlaying ? '暂停演示' : '自动演示' }}
        </el-button>

        <el-tooltip content="下一步" placement="top">
          <el-button
            circle
            size="large"
            :icon="ArrowRight"
            @click="nextStep"
            :disabled="currentStep >= steps.length || !hasSolved || is3DBusy"
            class="nav-btn"
          />
        </el-tooltip>
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
              @click="jumpToStep(index)"
            >
              <div class="node-idx">{{ index + 1 }}</div>
              <div class="node-move">{{ step }}</div>
            </div>
          </div>
        </el-scrollbar>
      </div>
    </div>
  </div>

  <div class="container">
    <CubeScanner
      :visible="isScannerVisible"
      @close="isScannerVisible = false"
      @scanned="handleScannedResult"
    />
  </div>
</template>

<script setup>
import { ref, nextTick, onUnmounted } from "vue";
import {solveCube, saveCubeState} from "../api/cubeService.js";
import { createCubeFromJson } from "../utils/cubeState";
import {applyMove, invertMove} from "../utils/cubeMoves";
import Face2DView from "../components/Face2DView.vue";
import Cube3DView from "../components/Cube3DView.vue";
import CubeScanner from '../components/CubeScanner.vue';
import {
  Camera, Search, RefreshLeft, ArrowLeft, ArrowRight, InfoFilled, VideoPlay, VideoPause
} from "@element-plus/icons-vue";
import { ElMessage } from 'element-plus';

// 状态
const loading = ref(false);
const hasSolved = ref(false);
const steps = ref([]);
const currentStep = ref(0);
const cubeState = ref(createCubeFromJson());
const cube3dRef = ref(null);
const solutionMoves = ref([]);
const is3DBusy = ref(false);
const isScannerVisible = ref(false);
const COLOR_ORDER = ['white', 'yellow', 'red', 'orange', 'blue', 'green'];

// 自动播放相关状态
const isAutoPlaying = ref(false);
let autoPlayTimer = null;
const AUTO_PLAY_INTERVAL = 800; // 自动播放间隔 (ms)，需大于动画时长

// 打开扫描器的方法
const openScanner = () => {
  isScannerVisible.value = true;
};

// 处理扫描结果
const handleScannedResult = (result) => {
  isScannerVisible.value = false;
  const newCube = createCubeFromJson(result);
  cubeState.value.cubies = newCube.cubies;
  cubeState.value.faces = newCube.faces;
  ElMessage.success('扫描成功，请点击 2D 图纠正可能的识别错误');
};

const toggleColor = (faceKey, index) => {
  if (hasSolved.value) {
    ElMessage.info("请先完成当前解法或重置魔方后再修改状态");
    return;
  }
  const faceData = cubeState.value.faces[faceKey];
  if (!faceData) return;

  let currentColor;
  let row, col;

  if (Array.isArray(faceData[0])) {
    row = Math.floor(index / 3);
    col = index % 3;
    currentColor = faceData[row][col];
  } else {
    currentColor = faceData[index];
  }

  let nextColor;
  if (!COLOR_ORDER.includes(currentColor)) {
    nextColor = COLOR_ORDER[0];
  } else {
    const nextIdx = (COLOR_ORDER.indexOf(currentColor) + 1) % COLOR_ORDER.length;
    nextColor = COLOR_ORDER[nextIdx];
  }

  if (Array.isArray(faceData[0])) {
    faceData[row][col] = nextColor;
  } else {
    faceData[index] = nextColor;
  }

  const updatedCube = createCubeFromJson(cubeState.value.faces);
  cubeState.value.cubies = updatedCube.cubies;
  hasSolved.value = false;
};

async function fetchSolution() {
  loading.value = true;
  stopAutoPlay(); // 重新求解前停止播放
  try {
    await saveCubeState(cubeState.value.faces);
    const res = await solveCube();
    const data = res.data.data;

    if (data?.raw_solution && data.raw_solution.startsWith("Error")) {
      ElMessage.error("颜色布局不合法，请检查是否有重复颜色或方向错误");
      hasSolved.value = false;
      return;
    }

    steps.value = data.readable_solution;
    solutionMoves.value = data.moves;
    currentStep.value = 0;
    hasSolved.value = true;
    ElMessage.success('求解成功！');

  } catch (e) {
    console.error(e);
    ElMessage.error("请求失败，请检查网络");
  } finally {
    loading.value = false;
  }
}

// --- 自动播放逻辑 ---

function toggleAutoPlay() {
  if (isAutoPlaying.value) {
    stopAutoPlay();
  } else {
    startAutoPlay();
  }
}

function startAutoPlay() {
  if (currentStep.value >= steps.value.length) return;

  isAutoPlaying.value = true;
  // 立即执行一步，然后开始循环
  nextStep(true);

  autoPlayTimer = setInterval(() => {
    if (currentStep.value >= steps.value.length) {
      stopAutoPlay();
    } else {
      nextStep(true);
    }
  }, AUTO_PLAY_INTERVAL);
}

function stopAutoPlay() {
  isAutoPlaying.value = false;
  if (autoPlayTimer) {
    clearInterval(autoPlayTimer);
    autoPlayTimer = null;
  }
}

// --- 步骤控制 ---

function nextStep(isAuto = false) {
  if (!isAuto) {
    stopAutoPlay();
  }

  if (!hasSolved.value || is3DBusy.value) return;

  if (currentStep.value < solutionMoves.value.length) {
    const move = solutionMoves.value[currentStep.value];
    is3DBusy.value = true;
    applyMove(cubeState.value, move);
    cube3dRef.value.playMove(move);
    currentStep.value++;

    setTimeout(() => {
      is3DBusy.value = false;
    }, 350);

    nextTick(() => {
      const activeNode = document.querySelector('.step-node.is-active');
      if (activeNode) activeNode.scrollIntoView({ behavior: 'smooth', inline: 'center' });
    });
  } else {
    // 如果已经到最后一步，停止自动播放
    stopAutoPlay();
  }
}

function prevStep() {
  stopAutoPlay(); // 手动介入时停止自动播放
  if (!hasSolved.value || is3DBusy.value) return;

  if (currentStep.value > 0) {
    is3DBusy.value = true;
    currentStep.value--;
    const move = solutionMoves.value[currentStep.value];
    const reverseMove = invertMove(move);
    applyMove(cubeState.value, reverseMove);
    cube3dRef.value.playMove(reverseMove);
    setTimeout(() => {
      is3DBusy.value = false;
    }, 350);
  }
}

// 允许点击步骤条跳转（可选功能，暂未完全实现逻辑，仅作为占位）
function jumpToStep(index) {
  // 复杂的跳转逻辑需要计算中间差值，这里暂时只停止播放
  stopAutoPlay();
}

function resetCube() {
  stopAutoPlay();
  cubeState.value = createCubeFromJson();
  steps.value = [];
  solutionMoves.value = [];
  currentStep.value = 0;
  hasSolved.value = false;
}

// 组件卸载时清理定时器
onUnmounted(() => {
  stopAutoPlay();
});
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

/* 优化后的 2D 容器 */
.view-2d-box {
  flex: 1.2; /* 稍微增加占比以适应垂直布局 */
  background: white;
  border-radius: 24px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  overflow-y: auto; /* 如果内容过多允许内部滚动 */
}

/* 垂直容器 */
.vertical-net {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  align-items: center;
}

/* 2x2 网格处理中间四个面，防止横向溢出 */
.face-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.face-wrapper {
  padding: 8px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #f1f5f9;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.2s;
}

/* 移除那个“蓝色的框”，保持统一的灰色边框，仅在 hover 时反馈 */
.face-wrapper:hover {
  border-color: #cbd5e1;
  background: #f1f5f9;
}

.face-id {
  font-size: 11px;
  font-weight: 700;
  color: #64748b;
  margin-bottom: 6px;
  text-transform: uppercase;
}

.hint-text {
  margin-top: 20px;
  font-size: 12px;
  color: #94a3b8;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 当已经有解法时，2D区域的样式 */
.is-solved-locked {
  cursor: not-allowed;
  position: relative;
}

/* 4. 底部操作区：修复挡住问题 */
.solver-footer {
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 30px 30px 0 0;
  padding: 24px 40px 35px; /* 底部增加 padding 确保不贴边 */
  box-shadow: 0 -15px 50px rgba(0,0,0,0.04);
  z-index: 10;
}

/* 播放控制器样式优化 */
.playback-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px; /* 按钮间距 */
  margin-bottom: 24px;
}

/* 播放按钮突出显示 */
.play-btn {
  width: 140px;
  font-weight: 600;
  letter-spacing: 1px;
  transition: all 0.3s;
}
.play-btn:not(:disabled):hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
}

/* 导航按钮样式 */
.nav-btn {
  border-color: #e2e8f0;
  color: #64748b;
}
.nav-btn:not(:disabled):hover {
  border-color: #3b82f6;
  color: #3b82f6;
  background: #eff6ff;
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