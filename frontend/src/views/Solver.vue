<template>
  <div class="cube-solver-page">
    <div class="solver-header">
      <div class="title-group">
        <h2 class="main-title">Kociemba 智能求解演示</h2>
        <p class="sub-title">
          算法层级：二阶段缩减算法 | 最优解步数：{{ steps.length }}
        </p>
      </div>
      <div class="header-actions">
        <!-- 1. 扫描识别 (Ins风格 -> 蓝青渐变胶囊) -->
        <button
          class="btn-scan-glass"
          @click="openScanner"
          :disabled="scanning || loading || hasSolved"
        >
          <span class="svgContainer">
            <el-icon v-if="scanning" class="is-loading"><Loading /></el-icon>
            <el-icon v-else><Camera /></el-icon>
          </span>
          <span class="BG"></span>
          <!-- 新增文字，让它变长 -->
          <span class="btn-text">{{
            scanning ? "扫描中..." : "扫描识别"
          }}</span>
        </button>

        <!-- 2. 智能求解 (Send风格 -> 搜索飞行) -->
        <button
          class="btn-solve-fly"
          @click="fetchSolution"
          :disabled="loading || hasSolved"
        >
          <div class="svg-wrapper-1">
            <div class="svg-wrapper">
              <el-icon v-if="loading" class="is-loading"><Loading /></el-icon>
              <el-icon v-else><Search /></el-icon>
            </div>
          </div>
          <span>{{ loading ? "计算中..." : "智能求解" }}</span>
        </button>

        <!-- 3. 重置魔方 (极简红框) -->
        <button class="btn-reset-minimal" @click="resetCube">
          <el-icon><RefreshLeft /></el-icon>
          重置
        </button>
      </div>
    </div>

    <!-- 中间内容区：flex: 1 自动撑开，溢出滚动 -->
    <div class="solver-content-wrapper">
      <div class="solver-main-content">
        <div class="view-3d-box">
          <Cube3DView
            ref="cube3dRef"
            :cubeState="cubeState"
            :interactive="!hasSolved"
            :enableControls="true"
            :moveDuration="demoSpeed"
            :customization="config"
          />
          <div class="step-counter" v-if="steps.length">
            <span class="curr">{{ currentStep }}</span>
            <span class="total">/ {{ steps.length }}</span>
          </div>
        </div>

        <div class="view-2d-box" :class="{ 'is-solved-locked': hasSolved }">
          <div class="box-label">2D 状态校准</div>

          <div class="editor-container">
            <div class="vertical-net">
              <div class="face-group">
                <div class="face-wrapper">
                  <span class="face-id">U (顶面)</span>
                  <Face2DView
                    :face="cubeState.faces.U"
                    @cell-click="(idx) => toggleColor('U', idx)"
                  />
                </div>
              </div>
              <div class="face-grid">
                <div class="face-wrapper">
                  <span class="face-id">L (左)</span>
                  <Face2DView
                    :face="cubeState.faces.L"
                    @cell-click="(idx) => toggleColor('L', idx)"
                  />
                </div>
                <div class="face-wrapper">
                  <span class="face-id">F (前)</span>
                  <Face2DView
                    :face="cubeState.faces.F"
                    @cell-click="(idx) => toggleColor('F', idx)"
                  />
                </div>
                <div class="face-wrapper">
                  <span class="face-id">R (右)</span>
                  <Face2DView
                    :face="cubeState.faces.R"
                    @cell-click="(idx) => toggleColor('R', idx)"
                  />
                </div>
                <div class="face-wrapper">
                  <span class="face-id">B (后)</span>
                  <Face2DView
                    :face="cubeState.faces.B"
                    @cell-click="(idx) => toggleColor('B', idx)"
                  />
                </div>
              </div>
              <div class="face-group">
                <div class="face-wrapper">
                  <span class="face-id">D (底面)</span>
                  <Face2DView
                    :face="cubeState.faces.D"
                    @cell-click="(idx) => toggleColor('D', idx)"
                  />
                </div>
              </div>
            </div>

            <div class="palette-toolbar">
              <div class="palette-label">画笔</div>
              <div
                v-for="color in PALETTE"
                :key="color.name"
                class="palette-item"
                :class="{ active: activeColor === color.name }"
                :style="{ backgroundColor: color.hex }"
                @click="activeColor = color.name"
                :title="color.label"
              >
                <div v-if="activeColor === color.name" class="check-mark"></div>
              </div>
            </div>
          </div>

          <p class="hint-text">
            <el-icon><InfoFilled /></el-icon> 选择画笔颜色后点击方块修改
          </p>
        </div>
      </div>
    </div>

    <div class="solver-footer">
      <div class="playback-controls">
        <div class="speed-control-wrapper">
          <span class="speed-label">速度</span>
          <el-radio-group v-model="demoSpeed" size="small" class="speed-radios">
            <el-radio-button :value="800">慢</el-radio-button>
            <el-radio-button :value="300">中</el-radio-button>
            <el-radio-button :value="150">快</el-radio-button>
          </el-radio-group>
        </div>

        <div class="main-controls">
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
            {{ isAutoPlaying ? "暂停演示" : "自动演示" }}
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

        <div class="control-spacer"></div>
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
                'is-past': index < currentStep - 1,
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
import { ref, nextTick, onUnmounted, watch } from "vue";
import { solveCube, saveCubeState } from "../api/cubeService.js";
import { createCubeFromJson } from "../utils/cubeState";
import { applyMove, invertMove } from "../utils/cubeMoves";
import Face2DView from "../components/Face2DView.vue";
import Cube3DView from "../components/Cube3DView.vue";
import CubeScanner from "../components/CubeScanner.vue";
import {
  Camera,
  Search,
  RefreshLeft,
  ArrowLeft,
  ArrowRight,
  InfoFilled,
  VideoPlay,
  VideoPause,
  Loading,
} from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { useCubeCustomization } from "../composables/useCubeCustomization.js";

