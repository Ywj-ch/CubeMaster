<template>
  <div class="cube-spinner" :class="[`size-${size}`]">
    <div class="spinner">
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
    </div>
    <span v-if="text" class="spinner-text">{{ text }}</span>
  </div>
</template>

<script setup>
defineProps({
  size: {
    type: String,
    default: "medium",
    validator: (value) => ["small", "medium", "large"].includes(value),
  },
  text: {
    type: String,
    default: "",
  },
});
</script>

<style scoped>
.cube-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.spinner {
  transform-style: preserve-3d;
  animation: spinner-rotate 2s infinite ease;
}

.spinner > div {
  background-color: rgba(0, 77, 255, 0.15);
  height: 100%;
  position: absolute;
  width: 100%;
  border: 2px solid #3b82f6;
  border-radius: 4px;
}

.spinner div:nth-of-type(1) {
  transform: translateZ(-22px) rotateY(180deg);
}

.spinner div:nth-of-type(2) {
  transform: rotateY(-270deg) translateX(50%);
  transform-origin: top right;
}

.spinner div:nth-of-type(3) {
  transform: rotateY(270deg) translateX(-50%);
  transform-origin: center left;
}

.spinner div:nth-of-type(4) {
  transform: rotateX(90deg) translateY(-50%);
  transform-origin: top center;
}

.spinner div:nth-of-type(5) {
  transform: rotateX(-90deg) translateY(50%);
  transform-origin: bottom center;
}

.spinner div:nth-of-type(6) {
  transform: translateZ(22px);
}

@keyframes spinner-rotate {
  0% {
    transform: rotate(45deg) rotateX(-25deg) rotateY(25deg);
  }
  50% {
    transform: rotate(45deg) rotateX(-385deg) rotateY(25deg);
  }
  100% {
    transform: rotate(45deg) rotateX(-385deg) rotateY(385deg);
  }
}

.spinner-text {
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  letter-spacing: 0.5px;
}

.size-small .spinner {
  width: 32px;
  height: 32px;
}

.size-small .spinner > div {
  border-width: 1.5px;
}

.size-small .spinner div:nth-of-type(1) {
  transform: translateZ(-16px) rotateY(180deg);
}

.size-small .spinner div:nth-of-type(2) {
  transform: rotateY(-270deg) translateX(50%);
}

.size-small .spinner div:nth-of-type(3) {
  transform: rotateY(270deg) translateX(-50%);
}

.size-small .spinner div:nth-of-type(4) {
  transform: rotateX(90deg) translateY(-50%);
}

.size-small .spinner div:nth-of-type(5) {
  transform: rotateX(-90deg) translateY(50%);
}

.size-small .spinner div:nth-of-type(6) {
  transform: translateZ(16px);
}

.size-medium .spinner {
  width: 48px;
  height: 48px;
}

.size-medium .spinner div:nth-of-type(1) {
  transform: translateZ(-24px) rotateY(180deg);
}

.size-medium .spinner div:nth-of-type(2) {
  transform: rotateY(-270deg) translateX(50%);
}

.size-medium .spinner div:nth-of-type(3) {
  transform: rotateY(270deg) translateX(-50%);
}

.size-medium .spinner div:nth-of-type(4) {
  transform: rotateX(90deg) translateY(-50%);
}

.size-medium .spinner div:nth-of-type(5) {
  transform: rotateX(-90deg) translateY(50%);
}

.size-medium .spinner div:nth-of-type(6) {
  transform: translateZ(24px);
}

.size-large .spinner {
  width: 64px;
  height: 64px;
}

.size-large .spinner > div {
  border-width: 3px;
}

.size-large .spinner div:nth-of-type(1) {
  transform: translateZ(-32px) rotateY(180deg);
}

.size-large .spinner div:nth-of-type(2) {
  transform: rotateY(-270deg) translateX(50%);
}

.size-large .spinner div:nth-of-type(3) {
  transform: rotateY(270deg) translateX(-50%);
}

.size-large .spinner div:nth-of-type(4) {
  transform: rotateX(90deg) translateY(-50%);
}

.size-large .spinner div:nth-of-type(5) {
  transform: rotateX(-90deg) translateY(50%);
}

.size-large .spinner div:nth-of-type(6) {
  transform: translateZ(32px);
}

.size-large .spinner-text {
  font-size: 16px;
}

[data-theme="dark"] .spinner > div {
  background-color: rgba(96, 165, 250, 0.15);
  border-color: #60a5fa;
}

[data-theme="dark"] .spinner-text {
  color: #94a3b8;
}
</style>
