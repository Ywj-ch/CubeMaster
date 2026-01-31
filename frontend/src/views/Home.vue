<template>
  <div class="home-page-scroller">
    <!-- === 全局统一背景 (层级 z-0) === -->
    <div class="grid-background"></div>

    <!-- === Hero Section (层级 z-1) === -->
    <section class="hero-section-wrapper">
      <el-row :gutter="40" align="middle" class="hero-content">
        <!-- 左侧文本区 -->
        <el-col :xs="24" :md="12" class="text-side relative-position">
          <!-- 氛围光晕 -->
          <div class="text-glow"></div>

          <div class="badge-pill animate-entry delay-1">
            <span class="dot"></span> 赶工中 别急......
          </div>

          <h1 class="main-title animate-entry delay-2">
            <span class="gradient-text">解构魔方</span>
            <br />
            <span class="solid-text">重塑还原体验</span>
          </h1>

          <p class="sub-title animate-entry delay-3">
            告别复杂的公式记忆。集成
            <span class="highlight-tag">OpenCV</span> 视觉识别与
            <span class="highlight-tag">Kociemba</span> 算法，
            为您提供从状态捕捉到 3D 演示的一站式还原方案。
          </p>

          <div class="action-group animate-entry delay-4">
            <!-- Uiverse 主按钮 -->
            <button class="learn-more" @click="handleEnterSolver">
              <span class="circle" aria-hidden="true">
                <span class="icon arrow"></span>
              </span>
              <span class="button-text">立即求解</span>
            </button>

            <!-- Uiverse 次级按钮 -->
            <button
              class="secondary-btn-uiverse"
              @click="handleEnterPlayground"
            >
              <span class="btn-content">
                <el-icon class="btn-icon"><Pointer /></el-icon>
                自由练习
              </span>
            </button>
          </div>

          <div class="tech-badges animate-entry delay-5">
            <span class="tech-label">Powered by:</span>
            <el-tooltip content="Vue.js" placement="top">
              <img src="/icons/logo_vue.svg" class="tech-icon" alt="Vue" />
            </el-tooltip>
            <el-tooltip content="Three.js" placement="top">
              <img
                src="/icons/logo_threejs.svg"
                class="tech-icon"
                alt="Three"
              />
            </el-tooltip>
            <el-tooltip content="OpenCV" placement="top">
              <img
                src="/icons/logo_opencv.svg"
                class="tech-icon"
                alt="OpenCV"
              />
            </el-tooltip>
          </div>
        </el-col>

        <!-- 右侧 3D 魔方区 -->
        <el-col :xs="24" :md="12" class="cube-side animate-entry-right">
          <!-- 玻璃拟态容器 -->
          <div class="glass-card-wrap">
            <div class="cube-stage-3d">
              <Cube3DView
                :cubeState="homeCubeState"
                :interactive="false"
                :enableControls="true"
                :autoRotate="true"
                :autoRotateSpeed="1.5"
                :cameraPosition="[5, 5, 5]"
                :enableZoom="false"
              />
            </div>
          </div>
        </el-col>
      </el-row>
    </section>

    <!-- === Features Section === -->
    <section class="section-wrapper features-clean-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title animate-entry delay-2">不仅仅是求解器</h2>
          <p class="section-desc animate-entry delay-3">
            我们将硬核算法封装在极简交互之下
          </p>
        </div>

        <!-- === 扇形展开卡片容器 === -->
        <div class="features-spread-container animate-entry delay-4">
          <div
            v-for="(feat, idx) in features"
            :key="idx"
            class="feature-glass-card"
            :style="{ '--r': -15 + idx * 20 }"
          >
            <!-- 上半部分：文字内容 -->
            <div class="card-content-top">
              <h3>{{ feat.title }}</h3>
              <p>{{ feat.desc }}</p>
            </div>

            <!-- 下半部分：图标基座 -->
            <div class="card-icon-bottom">
              <div class="icon-wrapper" :class="feat.colorClass">
                <el-icon><component :is="feat.icon" /></el-icon>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- === Learning Section === -->
    <section class="section-wrapper learning-modern-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title animate-entry delay-1">
            构建你的魔方知识库
          </h2>
          <p class="section-desc animate-entry delay-2">
            从零基础到竞速玩家，这里有你需要的进阶路径
          </p>
        </div>

        <el-row :gutter="30" justify="center" class="animate-entry delay-3">
          <el-col
            :xs="24"
            :sm="12"
            :md="8"
            v-for="(course, i) in courses_data"
            :key="i"
          >
            <div class="course-modern-card" @click="course.action">
              <!-- 顶部装饰区 -->
              <div
                class="course-header"
                :style="{ '--glow-color': course.color }"
              >
                <div class="level-badge">{{ course.level }}</div>
                <div class="course-icon-box">
                  <el-icon><component :is="course.icon" /></el-icon>
                </div>
                <!-- 装饰光晕 -->
                <div class="inner-glow"></div>
              </div>

              <!-- 文字内容区 -->
              <div class="course-body">
                <h4>{{ course.title }}</h4>
                <p>{{ course.desc }}</p>

                <div class="course-footer">
                  <div class="meta-info">
                    <el-icon
                      ><Timer v-if="i === 0" /><Collection
                        v-else-if="i === 1" /><Unlock v-else
                    /></el-icon>
                    <span>{{ course.meta }}</span>
                  </div>
                  <button class="learn-arrow-btn">
                    <span>{{ course.btnText }}</span>
                    <el-icon class="arrow-icon"><ArrowRight /></el-icon>
                  </button>
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </section>

    <!-- === FAQ Section === -->
    <section class="section-wrapper faq-modern-section">
      <div class="container narrow">
        <!-- 标题：加入入场动画 -->
        <div class="section-header center animate-entry delay-1">
          <h2 class="section-title">常见问题</h2>
          <p class="section-desc">关于 CubeMaster，你想知道的都在这里</p>
        </div>

        <!-- 容器：移除默认边框 -->
        <div class="faq-list-container animate-entry delay-2">
          <el-collapse
            v-model="activeNames"
            accordion
            class="custom-modern-collapse"
          >
            <el-collapse-item
              v-for="(faq, index) in faqs"
              :key="faq.id"
              :name="faq.id"
              class="faq-item"
            >
              <!-- 自定义标题插槽：增加序号 -->
              <template #title>
                <div class="faq-header-content">
                  <span class="faq-index">0{{ index + 1 }}</span>
                  <span class="faq-question">{{ faq.title }}</span>
                </div>
              </template>

              <div class="faq-answer-content">
                {{ faq.content }}
              </div>
            </el-collapse-item>
          </el-collapse>
        </div>

        <!-- 底部“关于”链接 -->
        <div class="about-cta-wrapper animate-entry delay-3">
          <!-- 极简横线 -->
          <div class="footer-divider"></div>

          <div class="about-cta-content">
            <p>想要了解更多项目背后的故事？</p>
            <router-link to="/about" class="modern-about-link">
              查看关于页面 <el-icon><DArrowRight /></el-icon>
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Cube3DView from "../components/Cube3DView.vue";
import { createCubeFromJson } from "../utils/cubeState";

