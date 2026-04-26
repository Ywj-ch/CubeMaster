<template>
  <div class="cube-free-page">
    <!-- 顶部计时器 -->
    <div class="timer-container-hybrid">
      <div class="timer-label-small">用时</div>

      <div class="flip-clock-row">
        <!-- 分钟 (翻页) -->
        <DigitRoll :val="minStr" />

        <span class="colon">:</span>

        <!-- 秒 (翻页) -->
        <DigitRoll :val="secStr" />

        <span class="dot">.</span>

        <!-- 毫秒 (数字跳动) -->
        <div class="ms-card">
          {{ msStr }}
        </div>
      </div>
    </div>

    <!-- 帮助按钮 -->
    <div class="hint-wrapper">
      <div class="hint" data-position="1" @click="showHelp = true">
        <span class="hint-dot">?</span>
        <div class="hint-content">
          <p>操作指南</p>
        </div>
      </div>
    </div>

    <!-- 头部区域：标题 -->
    <div class="header-section">
      <h2 class="mode-title gradient-text">自由练习</h2>
    </div>

    <!-- 状态指示器 -->
    <div class="status-badge" :class="statusClass">
      <span class="status-dot"></span>
      <span class="status-text">{{ statusText }}</span>
    </div>

    <!-- 主显示区 -->
    <div class="main-display-area">
      <div class="cube-container-box">
        <!-- 3D 视图组件 -->
        <Cube3DView
          ref="cubeRef"
          :cubeState="cubeState"
          :interactive="isGameStarted && !isAutoOperating && !isMoving"
          :enableControls="true"
          :customization="config"
          @move="handle3DMove"
        />
      </div>
    </div>

    <!-- 底部控制栏 -->
    <div class="bottom-controls">
      <div class="action-buttons">
        <button
          class="start-challenge-btn"
          v-if="!isGameStarted"
          @click="startChallenge"
        >
          <svg
            class="cube-icon"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            width="32"
            height="32"
          >
            <path
              fill="currentColor"
              d="M12,2L4.5,6.3V15.7L12,20L19.5,15.7V6.3L12,2M12,4.1L17.5,7.3L12,10.5L6.5,7.3L12,4.1M6.5,17.4V9.6L11,12.2V20L6.5,17.4M13,20V12.2L17.5,9.6V17.4L13,20Z"
            />
          </svg>
          <span class="go-text">开始！</span>
          <span class="start-text">开始游戏</span>
        </button>

        <button
          class="btn-secondary scramble-btn"
          @click="scrambleWithAnimation"
          :disabled="isAutoOperating"
        >
          <el-icon class="refresh-icon"><Refresh /></el-icon>
          <span>随机打乱</span>
        </button>

        <button class="btn-secondary reset-btn" @click="resetAll">
          <el-icon><RefreshLeft /></el-icon>
          <span>重置</span>
        </button>
      </div>

      <div class="sequence-display">
        <div class="seq-label">序列</div>
        <el-scrollbar ref="scrollRef">
          <div class="seq-items">
            <transition-group name="slide">
              <span v-for="(move, idx) in history" :key="idx" class="seq-tag">
                {{ move }}
              </span>
            </transition-group>
            <div v-if="history.length === 0" class="seq-empty">
              {{
                isGameStarted ? "请开始你的操作..." : '点击"开始游戏"进行计时'
              }}
            </div>
          </div>
        </el-scrollbar>
      </div>
    </div>

    <!-- 统计面板 -->
    <StatsPanel />

    <!-- 操作指南弹窗 -->
    <el-dialog
      v-model="showHelp"
      title="操作指南"
      width="450px"
      center
      align-center
      class="glass-dialog"
    >
      <div class="help-content">
        <div class="help-section">
          <h4>🖱️ 鼠标操作</h4>
          <p>• <strong>左键拖拽魔方层</strong>：旋转对应层</p>
          <p>• <strong>空白处拖拽</strong>：旋转视角</p>
          <p>• <strong>滚轮</strong>：缩放视角</p>
        </div>
        <div class="help-section">
          <h4>⌨️ 键盘快捷键</h4>
          <div class="key-map-grid">
            <div class="key-item"><span class="key">U</span> 顶层 (Up)</div>
            <div class="key-item"><span class="key">D</span> 底层 (Down)</div>
            <div class="key-item"><span class="key">L</span> 左层 (Left)</div>
            <div class="key-item"><span class="key">R</span> 右层 (Right)</div>
            <div class="key-item"><span class="key">F</span> 前层 (Front)</div>
            <div class="key-item"><span class="key">B</span> 后层 (Back)</div>
          </div>
          <p class="tip-text">
            注：按住 <span class="key small">Shift</span> + 字母可进行逆时针旋转
          </p>
        </div>
      </div>
    </el-dialog>

    <!-- 胜利结算卡片 -->
    <transition name="fade">
      <div v-if="isVictory" class="victory-overlay">
        <div class="victory-card">
          <div class="victory-icon">🏆</div>
          <h3>恭喜还原！</h3>
          <div class="stats-grid">
            <div class="stat-item">
              <span class="label">最终用时</span>
              <span class="value time">{{ finalTimeStr }}</span>
            </div>
            <div class="stat-item">
              <span class="label">总步数</span>
              <span class="value">{{ history.length }}</span>
            </div>
            <div class="stat-item">
              <span class="label">TPS (步数/秒)</span>
              <span class="value">{{ tps }}</span>
            </div>
          </div>
          <div class="victory-actions">
            <el-button
              type="primary"
              size="large"
              @click="scrambleWithAnimation"
              >再来一局</el-button
            >
            <el-button size="large" @click="isVictory = false">完成</el-button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from "vue";
