import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import "element-plus/theme-chalk/dark/css-vars.css";
import "./style.css";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";

const app = createApp(App);
app.use(router);
app.use(ElementPlus);

// 注册所有 Element Plus 图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// ============================================
// 全局主题初始化（不依赖 Vue 组件生命周期）
// ============================================
const THEME_KEY = "cube-master-theme";

function getSystemPreference() {
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function loadSavedTheme() {
  try {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved === "light" || saved === "dark" || saved === "auto") {
      return saved;
    }
  } catch (err) {
    console.warn("读取主题设置失败:", err);
  }
  return "auto";
}

function applyTheme(mode) {
  let applied;

  if (mode === "auto") {
    applied = getSystemPreference();
  } else {
    applied = mode;
  }

  // 更新 html 元素的 data-theme 属性
  const html = document.documentElement;
  html.setAttribute("data-theme", applied);

  // 同时设置 dark 类名，用于 Element Plus
  if (applied === "dark") {
    html.classList.add("dark");
  } else {
    html.classList.remove("dark");
  }

  return applied;
}

function initTheme() {
  const mode = loadSavedTheme();
  applyTheme(mode);

  // 监听系统主题变化（仅当主题模式为 auto 时）
  const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
  mediaQuery.addEventListener("change", () => {
    const currentMode = loadSavedTheme();
    if (currentMode === "auto") {
      applyTheme("auto");
    }
  });
}

// 初始化主题
initTheme();

app.mount("#app");