import {
  Camera,
  Pointer,
  ArrowRight,
  Reading,
  DataLine,
  Trophy,
  Timer,
  Collection,
  Unlock,
  DArrowRight,
  Monitor,
  Cpu,
  VideoPlay,
} from "@element-plus/icons-vue";

const router = useRouter();
const loading = ref(false);
const activeNames = ref("1");
const homeCubeState = ref(createCubeFromJson());

const handleEnterSolver = () => router.push("/solver");
const handleEnterPlayground = () => router.push("/cube");
const handleEnterLearningBasic = () => router.push("/learning/basic");
const handleEnterLearningLbl = () => router.push("/learning/lbl");
const handleEnterLearningCfop = () => router.push("/learning/cfop");

// === 1. 特性板块数据 (Features) ===
const features = [
  {
    title: "实时交互",
    desc: "物理魔方状态实时映射到 Web 端 3D 模型，零延迟的数字孪生体验。",
    icon: "Monitor",
    colorClass: "icon-blue",
  },
  {
    title: "智能算法",
    desc: "采用 Kociemba 二阶段算法，在 20 步之内解决任何打乱状态。",
    icon: "Cpu",
    colorClass: "icon-purple",
  },
  {
    title: "直观教学",
    desc: "抛弃晦涩的公式书。步骤分解演示，让逻辑清晰可见。",
    icon: "VideoPlay",
    colorClass: "icon-green",
  },
];

