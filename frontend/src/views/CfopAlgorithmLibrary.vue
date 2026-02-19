<!-- frontend/src/views/CfopAlgorithmLibrary.vue -->
<template>
  <div class="cfop-lib-page">
    <div class="container">
      <!-- 1. Header: 标题根据 :step 动态变化 -->
      <header class="lib-header">
        <div class="header-left">
          <button
            @click="
              $router.push({
                path: '/cfop',
                state: { scrollTarget: 'full-roadmap' },
              })
            "
            class="minimal-back-btn"
          >
            <el-icon><ArrowLeft /></el-icon>
            <span>BACK TO CFOP INFO</span>
          </button>
          <!-- 动态展示 PLL 或 OLL -->
          <h1 class="glow-title">
            {{ currentConfig.title }} <span class="thin">LIBRARY</span>
          </h1>
        </div>

        <div class="wave-group">
          <input required v-model="searchQuery" type="text" class="input" />
          <span class="bar"></span>
          <label class="label">
            <span
              v-for="(c, i) in 'SEARCH'.split('')"
              :key="i"
              class="label-char"
              :style="{ '--index': i }"
              >{{ c }}</span
            >
          </label>
        </div>
      </header>

      <!-- 2. 分类导航 (数据源动态切换) -->
      <div class="filter-wrapper">
        <div class="glass-radio-group scrollable-hide-bar" ref="radioGroupRef">
          <template v-for="cat in currentConfig.categories" :key="cat.value">
            <input
              type="radio"
              name="category"
              :id="'cat-' + cat.value"
              :value="cat.value"
              v-model="currentCategory"
            />
            <label :for="'cat-' + cat.value">{{ cat.label }}</label>
          </template>
          <div class="glass-glider" :style="gliderStyle"></div>
        </div>
      </div>

      <!-- 3. 算法网格 ( filteredList 会自动根据新数据计算 ) -->
      <div class="algo-grid" v-if="filteredList.length > 0">
        <div
          v-for="item in filteredList"
          :key="item.id"
          class="premium-card"
          @click="openDemo(item)"
        >
          <div class="card-inner">
            <div class="card-header">
              <span class="algo-name">{{ item.name }}</span>
              <div class="difficulty-indicator">
                <span
                  v-for="n in 3"
                  :key="n"
                  :class="['dot', { active: n <= item.difficulty }]"
                ></span>
              </div>
            </div>
            <div class="formula-display">
              <span class="formula-label">ALGORITHM</span>
              <code class="mono-text">{{ item.algorithm }}</code>
            </div>
            <div class="card-footer">
              <p class="recog-text">{{ item.recognition }}</p>
              <div class="tag-row">
                <span v-for="tag in item.tags" :key="tag" class="mini-tag"
                  ># {{ tag }}</span
                >
              </div>
            </div>
          </div>
          <div class="play-overlay">
            <div class="play-icon-circle">
              <el-icon><VideoPlay /></el-icon>
            </div>
          </div>
        </div>
      </div>

      <el-empty v-else description="暂无数据" />
    </div>

    <!-- 4. 3D 弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      width="700px"
      class="immersive-dialog"
      :show-close="true"
      align-center
      destroy-on-close
    >
      <template #header>
        <div class="dialog-header-custom">
          <span class="dialog-id-badge">{{ selectedAlgo?.id }}</span>
          <h2>{{ selectedAlgo?.name }}</h2>
        </div>
      </template>

      <div class="dialog-body" v-if="selectedAlgo">
        <!-- 3D 舞台区域 -->
        <div class="cube-viewport">
          <div class="viewport-bg"></div>
          <TutorialCube
            ref="tutorialCubeRef"
            :setup="selectedAlgo.setup"
            :algorithm="selectedAlgo.demoAlgorithm || selectedAlgo.algorithm"
            :customization="config"
          />
        </div>

        <!-- 右侧/下方 信息区 -->
        <div class="info-panel">
          <div class="info-section">
            <h4 class="info-label">核心公式</h4>
            <div class="big-formula-box">
              <code class="huge-mono">{{ selectedAlgo.algorithm }}</code>
              <button
                class="copy-btn"
                @click="copyAlgo(selectedAlgo.algorithm)"
              >
                <el-icon><CopyDocument /></el-icon>
              </button>
            </div>
          </div>

          <div class="info-section">
            <h4 class="info-label">观察要点</h4>
            <p class="recog-desc">{{ selectedAlgo.recognition }}</p>
          </div>

          <div class="dialog-actions">
            <button class="primary-action-btn" @click="handlePlay">
              <el-icon><VideoPlay /></el-icon>
              <span>开始演示</span>
            </button>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from "vue";
