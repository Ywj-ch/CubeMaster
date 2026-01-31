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
          <!-- 添加 popper-class 以便自定义下拉菜单的样式 -->
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

        <!-- 菜单区域 -->
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
        <!-- 只有当前课程有步骤数据时才显示内容 -->
        <div v-if="currentStep">
          <!-- 章节标题区 -->
          <div class="step-header">
            <h1>{{ currentStep.title }}</h1>
            <p class="step-desc">{{ currentStep.description }}</p>
          </div>

          <el-divider />

          <!-- 遍历当前章节的所有“情况” -->
          <div
            v-for="(item, index) in currentStep.cases"
            :key="item.id"
            class="case-card"
          >
            <el-card shadow="hover" class="styled-card">
              <template #header>
                <div class="card-header">
                  <!-- 这里加上了 index+1 是为了区分情况1、情况2，这通常是保留的 -->
                  <el-tag effect="light" round style="margin-right: 10px"
                    >情况 {{ index + 1 }}</el-tag
                  >
                  <span class="case-title">{{ item.title }}</span>
                </div>
              </template>

              <el-row :gutter="30" align="middle">
                <!-- 左侧：文字讲解 -->
                <el-col :span="14">
                  <div class="instruction-text">
                    <p>{{ item.description }}</p>

                    <div class="algorithm-box" v-if="item.algorithm">
                      <div class="algo-content">
                        <span class="label">公式:</span>
                        <code class="algo-text">{{ item.algorithm }}</code>
                      </div>
                      <!-- 绑定点击事件 -->
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

                <!-- 右侧：3D 演示区 -->
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

        <!-- 空状态 -->
        <div v-else class="empty-state">
          <el-empty description="该课程内容正在开发中，敬请期待..." />
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { VideoPlay } from "@element-plus/icons-vue";
import { courseList } from "../data/courses.js";
import TutorialCube from "../components/TutorialCube.vue";

// 引入路由钩子
const route = useRoute();
const router = useRouter();

// --- 状态定义 ---

// 1. 初始化当前课程 ID：优先从路由参数获取，如果没有则取列表第一个
// 注意：路由守卫通常会保证 params.courseId 存在且有效
const currentCourseId = ref(route.params.courseId || courseList[0]?.id);

const currentStepIndex = ref(0);
const cubeRefs = ref({});

// --- 计算属性 ---

const currentCourse = computed(() => {
  return (
    courseList.find((c) => c.id === currentCourseId.value) || courseList[0]
  );
});

const currentSteps = computed(() => {
  return currentCourse.value.steps || [];
});

const currentStep = computed(() => {
  if (!currentSteps.value || currentSteps.value.length === 0) return null;
  return currentSteps.value[currentStepIndex.value];
});

// --- 监听器 ---

// 监听路由参数变化 (例如点击浏览器前进/后退，或通过下拉框跳转)
watch(
  () => route.params.courseId,
  (newId) => {
    // 只有当 ID 真的改变且有效时才更新
    if (newId && newId !== currentCourseId.value) {
      currentCourseId.value = newId;
      // 切换课程后，重置到第一章，并清空魔方实例引用
      currentStepIndex.value = 0;
      cubeRefs.value = {};
      // 滚动回顶部
      document.querySelector(".tutorial-content")?.scrollTo(0, 0);
    }
  },
);

// --- 方法 ---

const setCubeRef = (el, id) => {
  if (el) {
    cubeRefs.value[id] = el;
  }
};

// 修改：下拉框切换课程时，触发路由跳转
// 路由跳转会触发上面的 watch，从而更新 currentCourseId 和界面
const handleCourseChange = (newId) => {
  router.push({ name: "Learning", params: { courseId: newId } });
};

const handleSelectStep = (index) => {
  currentStepIndex.value = parseInt(index);
  cubeRefs.value = {};
  document.querySelector(".tutorial-content")?.scrollTo(0, 0);
};

const handlePlay = (caseId) => {
  const cubeInstance = cubeRefs.value[caseId];
  if (cubeInstance) {
    cubeInstance.play();
  } else {
    console.warn(`未找到 ID 为 ${caseId} 的魔方实例`);
  }
};
</script>

<style scoped>
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

/* --- 侧边栏头部 (深色背景) --- */
.sidebar-header {
  padding: 24px 20px;
  background: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
  gap: 15px;
  flex-shrink: 0; /* 防止被挤压 */
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

/* --- 下拉框样式定制 (核心修改) --- */
.course-select {
  width: 100%;
}

/* 强制修改 Element Plus 输入框背景为半透明 */
:deep(.el-select__wrapper) {
  background-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.2) inset; /* 使用 box-shadow 模拟边框 */
  color: white;
}

:deep(.el-select__wrapper:hover) {
  background-color: rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.5) inset;
}

:deep(.el-select__wrapper.is-focused) {
  box-shadow: 0 0 0 1px #409eff inset !important;
}

/* 修改下拉框内的文字颜色和占位符颜色 */
:deep(.el-select__selected-item),
:deep(.el-select__placeholder) {
  color: white !important;
}

/* 下拉箭头颜色 */
:deep(.el-select__suffix) {
  color: rgba(255, 255, 255, 0.7);
}

/* --- 侧边栏菜单 --- */
.sidebar-menu {
  border-right: none;
}

/* 选中项高亮样式 */
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

/* --- 主内容区 --- */
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

/* --- 卡片区域 --- */
.case-card {
  margin-bottom: 35px;
}

.styled-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
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

.instruction-text p {
  line-height: 1.8;
  color: #303133;
  margin-bottom: 25px;
  font-size: 1.05rem;
}

/* 公式盒子优化 */
.algorithm-box {
  background-color: #f4f4f5;
  padding: 15px 20px;
  border-radius: 8px;
  border-left: 5px solid #909399; /* 默认灰色，下面 hover 变色 */
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

/* 魔方容器 */
.cube-container {
  width: 100%;
  height: 320px;
  background-color: #eaeff5; /* 更柔和的底色 */
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
</style>