import Cube3DView from "../components/Cube3DView.vue";
import StatsPanel from "../components/StatsPanel.vue";
import { createCubeFromJson } from "../utils/cubeState";
import { applyMove, invertMove } from "../utils/cubeMoves";
import { useRecords } from "../composables/useRecords.js";
import {
  Timer,
  Refresh,
  RefreshLeft,
  VideoPlay,
  QuestionFilled,
} from "@element-plus/icons-vue";
import confetti from "canvas-confetti";
import DigitRoll from "../components/DigitRoll.vue";
import { useCubeCustomization } from "../composables/useCubeCustomization.js";

const { config } = useCubeCustomization();

const cubeState = ref(createCubeFromJson());
const cubeRef = ref(null);
const history = ref([]);
const isAutoOperating = ref(false);
const isMoving = ref(false);
const isGameStarted = ref(false);
const scrollRef = ref(null);

const currentTime = ref(0);
const timerId = ref(null);
const isTimerRunning = ref(false);
let startTime = 0;

const showHelp = ref(false);
const isVictory = ref(false);
const finalTimeStr = ref("00:00.00");
const tps = ref("0.00");
const scrambleSequence = ref("");

const { addRecord } = useRecords();

// --- 状态计算属性 ---
const statusText = computed(() => {
  if (isAutoOperating.value) return "正在打乱...";
  if (isGameStarted.value) return "挑战进行中";
  return "准备就绪";
});

const statusClass = computed(() => {
  if (isAutoOperating.value) return "status-busy";
  if (isGameStarted.value) return "status-active";
  return "status-ready";
});

// --- 时间计算属性 ---
const timeDisplay = computed(() => {
  return formatTime(currentTime.value);
});
const minStr = computed(() =>
  Math.floor(currentTime.value / 60000)
    .toString()
    .padStart(2, "0"),
);
const secStr = computed(() =>
  Math.floor((currentTime.value % 60000) / 1000)
    .toString()
    .padStart(2, "0"),
);
const msStr = computed(() =>
  Math.floor((currentTime.value % 1000) / 10)
    .toString()
    .padStart(2, "0"),
);