import { useRoute } from "vue-router";
import { ArrowLeft, VideoPlay, CopyDocument } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import TutorialCube from "../components/TutorialCube.vue";
import { pllAlgorithms, pllCategories } from "../data/cfop/pll.js";
import { ollAlgorithms, ollCategories } from "../data/cfop/oll.js";
import { f2lAlgorithms, f2lCategories } from "../data/cfop/f2l.js";
import { useCubeCustomization } from "../composables/useCubeCustomization.js";

const route = useRoute();
const { config } = useCubeCustomization();

// --- 1. 数据映射表 ---
const dataMap = {
  pll: {
    title: "PLL",
    list: pllAlgorithms,
    categories: pllCategories,
  },
  oll: {
    title: "OLL",
    list: ollAlgorithms,
    categories: ollCategories,
  },
  f2l: {
    title: "F2L",
    list: f2lAlgorithms,
    categories: f2lCategories,
  },
};

const currentConfig = computed(() => {
  const step = route.params.step;
  return dataMap[step] || dataMap.pll;
});

// --- 2. 状态控制 ---
const currentCategory = ref("all");
const searchQuery = ref("");
const dialogVisible = ref(false);
const selectedAlgo = ref(null);
const tutorialCubeRef = ref(null);

// DOM 引用
const radioGroupRef = ref(null);
// 滑块样式 (改为响应式对象)
const gliderStyle = ref({ width: "0px", transform: "translateX(0)" });

// --- 3. 核心：基于 DOM 的滑块位置计算 + 自动滚动 ---
const updateGlider = () => {
  const container = radioGroupRef.value;
  if (!container) return;

  // 1. 找到所有 Label 和当前选中项索引
  const labels = container.querySelectorAll("label");
  const currentIndex = currentConfig.value.categories.findIndex(
    (c) => c.value === currentCategory.value,
  );

  // 2. 如果找到了选中的项
  if (currentIndex !== -1 && labels[currentIndex]) {
    const targetLabel = labels[currentIndex];

    // 获取参数
    const left = targetLabel.offsetLeft;
    const width = targetLabel.offsetWidth;

    // A. 移动黑块 (Glider)
    gliderStyle.value = {
      width: `${width}px`,
      transform: `translateX(${left}px)`,
    };

    // B. 滚动容器 (Scroll Container)
    // 算法：标签左边距 - (容器一半宽 - 标签一半宽) = 让标签居中
    const scrollTarget = left - container.offsetWidth / 2 + width / 2;

    container.scrollTo({
      left: scrollTarget,
      behavior: "smooth",
    });
  } else {
    // 3. 没选中时隐藏黑块
    gliderStyle.value = { width: "0px", transform: "translateX(0)" };
  }
};

// --- 4. 监听器 ---

// 监听分类切换 -> 更新滑块
watch(currentCategory, () => {
  nextTick(updateGlider);
});

// 监听路由切换 -> 重置状态并更新滑块
watch(
  () => route.params.step,
  () => {
    currentCategory.value = "all";
    searchQuery.value = "";
    // 等待 DOM 更新（因为 categories 列表变了）后再计算
    nextTick(() => {
      // 稍微延迟一点点，确保新的 Label 渲染完成
      setTimeout(updateGlider, 50);
    });
  },
  { immediate: true }, // 立即执行一次
);

// 初始化和窗口缩放监听
onMounted(() => {
  // 延时确保字体加载完成，宽度计算准确
  setTimeout(updateGlider, 100);
  window.addEventListener("resize", updateGlider);
});

// --- 5. 搜索框筛选逻辑 ---
const filteredList = computed(() => {
  return currentConfig.value.list.filter((item) => {
    const catMatch =
      currentCategory.value === "all" ||
      item.category === currentCategory.value;
    const searchMatch =
      item.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.algorithm.toLowerCase().includes(searchQuery.value.toLowerCase());
    return catMatch && searchMatch;
  });
});

