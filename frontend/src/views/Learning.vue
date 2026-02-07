<template>
  <div class="learning-container">
    <el-container style="height: 100vh">
      <!-- 1. 左侧导航栏 -->
      <el-aside width="280px" class="tutorial-sidebar">
        <div class="sidebar-header">
          <div class="header-top">
            <h2>魔方学院</h2>
          </div>

          <!-- 课程切换下拉框 -->
          <el-select
            :model-value="currentCourseId"
            placeholder="选择教程"
            class="course-select"
            @change="handleCourseChange"
            size="large"
          >
            <el-option
              v-for="course in courseList"
              :key="course.id"
              :label="course.title"
              :value="course.id"
            />
          </el-select>

          <p class="course-desc">{{ currentCourse.description }}</p>
        </div>

        <el-scrollbar>
          <el-menu
            :default-active="currentStepIndex.toString()"
            @select="handleSelectStep"
            class="sidebar-menu"
          >
            <el-menu-item
              v-for="(step, index) in currentSteps"
              :key="step.id || index"
              :index="index.toString()"
            >
              <span>{{ step.title }}</span>
            </el-menu-item>
          </el-menu>
        </el-scrollbar>
      </el-aside>

      <!-- 2. 右侧主内容区 -->
      <el-main class="tutorial-content">
        <div v-if="currentStep">
          <!-- 章节标题区 -->
          <div class="step-header">
            <h1>{{ currentStep.title }}</h1>
            <p class="step-desc">{{ currentStep.description }}</p>
          </div>

          <el-divider />

          <!-- === 新增容器：用于控制两列网格布局 === -->
          <div
            class="cases-wrapper"
            :class="{ 'grid-layout': isAlgorithmMode }"
          >
            <!-- 遍历当前章节的所有“情况” -->
            <div
              v-for="(item, index) in currentStep.cases"
              :key="item.id"
              class="case-block"
            >
              <div
                v-if="item.type === 'algorithm-card'"
                class="algo-3d-perspective-wrap"
              >
                <div class="algo-3d-card" @click="openDemo(item)">
                  <div class="algo-card-header">
                    <div class="algo-thumb-box">
                      <Face2DView
                        :face="item.topPattern"
                        :cellSize="22"
                        :interactive="false"
                      />
                    </div>
                    <div class="algo-meta-info">
                      <div class="algo-id-row">
                        <span class="algo-no">#{{ index + 1 }}</span>
                        <el-tag
                          v-for="tag in item.tags"
                          :key="tag"
                          size="default"
                          effect="light"
                          type="info"
                          >{{ tag }}</el-tag
                        >
                      </div>
                      <h3 class="algo-title-text">{{ item.title }}</h3>
                    </div>
                  </div>
                  <div class="algo-formula-zone">
                    <code class="formula-code">{{ item.algorithm }}</code>
                    <span class="steps-tag">{{ item.stepsCount }} STEPS</span>
                  </div>
                  <div class="algo-recognition-box">
                    <div class="rec-label">识别技巧:</div>
                    <ul class="rec-list">
                      <li v-for="(rec, rIdx) in item.recognition" :key="rIdx">
                        {{ rec }}
                      </li>
                    </ul>
                  </div>
                  <div class="algo-card-footer">
                    <span class="view-demo-link">
                      <el-icon size="20"><VideoPlay /></el-icon> 查看3D演示
                    </span>
                  </div>
                </div>
              </div>

              <div v-else class="case-card">
                <el-card shadow="hover" class="styled-card">
                  <template #header>
                    <div class="card-header">
                      <el-tag
                        effect="dark"
                        round
                        :type="getTagColor(item.type)"
                        style="margin-right: 10px"
                      >
                        {{ getTagLabel(item.type, index) }}
                      </el-tag>
                      <span class="case-title">{{ item.title }}</span>
                    </div>
                  </template>

                  <!-- 模式 1: 基础图文 -->
                  <div v-if="item.type === 'graphic'" class="graphic-layout">
                    <el-row :gutter="40" align="middle">
                      <el-col :span="10">
                        <div class="concept-image-box">
                          <img
                            v-if="item.image"
                            :src="item.image"
                            class="concept-img"
                            alt="Illustration"
                          />
                          <div v-else class="placeholder-img">
                            <el-icon :size="40"><Picture /></el-icon
                            ><span>暂无图片</span>
                          </div>
                        </div>
                      </el-col>
                      <el-col :span="14">
                        <div class="concept-points">
                          <div
                            v-for="(point, pIdx) in item.points"
                            :key="pIdx"
                            class="point-item"
                          >
                            <el-icon class="point-icon"><Select /></el-icon>
                            <span class="point-text">{{ point }}</span>
                          </div>
                        </div>
                      </el-col>
                    </el-row>
                  </div>

                  <!-- 模式 2: 符号网格 -->
                  <div
                    v-else-if="item.type === 'notation-grid'"
                    class="notation-layout"
                  >
                    <p class="notation-desc">{{ item.description }}</p>
                    <div v-if="item.image" class="notation-ref-img">
                      <img :src="item.image" />
                    </div>
                    <div class="notation-grid">
                      <div
                        v-for="note in item.notationItems"
                        :key="note.key"
                        class="notation-item"
                      >
                        <div class="keycap">{{ note.key }}</div>
                        <div class="note-info">
                          <span class="note-name">{{ note.name }}</span
                          ><span class="note-desc">{{ note.desc }}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- 模式 3: 默认 3D 演示 -->
                  <el-row v-else :gutter="30" align="middle">
                    <el-col :span="14">
                      <div class="instruction-text">
                        <p>{{ item.description }}</p>
                        <div class="algorithm-box" v-if="item.algorithm">
                          <div class="algo-content">
                            <span class="label">公式:</span
                            ><code class="algo-text">{{ item.algorithm }}</code>
                          </div>
                          <el-button
                            type="primary"
                            circle
                            :icon="VideoPlay"
                            class="play-btn"
                            @click="handlePlay(item.id)"
                            title="播放演示"
                          />
                        </div>
                        <el-alert
                          v-if="item.tips"
                          :title="item.tips"
                          type="info"
                          :closable="false"
                          show-icon
                          class="tip-alert"
                        />
                      </div>
                    </el-col>
                    <el-col :span="10">
                      <div class="cube-container">
                        <TutorialCube
                          :ref="(el) => setCubeRef(el, item.id)"
                          :setup="item.setup"
                          :algorithm="item.algorithm"
                        />
                      </div>
                    </el-col>
                  </el-row>
                </el-card>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <el-empty description="该课程内容正在开发中，敬请期待..." />
        </div>
      </el-main>

      <!-- 3D 算法演示弹窗 -->
      <el-dialog
        v-model="demoVisible"
        width="700px"
        class="immersive-dialog"
        :show-close="true"
        align-center
        destroy-on-close
      >
        <!-- 自定义头部 -->
        <template #header>
          <div class="dialog-header-custom">
            <!-- 这是一个小小的 ID 胶囊 -->
            <span class="dialog-id-badge">{{ currentDemoItem.id }}</span>
            <h2>{{ currentDemoItem.title }}</h2>
          </div>
        </template>

        <div class="dialog-body">
          <!-- 3D 舞台区域  -->
          <div class="cube-viewport">
            <div class="viewport-bg"></div>
            <TutorialCube
              v-if="demoVisible"
              ref="demoCubeRef"
              :setup="currentDemoItem.setup"
              :algorithm="currentDemoItem.algorithm"
            />
          </div>

          <!-- 右侧/下方 信息区 -->
          <div class="info-panel">
            <!-- 公式展示 -->
            <div class="info-section">
              <h4 class="info-label">核心公式</h4>
              <div class="big-formula-box">
                <code class="huge-mono">{{ currentDemoItem.algorithm }}</code>
                <button
                  class="copy-btn"
                  @click="copyAlgo(currentDemoItem.algorithm)"
                >
                  <el-icon><CopyDocument /></el-icon>
                </button>
              </div>
            </div>

            <!-- 提示/技巧展示 -->
            <div class="info-section" v-if="currentDemoItem.tips">
              <h4 class="info-label">观察技巧 / TIPS</h4>
              <p class="recog-desc">{{ currentDemoItem.tips }}</p>
            </div>

            <!-- 底部操作按钮 (居中胶囊样式) -->
            <div class="dialog-actions">
              <button class="primary-action-btn" @click="handleDemoPlay">
                <el-icon><VideoPlay /></el-icon>
                <span>开始演示</span>
              </button>
            </div>
          </div>
        </div>
      </el-dialog>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  VideoPlay,
  Picture,
  Select,
  CopyDocument,
} from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { courseList } from "../data/courses.js";
import TutorialCube from "../components/TutorialCube.vue";
import Face2DView from "../components/Face2DView.vue";