function formatTime(ms) {
  const m = Math.floor(ms / 60000)
    .toString()
    .padStart(2, "0");
  const s = Math.floor((ms % 60000) / 1000)
    .toString()
    .padStart(2, "0");
  const msec = Math.floor((ms % 1000) / 10)
    .toString()
    .padStart(2, "0");
  return `${m}:${s}.${msec}`;
}

function startChallenge() {
  if (isAutoOperating.value) return;
  isGameStarted.value = true;
  isVictory.value = false;
  history.value = [];
  currentTime.value = 0;
  startTimer();
}

function startTimer() {
  if (isTimerRunning.value) return;
  isTimerRunning.value = true;
  startTime = Date.now() - (Number(currentTime.value) || 0);
  timerId.value = setInterval(() => {
    currentTime.value = Date.now() - startTime;
  }, 10);
}

function stopTimer() {
  isTimerRunning.value = false;
  if (timerId.value) clearInterval(timerId.value);
}

function checkSolved() {
  if (!isGameStarted.value || history.value.length === 0) return;
  const faces = cubeState.value.faces;
  const faceKeys = ["U", "D", "L", "R", "F", "B"];
  for (const key of faceKeys) {
    let faceData = faces[key];
    if (Array.isArray(faceData[0])) {
      faceData = faceData.flat();
    }
    const centerColor = faceData[4];
    const isFaceSolved = faceData.every((c) => c === centerColor);
    if (!isFaceSolved) return;
  }
  handleVictory();
}

function handleVictory() {
  stopTimer();
  isGameStarted.value = false;
  finalTimeStr.value = timeDisplay.value;
  const seconds = currentTime.value / 1000;
  tps.value =
    seconds > 0 ? (history.value.length / seconds).toFixed(2) : "0.00";
  isVictory.value = true;
  triggerConfetti();

  // Save record to localStorage
  addRecord({
    time: currentTime.value,
    scramble: scrambleSequence.value || "",
    moves: history.value.length,
    tps: parseFloat(tps.value),
  });
}

function triggerConfetti() {
  const count = 200;
  const defaults = { origin: { y: 0.7 }, zIndex: 3000 };
  function fire(particleRatio, opts) {
    confetti(
      Object.assign({}, defaults, opts, {
        particleCount: Math.floor(count * particleRatio),
      }),
    );
  }
  fire(0.25, { spread: 26, startVelocity: 55 });
  fire(0.2, { spread: 60 });
  fire(0.35, { spread: 100, decay: 0.91, scalar: 0.8 });
  fire(0.1, { spread: 120, startVelocity: 25, decay: 0.92, scalar: 1.2 });
  fire(0.1, { spread: 120, startVelocity: 45 });
}

function handle3DMove(move) {
  executeMove(move);
}

async function executeMove(move, force = false) {
  if (isAutoOperating.value && !force) return;
  if (!isGameStarted.value && !force) return;
  if (isMoving.value) return;

  if (cubeRef.value) {
    isMoving.value = true;
    cubeRef.value.playMove(move);
    applyMove(cubeState.value, move);
    if (!force) {
      history.value.push(move);
      nextTick(() => {
        const inner = scrollRef.value?.$el.querySelector(".el-scrollbar__wrap");
        if (inner) inner.scrollLeft = inner.scrollWidth;
      });
    }
    setTimeout(() => {
      isMoving.value = false;
      if (!force) checkSolved();
    }, 320);
  }
}

async function scrambleWithAnimation() {
  if (isAutoOperating.value) return;
  isVictory.value = false;
  isGameStarted.value = false;
  stopTimer();
  currentTime.value = 0;
  history.value = [];
  scrambleSequence.value = "";
  isAutoOperating.value = true;
  const moves = [
    "R",
    "L",
    "U",
    "D",
    "F",
    "B",
    "R'",
    "L'",
    "U'",
    "D'",
    "F'",
    "B'",
  ];
  const scrambleMoves = [];
  for (let i = 0; i < 2; i++) {
    const randomMove = moves[Math.floor(Math.random() * moves.length)];
    scrambleMoves.push(randomMove);
    if (cubeRef.value) {
      await cubeRef.value.playMove(randomMove);
      applyMove(cubeState.value, randomMove);
      await new Promise((r) => setTimeout(r, 150));
    }
  }
  scrambleSequence.value = scrambleMoves.join(" ");
  isAutoOperating.value = false;
}