// === 2. 课程板块数据 (Learning) ===
const courses_data = [
  {
    title: "魔方基础结构与记号",
    level: "基础",
    desc: "了解中心块、棱块区别，掌握 U R F 等基础转动语言。",
    icon: "Reading",
    meta: "10分钟",
    btnText: "开始学习",
    color: "#3b82f6",
    action: handleEnterLearningBasic,
  },
  {
    title: "层先法 (LBL) 详解",
    level: "入门",
    desc: "最经典的七步还原法，无需大量公式，逻辑清晰易上手。",
    icon: "DataLine",
    meta: "7 章节",
    btnText: "查看课程",
    color: "#8b5cf6",
    action: handleEnterLearningLbl,
  },
  {
    title: "CFOP 高级算法",
    level: "进阶",
    desc: "世界纪录保持者都在用的速拧方法，F2L/OLL/PLL 全解析。",
    icon: "Trophy",
    meta: "待解锁",
    btnText: "开发中",
    color: "#f43f5e",
    action: handleEnterLearningCfop,
  },
];

// === 3、 FAQ 板块数据 ===
const faqs = [
  {
    id: "1",
    title: "识别魔方需要特殊的摄像头吗？",
    content:
      "不需要。使用电脑自带的摄像头即可。为了获得最佳效果，建议在光线均匀的环境下拍摄，避免魔方表面产生强烈反光。",
  },
  {
    id: "2",
    title: "为什么我的魔方总是识别失败？",
    content:
      "请检查是否有颜色贴纸破损或光线太暗。同时，CubeMaster 内置了手动修正功能，如果识别有误，您可以在 2D 展开图中点击色块进行手动调整。",
  },
  {
    id: "3",
    title: "自由练习模式支持计时吗？",
    content:
      "支持。自由探索模式集成了专业的计时器功能，您可以点击“开始挑战”来记录您的还原时间，并模拟真实的打乱过程。",
  },
  {
    id: "4",
    title: "这个项目是开源的吗？",
    content: "是的，这是一个基于 MIT 协议的开源项目。我们欢迎开发者参与贡献。",
  },
];