// --- 6. 交互方法 ---
const openDemo = (item) => {
  selectedAlgo.value = item;
  dialogVisible.value = true;
};
const handlePlay = () => tutorialCubeRef.value?.play();
const copyAlgo = (text) => {
  navigator.clipboard.writeText(text);
  ElMessage.success("已复制");
};
</script>

<style scoped>
/* --- 页面基础 --- */
.cfop-lib-page {
  min-height: 100vh;
  background-color: #f3f3f3; /* 配合你新的网格背景 */
  padding: 60px 0;
  color: #1e293b;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* --- Header & Wave Search --- */
.lib-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 50px;
}

.glow-title {
  font-size: 3rem;
  font-weight: 900;
  letter-spacing: -2px;
  margin: 0;
  line-height: 1;
}
.glow-title .thin {
  font-weight: 300;
  color: #94a3b8;
}

.minimal-back-btn {
  background: none;
  border: none;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #94a3b8;
  font-weight: 700;
  font-size: 14px;
  letter-spacing: 1px;
  cursor: pointer;
  margin-bottom: 12px;
  transition: color 0.3s;
}
.minimal-back-btn:hover {
  color: #3b82f6;
}

/* Wave Search Style */
.wave-group {
  position: relative;
}
.wave-group .input {
  font-size: 16px;
  padding: 10px 10px 10px 5px;
  display: block;
  width: 240px;
  border: none;
  border-bottom: 2px solid #cbd5e1;
  background: transparent;
  transition: border-color 0.3s;
}
.wave-group .input:focus {
  outline: none;
  border-color: #3b82f6;
}
.wave-group .label {
  color: #94a3b8;
  font-size: 16px;
  font-weight: 700;
  position: absolute;
  pointer-events: none;
  left: 5px;
  top: 10px; /* 初始位置在横线上 */
  display: flex;
}

.wave-group .label-char {
  display: inline-block;
  transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1) all;
  transition-delay: calc(var(--index) * 0.05s);
}

/* 核心：当 focus 或 input 有效(非空)时文字跳动 */
.wave-group .input:focus ~ label .label-char,
.wave-group .input:valid ~ label .label-char {
  transform: translateY(-26px); /* 向上跳动 26px */
  font-size: 12px;
  color: #3b82f6;
}
.wave-group .bar {
  position: relative;
  display: block;
  width: 240px;
}
.wave-group .bar:before,
.wave-group .bar:after {
  content: "";
  height: 2px;
  width: 0;
  bottom: 0px;
  position: absolute;
  background: #3b82f6;
  transition: 0.3s ease all;
}
.wave-group .bar:before {
  left: 50%;
}
.wave-group .bar:after {
  right: 50%;
}
.wave-group .input:focus ~ .bar:before,
.wave-group .input:focus ~ .bar:after {
  width: 50%;
}

/* --- Glass Radio Group (Updated for Scrolling) --- */
.filter-wrapper {
  margin-bottom: 50px;
  display: flex;
  justify-content: center;
  width: 100%; /* 确保外层容器占满宽度，这样里面的 radio-group 居中后，如果太宽就能向两边延伸 */
}

.glass-radio-group {
  --bg: rgba(255, 255, 255, 0.6);
  display: flex;
  position: relative;
  background: var(--bg);
  border-radius: 14px;
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);

  /* 核心修改：支持横向滚动 */
  overflow-x: auto;
  overflow-y: hidden;
  max-width: 100%; /* 限制最大宽度不超过屏幕 */
  white-space: nowrap; /* 强制所有 label 在一行 */

  /* 隐藏滚动条 (兼容性写法) */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE/Edge */

  padding: 4px; /* 保持内边距 */
  width: fit-content; /* 内容少时收缩，内容多时被 max-width 限制 */
}

/* Chrome/Safari 隐藏滚动条 */
.glass-radio-group::-webkit-scrollbar {
  display: none;
}

.glass-radio-group input {
  display: none;
}

.glass-radio-group label {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
  font-size: 14px;
  padding: 10px 20px;
  cursor: pointer;
  font-weight: 700;
  color: #64748b;
  position: relative;
  z-index: 2;
  transition: color 0.3s;
}

