<template>
  <div class="cube-free-page">
    <div class="timer-badge-new">
      <div class="timer-header">
        <el-icon><Timer /></el-icon>
        <span class="timer-label">ELAPSED</span>
      </div>
      <div class="timer-num">{{ timeDisplay }}</div>
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
       <Cube3DView
          ref="cubeRef"
          :cubeState="cubeState"
          :interactive="isGameStarted && !isAutoOperating && !isMoving"
          :enableControls="true"
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';
import Cube3DView from '../components/Cube3DView.vue';
import { createCubeFromJson } from '../utils/cubeState';
import { applyMove } from '../utils/cubeMoves';
import { Timer, Refresh, RefreshLeft, VideoPlay } from '@element-plus/icons-vue';

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

const timeDisplay = computed(() => {
  const diff = currentTime.value || 0;
  const m = Math.floor(diff / 60000).toString().padStart(2, '0');
  const s = Math.floor((diff % 60000) / 1000).toString().padStart(2, '0');
  const ms = Math.floor((diff % 1000) / 10).toString().padStart(2, '0');
  return `${m}:${s}.${ms}`;
});

// 开始挑战
function startChallenge() {
  if (isAutoOperating.value) return;
  isGameStarted.value = true;
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
 * 执行转动
 * @param {string} move 指令
 * @param {boolean} force 是否强制执行（用于打乱逻辑，绕过开始状态检查）
 */
async function executeMove(move, force = false) {
  // 1. 如果正在自动操作（打乱）且不是强制执行，拦截
  if (isAutoOperating.value && !force) return;
  // 2. 如果游戏未开始且不是强制执行，拦截
  if (!isGameStarted.value && !force) return;
  // 3. 关键：如果当前 3D 动画正在进行，拦截所有新指令，防止魔方乱掉
  if (isMoving.value) return;

  if (cubeRef.value) {
    isMoving.value = true; // 锁定

    cubeRef.value.playMove(move);
    applyMove(cubeState.value, move);

    if (!force) {
      history.value.push(move);
      nextTick(() => {
        const inner = scrollRef.value?.$el.querySelector('.el-scrollbar__wrap');
        if (inner) inner.scrollLeft = inner.scrollWidth;
      });
    }

    // 4. 等待动画时长（根据 Cube3DView 的 300ms 设定，给 320ms 缓冲时间）
    setTimeout(() => {
      isMoving.value = false; // 解锁
    }, 320);
  }
}

async function scrambleWithAnimation() {
  if (isAutoOperating.value) return;
  isGameStarted.value = false; // 打乱时重置开始状态
  stopTimer();
  currentTime.value = 0;
  history.value = [];
  isAutoOperating.value = true;

  const moves = ["R", "L", "U", "D", "F", "B", "R'", "L'", "U'", "D'", "F'", "B'"];
  for (let i = 0; i < 40; i++) {
    const randomMove = moves[Math.floor(Math.random() * moves.length)];
    // 打乱逻辑通过 playMove 和 applyMove 直接执行，不走 executeMove 的锁定逻辑以保证速度
    // 但为了 3D 表现，我们依然需要微小的等待
    if (cubeRef.value) {
      cubeRef.value.playMove(randomMove);
      applyMove(cubeState.value, randomMove);
      await new Promise(r => setTimeout(r, 320)); // 等待 3D 动画完成
    }
  }
  isAutoOperating.value = false;
}

function resetAll() {
  stopTimer();
  isGameStarted.value = false;
  isMoving.value = false;
  currentTime.value = 0;
  history.value = [];
  cubeState.value = createCubeFromJson();
  if (cubeRef.value) {
    cubeRef.value.renderCubies(cubeState.value.cubies);
    cubeRef.value.resetView();
  }
}

function handleKeydown(e) {
  // 正在自动打乱、未开始、或者 3D 动画正在执行时，拦截按键
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
/* 保持原有样式不变 */
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

/* 开始按钮特别样式 */
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
</style>