function resetAll() {
  stopTimer();
  isGameStarted.value = false;
  isMoving.value = false;
  isVictory.value = false;
  currentTime.value = 0;
  history.value = [];
  cubeState.value = createCubeFromJson();
  if (cubeRef.value) {
    cubeRef.value.renderCubies(cubeState.value.cubies);
    cubeRef.value.resetView();
  }
}

function handleKeydown(e) {
  if (isAutoOperating.value || !isGameStarted.value || isMoving.value) return;
  const key = e.key.toUpperCase();
  const shift = e.shiftKey;
  const validKeys = ["U", "D", "L", "R", "F", "B"];
  if (validKeys.includes(key)) {
    executeMove(key + (shift ? "'" : ""));
  }
}

onMounted(() => {
  window.addEventListener("keydown", handleKeydown);
  document.body.style.overflow = "hidden";
});

onUnmounted(() => {
  window.removeEventListener("keydown", handleKeydown);
  document.body.style.overflow = "";
  stopTimer();
});
</script>

<style scoped>
.cube-free-page {
  position: relative;
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  background-color: #f8fafc;
  padding: 12px 60px;
  box-sizing: border-box;
  overflow: hidden;
}

/* 计时器 */
.timer-container-hybrid {
  position: fixed;
  top: 100px;
  right: 60px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  z-index: 50;
}

.timer-label-small {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  color: #94a3b8;
  margin-bottom: 8px;
  margin-right: 4px;
}

.flip-clock-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.colon,
.dot {
  font-size: 40px;
  font-weight: 700;
  color: #cbd5e1;
  margin-top: -8px;
}

/* 毫秒卡片：蓝色高亮，不翻页 */
.ms-card {
  width: 50px;
  height: 70px;
  background: #2563eb;
  border-radius: 6px;
  color: #fff;
  font-size: 32px;
  font-family: "JetBrains Mono", monospace;
  font-weight: 700;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 10px 20px rgba(37, 99, 235, 0.3);
}

/* 头部标题区 */
.header-section {
  margin-top: 70px;
  margin-bottom: 100px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: relative;
  z-index: 100;
}

