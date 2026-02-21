<template>
  <div class="tutorial-cube-wrapper">
    <Cube3DView
      ref="cubeViewRef"
      :cubeState="displayColors"
      :interactive="true"
      :moveDuration="500"
      :customization="customization"
      style="width: 100%; height: 100%"
    />

    <!-- 悬浮重置按钮 -->
    <div class="controls">
      <el-button
        size="default"
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
  SOLVED_STATE_NUMERIC,
  cloneStateNumeric,
  applyMoveNumeric,
  numericToColors,
} from "../utils/cubeMoves.js";

const props = defineProps({
  setup: { type: String, default: "" },
  algorithm: { type: String, default: "" },
  customization: { type: Object, default: null },
});

const currentLogicState = ref(cloneStateNumeric(SOLVED_STATE_NUMERIC));
const displayColors = ref([]);
const isAnimating = ref(false);
const cubeViewRef = ref(null);

const initCube = () => {
  let state = cloneStateNumeric(SOLVED_STATE_NUMERIC);

  if (props.setup) {
    const moves = props.setup.split(" ");
    moves.forEach((move) => {
      if (move) state = applyMoveNumeric(state, move);
    });
  }

  currentLogicState.value = state;
  displayColors.value = numericToColors(state);
};

const playAlgorithm = async () => {
  if (isAnimating.value || !props.algorithm) return;
  isAnimating.value = true;

  const moves = props.algorithm.split(" ");

  for (const move of moves) {
    if (!move) continue;

    if (cubeViewRef.value) {
      await cubeViewRef.value.triggerMove(move);
    }

    currentLogicState.value = applyMoveNumeric(currentLogicState.value, move);
  }

  isAnimating.value = false;
};

defineExpose({
  play: playAlgorithm,
  reset: initCube,
});

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
.tutorial-cube-wrapper {
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

/* Dark Mode Styles */
[data-theme="dark"] .tutorial-cube-wrapper {
  background: var(--dm-bg-page);
}
</style>
