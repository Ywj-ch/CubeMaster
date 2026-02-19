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
  grid-template-columns: repeat(3, var(--size));
  grid-template-rows: repeat(3, var(--size));
  gap: 3px; /* 增加一点间隙，让每个块更独立 */
  border: none; /* 去掉硬边框 */
  padding: 3px;
  background: #1e293b; /* 优雅的深蓝黑底座 */
  border-radius: 6px; /* 整个魔方带一点圆角 */
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.cell {
  width: var(--size);
  height: var(--size);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 4px; /* 每个小块都有圆角，像真实的贴纸/塑料块 */

  /* 核心：内阴影制造立体感 (Inset Shadow) */
  /* 上方亮光，下方暗影，模拟微凸效果 */
  box-shadow:
    inset 0 1px 1px rgba(255, 255, 255, 0.3),
    inset 0 -2px 2px rgba(0, 0, 0, 0.05);
}

/*
   特殊处理白色块：因为白色背景上白色高光看不见，
   我们需要给白色块加一点点灰度渐变，让它看起来像陶瓷
*/
.cell[style*="rgb(255, 255, 255)"],
.cell[style*="#FFFFFF"] {
  background: linear-gradient(145deg, #ffffff, #f1f5f9) !important;
  border: 1px solid rgba(0, 0, 0, 0.05); /* 极细描边防止融入背景 */
}

/* 黑色块（未还原部分）也优化一下，不要死黑 */
.cell[style*="rgb(0, 0, 0)"],
.cell[style*="#000000"] {
  background-color: #334155 !important; /* 改为深岩灰，更有质感 */
  box-shadow: inset 0 0 4px rgba(0, 0, 0, 0.5); /* 内陷感 */
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

/* Dark Mode Styles */
[data-theme="dark"] .face {
  background: var(--dm-bg-page);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
}
</style>