.mode-title {
  font-size: 36px;
  font-weight: 800;
  margin: 0;
  letter-spacing: -1px;
  /* 渐变标题 */
  background: linear-gradient(135deg, #1e293b 0%, #3b82f6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 状态胶囊 */
.status-badge {
  position: absolute;
  top: 120px;
  left: 60px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  width: fit-content;
  transition: all 0.3s ease;
  z-index: 150;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

/* 状态变体 */
.status-ready {
  background: #f1f5f9;
  color: #64748b;
  border: 1px solid #e2e8f0;
}
.status-ready .status-dot {
  background: #94a3b8;
}

.status-active {
  background: #ecfdf5;
  color: #059669;
  border: 1px solid #a7f3d0;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.1);
}
.status-active .status-dot {
  background: #10b981;
  box-shadow: 0 0 8px #10b981;
  animation: pulse-green 2s infinite;
}

.status-busy {
  background: #fff7ed;
  color: #ea580c;
  border: 1px solid #fed7aa;
}
.status-busy .status-dot {
  background: #f97316;
  animation: spin 1s linear infinite; /* 让点转起来 */
}

@keyframes pulse-green {
  0% {
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4);
  }
  70% {
    box-shadow: 0 0 0 6px rgba(16, 185, 129, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
  }
}
@keyframes spin {
  from {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
  to {
    opacity: 1;
  }
}

/* 主显示区 */
.main-display-area {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 0;
  transform: translateY(0);
}

.cube-container-box {
  width: 58vh;
  height: 58vh;
  max-width: 720px;
  max-height: 720px;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 40px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.04);
  position: relative;
}

/* 底部控制栏 */
.bottom-controls {
  padding: 100px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 25px;
}

.action-buttons {
  display: flex;
  gap: 24px;
  align-items: center;
}

.sequence-display {
  width: 100%;
  max-width: 1200px;
  background: white;
  padding: 20px 30px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}
.seq-label {
  font-weight: 800;
  color: #94a3b8;
  margin-right: 25px;
  font-size: 12px;
}
.seq-items {
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 44px;
}
.seq-tag {
  background: #f1f5f9;
  color: #3b82f6;
  padding: 10px 18px;
  border-radius: 12px;
  font-family: "JetBrains Mono", monospace;
  font-weight: 700;
}
.seq-empty {
  color: #cbd5e1;
  font-size: 14px;
}

/* === 帮助按钮 - 现代化设计 === */
.hint-wrapper {
  position: absolute;
  top: 120px;
  left: 160px;
  z-index: 9999;
}

.hint {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

/* 扩散光圈 - 已移除 */
.hint-radius {
  display: none;
}

/* 按钮圆点 - 32px */
.hint-dot {
  z-index: 3;
  width: 32px;
  height: 32px;
  border: 2px solid rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  font-size: 16px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  transform: scale(0.95);
  transition: all 0.3s ease;
  box-shadow: 0 3px 10px rgba(59, 130, 246, 0.35);
}

.hint:hover .hint-dot {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: scale(1);
  box-shadow: 0 5px 15px rgba(59, 130, 246, 0.45);
}

/* Tooltip内容 - 仅保留文字 */
.hint[data-position="1"] .hint-content {
  position: absolute;
  top: -28px;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  pointer-events: none;
}

/* 文字样式 */
.hint-content p {
  margin: 0;
  padding: 0;
  color: #64748b;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  opacity: 0;
  transform: translateY(5px);
  transition: all 0.25s ease;
}

/* Hover状态 - 仅显示文字 */
.hint:hover .hint-content {
  opacity: 1;
  visibility: visible;
}

.hint:hover .hint-content p {
  opacity: 1;
  transform: translateY(0);
}

/* 暗色模式适配 */
[data-theme="dark"] .hint-dot {
  background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
  border-color: rgba(255, 255, 255, 0.7);
  box-shadow: 0 3px 10px rgba(96, 165, 250, 0.35);
}

[data-theme="dark"] .hint:hover .hint-dot {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  box-shadow: 0 5px 15px rgba(96, 165, 250, 0.45);
}

[data-theme="dark"] .hint-radius {
  background-color: rgba(96, 165, 250, 0.2);
}

[data-theme="dark"] .hint-content p {
  color: #94a3b8;
}

/* === 弹窗深度美化 === */
:deep(.el-dialog) {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.5);
  padding: 20px;
}
:deep(.el-dialog__header) {
  margin-right: 0;
  text-align: center;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}
:deep(.el-dialog__title) {
  font-weight: 800;
  color: #1e293b;
  font-size: 1.2rem;
}

.help-section h4 {
  color: #3b82f6;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 15px;
}

/* 键盘按键样式 */
.key {
  display: inline-block;
  min-width: 24px;
  padding: 4px 8px;
  margin-right: 8px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-bottom: 3px solid #cbd5e1;
  border-radius: 6px;
  color: #1e293b;
  font-family: "JetBrains Mono", monospace;
  font-weight: 700;
  font-size: 12px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.1s;
}
.key.small {
  font-size: 10px;
  padding: 4px 6px;
}
.key-item:hover .key {
  transform: translateY(2px);
  border-bottom-width: 1px;
  background: #f8fafc;
}

/* 胜利结算 */
.victory-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(5px);
  z-index: 2000;
  display: flex;
  justify-content: center;
  align-items: center;
}
.victory-card {
  background: white;
  padding: 40px 60px;
  border-radius: 30px;
  text-align: center;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
  animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.victory-icon {
  font-size: 60px;
  margin-bottom: 10px;
}
.victory-card h3 {
  font-size: 28px;
  margin: 0 0 30px 0;
  color: #1e293b;
}
.stats-grid {
  display: flex;
  gap: 40px;
  margin-bottom: 40px;
}
.stat-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.stat-item .label {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
}
.stat-item .value {
  font-size: 24px;
  font-weight: 800;
  color: #3b82f6;
  font-family: "JetBrains Mono", monospace;
}
.stat-item .value.time {
  color: #10b981;
}
.victory-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
}

@keyframes popIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* === 开始游戏按钮 === */
.start-challenge-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 0 25px;
  height: 56px; /* 与旁边按钮对齐 */
  color: white;
  text-transform: uppercase;
  cursor: pointer;
  border: none; /* 去掉黑边，改用无边框设计 */
  letter-spacing: 1px;
  font-weight: 800;
  font-size: 16px;
  background-color: #10b981; /* 充满活力的绿色 */
  border-radius: 16px; /* 配合你页面的大圆角风格 */
  position: relative;
  overflow: hidden;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 10px 20px rgba(16, 185, 129, 0.3);
}

.start-challenge-btn:active {
  transform: scale(0.95);
}

.cube-icon {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 2;
  color: rgba(255, 255, 255, 0.9);
}

.start-text {
  transition: all 0.5s ease;
  transition-delay: 100ms;
}

/* --- 悬浮动画逻辑 --- */
.start-challenge-btn:hover {
  background-color: #059669; /* 悬浮时颜色加深 */
  box-shadow: 0 15px 30px rgba(16, 185, 129, 0.4);
}

/* 图标放大并位移到背景 */
.start-challenge-btn:hover .cube-icon {
  transform: scale(4) translate(40%, -10%);
  opacity: 0.2; /* 变淡，作为背景装饰 */
}

.go-text {
  position: absolute;
  left: 0;
  transform: translateX(-100%);
  transition: all 0.5s ease;
  z-index: 2;
  font-size: 20px;
}

/* 文字切换 */
.start-challenge-btn:hover .go-text {
  transform: translateX(35px); /* 移入视图 */
  transition-delay: 200ms;
}

.start-challenge-btn:hover .start-text {
  transform: translateX(200%); /* 移出视图 */
  opacity: 0;
}

/* === 随即打乱和重置按钮 === */
.btn-secondary {
  height: 56px; /* 必须与主按钮高度一致 */
  padding: 0 28px;
  border-radius: 16px; /* 统一的圆角语言 */
  background: #ffffff;
  color: #64748b; /* 默认灰色，不抢戏 */
  font-size: 15px;
  font-weight: 700;
  border: 1px solid #e2e8f0;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
}

/* 悬浮通用反馈 */
.btn-secondary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
}

