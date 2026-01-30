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
        <router-link to="/about" class="nav-item">关于</router-link>
      </nav>
    </header>

    <!-- Main: 非首页时自动空出 header 的高度，防止内容重叠 -->
    <main :class="['main-content', { 'main-content-padded': !isHomePage }]">
      <router-view />
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

const showHeader = ref(true);
const isScrolled = ref(false);
let lastScrollPosition = 0;
const router = useRouter();
const route = useRoute();

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
  padding: 32px 0; /* 压缩间距 */
  display: flex;
  justify-content: center;
  align-items: center;
  background: transparent;
}
.copyright {
  color: #94a3b8;
  font-size: 14px; /* 进一步减小字号，更显精致 */
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
  } /* 手机端隐藏名称只留 logo */
}
</style>