const route = useRoute();
const router = useRouter();

// --- 状态定义 ---
const currentCourseId = ref(route.params.courseId || courseList[0]?.id);
const currentStepIndex = ref(0);
const cubeRefs = ref({});
const demoVisible = ref(false);
const currentDemoItem = ref({});
const demoCubeRef = ref(null);

// --- 计算属性 ---
const currentCourse = computed(
  () => courseList.find((c) => c.id === currentCourseId.value) || courseList[0],
);

const currentSteps = computed(() => currentCourse.value.steps || []);

const currentStep = computed(() =>
  !currentSteps.value || currentSteps.value.length === 0
    ? null
    : currentSteps.value[currentStepIndex.value],
);

// 新增：判断是否为算法网格模式
const isAlgorithmMode = computed(() => {
  if (!currentStep.value || !currentStep.value.cases.length) return false;
  return currentStep.value.cases[0].type === "algorithm-card";
});

// --- 辅助函数 ---
const getTagLabel = (type, index) => {
  if (type === "graphic") return `概念 ${index + 1}`;
  if (type === "notation-grid") return `符号表`;
  return `情况 ${index + 1}`;
};

const getTagColor = (type) => {
  if (type === "graphic") return "primary";
  if (type === "notation-grid") return "warning";
  return "";
};

