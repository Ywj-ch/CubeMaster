<template>
  <!--
    动态绑定 CSS 变量 --size
    根据 interactive 属性动态切换 can-hover 类
  -->
  <div
    class="face"
    :class="{ 'can-hover': interactive }"
    :style="{ '--size': cellSize + 'px' }"
  >
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
  face: { type: Array, required: true },
  // 新增：单元格大小，默认为 40px
  cellSize: { type: Number, default: 40 },
  // 新增：是否可交互，默认为 true
  interactive: { type: Boolean, default: true },
});

const emit = defineEmits(["cell-click"]);

const colorMap = {
  white: "#FFFFFF",
  yellow: "#FFD500",
  red: "#C41E3A",
  orange: "#FF5800",
  blue: "#0051BA",
  green: "#009E60",
  black: "#000000",
};

const handleCellClick = (index) => {
  // 只有在可交互模式下才发送点击事件
  if (props.interactive) {
    emit("cell-click", index);
  }
};
</script>

<style scoped>
.face {
  display: grid;
  /* 使用 CSS 变量控制网格大小 */
  grid-template-columns: repeat(3, var(--size));
  grid-template-rows: repeat(3, var(--size));
  gap: 2px;
  background-color: #333;
  border: 2px solid #333;
  width: fit-content;
}

.cell {
  width: var(--size);
  height: var(--size);
  transition: all 0.1s;
}

/* 只有带有 can-hover 类的组件才会有点击手势和悬停效果 */
.face.can-hover .cell {
  cursor: pointer;
}

.face.can-hover .cell:hover {
  filter: brightness(1.2);
  transform: scale(1.05);
  z-index: 2;
}
</style>
