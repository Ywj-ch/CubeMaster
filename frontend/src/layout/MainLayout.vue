<template>
  <div class="layout-container">
    <header :class="['header', { 'header-hidden': !showHeader, 'header-scrolled': isScrolled }]">
      <div class="header-left" @click="goHome">
        <div class="logo-container">
          <img src="/icons/logo_icon.svg" alt="CubeMaster Logo" width="26" height="26" />
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

    <main class="main-content">
      <router-view />
    </main>

    <footer class="footer">
      <p>Copyright © 2026 chippanda</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const showHeader = ref(true);
const isScrolled = ref(false);
let lastScrollPosition = 0;
const router = useRouter();

const goHome = () => {
  router.push('/');
};

const handleScroll = () => {
  const currentScrollPosition = window.pageYOffset || document.documentElement.scrollTop;

  // 判断是否已经离开了顶部
  isScrolled.value = currentScrollPosition > 20;

  // 滚动逻辑：向下滑动且超过 header 高度时隐藏，向上滑动时显示
  if (currentScrollPosition < 0) return;

  if (Math.abs(currentScrollPosition - lastScrollPosition) < 60) return; // 设定阈值避免抖动

  showHeader.value = currentScrollPosition < lastScrollPosition || currentScrollPosition < 80;
  lastScrollPosition = currentScrollPosition;
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
/* 1. 布局基础 */
.layout-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased; /* Apple 风格平滑字体 */
}

/* 2. Header: 毛玻璃与智能显隐 */
.header {
  height: 64px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  box-sizing: border-box;
  background: rgba(255, 255, 255, 0.8); /* 降低透明度 */
  backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 0.5px solid rgba(0, 0, 0, 0.08); /* 极细分割线 */
  position: fixed;
  top: 0;
  z-index: 1000;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), background 0.3s; /* 丝滑动画 */
}

.header-hidden {
  transform: translateY(-100%); /* 向下滑动时完全隐藏 */
}

.header-scrolled {
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.03); /* 滚动后才出现的细腻阴影 */
}

/* 3. Logo: 拟物化微质感 (Skeuomorphic) */
.header-left {
  display: flex;
  align-items: center; /* 垂直居中 */
  gap: 12px;           /* 在 Logo 和网站名之间留出 12px 的高级感间距 */
  cursor: pointer;    /* 增加交互感 */
}

.header-left:hover {
  opacity: 0.8;
}

.logo-container {
  width: 38px;
  height: 38px;
  background: linear-gradient(145deg, #ffffff, #f0f0f0);
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  /* 核心：三重阴影实现物理悬浮感 */
  box-shadow:
    2px 2px 5px rgba(0, 0, 0, 0.05),      /* 外部投影 */
    -1px -1px 2px rgba(255, 255, 255, 1), /* 反光高光 */
    inset 0 1px 1px rgba(255, 255, 255, 0.8); /* 内部边缘光 */
  border: 0.5px solid rgba(0, 0, 0, 0.05);
}

.site-name {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: -0.02em; /* 紧凑排版 */
  color: #1d1d1f;
}

/* 4. 导航栏交互 */
.nav-wrapper {
  display: flex;
  gap: 28px;
}

.nav-item {
  text-decoration: none;
  font-size: 15px;
  color: #515154;
  font-weight: 500;
  transition: color 0.2s;
  position: relative;
  padding: 4px 0;
}

.nav-item:hover {
  color: #0071e3;
}

/* 激活状态：使用极简的微点或短横线 */
.router-link-exact-active {
  color: #1d1d1f;
}

.router-link-exact-active::after {
  content: "";
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 4px;
  height: 4px;
  background-color: #0071e3;
  border-radius: 50%; /* 圆点指示器，比横线更高级 */
}

/* 5. 主内容与页脚 */
.main-content {
  flex: 1;
  margin-top: 0;
  padding-top: 64px;
  background: #ffffff;
}

.footer {
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f5f7;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  color: #86868b;
  font-size: 14px;
  letter-spacing: 0.01em;
}
</style>