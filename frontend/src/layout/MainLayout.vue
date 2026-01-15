<template>
  <div class="layout-container">
    <header class="header">
      <div class="header-left">
        <div class="logo-container">
          <img src="/icons/logo_icon.svg" alt="CubeMaster Logo" width="30" height="30" />
        </div>
        <span class="site-name">CubeMaster</span>
      </div>

      <nav class="nav-wrapper">
        <router-link to="/" class="nav-item">首页</router-link>
        <router-link to="/cube" class="nav-item">3D魔方</router-link>
        <router-link to="/solver" class="nav-item">魔方求解器</router-link>
        <router-link to="/learning" class="nav-item">学习</router-link>
        <router-link to="/about" class="nav-item">关于</router-link>
      </nav>
    </header>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="footer">
      Copyright © 2026 chippanda
    </footer>
  </div>
</template>

<style scoped>
.layout-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  height: 80px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 60px;
  box-sizing: border-box;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #eee;
  position: fixed;
  top: 0;
  z-index: 1000;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logo-container {
  width: 45px;
  height: 45px;
  background: #edf0f3;
  color: white;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.site-name {
  font-size: 20px;
  font-weight: bold;
  color: #2D3748;
}

.nav-wrapper {
  display: flex;
  gap: 32px;
  align-items: center;
  flex-shrink: 0;
}

.nav-item {
  text-decoration: none;
  font-size: 18px;
  color: #4A5568;
  font-weight: 500;
  white-space: nowrap;
  transition: all 0.2s;
  padding: 5px 0;
}

.nav-item:hover {
  color: #4299E1;
}

/* 激活状态的样式 */
.router-link-exact-active {
  color: #4299E1;
  border-bottom: 2px solid #4299E1;
}

.main-content {
  flex: 1;
  margin-top: 80px;
  background: #f7fafc;
}

.footer {
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: white;
  border-top: 1px solid #eee;
  color: #a0aec0;
}
</style>