// === 核心逻辑：滚动触发动画 ===
onMounted(() => {
  const observerOptions = {
    threshold: 0.15, // 元素露出 15% 时触发
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        // 当元素进入视野，添加 is-visible 类触发 CSS 动画
        entry.target.classList.add("is-visible");
        // 触发后停止观察，保证动画只跑一次
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // 扫描所有需要入场动画的元素
  const animElements = document.querySelectorAll(
    ".animate-entry, .animate-entry-right",
  );
  animElements.forEach((el) => observer.observe(el));
});
</script>

<style scoped>
/* --- 全局布局与背景 --- */
.home-page-scroller {
  width: 100%;
  min-height: 100vh;
  position: relative;
  font-family:
    "Inter",
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Roboto,
    sans-serif;
  color: #0f172a;
  background-color: #f8fafc; /* 兜底背景色 */
}

/* 统一的大背景网格 */
.grid-background {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 0; /* 放在最底层 */
  background-image:
    linear-gradient(to right, #e2e8f0 1px, transparent 1px),
    linear-gradient(to bottom, #e2e8f0 1px, transparent 1px);
  background-size: 40px 40px;
  /* 径向遮罩：让网格在中心清晰，边缘淡出，避免死板 */
  -webkit-mask-image: radial-gradient(
    ellipse 80% 50% at 50% 0%,
    #000 70%,
    transparent 100%
  );
  mask-image: radial-gradient(
    ellipse 80% 50% at 50% 0%,
    #000 70%,
    transparent 100%
  );
  pointer-events: none;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* --- 通用 Section 设置 --- */
/* 关键：让 section 透明，从而显示底部的全局网格 */
.hero-section-wrapper,
.section-wrapper {
  position: relative;
  z-index: 1; /* 浮在网格之上 */
  background: transparent;
  padding: 120px 0;
}

/* Hero 特殊高度 */
.hero-section-wrapper {
  min-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 60px;
}

.hero-content {
  width: 100%;
  max-width: 1200px;
}

/* --- Hero 文本区域 --- */
.relative-position {
  position: relative;
}

/* 氛围光 */
.text-glow {
  position: absolute;
  top: -40%;
  left: -30%;
  width: 150%;
  height: 150%;
  background: radial-gradient(
    circle at center,
    rgba(59, 130, 246, 0.12) 0%,
    /* 稍微调低透明度 */ rgba(255, 255, 255, 0) 70%
  );
  filter: blur(90px);
  z-index: -1;
  pointer-events: none;
}

.badge-pill {
  display: inline-flex;
  align-items: center;
  padding: 6px 16px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 100px;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
  margin-bottom: 32px;
}
.dot {
  width: 8px;
  height: 8px;
  background: #2563eb;
  border-radius: 50%;
  margin-right: 8px;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
}

.main-title {
  font-size: 5rem;
  font-weight: 850;
  line-height: 1;
  margin-bottom: 32px;
  letter-spacing: -3px;
  color: #0f172a;
}

.gradient-text {
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
  padding-bottom: 10px;
}

.solid-text {
  display: block;
  margin-top: 5px;
}

.sub-title {
  font-size: 1.25rem;
  color: #475569;
  line-height: 1.7;
  max-width: 560px;
  margin-bottom: 50px;
  font-weight: 400;
}

.highlight-tag {
  background: #eff6ff;
  color: #7298ec;
  padding: 2px 6px;
  border-radius: 6px;
  font-weight: 600;
  font-family: monospace;
  border: 1px solid #dbeafe;
  margin: 0 2px;
}

.action-group {
  display: flex;
  gap: 20px;
  margin-bottom: 60px;
  align-items: center;
}

/* --- 底部 Logo --- */
.tech-badges {
  display: flex;
  align-items: center;
  gap: 20px;
  opacity: 0.5;
  transition: 0.3s;
}
.tech-badges:hover {
  opacity: 1;
}
.tech-label {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
}
.tech-icon {
  height: 26px;
  filter: grayscale(1);
  transition: 0.3s;
  opacity: 0.7;
}
.tech-icon:hover {
  filter: grayscale(0%);
  transform: scale(1.1);
  opacity: 1;
}

/* --- 3D 魔方容器 --- */
.cube-side {
  display: flex;
  justify-content: center;
  align-items: center;
  perspective: 1000px;
}

.glass-card-wrap {
  position: relative;
  width: 100%;
  max-width: 600px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 32px;
  box-shadow:
    0 20px 50px -12px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.5) inset;
  animation: float-card 6s ease-in-out infinite;
}
.cube-stage-3d {
  width: 100%;
  height: 500px;
}
@keyframes float-card {
  0%,
  100% {
    transform: translateY(0) rotateX(0);
  }
  50% {
    transform: translateY(-30px) rotateX(1deg);
  }
}

/* --- Section Headers --- */
.section-header {
  margin-bottom: 60px;
}
.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 16px;
  letter-spacing: -1px;
}
.section-desc {
  font-size: 1.15rem;
  color: #64748b;
}

/* --- Features Section 全局透明，显示大背景网格 --- */
.features-clean-section {
  background: transparent !important;
  padding: 160px 0; /* 增加上下留白，更有呼吸感 */
}

.features-spread-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 80px;
  height: 400px; /* 给展开留足空间 */
}

/* --- 核心卡片样式 --- */
.feature-glass-card {
  position: relative;
  width: 260px; /* 宽度增加，方便排版文字 */
  height: 320px; /* 高度增加 */

  /* 白玻璃材质 */
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 24px;

  /* 弥散阴影 */
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);

  display: flex;
  flex-direction: column;
  transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1);
  margin: 0 -60px; /* 初始重叠 */
  transform: rotate(calc(var(--r) * 1deg));
  cursor: pointer;
  overflow: hidden;
}