// --- 监听器 & 方法 ---
watch(
  () => route.params.courseId,
  (newId) => {
    if (newId && newId !== currentCourseId.value) {
      currentCourseId.value = newId;
      resetView();
    }
  },
);

const setCubeRef = (el, id) => {
  if (el) cubeRefs.value[id] = el;
};

const handleCourseChange = (newId) => {
  if (newId === "cfop") {
    router.push("/cfop");
    return;
  }
  currentStepIndex.value = 0;
  router.push({ params: { courseId: newId } });
};

const handleSelectStep = (index) => {
  currentStepIndex.value = parseInt(index);
  cubeRefs.value = {};
  document.querySelector(".tutorial-content")?.scrollTo(0, 0);
};

const handlePlay = (caseId) => {
  const cubeInstance = cubeRefs.value[caseId];
  if (cubeInstance) cubeInstance.play();
};

const copyAlgo = (text) => {
  if (!text) return;
  navigator.clipboard.writeText(text);
  ElMessage.success("公式已复制");
};

const resetView = () => {
  currentStepIndex.value = 0;
  cubeRefs.value = {};
  document.querySelector(".tutorial-content")?.scrollTo(0, 0);
};

// 新增：演示逻辑
const openDemo = (item) => {
  currentDemoItem.value = item;
  demoVisible.value = true;
};

const handleDemoPlay = () => {
  if (demoCubeRef.value) demoCubeRef.value.play();
};
</script>