/* --- 针对“随机打乱按钮”的特化 --- */
.scramble-btn:hover:not(:disabled) {
  color: #2563eb; /* 悬浮变蓝，呼应主题 */
  border-color: #cbd5e1;
}

/* 图标旋转效果 */
.scramble-btn:hover .refresh-icon {
  transform: rotate(180deg);
  transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* --- 针对“重置”按钮的特化 --- */
.reset-btn:hover {
  color: #ef4444 !important; /* 悬浮变红，警示危险 */
  background-color: #fef2f2 !important;
  border-color: #fecaca !important;
}

/* 禁用状态处理 */
.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  filter: grayscale(1);
}

/* ==================== Dark Mode Styles ==================== */
/* 页面背景 */
[data-theme="dark"] .cube-free-page {
  background-color: var(--dm-bg-page);
}

/* 弹窗暗色模式适配 - 参考Learning.vue实现 */
html[data-theme="dark"] .cube-free-page :deep(.el-dialog) {
  background: #1e293b !important;
  border: 1px solid #334155 !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
  outline: none !important;
}

html[data-theme="dark"] .cube-free-page :deep(.el-dialog__header) {
  border-bottom: 1px solid #334155 !important;
  background: #1e293b !important;
}

html[data-theme="dark"] .cube-free-page :deep(.el-dialog__title) {
  color: #e2e8f0;
}

