<template>
  <div class="tutorial-cube-wrapper">
    <Cube3DView
      ref="cubeViewRef"
      :cubeState="displayColors"
      :interactive="true"
      :moveDuration="500"
      style="width: 100%; height: 100%"
    />

    <!-- 悬浮重置按钮 -->
    <div class="controls">
      <el-button
        size="small"
        circle
        icon="Refresh"
        @click="initCube"
        title="重置状态"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import Cube3DView from "../components/Cube3DView.vue";
import {
  SOLVED_STATE,
  cloneState,
  applyMove,
  stateToColors,
} from "../utils/cubeLogic.js";

const props = defineProps({
  setup: { type: String, default: "" }, // 初始设置动作，如 "F2"
  algorithm: { type: String, default: "" }, // 演示动作，如 "R U R'"
});

// 内部状态
const currentLogicState = ref(cloneState(SOLVED_STATE)); // 数字状态
const displayColors = ref([]); // 传给 3DView 的颜色字符串数组
const isAnimating = ref(false);
const cubeViewRef = ref(null); // 获取 3DView 实例

// 初始化魔方状态
const initCube = () => {
  // 1. 拿一个复原的魔方
  let state = cloneState(SOLVED_STATE);

  // 2. 如果有 setup 步骤，瞬间执行完（不播放动画）
  if (props.setup) {
    const moves = props.setup.split(" ");
    moves.forEach((move) => {
      if (move) state = applyMove(state, move);
    });
  }

  // 3. 更新 UI
  currentLogicState.value = state;
  displayColors.value = stateToColors(state);
};

// 播放演示动画
const playAlgorithm = async () => {
  if (isAnimating.value || !props.algorithm) return;
  isAnimating.value = true;

  const moves = props.algorithm.split(" ");

  // 逐个执行动画
  for (const move of moves) {
    if (!move) continue;

    // 1. 触发 3D 动画 (通过 ref 调用子组件方法，或者通过 prop 传递 trigger)
    // 这里我们假设 Cube3DView 暴露了 executeMove 方法，或者我们通过更新状态来驱动
    // 为了平滑动画，最好是调用 Cube3DView 的方法
    if (cubeViewRef.value) {
      await cubeViewRef.value.triggerMove(move); // 假设子组件有这个方法
    }

    // 2. 逻辑层同步更新 (防止动画和数据脱节)
    currentLogicState.value = applyMove(currentLogicState.value, move);
  }

  isAnimating.value = false;
};

// 暴露给父组件的方法
defineExpose({
  play: playAlgorithm,
  reset: initCube,
});

// 监听 setup 变化（比如切换章节时），重置魔方
watch(
  () => props.setup,
  () => {
    initCube();
  },
);

onMounted(() => {
  initCube();
});
</script>

<style scoped>
.tutorial-cube-wra pper {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 250px;
  background: #f0f2f5;
  border-radius: 8px;
  overflow: hidden;
}

.controls {
  position: absolute;
  bottom: 10px;
  right: 10px;
  z-index: 10;
}
</style>