<style scoped>
/* ==================== 1. 保留所有原有样式 ==================== */
.learning-container {
  height: 100vh;
  background-color: #f5f7fa;
}
.tutorial-sidebar {
  background-color: #fff;
  border-right: 1px solid #e6e6e6;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.02);
  z-index: 10;
}
.sidebar-header {
  padding: 24px 20px;
  background: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
  gap: 15px;
  flex-shrink: 0;
}
.header-top h2 {
  margin: 0;
  font-size: 1.4rem;
  letter-spacing: 1px;
}
.course-desc {
  margin: 0;
  font-size: 0.85rem;
  opacity: 0.7;
  line-height: 1.5;
}
.course-select {
  width: 100%;
}
:deep(.el-select__wrapper) {
  background-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.2) inset;
  color: white;
}
:deep(.el-select__wrapper:hover) {
  background-color: rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.5) inset;
}
:deep(.el-select__wrapper.is-focused) {
  box-shadow: 0 0 0 1px #409eff inset !important;
}
:deep(.el-select__selected-item),
:deep(.el-select__placeholder) {
  color: white !important;
}
:deep(.el-select__suffix) {
  color: rgba(255, 255, 255, 0.7);
}
.sidebar-menu {
  border-right: none;
}
.sidebar-menu :deep(.el-menu-item.is-active) {
  background-color: #ecf5ff;
  color: #409eff;
  border-right: 3px solid #409eff;
  font-weight: 600;
}
.sidebar-menu :deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
  margin: 4px 0;
}
.tutorial-content {
  padding: 40px 50px;
  overflow-y: auto;
  scroll-behavior: smooth;
}
.step-header h1 {
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 2rem;
}
.step-desc {
  color: #606266;
  font-size: 1.1rem;
  line-height: 1.6;
  margin-top: 15px;
}
.case-card {
  margin-bottom: 35px;
}
.styled-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
  background-color: #fff;
}
.card-header {
  display: flex;
  align-items: center;
}
.case-title {
  font-weight: bold;
  font-size: 1.15rem;
  color: #303133;
}
.graphic-layout {
  padding: 10px;
}
.concept-image-box {
  background: #f8f9fa;
  border: 1px solid #e4e7ed;
  border-radius: 12px;
  overflow: hidden;
  height: 240px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.concept-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 20px;
}
.placeholder-img {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: #909399;
}
.concept-points {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 10px;
}
.point-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  line-height: 1.6;
}
.point-icon {
  color: #10b981;
  margin-top: 4px;
  font-weight: bold;
}
.point-text {
  font-size: 1.05rem;
  color: #303133;
}
.notation-layout {
  padding: 10px;
}
.notation-desc {
  color: #606266;
  margin-bottom: 20px;
}
.notation-ref-img {
  text-align: center;
  margin-bottom: 30px;
}
.notation-ref-img img {
  max-width: 300px;
  border-radius: 12px;
}
.notation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}
.notation-item {
  display: flex;
  align-items: center;
  gap: 15px;
  background: #fcfcfc;
  padding: 15px;
  border-radius: 12px;
  border: 1px solid #ebeef5;
  transition: transform 0.2s;
}
.notation-item:hover {
  transform: translateY(-2px);
  border-color: #409eff;
}
.keycap {
  width: 40px;
  height: 40px;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-bottom: 4px solid #94a3b8;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: "JetBrains Mono", monospace;
  font-weight: 800;
  font-size: 1.2rem;
  color: #1e293b;
}
.note-info {
  display: flex;
  flex-direction: column;
}
.note-name {
  font-weight: 700;
  color: #303133;
  font-size: 1rem;
}
.note-desc {
  font-size: 0.85rem;
  color: #909399;
}
.instruction-text p {
  line-height: 1.8;
  color: #303133;
  margin-bottom: 25px;
  font-size: 1.05rem;
}
.algorithm-box {
  background-color: #f4f4f5;
  padding: 15px 20px;
  border-radius: 8px;
  border-left: 5px solid #909399;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  transition: all 0.3s;
}
.algorithm-box:hover {
  background-color: #ecf5ff;
  border-left-color: #409eff;
}
.algo-content {
  display: flex;
  align-items: center;
  gap: 12px;
}
.label {
  font-weight: bold;
  color: #909399;
}
.algo-text {
  font-family: "Courier New", Courier, monospace;
  font-size: 1.3rem;
  font-weight: bold;
  color: #303133;
  letter-spacing: 1px;
}
.play-btn {
  font-size: 1.2rem;
  transition: transform 0.2s;
}
.play-btn:hover {
  transform: scale(1.1);
}
.tip-alert {
  background-color: #fdf6ec;
  color: #e6a23c;
}
.cube-container {
  width: 100%;
  height: 320px;
  background-color: #eaeff5;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #dcdfe6;
  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.02);
}
.empty-state {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ==================== 2. 修正后的新增样式 ==================== */

/* 强制两列布局容器 */
.cases-wrapper.grid-layout {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  align-items: stretch;
  gap: 32px;
  width: 100%;
}

.case-block {
  /* 确保外层容器也是满高度 */
  height: 100%;
}

/* 进阶算法卡片主体：去重叠、明亮化 */
.algo-3d-card {
  width: 100%;
  height: 100%; /* 占满 grid 分配的高度 */
  min-height: 420px; /* 增加最小高度，让它更接近正方形 */
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px; /* 圆角加大 */
  padding: 32px; /* 内边距加大 */
  cursor: pointer;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.algo-3d-card:hover {
  /* 去掉 3D 旋转效果，改为优雅上浮 */
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  border-color: #3b82f6;
}

/* 卡片内部元素调色与排版 */
.algo-card-header {
  display: flex;
  gap: 24px;
  align-items: center;
  margin-bottom: 24px;
}
.algo-thumb-box {
  background: #f8fafc;
  padding: 12px;
  border-radius: 14px;
  border: 1px solid #edf2f7;
  /* 稍微放大缩略图区域 */
  min-width: 100px;
  display: flex;
  justify-content: center;
}

.algo-meta-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px; /* 标题和标签之间的间距 */
}

.algo-id-row {
  display: flex;
  align-items: center;
  gap: 10px; /* 标签之间的间距拉开 */
}

.algo-no {
  font-family: "JetBrains Mono", monospace;
  color: #97b4de;
  font-weight: 700;
  font-size: 16px; /* 序号字体加大 */
}

.algo-title-text {
  font-size: 1.5rem; /* 标题字体加大 */
  color: #141c2f; /* 颜色加深 */
  margin: 0;
  font-weight: 700;
  line-height: 1.2;
}

/* 4. 公式区域 (字体加大) */
.algo-formula-zone {
  background: #f1f5f9;
  padding: 18px 24px;
  border-radius: 12px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #e2e8f0;
}

.formula-code {
  font-family: "JetBrains Mono", monospace;
  font-size: 1.2rem;
  color: #2563eb;
  font-weight: 700;
  letter-spacing: 1px;
}

.steps-tag {
  font-size: 12px;
  color: #64748b;
  font-weight: 800;
  background: #ffffff;
  padding: 4px 8px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

/* 5. 识别技巧 (自动撑开，底部对齐) */
.algo-recognition-box {
  flex: 1; /* 自动占据剩余空间 */
  margin-bottom: 20px;
}

.rec-label {
  font-size: 16px;
  color: #94a3b8;
  font-weight: 800;
  letter-spacing: 1px;
  margin-bottom: 12px;
}

.rec-list li {
  font-size: 16px;
  color: #475569;
  margin-bottom: 10px;
  line-height: 1.6;
  position: relative;
  padding-left: 20px;
}

.algo-card-footer {
  margin-top: auto;
  padding-top: 15px;
  border-top: 1px solid #f1f5f9;
}
.view-demo-link {
  color: #94a3b8;
  font-size: 16px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 6px;
}
.algo-3d-card:hover .view-demo-link {
  color: #3b82f6;
}

/*------------ 弹窗及控制器样式 ---------------*/
/* 1. 弹窗容器去边框、加模糊 */
:deep(.immersive-dialog) {
  border-radius: 28px;
  overflow: hidden;
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.95); /* 稍微不透明一点，保证阅读 */
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 40px 100px rgba(0, 0, 0, 0.2);
}

:deep(.el-dialog__header) {
  margin-right: 0;
  padding: 20px 24px 10px;
}

/* 2. 头部样式 */
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
  text-transform: uppercase;
}
.dialog-header-custom h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #0f172a;
}