const { config } = useCubeCustomization();

const loading = ref(false);
const scanning = ref(false);
const hasSolved = ref(false);
const steps = ref([]);
const currentStep = ref(0);
const cubeState = ref(createCubeFromJson());
const cube3dRef = ref(null);
const solutionMoves = ref([]);
const is3DBusy = ref(false);
const isScannerVisible = ref(false);

const PALETTE = [
  { name: "white", hex: "#FFFFFF", label: "白" },
  { name: "yellow", hex: "#FFD500", label: "黄" },
  { name: "red", hex: "#C41E3A", label: "红" },
  { name: "orange", hex: "#FF5800", label: "橙" },
  { name: "blue", hex: "#0051BA", label: "蓝" },
  { name: "green", hex: "#009E60", label: "绿" },
];
const activeColor = ref("white");

const isAutoPlaying = ref(false);
let autoPlayTimer = null;
const demoSpeed = ref(300);

const openScanner = () => {
  scanning.value = true;
  isScannerVisible.value = true;
};
const handleScannedResult = (result) => {
  scanning.value = false;
  isScannerVisible.value = false;
  const newCube = createCubeFromJson(result);
  cubeState.value.cubies = newCube.cubies;
  cubeState.value.faces = newCube.faces;
  ElMessage.success("扫描成功，请点击 2D 图纠正可能的识别错误");
};

const toggleColor = (faceKey, index) => {
  if (hasSolved.value) {
    ElMessage.info("请先完成当前解法或重置魔方后再修改状态");
    return;
  }
  const faceData = cubeState.value.faces[faceKey];
  if (!faceData) return;
  const newColor = activeColor.value;
  let row, col;
  if (Array.isArray(faceData[0])) {
    row = Math.floor(index / 3);
    col = index % 3;
    faceData[row][col] = newColor;
  } else {
    faceData[index] = newColor;
  }
  const updatedCube = createCubeFromJson(cubeState.value.faces);
  cubeState.value.cubies = updatedCube.cubies;
  hasSolved.value = false;
};

async function fetchSolution() {
  loading.value = true;
  stopAutoPlay();
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
    ElMessage.success("求解成功！");
  } catch (e) {
    console.error(e);
    ElMessage.error("请求失败，请检查网络");
  } finally {
    loading.value = false;
  }
}

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
  nextStep(true);
  const interval = demoSpeed.value + 50;
  autoPlayTimer = setInterval(() => {
    if (currentStep.value >= steps.value.length) {
      stopAutoPlay();
    } else {
      nextStep(true);
    }
  }, interval);
}

