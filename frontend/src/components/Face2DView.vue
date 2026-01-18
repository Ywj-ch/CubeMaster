<template>
  <div class="face">
    <div
      v-for="(cell, index) in face.flat()"
      :key="index"
      class="cell"
      :style="{ backgroundColor: colorMap[cell] }"
      @click="handleCellClick(index)"
    ></div>
  </div>
</template>

<script setup>
const props = defineProps({
  face: { type: Array, required: true }
});

const emit = defineEmits(['cell-click']);

const colorMap = {
  white: "#FFFFFF", yellow: "#FFD500", red: "#C41E3A",
  orange: "#FF5800", blue: "#0051BA", green: "#009E60",
};

const handleCellClick = (index) => {
  // 直接发送 0-8 的索引，让父组件去处理坐标转换
  emit('cell-click', index);
};
</script>

<style scoped>
.face {
  display: grid;
  grid-template-columns: repeat(3, 40px);
  grid-template-rows: repeat(3, 40px);
  gap: 2px;
  background-color: #333;
  border: 2px solid #333;
}
.cell {
  width: 40px; height: 40px;
  cursor: pointer;
  transition: all 0.1s;
}
.cell:hover { filter: brightness(1.2); transform: scale(1.05); z-index: 2; }
</style>