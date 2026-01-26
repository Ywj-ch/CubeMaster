<template>
  <div class="cube-free-page">
    <!-- 顶部计时器 -->
    <div class="timer-badge-new">
      <div class="timer-header">
        <el-icon><Timer /></el-icon>
        <span class="timer-label">ELAPSED</span>
      </div>
      <div class="timer-num">{{ timeDisplay }}</div>
    </div>

    <!-- 帮助按钮 (新增) -->
    <div class="help-btn-wrapper">
      <el-button circle @click="showHelp = true" :icon="QuestionFilled" size="large" />
    </div>

    <div class="header-section">
      <h2 class="mode-title">自由探索</h2>
      <div class="status-indicator">
        <span class="dot" :class="{ 'is-active': isGameStarted && !isAutoOperating }"></span>
        {{ isAutoOperating ? '正在打乱...' : (isGameStarted ? '挑战进行中' : '准备就绪') }}
      </div>
    </div>

    <div class="main-display-area">
      <div class="cube-container-box">
        <!-- 3D 视图组件 -->
        <Cube3DView
          ref="cubeRef"
          :cubeState="cubeState"
          :interactive="isGameStarted && !isAutoOperating && !isMoving"
          :enableControls="true"
          @move="handle3DMove"
        />
      </div>
    </div>

    <div class="bottom-controls">
      <div class="action-buttons">
        <el-button
          v-if="!isGameStarted"
          type="success"
          size="large"
          @click="startChallenge"
          :disabled="isAutoOperating"
          :icon="VideoPlay"
          class="ctrl-btn start-btn"
        >
          开始挑战
        </el-button>

        <el-button
          type="primary"
          size="large"
          @click="scrambleWithAnimation"
          :disabled="isAutoOperating"
          :icon="Refresh"
          class="ctrl-btn"
        >
          随机打乱
        </el-button>

        <el-button
          size="large"
          @click="resetAll"
          :icon="RefreshLeft"
          class="ctrl-btn"
        >
          重置
        </el-button>
      </div>

      <div class="sequence-display">
        <div class="seq-label">SEQUENCE</div>
        <el-scrollbar ref="scrollRef">
          <div class="seq-items">
            <transition-group name="slide">
              <span v-for="(move, idx) in history" :key="idx" class="seq-tag">
                {{ move }}
              </span>
            </transition-group>
            <div v-if="history.length === 0" class="seq-empty">
              {{ isGameStarted ? '请开始你的操作...' : '点击“开始挑战”进行计时' }}
            </div>
          </div>
        </el-scrollbar>
      </div>
    </div>

    <!-- 操作指南弹窗 -->
    <el-dialog v-model="showHelp" title="操作指南" width="400px" center align-center>
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
          <p class="tip-text">注：按住 <code>Shift</code> + 字母可进行逆时针旋转</p>
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
              <span class="label">TPS (手速)</span>
              <span class="value">{{ tps }}</span>
            </div>
          </div>
          <div class="victory-actions">
            <el-button type="primary" size="large" @click="scrambleWithAnimation">再来一局</el-button>
            <el-button size="large" @click="isVictory = false">关闭</el-button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';
import Cube3DView from '../components/Cube3DView.vue';
import { createCubeFromJson } from '../utils/cubeState';
import { applyMove, invertMove } from '../utils/cubeMoves';
import { Timer, Refresh, RefreshLeft, VideoPlay, QuestionFilled } from '@element-plus/icons-vue';
import confetti from 'canvas-confetti'; // 引入撒花库

const cubeState = ref(createCubeFromJson());
const cubeRef = ref(null);
const history = ref([]);
const isAutoOperating = ref(false); // 打乱模式锁定
const isMoving = ref(false);        // 单步动画锁定
const isGameStarted = ref(false);   // 游戏开始状态
const scrollRef = ref(null);

const currentTime = ref(0);
const timerId = ref(null);
const isTimerRunning = ref(false);
let startTime = 0;

// 新增状态
const showHelp = ref(false);
const isVictory = ref(false);
const finalTimeStr = ref("00:00.00");
const tps = ref("0.00");

const timeDisplay = computed(() => {
  return formatTime(currentTime.value);
});

function formatTime(ms) {
  const m = Math.floor(ms / 60000).toString().padStart(2, '0');
  const s = Math.floor((ms % 60000) / 1000).toString().padStart(2, '0');
  const msec = Math.floor((ms % 1000) / 10).toString().padStart(2, '0');
  return `${m}:${s}.${msec}`;
}

// 开始挑战
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

/**
 * 检查魔方是否还原
 */
function checkSolved() {
  if (!isGameStarted.value || history.value.length === 0) return;

  const faces = cubeState.value.faces;
  const faceKeys = ['U', 'D', 'L', 'R', 'F', 'B'];

  for (const key of faceKeys) {
    let faceData = faces[key];

    if (Array.isArray(faceData[0])) {
      faceData = faceData.flat();
    }

    const centerColor = faceData[4];

    const isFaceSolved = faceData.every(c => c === centerColor);

    if (!isFaceSolved) return;
  }

  handleVictory();
}

function handleVictory() {
  stopTimer();
  isGameStarted.value = false;
  finalTimeStr.value = timeDisplay.value;

  const seconds = currentTime.value / 1000;
  tps.value = seconds > 0 ? (history.value.length / seconds).toFixed(2) : "0.00";

  isVictory.value = true;

  // --- 触发撒花特效 ---
  triggerConfetti();
}

