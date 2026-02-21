<template>
  <div class="app-container">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>

    <Transition name="loading-fade">
      <div v-if="isLoading" class="global-loading-overlay">
        <CubeSpinner size="medium" :text="loadingText || '加载中...'" />
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { useLoading } from "./composables/useLoading";
import CubeSpinner from "./components/CubeSpinner.vue";

const { isLoading, loadingText } = useLoading();
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
  background-color: #f8f9fa;
}

[data-theme="dark"] body {
  background-color: #0f172a;
}

.app-container {
  min-height: 100vh;
}

.global-loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(4px);
  z-index: 9998;
}

[data-theme="dark"] .global-loading-overlay {
  background: rgba(15, 23, 42, 0.85);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.loading-fade-enter-active,
.loading-fade-leave-active {
  transition: opacity 0.3s ease;
}

.loading-fade-enter-from,
.loading-fade-leave-to {
  opacity: 0;
}
</style>