/* --- 悬浮展开逻辑 --- */
.features-spread-container:hover .feature-glass-card {
  transform: rotate(0deg) translateY(-20px); /* 变正并上浮 */
  margin: 0 20px; /* 间距拉开 */
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.1);
}

/* 单独悬浮某张卡片时再突出一点 */
.feature-glass-card:hover {
  transform: rotate(0deg) translateY(-40px) scale(1.05) !important;
  z-index: 100;
  border-color: #409eff;
}

/* --- 卡片内部排版 --- */

/* 1. 上部文字区 */
.card-content-top {
  flex: 1;
  padding: 30px 25px;
  text-align: left;
}

.card-content-top h3 {
  font-size: 1.4rem;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 15px;
  letter-spacing: -0.5px;
}

.card-content-top p {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #64748b;
  opacity: 0.8;
  transition: opacity 0.3s;
}

.feature-glass-card:hover .card-content-top p {
  opacity: 1;
}

/* 2. 下部图标条 (基座) */
.card-icon-bottom {
  height: 60px;
  background: rgba(64, 158, 255, 0.05); /* 极淡的主题色背景 */
  display: flex;
  justify-content: center;
  align-items: center;
  border-top: 1px solid rgba(255, 255, 255, 0.5);
  transition: all 0.3s;
}

.feature-glass-card:hover .card-icon-bottom {
  background: rgba(64, 158, 255, 0.1);
}

.icon-wrapper {
  font-size: 24px;
  display: flex;
  align-items: center;
  transition: transform 0.3s ease;
}

.feature-glass-card:hover .icon-wrapper {
  transform: scale(1.2);
}

/* 图标颜色 */
.icon-blue {
  color: #3b82f6;
}
.icon-purple {
  color: #8b5cf6;
}
.icon-green {
  color: #10b981;
}

/* 响应式：手机端取消扇形，恢复竖排 */
@media (max-width: 768px) {
  .features-spread-container {
    flex-direction: column;
    height: auto;
    gap: 30px;
  }
  .feature-glass-card {
    margin: 0 !important;
    transform: none !important;
    width: 100%;
  }
}

/* --- Learning Cards --- */
.learning-modern-section {
  background: transparent !important; /* 维持大背景连贯 */
  padding-bottom: 160px;
}

.course-modern-card {
  background: #ffffff;
  border-radius: 28px;
  border: 1px solid #f1f5f9;
  padding: 12px; /* 留出内边距，产生一种“嵌套”的高级感 */
  transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.course-modern-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.08);
  border-color: #e2e8f0;
}

