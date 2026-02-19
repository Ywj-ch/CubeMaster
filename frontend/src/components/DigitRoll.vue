<template>
  <div class="digit-box">
    <transition name="slide-up">
      <!-- 这里的 :key="val" 是核心，当数值变化时，Vue 会自动触发进场/出场动画 -->
      <div :key="val" class="num">
        {{ val }}
      </div>
    </transition>
  </div>
</template>

<script setup>
defineProps({
  val: { type: [Number, String], required: true },
});
</script>

<style scoped>
.digit-box {
  position: relative; /* 必须相对定位，作为绝对定位子元素的参考 */
  display: inline-block;
  width: 46px;
  height: 64px;
  background: #ffffff;
  border-radius: 8px;
  overflow: hidden; /* 隐藏跑到外面的数字 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.num {
  /* 关键：绝对定位让新旧数字可以重叠在同一个容器里同时运动 */
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 40px;
  font-family: "JetBrains Mono", monospace;
  font-weight: 700;
  color: #1e293b;
  /* 开启 GPU 加速，防止模糊动画卡顿 */
  will-change: transform, opacity, filter;
  backface-visibility: hidden;
}

/* === Vue Transition 动画定义 === */

/* 1. 进场初始状态 (新数字在底部，透明，模糊) */
.slide-up-enter-from {
  transform: translateY(100%);
  opacity: 0;
  filter: blur(5px);
}

/* 2. 离场结束状态 (旧数字去顶部，变透明，变模糊) */
.slide-up-leave-to {
  transform: translateY(-100%);
  opacity: 0;
  filter: blur(5px);
}

/* 3. 动画过程 (控制速度和曲线) */
.slide-up-enter-active,
.slide-up-leave-active {
  /* 0.6s 是你想要变慢的速度，cubic-bezier 让运动更优雅 */
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 4. 确保离场的元素保持绝对定位，不会挤压布局 */
.slide-up-leave-active {
  position: absolute;
}

/* Dark Mode Styles */
[data-theme="dark"] .digit-box {
  background: var(--dm-bg-card);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  border: 1px solid var(--dm-border);
}

[data-theme="dark"] .num {
  color: var(--dm-text-primary);
}
</style>
