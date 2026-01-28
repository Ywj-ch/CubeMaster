<template>
  <div class="learning-container">
    <el-container style="height: 100vh;">

      <!-- 1. 左侧导航栏 -->
      <el-aside width="260px" class="tutorial-sidebar">
        <div class="sidebar-header">
          <h2>魔方学院</h2>
          <p>从零开始的大师之路</p>
        </div>

        <el-menu
          :default-active="currentStepIndex.toString()"
          @select="handleSelect"
          class="sidebar-menu"
        >
          <el-menu-item
            v-for="(step, index) in tutorialData"
            :key="step.id"
            :index="index.toString()"
          >
            <span>{{ step.title }}</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 2. 右侧主内容区 -->
      <el-main class="tutorial-content">

        <!-- 章节标题区 -->
        <div class="step-header">
          <h1>{{ currentStep.title }}</h1>
          <p class="step-desc">{{ currentStep.description }}</p>
        </div>

        <el-divider />

        <!-- 遍历当前章节的所有“情况” -->
        <div v-for="(item, index) in currentStep.cases" :key="item.id" class="case-card">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <span class="case-title">情况 {{ index + 1 }}: {{ item.title }}</span>
              </div>
            </template>

            <el-row :gutter="20" align="middle">

              <!-- 左侧：文字讲解 -->
              <el-col :span="14">
                <div class="instruction-text">
                  <p>{{ item.description }}</p>

                  <div class="algorithm-box" v-if="item.algorithm">
                    <span class="label">公式:</span>
                    <code class="algo-text">{{ item.algorithm }}</code>
                    <!-- 绑定点击事件 -->
                    <el-button
                      type="primary"
                      circle
                      size="small"
                      :icon="VideoPlay"
                      class="play-btn"
                      @click="handlePlay(item.id)"
                    />
                  </div>

                  <el-alert
                    v-if="item.tips"
                    :title="item.tips"
                    type="warning"
                    :closable="false"
                    show-icon
                    style="margin-top: 15px;"
                  />
                </div>
              </el-col>

              <!-- 右侧：3D 演示区 (已替换占位符) -->
              <el-col :span="10">
                <div class="cube-container">
                  <!--
                    关键点：
                    1. :ref 动态绑定
                    2. 传入 setup 和 algorithm
                  -->
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

      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue';
import { tutorialData } from '../data/tutorials.js';
import { VideoPlay, Compass } from '@element-plus/icons-vue';
import TutorialCube from '../components/TutorialCube.vue';

// 当前选中的章节索引
const currentStepIndex = ref(0);

// 存储所有 TutorialCube 组件实例的字典 { caseId: componentInstance }
const cubeRefs = ref({});

// 动态设置 Ref 的函数 (Vue 3 v-for 写法)
const setCubeRef = (el, id) => {
  if (el) {
    cubeRefs.value[id] = el;
  }
};

// 计算属性：当前章节数据
const currentStep = computed(() => {
  return tutorialData[currentStepIndex.value];
});

// 切换章节
const handleSelect = (index) => {
  currentStepIndex.value = parseInt(index);
  // 切换章节时，清空旧的 ref 引用，防止内存泄漏（可选，Vue 会自动处理大部分）
  cubeRefs.value = {};
};

// 点击播放按钮
const handlePlay = (caseId) => {
  const cubeInstance = cubeRefs.value[caseId];
  if (cubeInstance) {
    // 调用 TutorialCube 暴露的 play 方法
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
}

.sidebar-header {
  padding: 20px;
  background: #2c3e50;
  color: white;
}
.sidebar-header h2 { margin: 0; font-size: 1.2rem; }
.sidebar-header p { margin: 5px 0 0; font-size: 0.8rem; opacity: 0.8; }

.tutorial-content {
  padding: 40px;
  overflow-y: auto;
}

.step-header h1 { color: #2c3e50; margin-bottom: 10px; }
.step-desc { color: #606266; font-size: 1.1rem; line-height: 1.6; margin-top: 15px; }

.orientation-tip { margin: 10px 0; }

.case-card { margin-bottom: 30px; }
.case-title { font-weight: bold; font-size: 1.1rem; }

.instruction-text p {
  line-height: 1.8;
  color: #303133;
  margin-bottom: 20px;
}

.algorithm-box {
  background-color: #ecf5ff;
  padding: 15px;
  border-radius: 8px;
  border-left: 5px solid #409eff;
  display: flex;
  align-items: center;
  gap: 15px;
}
.algo-text {
  font-family: 'Courier New', Courier, monospace;
  font-size: 1.2rem;
  font-weight: bold;
  color: #409eff;
  letter-spacing: 2px;
}

/* 魔方容器样式 */
.cube-container {
  width: 100%;
  height: 300px; /* 必须给高度，否则 Canvas 塌陷 */
  background-color: #f0f2f5; /* 浅灰底色，突显魔方 */
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #dcdfe6;
}
</style>