// 撒花配置函数
function triggerConfetti() {
  const count = 200;
  const defaults = {
    origin: { y: 0.7 },
    zIndex: 3000
  };

  function fire(particleRatio, opts) {
    confetti(Object.assign({}, defaults, opts, {
      particleCount: Math.floor(count * particleRatio)
    }));
  }

  fire(0.25, { spread: 26, startVelocity: 55, });
  fire(0.2, { spread: 60, });
  fire(0.35, { spread: 100, decay: 0.91, scalar: 0.8 });
  fire(0.1, { spread: 120, startVelocity: 25, decay: 0.92, scalar: 1.2 });
  fire(0.1, { spread: 120, startVelocity: 45, });
}

// 处理 3D 组件的转动事件
function handle3DMove(move) {
  executeMove(move);
}

/**
 * 执行转动
 */
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
        const inner = scrollRef.value?.$el.querySelector('.el-scrollbar__wrap');
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
  isAutoOperating.value = true;

  const moves = ["R", "L", "U", "D", "F", "B", "R'", "L'", "U'", "D'", "F'", "B'"];
  for (let i = 0; i < 2; i++) {
    const randomMove = moves[Math.floor(Math.random() * moves.length)];
    if (cubeRef.value) {
      cubeRef.value.playMove(randomMove);
      applyMove(cubeState.value, randomMove);
      await new Promise(r => setTimeout(r, 320));
    }
  }
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
  const validKeys = ['U', 'D', 'L', 'R', 'F', 'B'];
  if (validKeys.includes(key)) {
    executeMove(key + (shift ? "'" : ""));
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown);
  document.body.style.overflow = 'hidden';
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown);
  document.body.style.overflow = '';
  stopTimer();
});
</script>

<style scoped>
/* 保持原有布局样式 */
.cube-free-page {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  background-color: #f8fafc;
  padding: 12px 60px;
  box-sizing: border-box;
  overflow: hidden;
}

.timer-badge-new {
  position: absolute;
  top: 120px;
  right: 60px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  padding: 15px 35px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.5);
  z-index: 100;
}
.timer-header {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #1969d9;
  margin-bottom: 5px;
}
.timer-label { font-size: 11px; letter-spacing: 1.5px; font-weight: 600; }
.timer-num { font-size: 36px; font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #1e293b; }

/* 帮助按钮样式 */
.help-btn-wrapper {
  position: absolute;
  top: 126px;
  left: 215px;
  z-index: 100;
}

.header-section { margin-top: 20px; }
.mode-title { font-size: 32px; color: #1e293b; font-weight: 800; margin-bottom: 10px; }
.status-indicator { display: flex; align-items: center; gap: 8px; font-size: 14px; color: #64748b; }
.dot { width: 8px; height: 8px; background: #cbd5e1; border-radius: 50%; }
.dot.is-active { background: #10b981; box-shadow: 0 0 8px #10b981; }

.main-display-area {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 0;
  transform: translateY(-20px);
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

.bottom-controls {
  padding: 100px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 25px;
}

.action-buttons { display: flex; gap: 24px; }
.ctrl-btn { padding: 25px 40px; font-size: 16px; border-radius: 15px; }

.start-btn {
  background: #10b981;
  border-color: #10b981;
  box-shadow: 0 4px 14px 0 rgba(16, 185, 129, 0.39);
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
.seq-label { font-weight: 800; color: #94a3b8; margin-right: 25px; font-size: 12px; }
.seq-items { display: flex; align-items: center; gap: 10px; min-height: 44px; }
.seq-tag {
  background: #f1f5f9;
  color: #3b82f6;
  padding: 10px 18px;
  border-radius: 12px;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
}
.seq-empty { color: #cbd5e1; font-size: 14px; }

/* 帮助弹窗样式 */
.help-content { padding: 0 10px; }
.help-section { margin-bottom: 20px; }
.help-section h4 { margin: 0 0 10px 0; color: #1e293b; }
.help-section p { margin: 5px 0; color: #64748b; font-size: 14px; }
.key-map-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-bottom: 10px;
}
.key-item { font-size: 14px; color: #475569; }
.key {
  display: inline-block;
  padding: 2px 8px;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  font-family: monospace;
  font-weight: 700;
  margin-right: 5px;
}
.tip-text { font-size: 12px !important; color: #94a3b8 !important; }

/* 胜利结算遮罩 */
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
  box-shadow: 0 20px 50px rgba(0,0,0,0.2);
  animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.victory-icon { font-size: 60px; margin-bottom: 10px; }
.victory-card h3 { font-size: 28px; margin: 0 0 30px 0; color: #1e293b; }
.stats-grid {
  display: flex;
  gap: 40px;
  margin-bottom: 40px;
}
.stat-item { display: flex; flex-direction: column; gap: 5px; }
.stat-item .label { font-size: 12px; color: #94a3b8; font-weight: 600; }
.stat-item .value { font-size: 24px; font-weight: 800; color: #3b82f6; font-family: 'JetBrains Mono', monospace; }
.stat-item .value.time { color: #10b981; }
.victory-actions { display: flex; gap: 15px; justify-content: center; }

@keyframes popIn {
  from { opacity: 0; transform: scale(0.8); }
  to { opacity: 1; transform: scale(1); }
}
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>