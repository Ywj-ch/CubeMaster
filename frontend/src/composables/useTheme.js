/**
 * @fileoverview 主题管理组合式函数
 * 
 * 提供全局主题切换功能，支持：
 * - 亮色/暗色主题切换
 * - 跟随系统偏好 (auto 模式)
 * - localStorage 持久化
 * - Element Plus 暗色模式集成
 * 
 * @module composables/useTheme
 */

import { ref, onMounted, watch } from "vue";

/**
 * 主题管理组合式函数
 * 支持亮色/暗色主题切换，系统偏好检测，localStorage持久化
 * @returns {Object} 响应式状态和方法
 */
export function useTheme() {
  const THEME_KEY = "cube-master-theme";
  const THEME_LIGHT = "light";
  const THEME_DARK = "dark";
  const THEME_AUTO = "auto";

  // 当前主题模式（light/dark/auto）
  const themeMode = ref(THEME_AUTO);
  
  // 实际应用的主题（light/dark）
  const currentTheme = ref(THEME_LIGHT);
  
  // 是否启用暗色主题
  const isDark = ref(false);

  /**
   * 获取系统颜色偏好
   * @returns {string} 'light' 或 'dark'
   */
  function getSystemPreference() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches 
      ? THEME_DARK 
      : THEME_LIGHT;
  }

  /**
   * 从localStorage加载保存的主题设置
   */
  function loadSavedTheme() {
    try {
      const saved = localStorage.getItem(THEME_KEY);
      if (saved === THEME_LIGHT || saved === THEME_DARK || saved === THEME_AUTO) {
        themeMode.value = saved;
      } else {
        // 如果没有保存的设置，使用auto
        themeMode.value = THEME_AUTO;
      }
    } catch (err) {
      console.warn("读取主题设置失败:", err);
      themeMode.value = THEME_AUTO;
    }
  }

  /**
   * 保存主题设置到localStorage
   */
  function saveTheme() {
    try {
      localStorage.setItem(THEME_KEY, themeMode.value);
    } catch (err) {
      console.warn("保存主题设置失败:", err);
    }
  }

  /**
   * 更新实际应用的主题
   */
  function updateAppliedTheme() {
    let applied;
    
    if (themeMode.value === THEME_AUTO) {
      applied = getSystemPreference();
    } else {
      applied = themeMode.value;
    }
    
    currentTheme.value = applied;
    isDark.value = applied === THEME_DARK;
    
    // 更新html元素的data-theme属性
    const html = document.documentElement;
    html.setAttribute("data-theme", applied);
    
    // 同时设置dark类名，用于Element Plus
    if (applied === THEME_DARK) {
      html.classList.add("dark");
    } else {
      html.classList.remove("dark");
    }
  }

  /**
   * 设置主题模式
   * @param {string} mode - 'light'、'dark' 或 'auto'
   */
  function setTheme(mode) {
    if (mode !== THEME_LIGHT && mode !== THEME_DARK && mode !== THEME_AUTO) {
      console.warn(`无效的主题模式: ${mode}`);
      return;
    }
    
    themeMode.value = mode;
    saveTheme();
    updateAppliedTheme();
  }

  /**
   * 切换亮色/暗色主题
   */
  function toggleTheme() {
    if (themeMode.value === THEME_LIGHT) {
      setTheme(THEME_DARK);
    } else if (themeMode.value === THEME_DARK) {
      setTheme(THEME_LIGHT);
    } else {
      // 如果是auto模式，切换到与当前系统偏好相反的模式
      const systemPref = getSystemPreference();
      setTheme(systemPref === THEME_LIGHT ? THEME_DARK : THEME_LIGHT);
    }
  }

  /**
   * 初始化主题系统
   */
  function initTheme() {
    loadSavedTheme();
    updateAppliedTheme();
    
    // 监听系统主题变化（仅当主题模式为auto时）
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    const handleSystemChange = () => {
      if (themeMode.value === THEME_AUTO) {
        updateAppliedTheme();
      }
    };
    
    mediaQuery.addEventListener("change", handleSystemChange);
    
    // 返回清理函数
    return () => {
      mediaQuery.removeEventListener("change", handleSystemChange);
    };
  }

  // 组件挂载时初始化
  onMounted(() => {
    const cleanup = initTheme();
    
    // 监听themeMode变化
    const stopWatch = watch(themeMode, () => {
      updateAppliedTheme();
    });
    
    // 组件卸载时清理
    return () => {
      cleanup();
      stopWatch();
    };
  });

  return {
    // 状态
    themeMode,
    currentTheme,
    isDark,
    
    // 方法
    setTheme,
    toggleTheme,
    getSystemPreference,
    
    // 常量（用于UI）
    THEME_LIGHT,
    THEME_DARK,
    THEME_AUTO,
  };
}