html[data-theme="dark"] .cube-free-page :deep(.el-dialog__body) {
  background: #1e293b !important;
}

[data-theme="dark"] .help-content {
  color: #e2e8f0;
}

[data-theme="dark"] .help-section h4 {
  color: #60a5fa;
}

[data-theme="dark"] .key-map-grid {
  background: rgba(30, 41, 59, 0.8);
  border-radius: 8px;
  padding: 12px;
}

[data-theme="dark"] .key-item {
  color: #cbd5e1;
}

[data-theme="dark"] .key {
  background: #334155;
  border-color: #475569;
  border-bottom-color: #64748b;
  color: #e2e8f0;
}

[data-theme="dark"] .key-item:hover .key {
  background: #1e293b;
  border-bottom-color: #475569;
}

[data-theme="dark"] .tip-text {
  color: #94a3b8;
}

[data-theme="dark"] .help-section p {
  color: #cbd5e1;
}

/* 计时器 */
[data-theme="dark"] .timer-label-small {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .colon,
[data-theme="dark"] .dot {
  color: var(--dm-border-light);
}

[data-theme="dark"] .ms-card {
  background: var(--dm-accent);
  box-shadow: 0 10px 20px rgba(96, 165, 250, 0.4);
}

/* 头部区域 */
[data-theme="dark"] .header-section {
  background: transparent;
}

[data-theme="dark"] .mode-title {
  background: linear-gradient(
    135deg,
    var(--dm-text-primary) 0%,
    var(--dm-accent) 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 状态胶囊 */
[data-theme="dark"] .status-badge {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .status-ready {
  background: var(--dm-bg-card);
  color: var(--dm-text-muted);
  border-color: var(--dm-border);
}

[data-theme="dark"] .status-ready .status-dot {
  background: var(--dm-text-muted);
}

[data-theme="dark"] .status-active {
  background: rgba(52, 211, 153, 0.15);
  color: #34d399;
  border-color: rgba(52, 211, 153, 0.3);
}

[data-theme="dark"] .status-active .status-dot {
  background: #34d399;
  box-shadow: 0 0 8px #34d399;
}

[data-theme="dark"] .status-busy {
  background: rgba(251, 146, 60, 0.15);
  color: #fb923c;
  border-color: rgba(251, 146, 60, 0.3);
}

[data-theme="dark"] .status-busy .status-dot {
  background: #fb923c;
}

/* 主显示区 */
[data-theme="dark"] .main-display-area {
  background: transparent;
}

[data-theme="dark"] .cube-container-box {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

/* 底部控制栏 */
[data-theme="dark"] .bottom-controls {
  background: transparent;
}

/* 开始游戏按钮 */
[data-theme="dark"] .start-challenge-btn {
  background-color: #10b981;
}

[data-theme="dark"] .start-challenge-btn:hover {
  background-color: #059669;
}

/* 序列显示 */
[data-theme="dark"] .sequence-display {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .seq-label {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .seq-tag {
  background: var(--dm-bg-hover);
  color: var(--dm-accent);
}

[data-theme="dark"] .seq-empty {
  color: var(--dm-text-muted);
}

/* 提示信息 */
[data-theme="dark"] .hint-text {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .hint-text .highlight {
  color: var(--dm-accent);
}

/* 胜利弹窗暗色模式适配 */
[data-theme="dark"] .victory-overlay {
  background: rgba(15, 23, 42, 0.7);
}

[data-theme="dark"] .victory-card {
  background: var(--dm-bg-card);
  border: 1px solid var(--dm-border);
  box-shadow: var(--dm-shadow-xl);
}

[data-theme="dark"] .victory-card h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .stat-item .label {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .stat-item .value {
  color: var(--dm-accent);
}

[data-theme="dark"] .stat-item .value.time {
  color: var(--dm-accent-success);
}
</style>
