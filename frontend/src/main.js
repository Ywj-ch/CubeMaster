import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./style.css";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";

const app = createApp(App);
app.use(router);

// 注册所有 Element Plus 图标（按需加载会自动处理组件）
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

// ============================================
// 动态标签页标题管理
// ============================================

// 学习中心课程标题映射
const courseTitles = {
  "basics": "基础入门",
  "lbl": "LBL 教学",
  "advanced": "进阶技巧"
};

/**
 * 更新浏览器标签页标题
 * @param {string} pageTitle - 页面标题（不含后缀）
 */
function updatePageTitle(pageTitle) {
  const title = pageTitle ? `${pageTitle} - CubeMaster` : "CubeMaster";
  document.title = title;
}

// 路由前置守卫 - 监听路由变化并更新标题
router.beforeEach((to, from, next) => {
  // 处理学习中心动态标题
  if (to.name === "Learning") {
    const courseTitle = courseTitles[to.params.courseId] || "学习中心";
    updatePageTitle(courseTitle);
  }
  // 处理 CFOP 算法库动态标题
  else if (to.name === "CfopLibrary") {
    const stepTitle = to.params.step ? `F${to.params.step} ${to.meta.title}` : to.meta.title;
    updatePageTitle(stepTitle);
  }
  // 其他页面使用路由配置的 meta.title
  else if (to.meta.title) {
    updatePageTitle(to.meta.title);
  }
  // 兜底处理
  else {
    updatePageTitle("");
  }

  next();
});

// 初始化主题
initTheme();

app.mount("#app");