function stopAutoPlay() {
  isAutoPlaying.value = false;
  if (autoPlayTimer) {
    clearInterval(autoPlayTimer);
    autoPlayTimer = null;
  }
}

watch(demoSpeed, () => {
  if (isAutoPlaying.value) {
    stopAutoPlay();
    startAutoPlay();
  }
});

// 监听扫描器关闭事件，重置扫描状态
watch(isScannerVisible, (newVal) => {
  if (!newVal && scanning.value) {
    scanning.value = false;
  }
});

function nextStep(isAuto = false) {
  if (!isAuto) stopAutoPlay();
  if (!hasSolved.value || is3DBusy.value) return;
  if (currentStep.value < solutionMoves.value.length) {
    const move = solutionMoves.value[currentStep.value];
    is3DBusy.value = true;
    applyMove(cubeState.value, move);
    cube3dRef.value.playMove(move);
    currentStep.value++;
    setTimeout(() => {
      is3DBusy.value = false;
    }, demoSpeed.value + 20);
    nextTick(() => {
      const activeNode = document.querySelector(".step-node.is-active");
      if (activeNode)
        activeNode.scrollIntoView({ behavior: "smooth", inline: "center" });
    });
  } else {
    stopAutoPlay();
  }
}

function prevStep() {
  stopAutoPlay();
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
    }, demoSpeed.value + 20);
  }
}

function jumpToStep(index) {
  stopAutoPlay();
}

async function resetCube() {
  let message = "";
  let title = "重置确认";

  if (hasSolved.value) {
    title = "开始新的求解";
    message =
      "求解已完成。如需重新扫描识别或重新求解，请先重置魔方状态。\n\n当前求解进度将丢失，确定要重置吗？";
  } else if (scanning.value || loading.value) {
    title = "取消当前操作";
    message = "当前正在进行操作，确定要取消并重置吗？";
  } else {
    message = "确定要重置魔方吗？当前状态将被清空。";
  }

  try {
    await ElMessageBox.confirm(message, title, {
      confirmButtonText: "确定重置",
      cancelButtonText: "取消",
      type: "warning",
      customClass: "reset-confirm-dialog",
      distinguishCancelAndClose: true,
    });
    stopAutoPlay();
    cubeState.value = createCubeFromJson();
    steps.value = [];
    solutionMoves.value = [];
    currentStep.value = 0;
    hasSolved.value = false;
    activeColor.value = "white";
    ElMessage.success("魔方已重置，可以开始新的扫描");
  } catch (error) {
    // 用户点击取消
  }
}

onUnmounted(() => {
  stopAutoPlay();
});
</script>