/* 顶部装饰区 */
.course-header {
  height: 160px;
  background: #f8fafc;
  border-radius: 20px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.course-icon-box {
  font-size: 52px;
  color: var(--glow-color);
  z-index: 2;
  transition: transform 0.5s ease;
}

.course-modern-card:hover .course-icon-box {
  transform: scale(1.15) rotate(-5deg);
}

/* 核心特效：微光 */
.inner-glow {
  position: absolute;
  width: 100px;
  height: 100px;
  background: var(--glow-color);
  filter: blur(50px);
  opacity: 0.1;
  transition: opacity 0.5s;
}

.course-modern-card:hover .inner-glow {
  opacity: 0.25;
  width: 150px;
  height: 150px;
}

/* 等级标签 */
.level-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  padding: 4px 12px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(4px);
  border-radius: 100px;
  font-size: 11px;
  font-weight: 700;
  color: #64748b;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

/* 内容区 */
.course-body {
  padding: 24px 12px 12px 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.course-body h4 {
  font-size: 1.25rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 12px;
}

.course-body p {
  font-size: 0.95rem;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 24px;
}

/* 底部功能区 */
.course-footer {
  margin-top: auto;
  padding-top: 20px;
  border-top: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.meta-info {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #94a3b8;
  font-weight: 500;
}

/* “开始学习”按钮的微动效 */
.learn-arrow-btn {
  background: transparent;
  border: none;
  display: flex;
  align-items: center;
  gap: 4px;
  font-weight: 700;
  font-size: 14px;
  color: #0f172a;
  cursor: pointer;
  transition: all 0.3s;
}

.arrow-icon {
  transition: transform 0.3s;
}

.course-modern-card:hover .learn-arrow-btn {
  color: var(--glow-color);
}

.course-modern-card:hover .arrow-icon {
  transform: translateX(5px);
}

/* --- FAQ Section 整体布局 --- */
.faq-modern-section {
  background: transparent !important;
  padding-bottom: 80px;
}

.faq-list-container {
  max-width: 800px;
  margin: 0 auto;
}

/* --- 深度重塑 Element Collapse --- */
.custom-modern-collapse {
  border: none !important;
}

/* 每一个折叠项 */
:deep(.el-collapse-item) {
  margin-bottom: 10px;
  border-radius: 16px;
  transition: all 0.3s ease;
  overflow: hidden;
  border-bottom: 1px solid #f1f5f9 !important; /* 只保留极淡的底线 */
}

/* 悬停效果：背景微亮 */
:deep(.el-collapse-item:hover) {
  background-color: rgba(248, 250, 252, 0.8);
}

/* 移除 Element 默认的边框和背景 */
:deep(.el-collapse-item__header) {
  height: 80px;
  background-color: transparent !important;
  border: none !important;
  padding: 0 20px;
  transition: all 0.3s;
}

:deep(.el-collapse-item__wrap) {
  background-color: transparent !important;
  border: none !important;
}

/* 标题布局 */
.faq-header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.faq-index {
  font-family: "JetBrains Mono", monospace;
  font-weight: 800;
  font-size: 14px;
  color: #cbd5e1; /* 平时是淡灰色 */
  transition: color 0.3s;
}

.faq-question {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
}

/* 激活状态（展开时）的样式 */
:deep(.el-collapse-item.is-active) {
  background-color: #ffffff;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05);
  border-bottom-color: transparent !important;
}

:deep(.el-collapse-item.is-active) .faq-index {
  color: #2563eb; /* 展开时序号变蓝 */
}

:deep(.el-collapse-item.is-active) .faq-question {
  color: #2563eb;
}

/* 回答内容的排版 */
.faq-answer-content {
  padding: 0 20px 30px 54px; /* 54px 是为了对齐序号后的文字 */
  line-height: 1.8;
  color: #64748b;
  font-size: 1rem;
}

/* --- 底部关于区域 --- */
.about-cta-wrapper {
  margin-top: 40px; /* 距离 FAQ 更近一点 */
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 极简横线样式 */
.footer-divider {
  width: 100%;
  max-width: 1000px; /* 横线比文字宽很多，产生视觉分割感 */
  height: 1px;
  background: linear-gradient(
    to right,
    transparent,
    #c1c3c7 20%,
    #f1f5f9 80%,
    transparent
  ); /* 渐变消失的横线，更高级 */
  margin-bottom: 60px;
}

.about-cta-content {
  text-align: center;
}

.about-cta-content p {
  color: #94a3b8;
  margin-bottom: 16px;
  font-size: 15px;
  letter-spacing: 0.5px;
}

/* 移除之前的背景、边框、投影 */
.modern-about-link {
  color: #2563eb;
  text-decoration: none;
  font-weight: 700;
  font-size: 1.1rem;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  padding: 10px 20px;
  border-radius: 100px;
}

/* 悬浮时给一个非常淡的背景，增加点击感 */
.modern-about-link:hover {
  gap: 15px;
  background-color: rgba(37, 99, 235, 0.05);
  color: #1d4ed8;
}

/* --- Responsive --- */
@media (max-width: 992px) {
  .hero-content {
    flex-direction: column;
    text-align: center;
    padding-top: 60px;
  }
  .text-side {
    margin-bottom: 60px;
  }
  .action-group {
    justify-content: center;
  }
  .main-title {
    font-size: 3.5rem;
  }
  .glass-card-wrap {
    max-width: 100%;
    padding: 10px;
  }
  .cube-stage-3d {
    height: 350px;
  }
}

/* === Uiverse Buttons === */
button.learn-more {
  position: relative;
  display: inline-block;
  cursor: pointer;
  outline: none;
  border: 0;
  vertical-align: middle;
  text-decoration: none;
  background: transparent;
  padding: 0;
  font-size: inherit;
  font-family: inherit;
  width: 12rem;
  height: auto;
}
button.learn-more .circle {
  transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
  position: relative;
  display: block;
  margin: 0;
  width: 3rem;
  height: 3rem;
  background: #2563eb;
  border-radius: 1.625rem;
}
button.learn-more .circle .icon {
  transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
  position: absolute;
  top: 0;
  bottom: 0;
  margin: auto;
  background: #fff;
}
button.learn-more .circle .icon.arrow {
  transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
  left: 0.625rem;
  width: 1.125rem;
  height: 0.125rem;
  background: none;
}
button.learn-more .circle .icon.arrow::before {
  position: absolute;
  content: "";
  top: -0.25rem;
  right: 0.0625rem;
  width: 0.625rem;
  height: 0.625rem;
  border-top: 0.125rem solid #fff;
  border-right: 0.125rem solid #fff;
  transform: rotate(45deg);
}
button.learn-more .button-text {
  transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 0.75rem 0;
  margin: 0 0 0 1.85rem;
  color: #2563eb;
  font-weight: 700;
  line-height: 1.6;
  text-align: center;
  text-transform: uppercase;
}
button.learn-more:hover .circle {
  width: 100%;
}
button.learn-more:hover .circle .icon.arrow {
  background: #fff;
  transform: translate(1rem, 0);
}
button.learn-more:hover .button-text {
  color: #fff;
}

.secondary-btn-uiverse {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 3rem;
  padding: 0 24px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 1.625rem;
  color: #64748b;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}
.btn-content {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  z-index: 1;
}
.btn-icon {
  font-size: 1.1em;
  transition: transform 0.3s ease;
}
.secondary-btn-uiverse:hover {
  background: #fff;
  border-color: #cbd5e1;
  color: #2563eb;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}
.secondary-btn-uiverse:hover .btn-icon {
  transform: rotate(-15deg) scale(1.1);
}
.secondary-btn-uiverse:active {
  transform: translateY(0) scale(0.98);
  box-shadow: none;
}

/* === 入场动画系统 === */

/* 1. 定义动画关键帧 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
    filter: blur(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
    filter: blur(0);
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 2. 修改动画类：默认不执行动画，只设置初始隐藏状态 */
.animate-entry,
.animate-entry-right {
  opacity: 0;
  will-change: transform, opacity;
}

/* 3. 激活类：大幅度拉长时间，并使用更平滑的曲线 */
.animate-entry.is-visible {
  animation: fadeInUp 1s cubic-bezier(0.33, 1, 0.68, 1) forwards;
}

.animate-entry-right.is-visible {
  animation: fadeInRight 1s cubic-bezier(0.33, 1, 0.68, 1) forwards;
}

/* 4. 延迟梯度 */
.delay-1 {
  animation-delay: 0.5s;
}
.delay-2 {
  animation-delay: 1s;
}
.delay-3 {
  animation-delay: 1.5s;
}
.delay-4 {
  animation-delay: 2s;
}
.delay-5 {
  animation-delay: 2.5s;
}
</style>