.glass-radio-group input:checked + label {
  color: #fff;
}

.glass-glider {
  position: absolute;
  top: 4px;
  bottom: 4px;
  background: #1e293b;
  border-radius: 10px;
  z-index: 1;
  transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
}

/* --- 3-Column Grid & Premium Cards --- */
.algo-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.premium-card {
  position: relative;
  background: #fff;
  border-radius: 24px;
  padding: 32px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.premium-card:hover .card-inner {
  filter: blur(8px); /* 增加高斯模糊 */
  opacity: 0.2; /* 降低不透明度，使背景内容若隐若现 */
  transform: scale(0.95); /* 稍微收缩，产生深度的视觉落差 */
}

.card-inner {
  position: relative;
  z-index: 1; /* 内容层在下 */
  transition: all 0.4s ease;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.algo-name {
  font-size: 1.5rem;
  font-weight: 800;
  color: #0f172a;
}

.difficulty-indicator {
  display: flex;
  gap: 4px;
}
.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #e2e8f0;
  transition: 0.3s;
}
.dot.active {
  background: #3b82f6;
  box-shadow: 0 0 8px rgba(59, 130, 246, 0.5);
}

.formula-display {
  background: #f8fafc;
  padding: 16px;
  border-radius: 14px;
  margin-bottom: 24px;
  border: 1px solid #f1f5f9;
}
.formula-label {
  font-size: 10px;
  font-weight: 800;
  color: #94a3b8;
  display: block;
  margin-bottom: 8px;
}
.mono-text {
  font-family: "JetBrains Mono", monospace;
  font-size: 1.1rem;
  color: #3b82f6;
  font-weight: 700;
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-footer p {
  font-size: 0.95rem;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 20px;
  height: 3rem;
  overflow: hidden;
}
.tag-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.mini-tag {
  font-size: 11px;
  font-weight: 700;
  color: #94a3b8;
  background: #f1f5f9;
  padding: 4px 10px;
  border-radius: 6px;
}

.play-overlay {
  position: absolute;
  inset: 0;
  background: transparent; /* 去掉之前的白色背景，改用内容虚化来突出 */
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  z-index: 10; /* 确保按钮在最上层 */
  transition: all 0.3s ease;
}

.premium-card:hover .play-overlay {
  opacity: 1;
}

.play-icon-circle {
  width: 70px; /* 稍微加大一点按钮 */
  height: 70px;
  background: #3b82f6;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  box-shadow: 0 15px 30px rgba(59, 130, 246, 0.4);
  /* 让按钮从中心微微放大弹出 */
  transform: scale(0.5);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.premium-card:hover .play-icon-circle {
  transform: scale(1);
}

/* --- Immersive Dialog --- */
:deep(.immersive-dialog) {
  border-radius: 28px;
  overflow: hidden;
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 40px 100px rgba(0, 0, 0, 0.2);
}

.dialog-header-custom {
  display: flex;
  align-items: center;
  gap: 15px;
}
.dialog-id-badge {
  background: #1e293b;
  color: white;
  padding: 4px 12px;
  border-radius: 8px;
  font-family: monospace;
  font-weight: 700;
  font-size: 12px;
}

.dialog-body {
  display: flex;
  flex-direction: column;
  gap: 30px;
  padding: 10px;
}

.cube-viewport {
  height: 380px;
  background: #f8fafc;
  border-radius: 20px;
  position: relative;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}
.viewport-bg {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    circle at 50% 50%,
    rgba(59, 130, 246, 0.05) 0%,
    transparent 70%
  );
}

.info-panel {
  padding: 0 10px;
}
.info-section {
  margin-bottom: 24px;
}
.info-label {
  font-size: 12px;
  font-weight: 800;
  color: #94a3b8;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.big-formula-box {
  background: #f1f5f9;
  padding: 20px;
  border-radius: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #e2e8f0;
}
.huge-mono {
  font-family: "JetBrains Mono", monospace;
  font-size: 1.4rem;
  color: #1e293b;
  font-weight: 800;
}
.copy-btn {
  background: white;
  border: 1px solid #e2e8f0;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  cursor: pointer;
  color: #64748b;
  transition: 0.3s;
}
.copy-btn:hover {
  color: #3b82f6;
  border-color: #3b82f6;
}

.recog-desc {
  font-size: 1.1rem;
  color: #475569;
  line-height: 1.6;
}

.dialog-actions {
  display: flex;
  justify-content: center; /* 核心：水平居中 */
  margin-top: 10px; /* 稍微收紧间距 */
  padding-bottom: 10px;
}

.primary-action-btn {
  width: 85%;
  height: 60px;
  background: #3b82f6;
  border: none;
  border-radius: 16px;
  color: white;
  font-weight: 800;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 15px 30px rgba(59, 130, 246, 0.2);
}
.primary-action-btn:hover {
  background: #2563eb;
  transform: translateY(-2px);
}

/* 响应式调整 */
@media (max-width: 992px) {
  .algo-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 600px) {
  .algo-grid {
    grid-template-columns: 1fr;
  }
  .glow-title {
    font-size: 2rem;
  }
  .wave-group {
    display: none;
  }
}

/* ==================== Dark Mode Styles ==================== */
[data-theme="dark"] .cfop-lib-page {
  background-color: var(--dm-bg-page);
  color: var(--dm-text-primary);
}

[data-theme="dark"] .glow-title {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .glow-title .thin {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .minimal-back-btn {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .minimal-back-btn:hover {
  color: var(--dm-accent);
}

[data-theme="dark"] .wave-group .input {
  border-bottom-color: var(--dm-border);
  color: var(--dm-text-primary);
}

[data-theme="dark"] .wave-group .input:focus {
  border-color: var(--dm-accent);
}

[data-theme="dark"] .wave-group .label {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .wave-group .input:focus ~ label .label-char,
[data-theme="dark"] .wave-group .input:valid ~ label .label-char {
  color: var(--dm-accent);
}

[data-theme="dark"] .glass-radio-group {
  --bg: var(--dm-glass-bg);
  background: var(--bg);
  border-color: var(--dm-glass-border);
}

[data-theme="dark"] .glass-radio-group label {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .glass-radio-group input:checked + label {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .glass-glider {
  background: var(--dm-accent);
}

[data-theme="dark"] .premium-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .algo-name {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .dot {
  background: var(--dm-border);
}

[data-theme="dark"] .dot.active {
  background: var(--dm-accent);
  box-shadow: 0 0 8px rgba(96, 165, 250, 0.5);
}

[data-theme="dark"] .formula-display {
  background: var(--dm-bg-hover);
  border-color: var(--dm-border);
}

[data-theme="dark"] .formula-label {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .mono-text {
  color: var(--dm-accent);
}

[data-theme="dark"] .card-footer p {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .mini-tag {
  color: var(--dm-text-muted);
  background: var(--dm-bg-hover);
}

[data-theme="dark"] .play-icon-circle {
  background: var(--dm-accent);
  box-shadow: 0 15px 30px rgba(59, 130, 246, 0.4);
}

html[data-theme="dark"] .cfop-lib-page :deep(.el-dialog) {
  background: #1e293b !important;
  border: 1px solid #334155 !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
  outline: none !important;
}

html[data-theme="dark"] .cfop-lib-page :deep(.el-dialog__header) {
  border-bottom: 1px solid #334155 !important;
}

html[data-theme="dark"] .cfop-lib-page :deep(.el-dialog__body) {
  background: #1e293b !important;
}

html[data-theme="dark"] .cfop-lib-page .dialog-id-badge {
  background: var(--dm-bg-hover);
  color: var(--dm-text-primary);
}

[data-theme="dark"] .cube-viewport {
  background: var(--dm-bg-hover);
  border-color: var(--dm-border);
}

[data-theme="dark"] .info-label {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .big-formula-box {
  background: var(--dm-bg-hover);
  border-color: var(--dm-border);
}

[data-theme="dark"] .huge-mono {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .copy-btn {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .copy-btn:hover {
  color: var(--dm-accent);
  border-color: var(--dm-accent);
}

[data-theme="dark"] .recog-desc {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .primary-action-btn {
  background: var(--dm-accent);
  box-shadow: 0 15px 30px rgba(59, 130, 246, 0.3);
}

[data-theme="dark"] .primary-action-btn:hover {
  background: var(--dm-accent-hover);
}
</style>
