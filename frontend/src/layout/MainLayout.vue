<template>
  <div class="layout-container">
    <!-- Header: 增加 isHomePage 判断，非首页直接应用 scrolled 样式 -->
    <header
      :class="[
        'header',
        {
          'header-hidden': !showHeader,
          'header-scrolled': isScrolled || !isHomePage,
          'header-on-home': isHomePage,
        },
      ]"
    >
      <div class="header-left" @click="goHome">
        <div class="logo-container">
          <img
            src="/icons/logo_icon.svg"
            alt="CubeMaster Logo"
            width="26"
            height="26"
          />
        </div>
        <span class="site-name">CubeMaster</span>
      </div>

      <nav class="nav-wrapper">
        <router-link to="/" class="nav-item">首页</router-link>
        <router-link to="/cube" class="nav-item">3D魔方</router-link>
        <router-link to="/solver" class="nav-item">求解器</router-link>
        <router-link to="/learning" class="nav-item">学习</router-link>
        <router-link to="/customizer" class="nav-item">外观定制</router-link>
        <router-link to="/about" class="nav-item">关于</router-link>
      </nav>

      <!-- 主题切换按钮 -->
      <div class="theme-toggle-wrapper">
        <button class="theme-toggle-btn" @click="toggleTheme" :title="isDark ? '切换到亮色模式' : '切换到暗色模式'">
          <el-icon v-if="isDark" class="theme-icon"><Sunny /></el-icon>
          <el-icon v-else class="theme-icon"><Moon /></el-icon>
        </button>
      </div>
    </header>

    <!-- Main: 非首页时自动空出 header 的高度，防止内容重叠 -->
    <main :class="['main-content', { 'main-content-padded': !isHomePage }]">
      <router-view :key="$route.fullPath" />
    </main>

    <!-- Footer: 极简紧凑版 -->
    <footer class="footer">
      <p class="copyright">Copyright © 2026 chippanda</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useTheme } from "../composables/useTheme.js";
import { Sunny, Moon } from "@element-plus/icons-vue";

const showHeader = ref(true);
const isScrolled = ref(false);
let lastScrollPosition = 0;
const router = useRouter();
const route = useRoute();

// 主题管理
const { isDark, toggleTheme } = useTheme();

// 核心逻辑：判断当前是否为首页
const isHomePage = computed(() => route.path === "/");

const goHome = () => router.push("/");

const handleScroll = () => {
  const currentScrollPosition =
    window.pageYOffset || document.documentElement.scrollTop;

  // 滚动反馈
  isScrolled.value = currentScrollPosition > 10;

  // 显隐逻辑
  if (currentScrollPosition < 0) return;
  if (Math.abs(currentScrollPosition - lastScrollPosition) < 40) return;

  showHeader.value =
    currentScrollPosition < lastScrollPosition || currentScrollPosition < 100;
  lastScrollPosition = currentScrollPosition;
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll);
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});
</script>

<style scoped>
.layout-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family:
    "Inter",
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Roboto,
    sans-serif;
  background-color: #ffffff;
}

/* --- Header 基础 --- */
.header {
  height: 64px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  box-sizing: border-box;
  position: fixed;
  top: 0;
  z-index: 1000;
  transition:
    transform 0.4s cubic-bezier(0.16, 1, 0.3, 1),
    background 0.3s,
    border-color 0.3s;
}

/* 初始状态：只有在首页且未滚动时才透明 */
.header.header-on-home:not(.header-scrolled) {
  background: transparent;
  border-bottom-color: transparent;
}

/* 激活状态：非首页或已滚动时，应用磨砂玻璃效果 */
.header-scrolled,
.header:not(.header-on-home) {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
}

.header-hidden {
  transform: translateY(-100%);
}

/* --- Logo & Nav --- */
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}
.logo-container {
  width: 34px;
  height: 34px;
  background: #ffffff;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.03);
}
.site-name {
  font-size: 17px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #0f172a;
}

.nav-wrapper {
  display: flex;
  gap: 28px;
  flex: 1;
  justify-content: center;
}
.nav-item {
  text-decoration: none;
  font-size: 14px;
  color: #64748b;
  font-weight: 600;
  position: relative;
  padding: 6px 0;
  transition: color 0.2s;
}
.nav-item:hover {
  color: #2563eb;
}
.router-link-exact-active {
  color: #0f172a;
}
.router-link-exact-active::after {
  content: "";
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 4px;
  height: 4px;
  background-color: #2563eb;
  border-radius: 50%;
}

/* --- 主题切换按钮 --- */
.theme-toggle-wrapper {
  display: flex;
  align-items: center;
}

.theme-toggle-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: rgba(0, 0, 0, 0.05);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.theme-toggle-btn:hover {
  background: rgba(0, 0, 0, 0.1);
  transform: scale(1.1);
}

.theme-icon {
  font-size: 18px;
  color: #64748b;
}

/* --- Content Area --- */
.main-content {
  flex: 1;
  background: transparent;
}

/* 关键优化：非首页页面增加顶部内边距，防止内容被 Header 遮挡 */
.main-content-padded {
  padding-top: 64px;
}

/* --- Footer: 紧凑收口 --- */
.footer {
  padding: 32px 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: transparent;
}
.copyright {
  color: #94a3b8;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.02em;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .header {
    padding: 0 20px;
  }
  .nav-wrapper {
    gap: 16px;
  }
  .nav-item {
    font-size: 13px;
  }
  .site-name {
    display: none;
  }
  .theme-toggle-btn {
    width: 32px;
    height: 32px;
  }
  .theme-icon {
    font-size: 16px;
  }
}

/* ============================================
   暗色模式覆盖
   ============================================ */

/* 布局容器 */
[data-theme="dark"] .layout-container {
  background-color: var(--dm-bg-page);
}

/* 导航栏 - 滚动状态 */
[data-theme="dark"] .header-scrolled,
[data-theme="dark"] .header:not(.header-on-home) {
  background: rgba(30, 41, 59, 0.8);
  border-bottom-color: rgba(255, 255, 255, 0.05);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

/* Logo容器 */
[data-theme="dark"] .logo-container {
  background: var(--dm-bg-card);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.05);
}

/* 网站名称 */
[data-theme="dark"] .site-name {
  color: var(--dm-text-primary);
}

/* 导航项 */
[data-theme="dark"] .nav-item {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .nav-item:hover {
  color: var(--dm-accent);
}

[data-theme="dark"] .router-link-exact-active {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .router-link-exact-active::after {
  background-color: var(--dm-accent);
}

/* 主题切换按钮 */
[data-theme="dark"] .theme-toggle-btn {
  background: rgba(255, 255, 255, 0.1);
}

[data-theme="dark"] .theme-toggle-btn:hover {
  background: rgba(255, 255, 255, 0.15);
}

[data-theme="dark"] .theme-icon {
  color: var(--dm-text-secondary);
}

/* 页脚版权 */
[data-theme="dark"] .copyright {
  color: var(--dm-text-muted);
}
</style>