/* 3. 内容布局 */
.dialog-body {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 0 10px 20px;
}

/* 3D 视口 */
.cube-viewport {
  height: 360px; /* 稍微调小一点，适配 Learning 页面的紧凑感 */
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

/* 信息面板 */
.info-panel {
  padding: 0 10px;
}
.info-section {
  margin-bottom: 20px;
}
.info-label {
  font-size: 12px;
  font-weight: 800;
  color: #94a3b8;
  text-transform: uppercase;
  margin-bottom: 8px;
  display: block;
}

/* 大号公式栏 */
.big-formula-box {
  background: #f1f5f9;
  padding: 16px 20px;
  border-radius: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #e2e8f0;
}
.huge-mono {
  font-family: "JetBrains Mono", monospace;
  font-size: 1.25rem;
  color: #1e293b;
  font-weight: 800;
  word-break: break-all; /* 防止公式太长溢出 */
}
.copy-btn {
  background: white;
  border: 1px solid #e2e8f0;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  cursor: pointer;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.3s;
  flex-shrink: 0;
}
.copy-btn:hover {
  color: #3b82f6;
  border-color: #3b82f6;
}

.recog-desc {
  font-size: 1rem;
  color: #475569;
  line-height: 1.6;
}

/* 4. 底部按钮 (胶囊居中) */
.dialog-actions {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.primary-action-btn {
  min-width: 180px;
  height: 48px;
  padding: 0 30px;
  background: #3b82f6;
  border: none;
  border-radius: 100px;
  color: white;
  font-weight: 700;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
  box-shadow: 0 10px 20px rgba(59, 130, 246, 0.2);
}
.primary-action-btn:hover {
  background: #2563eb;
  transform: translateY(-3px);
  box-shadow: 0 15px 30px rgba(59, 130, 246, 0.3);
}
.primary-action-btn:active {
  transform: translateY(-1px);
}

/* 响应式兼容 */
@media (max-width: 1100px) {
  .cases-wrapper.grid-layout {
    grid-template-columns: 1fr;
  }
}
</style>