<style scoped>
/* --- 布局修复 -- */
.cube-solver-page {
  /*
    使用 flex-grow: 1 自动占满父容器 (MainLayout) 的剩余空间。
    不再使用 100vh，这样就不会因为 Header 高度计算错误而溢出。
  */
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  background: radial-gradient(circle at 50% 50%, #f8fafc 0%, #f1f5f9 100%);
  padding: 0 40px;
  box-sizing: border-box;
  overflow: hidden; /* 防止页面整体滚动，只让内部区域滚动 */
}

/* 顶部 Header */
.solver-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
  flex-shrink: 0;
}
.main-title {
  font-size: 24px;
  letter-spacing: -0.5px;
  background: linear-gradient(120deg, #1e293b, #334155);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
}
.sub-title {
  color: #94a3b8;
  font-size: 13px;
  margin-top: 4px;
  font-weight: 500;
}
.header-actions {
  display: flex;
  gap: 16px;
  align-items: center;
}

/* --- 1. 扫描识别按钮 (Ins风格 -> 蓝青渐变胶囊) --- */
.btn-scan-glass {
  width: 130px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background-color: transparent;
  position: relative;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s;
  gap: 8px; /* 增加 gap */
}
.svgContainer {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  backdrop-filter: blur(4px);
  letter-spacing: 0.8px;
  border-radius: 50px;
  transition: all 0.3s;
  border: 1px solid rgba(156, 156, 156, 0.2);
  z-index: 2;
  position: absolute;
  inset: 0; /* 覆盖在背景上 */
}
.BG {
  position: absolute;
  content: "";
  width: 100%;
  height: 100%;
  /* 1. 改为线性流光渐变 (蓝 -> 青 -> 蓝) */
  background: linear-gradient(90deg, #2563eb, #06b6d4, #2563eb);
  /* 2. 放大背景尺寸，以便移动 */
  background-size: 200% 100%;
  z-index: 1;
  border-radius: 50px;
  pointer-events: none;
  transition: all 0.3s;
  /* 3. 默认静止，悬浮时才动，或者一直动也可以 */
  animation: scan-flow 3s linear infinite;
  opacity: 0.8;
}
/* 新增动画关键帧 */
@keyframes scan-flow {
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 200% 50%;
  }
}
.btn-text {
  z-index: 3;
  color: white;
  font-weight: 700;
  font-size: 14px;
  margin-left: 28px; /* 给图标留位置 */
  transition: all 0.3s;
}
.svgContainer .el-icon {
  font-size: 18px;
  color: white;
  position: absolute;
  left: 16px;
} /* 固定图标位置 */

.btn-scan-glass:hover .BG {
  transform: scale(1.05);
  filter: brightness(1.2);
  opacity: 1;
}
.btn-scan-glass:hover .svgContainer {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
}

/* --- 2. 智能求解按钮 (Send风格 -> 飞行) --- */
.btn-solve-fly {
  font-family: inherit;
  font-size: 16px;
  background: #2563eb;
  color: white;
  padding: 0.7em 1.5em;
  display: flex;
  align-items: center;
  border: none;
  border-radius: 50px;
  overflow: hidden;
  transition: all 0.2s;
  cursor: pointer;
  height: 44px;
  box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
}
.btn-solve-fly span {
  display: block;
  margin-left: 0.5em;
  transition: all 0.3s ease-in-out;
  font-weight: 700;
}
.btn-solve-fly .el-icon {
  font-size: 18px;
  display: block;
  transform-origin: center center;
  transition: transform 0.3s ease-in-out;
}
.btn-solve-fly:hover .svg-wrapper {
  animation: fly-1 0.6s ease-in-out infinite alternate;
}
.btn-solve-fly:hover .el-icon {
  transform: translateX(2.5em) scale(1.2);
  color: #fff;
}
.btn-solve-fly:hover span {
  transform: translateX(5em);
  opacity: 0;
}
.btn-solve-fly:active {
  transform: scale(0.95);
}
@keyframes fly-1 {
  from {
    transform: translateY(0.1em);
  }
  to {
    transform: translateY(-0.1em);
  }
}

/* --- 3. 重置按钮 (极简红框) --- */
.btn-reset-minimal {
  padding: 0 24px;
  height: 44px;
  background: transparent;
  border: 1px solid #fecaca;
  border-radius: 50px;
  color: #ef4444;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s;
}
.btn-reset-minimal:hover {
  background: #fef2f2;
  border-color: #ef4444;
  transform: translateY(-1px);
}

/* --- 中间内容区 (关键修改：限制高度，允许内部滚动) --- */
.solver-content-wrapper {
  flex: 1; /* 占据剩余高度 */
  min-height: 0; /* 允许 flex 子项收缩 */
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 防止溢出 */
}

.solver-main-content {
  flex: 1;
  display: flex;
  gap: 24px;
  min-height: 0; /* 关键：允许子元素滚动 */
  padding-bottom: 20px;
}

.view-3d-box {
  flex: 3.5;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 28px;
  position: relative;
  overflow: hidden;
  box-shadow:
    0 10px 40px rgba(0, 0, 0, 0.03),
    0 1px 2px rgba(0, 0, 0, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.step-counter {
  position: absolute;
  top: 20px;
  left: 20px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(4px);
  padding: 8px 16px;
  border-radius: 12px;
  border: 1px solid #f1f5f9;
}
.curr {
  font-size: 20px;
  font-weight: 800;
  color: #3b82f6;
}
.total {
  color: #94a3b8;
  font-size: 14px;
  margin-left: 4px;
}

/* --- 编辑器区域布局 --- */
.view-2d-box {
  flex: 1.2;
  background: white;
  border-radius: 24px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  overflow-y: auto; /* 允许右侧长内容滚动 */
}
.box-label {
  text-align: center;
  font-weight: 700;
  color: #64748b;
  margin-bottom: 15px;
}
.editor-container {
  display: flex;
  justify-content: center;
  gap: 32px;
  width: 100%;
}
.vertical-net {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
  transform: scale(0.95);
}
.palette-toolbar {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 10px;
  background: #f8fafc;
  border-radius: 16px;
  border: 1px solid #f1f5f9;
  height: fit-content;
  align-self: center;
}
.palette-label {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
  text-align: center;
  margin-bottom: 4px;
}
.palette-item {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: 2px solid rgba(0, 0, 0, 0.05);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}
.palette-item:hover {
  transform: scale(1.1);
  z-index: 1;
}
.palette-item.active {
  border-color: #3b82f6;
  transform: scale(1.15);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}
.check-mark {
  width: 8px;
  height: 8px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 50%;
}
.palette-item.active .check-mark {
  background: white;
}
.face-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}
.face-wrapper {
  padding: 6px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #f1f5f9;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.2s;
}
.face-wrapper:hover {
  border-color: #cbd5e1;
  background: #f1f5f9;
}
.face-id {
  font-size: 10px;
  font-weight: 700;
  color: #64748b;
  margin-bottom: 4px;
  text-transform: uppercase;
}
.hint-text {
  margin-top: auto;
  padding-top: 20px;
  font-size: 12px;
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}
.is-solved-locked {
  cursor: not-allowed;
  position: relative;
  opacity: 0.8;
  filter: grayscale(0.2);
}

/* 底部区域 */
.solver-footer {
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 30px 30px 0 0;
  padding: 24px 40px 35px;
  box-shadow: 0 -15px 50px rgba(0, 0, 0, 0.04);
  z-index: 10;
}
.playback-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  position: relative;
}
.speed-control-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 200px;
}
.speed-label {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
}
.speed-radios :deep(.el-radio-button__inner) {
  padding: 6px 12px;
  font-size: 12px;
}
.main-controls {
  display: flex;
  align-items: center;
  gap: 20px;
}
.control-spacer {
  width: 200px;
}
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
.nav-btn {
  border-color: #e2e8f0;
  color: #64748b;
}
.nav-btn:not(:disabled):hover {
  border-color: #3b82f6;
  color: #3b82f6;
  background: #eff6ff;
}
.steps-progress-bar {
  background: #f8fafc;
  padding: 12px;
  border-radius: 20px;
  border: 1px inset rgba(0, 0, 0, 0.01);
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
.step-node.is-active {
  background: #3b82f6;
  border-color: #3b82f6;
  box-shadow: 0 10px 20px rgba(59, 130, 246, 0.2);
  transform: translateY(-5px);
}
.step-node.is-active .node-move {
  color: white;
}
.step-node.is-active .node-idx {
  color: rgba(255, 255, 255, 0.7);
}
.step-node.is-past {
  opacity: 0.4;
  filter: grayscale(0.8);
}
.node-idx {
  font-size: 10px;
  color: #cbd5e1;
  font-weight: 700;
  margin-bottom: 4px;
}
.node-move {
  font-size: 17px;
  font-weight: 800;
  color: #334155;
}
:deep(.el-scrollbar__bar) {
  bottom: 0px;
}

/* ==================== Dark Mode Styles ==================== */
/* 页面背景 */
[data-theme="dark"] .cube-solver-page {
  background: radial-gradient(
    circle at 50% 50%,
    var(--dm-bg-page) 0%,
    #0a0f1a 100%
  );
}

/* 顶部 Header */
[data-theme="dark"] .solver-header {
  background: transparent;
}

[data-theme="dark"] .main-title {
  background: linear-gradient(120deg, var(--dm-text-primary), var(--dm-accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

[data-theme="dark"] .sub-title {
  color: var(--dm-text-muted);
}

/* 页面标题 */
[data-theme="dark"] .page-title {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .page-title .highlight {
  color: var(--dm-accent);
}

/* 扫描按钮 */
[data-theme="dark"] .btn-scan-glass .svgContainer {
  background-color: rgba(0, 0, 0, 0.3);
  border-color: rgba(96, 165, 250, 0.3);
}

[data-theme="dark"] .btn-scan-glass:hover .svgContainer {
  background-color: rgba(96, 165, 250, 0.2);
  border-color: rgba(96, 165, 250, 0.5);
}

/* 求解按钮 */
[data-theme="dark"] .btn-solve-fly {
  background: var(--dm-accent);
  box-shadow: 0 4px 15px rgba(96, 165, 250, 0.4);
}

[data-theme="dark"] .btn-solve-fly:hover {
  background: var(--dm-accent-hover);
}

/* 重置按钮 */
[data-theme="dark"] .btn-reset-minimal {
  background: transparent;
  border-color: rgba(248, 113, 113, 0.4);
  color: var(--dm-accent-error);
}

[data-theme="dark"] .btn-reset-minimal:hover {
  background: rgba(248, 113, 113, 0.1);
  border-color: var(--dm-accent-error);
}

/* 3D 视图区域 */
[data-theme="dark"] .view-3d-box {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .step-counter {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .curr {
  color: var(--dm-accent);
}

[data-theme="dark"] .total {
  color: var(--dm-text-muted);
}

/* 2D 编辑区域 */
[data-theme="dark"] .view-2d-box {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .box-label {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .palette-toolbar {
  background: var(--dm-bg-hover);
  border-color: var(--dm-border);
}

[data-theme="dark"] .palette-label {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .palette-item {
  border-color: var(--dm-border);
  box-shadow: var(--dm-shadow-sm);
}

[data-theme="dark"] .palette-item.active {
  border-color: var(--dm-accent);
  box-shadow: 0 4px 12px rgba(96, 165, 250, 0.4);
}

[data-theme="dark"] .face-wrapper {
  background: var(--dm-bg-hover);
  border-color: var(--dm-border);
}

[data-theme="dark"] .face-wrapper:hover {
  border-color: var(--dm-border-light);
  background: var(--dm-bg-card);
}

[data-theme="dark"] .face-id {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .hint-text {
  color: var(--dm-text-muted);
}

/* 底部控制区域 */
[data-theme="dark"] .solver-footer {
  background: var(--dm-bg-card);
  box-shadow: 0 -15px 50px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .speed-label {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .play-btn {
  background: var(--dm-accent);
  border-color: var(--dm-accent);
}

[data-theme="dark"] .play-btn:not(:disabled):hover {
  box-shadow: 0 4px 12px rgba(96, 165, 250, 0.5);
}

/* 主卡片 */
[data-theme="dark"] .solver-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
  box-shadow: var(--dm-shadow-md);
}

/* 扫描状态 */
[data-theme="dark"] .scan-status {
  background: var(--dm-bg-hover);
  border-color: var(--dm-border);
}

[data-theme="dark"] .scan-status.status-ready {
  background: rgba(96, 165, 250, 0.1);
  border-color: rgba(96, 165, 250, 0.2);
}

[data-theme="dark"] .scan-status.status-active {
  background: rgba(52, 211, 153, 0.1);
  border-color: rgba(52, 211, 153, 0.2);
}

[data-theme="dark"] .scan-status.status-busy {
  background: rgba(251, 146, 60, 0.1);
  border-color: rgba(251, 146, 60, 0.2);
}

[data-theme="dark"] .status-text {
  color: var(--dm-text-secondary);
}

/* 预览区域 */
[data-theme="dark"] .preview-section {
  background: var(--dm-bg-hover);
  border-color: var(--dm-border);
}

[data-theme="dark"] .preview-label {
  color: var(--dm-text-muted);
}

/* 控制按钮 */
[data-theme="dark"] .action-btn {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .action-btn:hover {
  background: var(--dm-bg-hover);
  border-color: var(--dm-border-hover);
  color: var(--dm-accent);
}

[data-theme="dark"] .action-btn.primary {
  background: var(--dm-accent);
  border-color: var(--dm-accent);
  color: #0f172a;
}

[data-theme="dark"] .action-btn.primary:hover {
  background: var(--dm-accent-hover);
  border-color: var(--dm-accent-hover);
}

/* 步骤面板 */
[data-theme="dark"] .steps-panel {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .panel-header {
  border-color: var(--dm-border);
}

[data-theme="dark"] .panel-title {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .step-count {
  color: var(--dm-text-muted);
}

/* 速度控制 */
[data-theme="dark"] .speed-label {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .nav-btn {
  border-color: var(--dm-border);
  color: var(--dm-text-muted);
}

[data-theme="dark"] .nav-btn:not(:disabled):hover {
  border-color: var(--dm-accent);
  color: var(--dm-accent);
  background: rgba(96, 165, 250, 0.1);
}

/* 步骤进度条 */
[data-theme="dark"] .steps-progress-bar {
  background: var(--dm-bg-hover);
  border-color: var(--dm-border);
}

[data-theme="dark"] .step-node {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .step-node.is-active {
  background: var(--dm-accent);
  border-color: var(--dm-accent);
  box-shadow: 0 10px 20px rgba(96, 165, 250, 0.3);
}

[data-theme="dark"] .step-node.is-active .node-move {
  color: #0f172a;
}

[data-theme="dark"] .step-node.is-active .node-idx {
  color: rgba(15, 23, 42, 0.7);
}

[data-theme="dark"] .node-move {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .node-idx {
  color: var(--dm-text-muted);
}

/* 结果区域 */
[data-theme="dark"] .result-section {
  background: var(--dm-bg-hover);
  border-color: var(--dm-border);
}

[data-theme="dark"] .result-label {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .result-value {
  color: var(--dm-text-primary);
}

/* 错误提示 */
[data-theme="dark"] .error-message {
  background: rgba(248, 113, 113, 0.1);
  border-color: rgba(248, 113, 113, 0.2);
  color: var(--dm-accent-error);
}
</style>

<!-- 全局样式：重置确认弹窗美化 -->
<style>
.reset-confirm-dialog {
  border-radius: 16px !important;
  padding: 8px !important;
  overflow: hidden;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15) !important;
}

.reset-confirm-dialog .el-message-box__header {
  padding: 20px 20px 10px !important;
  background: linear-gradient(135deg, #fef3f2 0%, #fff 100%);
  border-bottom: 1px solid #fee2e2;
}

.reset-confirm-dialog .el-message-box__title {
  font-weight: 700 !important;
  font-size: 18px !important;
  color: #334155 !important;
}

.reset-confirm-dialog .el-message-box__content {
  padding: 20px !important;
}

.reset-confirm-dialog .el-message-box__message {
  color: #64748b !important;
  font-size: 14px !important;
  line-height: 1.7 !important;
  white-space: pre-line !important;
}

.reset-confirm-dialog .el-message-box__btns {
  padding: 15px 20px 20px !important;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.reset-confirm-dialog .el-message-box__btns button {
  border-radius: 10px !important;
  padding: 10px 24px !important;
  font-weight: 600 !important;
  transition: all 0.2s !important;
}

.reset-confirm-dialog .el-button--primary {
  background: linear-gradient(135deg, #ef4444, #dc2626) !important;
  border: none !important;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3) !important;
}

.reset-confirm-dialog .el-button--primary:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.4) !important;
}

.reset-confirm-dialog .el-button--default {
  border: 1px solid #e2e8f0 !important;
  color: #64748b !important;
  background: #fff !important;
}

.reset-confirm-dialog .el-button--default:hover {
  border-color: #cbd5e1 !important;
  background: #f8fafc !important;
  color: #334155 !important;
}

.reset-confirm-dialog .el-message-box__status {
  font-size: 24px !important;
}

/* 黑夜模式适配 */
[data-theme="dark"] .reset-confirm-dialog {
  background: #1e293b !important;
  border-color: #334155 !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5) !important;
}

[data-theme="dark"] .reset-confirm-dialog .el-message-box__header {
  background: linear-gradient(
    135deg,
    rgba(239, 68, 68, 0.1) 0%,
    transparent 100%
  );
  border-bottom-color: rgba(239, 68, 68, 0.2);
}

[data-theme="dark"] .reset-confirm-dialog .el-message-box__title {
  color: #f1f5f9 !important;
}

[data-theme="dark"] .reset-confirm-dialog .el-message-box__content {
  background: transparent;
}

[data-theme="dark"] .reset-confirm-dialog .el-message-box__message {
  color: #94a3b8 !important;
}

[data-theme="dark"] .reset-confirm-dialog .el-button--primary {
  background: linear-gradient(135deg, #ef4444, #dc2626) !important;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4) !important;
}

[data-theme="dark"] .reset-confirm-dialog .el-button--primary:hover {
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.5) !important;
}

[data-theme="dark"] .reset-confirm-dialog .el-button--default {
  background: #334155 !important;
  border-color: #475569 !important;
  color: #94a3b8 !important;
}

[data-theme="dark"] .reset-confirm-dialog .el-button--default:hover {
  background: #475569 !important;
  border-color: #64748b !important;
  color: #f1f5f9 !important;
}
</style>
