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
            v-model="currentCourseId"
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
                          size="small"
                          effect="dark"
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
                      <el-icon><VideoPlay /></el-icon> 查看3D演示
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

      <!-- [新增] 3D 算法演示弹窗 -->
      <el-dialog
        v-model="demoVisible"
        title="3D 算法演示"
        width="620px"
        destroy-on-close
        align-center
      >
        <div class="demo-dialog-content">
          <div class="demo-cube-box">
            <!-- 只有弹窗打开时才渲染，节省性能 -->
            <TutorialCube
              v-if="demoVisible"
              ref="demoCubeRef"
              :setup="currentDemoItem.setup"
              :algorithm="currentDemoItem.algorithm"
            />
            <div class="demo-controls-overlay">
              <el-button
                type="primary"
                size="large"
                circle
                :icon="VideoPlay"
                class="demo-play-btn"
                @click="handleDemoPlay"
              />
            </div>
          </div>
          <div class="demo-info">
            <h3>{{ currentDemoItem.title }}</h3>
            <code class="big-formula">{{ currentDemoItem.algorithm }}</code>
            <p class="demo-tip">{{ currentDemoItem.tips }}</p>
          </div>
        </div>
      </el-dialog>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { VideoPlay, Picture, Select } from "@element-plus/icons-vue";
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
  currentStepIndex.value = 0;
  router.push({ name: "Learning", params: { courseId: newId } });
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

/* ==================== 2. 修正后的新增样式 (仅针对网格与进阶卡片) ==================== */

/* 强制两列布局容器 */
.cases-wrapper.grid-layout {
  display: grid;
  /* 强制锁定为 2 列，不再使用 auto-fill 避免挤出第三列 */
  grid-template-columns: 1fr 1fr;
  /* 让同一行的卡片自动等高，解决内容多撑开不一致的问题 */
  grid-auto-rows: 1fr;
  gap: 32px;
  width: 100%;
}

/* 进阶算法卡片主体：去重叠、明亮化 */
.algo-3d-card {
  width: 100%;
  /* 确保占据 grid 分配的所有高度 */
  height: 100%;
  /* 彻底移除导致重叠的负边距 */
  margin: 0 !important;
  background: #ffffff; /* 改为明亮主题 */
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 28px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  box-sizing: border-box;
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
  gap: 20px;
  align-items: center;
  margin-bottom: 20px;
}
.algo-thumb-box {
  background: #f8fafc;
  padding: 10px;
  border-radius: 12px;
  border: 1px solid #edf2f7;
}
.algo-title-text {
  font-size: 1.25rem;
  color: #1e293b;
  margin: 5px 0 0 0;
  font-weight: 800;
}
.algo-no {
  font-family: "JetBrains Mono", monospace;
  color: #94a3b8;
  font-weight: 700;
  font-size: 12px;
  margin-right: 10px;
}

.algo-formula-zone {
  background: #eff6ff; /* 浅蓝色块 */
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #dbeafe;
}
.formula-code {
  font-family: "JetBrains Mono", monospace;
  font-size: 1rem;
  color: #2563eb;
  font-weight: 700;
}
.steps-tag {
  font-size: 10px;
  color: #64748b;
  font-weight: 800;
}

/* 识别技巧：确保撑开空间实现底部对齐 */
.algo-recognition-box {
  flex: 1; /* 关键：自动伸缩，确保 footer 在最下方 */
  margin-bottom: 15px;
}
.rec-label {
  font-size: 11px;
  color: #94a3b8;
  font-weight: 800;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.rec-list {
  padding: 0;
  margin: 0;
  list-style: none;
}
.rec-list li {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 8px;
  position: relative;
  padding-left: 18px;
  line-height: 1.4;
}
.rec-list li::before {
  content: "→";
  position: absolute;
  left: 0;
  color: #3b82f6;
}

.algo-card-footer {
  margin-top: auto;
  padding-top: 15px;
  border-top: 1px solid #f1f5f9;
}
.view-demo-link {
  color: #94a3b8;
  font-size: 13px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 6px;
}
.algo-3d-card:hover .view-demo-link {
  color: #3b82f6;
}

/* 弹窗及控制器 */
.demo-cube-box {
  height: 380px;
  background-color: #f0f2f5;
  border-radius: 16px;
  border: 1px solid #dcdfe6;
  overflow: hidden;
  position: relative;
}
.demo-controls-overlay {
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 100;
}
.demo-play-btn {
  width: 56px !important;
  height: 56px !important;
  font-size: 24px;
  box-shadow: 0 4px 20px rgba(37, 99, 235, 0.4) !important;
}
.demo-info {
  text-align: center;
  margin-top: 20px;
}
.big-formula {
  font-size: 20px;
  font-weight: bold;
  font-family: "JetBrains Mono", monospace;
  color: #2563eb;
  background: #eff6ff;
  padding: 12px 24px;
  border-radius: 10px;
  display: inline-block;
  margin: 15px 0;
}

/* 响应式兼容 */
@media (max-width: 1100px) {
  .cases-wrapper.grid-layout {
    grid-template-columns: 1fr;
  }
}
</style>
