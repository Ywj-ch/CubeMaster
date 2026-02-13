<template>
  <div class="about-page-scroller">
    <!-- === 全局统一背景 === -->
    <div class="grid-background"></div>

    <!-- === 1. Hero Section === -->
    <section class="hero-section" v-animate>
      <div class="glow-bg glow-top-right"></div>
      <div class="glow-bg glow-bottom-left"></div>

      <div class="hero-content">
        <div class="badge-pill">
          <span class="pulse-dot"></span>
          <span>开发历程与技术架构</span>
        </div>

        <h1 class="hero-title">
          CubeMaster 项目
          <br />
          <span class="gradient-text">技术演进全记录</span>
        </h1>

        <p class="hero-subtitle">
          一个集计算机视觉识别、智能求解算法与3D交互教学于一体的现代化魔方应用。
          本页面记录从零到一的完整开发历程、技术架构与设计理念。
        </p>

        <!-- 统计数据胶囊 -->
        <div class="stats-pills">
          <div class="stat-pill">
            <span class="dot-indicator blue"></span>
            <span>70+ 天开发周期</span>
          </div>
          <div class="stat-pill">
            <span class="dot-indicator green"></span>
            <span>150+ 次代码提交</span>
          </div>
          <div class="stat-pill">
            <span class="dot-indicator purple"></span>
            <span>全栈分离架构</span>
          </div>
        </div>
      </div>
    </section>

    <!-- === 2. 开发历程时间轴 === -->
    <section class="section-block" v-animate>
      <h2 class="section-heading">开发历程时间轴</h2>
      <p class="section-sub">从项目初始化到功能完善的完整记录</p>

      <div class="roadmap-wrapper">
        <!-- 贯穿线 -->
        <div class="roadmap-line"></div>

        <!-- 时间轴节点 -->
        <div
          v-for="(milestone, index) in milestones"
          :key="index"
          class="roadmap-node"
        >
          <div class="node-marker">
            <div class="marker-circle">{{ milestone.icon }}</div>
          </div>

          <div class="node-card">
            <div class="card-header">
              <div class="header-left">
                <h3 class="step-title">{{ milestone.title }}</h3>
                <span class="step-date">{{ milestone.date }}</span>
              </div>
            </div>
            <div class="card-body">
              <p>{{ milestone.description }}</p>
              <div class="step-meta">
                <span class="meta-tag">{{ milestone.phase }}</span>
              </div>
              <div class="tech-tags" v-if="milestone.tech.length">
                <span
                  class="tech-tag"
                  v-for="tech in milestone.tech"
                  :key="tech"
                  >{{ tech }}</span
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- === 3. 技术文档导航 === -->
    <section class="section-block" v-animate>
      <h2 class="section-heading">深度技术文档</h2>
      <p class="section-sub">点击下方卡片深入理解项目核心技术原理</p>

      <div class="docs-grid">
        <div class="doc-card" @click="goToTechPage('yolo')">
          <div class="doc-icon">
            <img src="/icons/logo_yolov8.svg" alt="YOLOv8" />
          </div>
          <div class="doc-content">
            <h3>YOLOv8 视觉识别</h3>
            <p>深入解析卷积神经网络架构、特征金字塔网络与魔方颜色检测机制</p>
            <div class="doc-meta">
              <span class="doc-tag">计算机视觉</span>
              <span class="doc-tag">深度学习</span>
              <span class="doc-tag">目标检测</span>
            </div>
          </div>
          <div class="doc-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>

        <div class="doc-card" @click="goToTechPage('kociemba')">
          <div class="doc-icon">
            <img src="/icons/logo_kociemba.svg" alt="kociemba" />
          </div>
          <div class="doc-content">
            <h3>kociemba 二阶段算法</h3>
            <p>从群论基础到20步最优解，详解二阶段搜索、剪枝优化与性能分析</p>
            <div class="doc-meta">
              <span class="doc-tag">算法设计</span>
              <span class="doc-tag">群论</span>
              <span class="doc-tag">搜索优化</span>
            </div>
          </div>
          <div class="doc-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>

        <div class="doc-card" @click="goToTechPage('threejs')">
          <div class="doc-icon">
            <img src="/icons/logo_threejs.svg" alt="Three.js" />
          </div>
          <div class="doc-content">
            <h3>Three.js 渲染引擎</h3>
            <p>3D魔方建模、材质系统、动画同步与交互式渲染管线全解析</p>
            <div class="doc-meta">
              <span class="doc-tag">WebGL</span>
              <span class="doc-tag">3D图形</span>
              <span class="doc-tag">交互设计</span>
            </div>
          </div>
          <div class="doc-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>

        <div class="doc-card" @click="goToTechPage('architecture')">
          <div class="doc-icon">
            <img src="/icons/logo_fastapi.svg" alt="System Architecture" />
          </div>
          <div class="doc-content">
            <h3>前后端架构设计</h3>
            <p>RESTful API 设计、状态同步机制、性能监控与测试框架详解</p>
            <div class="doc-meta">
              <span class="doc-tag">系统架构</span>
              <span class="doc-tag">API设计</span>
              <span class="doc-tag">性能优化</span>
            </div>
          </div>
          <div class="doc-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>
      </div>
    </section>

    <!-- === 4. 快速链接 === -->
    <section class="section-block" v-animate>
      <h2 class="section-heading">项目功能体验</h2>
      <p class="section-sub">立即体验项目的核心功能模块</p>

      <div class="quick-links">
        <div class="quick-link-card" @click="goToPage('/solver')">
          <div class="link-icon">
            <el-icon><MagicStick /></el-icon>
          </div>
          <div class="link-content">
            <h3>智能求解器</h3>
            <p>摄像头识别魔方状态，20步内自动求解并展示3D还原动画</p>
          </div>
        </div>

        <div class="quick-link-card" @click="goToPage('/learning')">
          <div class="link-icon">
            <el-icon><Reading /></el-icon>
          </div>
          <div class="link-content">
            <h3>魔方学习系统</h3>
            <p>从基础层先法到CFOP高级算法，完整的魔方教学体系</p>
          </div>
        </div>

        <div class="quick-link-card" @click="goToPage('/cube')">
          <div class="link-icon">
            <el-icon><Pointer /></el-icon>
          </div>
          <div class="link-content">
            <h3>自由练习模式</h3>
            <p>交互式3D魔方练习环境，支持计时、打乱与算法练习</p>
          </div>
        </div>
      </div>
    </section>

    <!-- === 5. 技术栈展示 === -->
    <section class="section-block" v-animate>
      <h2 class="section-heading">技术栈全景</h2>
      <div class="tech-stack-container">
        <div class="tech-category">
          <h3>前端技术</h3>
          <div class="tech-icons">
            <el-tooltip content="Vue.js 3" placement="top">
              <div class="tech-icon-item">
                <img src="/icons/logo_vue.svg" alt="Vue.js" />
                <span>Vue 3</span>
              </div>
            </el-tooltip>
            <el-tooltip content="Three.js" placement="top">
              <div class="tech-icon-item">
                <img src="/icons/logo_threejs.svg" alt="Three.js" />
                <span>Three.js</span>
              </div>
            </el-tooltip>
            <el-tooltip content="Element Plus" placement="top">
              <div class="tech-icon-item">
                <img src="/icons/logo_elementplus.svg" alt="Element Plus" />
                <span>Element Plus</span>
              </div>
            </el-tooltip>
            <el-tooltip content="Vite" placement="top">
              <div class="tech-icon-item">
                <img src="/icons/logo_vite.svg" alt="Vite" />
                <span>Vite</span>
              </div>
            </el-tooltip>
          </div>
        </div>

        <div class="tech-category">
          <h3>后端技术</h3>
          <div class="tech-icons">
            <el-tooltip content="FastAPI" placement="top">
              <div class="tech-icon-item">
                <img src="/icons/logo_fastapi.svg" alt="FastAPI" />
                <span>FastAPI</span>
              </div>
            </el-tooltip>
            <el-tooltip content="PyTorch + YOLOv8" placement="top">
              <div class="tech-icon-item">
                <img src="/icons/logo_yolov8.svg" alt="YOLOv8" />
                <span>YOLOv8</span>
              </div>
            </el-tooltip>
            <el-tooltip content="kociemba算法" placement="top">
              <div class="tech-icon-item">
                <img src="/icons/logo_kociemba.svg" alt="kociemba" />
                <span>kociemba</span>
              </div>
            </el-tooltip>
            <el-tooltip content="Python 3.8+" placement="top">
              <div class="tech-icon-item">
                <img src="/icons/logo_python.svg" alt="Python" />
                <span>Python</span>
              </div>
            </el-tooltip>
          </div>
        </div>
      </div>
    </section>

    <!-- === 6. 常见问题 (FAQ) === -->
    <section class="section-block" v-animate>
      <h2 class="section-heading text-center">常见问题</h2>
      <div class="faq-container">
        <el-collapse
          v-model="activeFaqName"
          accordion
          class="custom-modern-collapse"
        >
          <el-collapse-item
            v-for="(faq, index) in faqs"
            :key="faq.id"
            :name="faq.id"
            class="faq-item"
          >
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
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import {
  ArrowRight,
  ElementPlus,
  MagicStick,
  Reading,
  Pointer,
} from "@element-plus/icons-vue";

const router = useRouter();

// --- 自定义指令：滚动入场动画 ---
const vAnimate = {
  mounted: (el) => {
    el.classList.add("before-enter");
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            el.classList.add("enter");
            observer.unobserve(el);
          }
        });
      },
      { threshold: 0.1 },
    );
    observer.observe(el);
  },
};

// --- 开发历程数据 ---
const milestones = [
  {
    date: "2025-12-03",
    icon: "🚀",
    title: "项目初始化",
    phase: "基础搭建",
    description:
      "完成项目结构初始化，确立前后端分离架构。创建基础工程结构、配置开发环境，为后续开发奠定基础。",
    tech: ["Vue 3", "FastAPI", "Python"],
  },
  {
    date: "2025-12-22",
    icon: "🏗️",
    title: "前后端分离架构",
    phase: "架构设计",
    description:
      "引入Vue3 + Vite构建前端，后端通过API提供魔方求解服务。建立前后端通信机制，实现基础数据流。",
    tech: ["Vite", "RESTful API", "CORS"],
  },
  {
    date: "2026-01-01",
    icon: "🎨",
    title: "3D魔方建模与渲染",
    phase: "核心功能",
    description:
      "完成3D魔方建模、渲染与还原流程。实现Cube3DView组件，支持原子化旋转动画和矩阵烘焙。",
    tech: ["Three.js", "WebGL", "动画系统"],
  },
  {
    date: "2026-01-22",
    icon: "🔍",
    title: "YOLOv8视觉识别集成",
    phase: "AI能力",
    description:
      "集成YOLOv8识别模型，实现魔方状态自动识别。重构3D交互组件，建立视觉识别全链路。",
    tech: ["YOLOv8", "OpenCV", "PyTorch"],
  },
  {
    date: "2026-01-28",
    icon: "📚",
    title: "学习模块框架搭建",
    phase: "教学系统",
    description:
      "完成学习模块框架，封装TutorialCube组件，实现层先法教学，建立算法教学体系。",
    tech: ["组件封装", "算法教学", "交互设计"],
  },
  {
    date: "2026-02-05",
    icon: "⚡",
    title: "CFOP高级算法库",
    phase: "进阶功能",
    description:
      "新增CFOP简介独立页面，完成OLL/PLL算法库录入，重构通用算法教学框架。",
    tech: ["CFOP", "算法库", "UI美化"],
  },
  {
    date: "2026-02-13",
    icon: "🧪",
    title: "测试框架与性能优化",
    phase: "质量保障",
    description:
      "后端添加API健康检查与测试框架，前端优化交互逻辑，完善项目文档与开发指南。",
    tech: ["pytest", "性能监控", "文档完善"],
  },
];

// --- FAQ 数据 ---
const activeFaqName = ref("1");
const faqs = [
  {
    id: "1",
    title: "CubeMaster 是什么项目？",
    content:
      "CubeMaster 是一个集计算机视觉识别、智能求解算法与3D交互教学于一体的现代化魔方应用。它能够通过摄像头识别魔方状态，使用Kociemba两阶段算法在20步内求解，并通过Three.js展示3D还原动画。",
  },
  {
    id: "2",
    title: "这个项目使用了哪些核心技术？",
    content:
      "前端使用Vue 3 + Three.js实现3D交互界面；后端使用FastAPI + PyTorch + YOLOv8进行魔方颜色识别；求解核心采用Kociemba两阶段算法；全栈采用前后端分离架构，通过RESTful API通信。",
  },
  {
    id: "3",
    title: "项目开发了多长时间？",
    content:
      "项目从2025年12月初开始，到2026年2月中旬基本完成核心功能，历时约70天。期间进行了多次架构重构和功能迭代，形成了当前稳定版本。",
  },
  {
    id: "4",
    title: "魔方识别准确率如何？",
    content:
      "经过200张标注图像的训练，YOLOv8模型在验证集上达到98.2%的准确率。在实际使用中，配合图像预处理和颜色空间验证，能够稳定识别各种光照条件下的魔方状态。",
  },
  {
    id: "5",
    title: "求解算法为什么选择Kociemba？",
    content:
      "Kociemba两阶段算法能够在平均20步内求解任意魔方状态，求解时间小于0.1秒，相比Thistlethwaite四阶段算法更高效，相比IDA*算法更快速，是实时求解的理想选择。",
  },
  {
    id: "6",
    title: "这个项目适合魔方初学者吗？",
    content:
      "完全适合！项目包含完整的魔方教学系统，从基础的层先法到高级的CFOP算法都有详细教程。同时，智能求解器可以帮助初学者验证自己的解法，3D演示功能可以直观展示还原步骤。",
  },
];

const goToTechPage = (page) => {
  router.push(`/tech/${page}`);
};

const goToPage = (path) => {
  router.push(path);
};

// --- 滚动动画初始化 ---
onMounted(() => {
  const observerOptions = { threshold: 0.15 };
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  const animElements = document.querySelectorAll(
    ".animate-entry, .animate-entry-right",
  );
  animElements.forEach((el) => observer.observe(el));
});
</script>

<style scoped>
/* --- 全局布局与背景 --- */
.about-page-scroller {
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
  background-color: #f8fafc;
}

/* 统一的大背景网格 */
.grid-background {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 0;
  pointer-events: none;

  --color: #e1e1e1;
  background-color: #f3f3f3;
  background-image:
    linear-gradient(
      0deg,
      transparent 24%,
      var(--color) 25%,
      var(--color) 26%,
      transparent 27%,
      transparent 74%,
      var(--color) 75%,
      var(--color) 76%,
      transparent 77%,
      transparent
    ),
    linear-gradient(
      90deg,
      transparent 24%,
      var(--color) 25%,
      var(--color) 26%,
      transparent 27%,
      transparent 74%,
      var(--color) 75%,
      var(--color) 76%,
      transparent 77%,
      transparent
    );
  background-size: 55px 55px;

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
}

/* --- 通用 Section 设置 --- */
.section-block {
  position: relative;
  z-index: 1;
  background: transparent;
  padding: 100px 0;
  max-width: 1200px;
  margin: 0 auto;
}

.section-heading {
  font-size: 2.5rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 20px;
  letter-spacing: -1px;
}

.section-sub {
  font-size: 1.15rem;
  color: #64748b;
  margin-bottom: 40px;
}

.text-center {
  text-align: center;
}

/* --- 1. Hero Section --- */
.hero-section {
  position: relative;
  min-height: calc(100vh - 160px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 24px;
  z-index: 1;
}

.glow-bg {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.2;
  z-index: -1;
}

.glow-top-right {
  top: -100px;
  right: -100px;
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
}

.glow-bottom-left {
  bottom: -100px;
  left: -100px;
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #10b981, #3b82f6);
}

.hero-content {
  max-width: 800px;
  text-align: center;
  z-index: 2;
}

.badge-pill {
  display: inline-flex;
  align-items: center;
  padding: 8px 20px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 100px;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 32px;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background: #2563eb;
  border-radius: 50%;
  margin-right: 10px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.hero-title {
  font-size: 4rem;
  font-weight: 850;
  line-height: 1.1;
  margin-bottom: 24px;
  letter-spacing: -2px;
  color: #0f172a;
}

.gradient-text {
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #475569;
  line-height: 1.7;
  max-width: 600px;
  margin: 0 auto 40px;
}

.stats-pills {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.stat-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 100px;
  font-size: 14px;
  font-weight: 600;
  color: #475569;
}

.dot-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot-indicator.blue {
  background: #3b82f6;
}
.dot-indicator.green {
  background: #10b981;
}
.dot-indicator.purple {
  background: #8b5cf6;
}

/* --- 2. 时间轴样式 --- */
.roadmap-wrapper {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  padding-left: 40px;
}

.roadmap-line {
  position: absolute;
  left: 19px;
  top: 20px;
  bottom: 20px;
  width: 2px;
  background: #e2e8f0;
  z-index: 0;
}

.roadmap-node {
  position: relative;
  margin-bottom: 40px;
  cursor: default;
}

.roadmap-node:last-child {
  margin-bottom: 0;
}

.roadmap-node:hover {
  cursor: default;
}

.roadmap-node:hover .marker-circle {
  border-color: #3b82f6;
  color: #3b82f6;
  transform: scale(1.1);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.roadmap-node:hover .node-card {
  border-color: #3b82f6;
  transform: translateX(10px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.node-marker {
  position: absolute;
  left: -40px;
  top: 24px;
  width: 40px;
  display: flex;
  justify-content: center;
  z-index: 1;
}

.marker-circle {
  width: 40px;
  height: 40px;
  background: #fff;
  border: 2px solid #e2e8f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 18px;
  color: #94a3b8;
  transition: all 0.3s;
}

.node-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 24px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.step-title {
  font-size: 1.25rem;
  font-weight: 800;
  margin: 0;
  color: #1e293b;
}

.step-date {
  font-size: 14px;
  color: #94a3b8;
  font-weight: 500;
}

.card-body p {
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 16px;
}

.step-meta {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.meta-tag {
  background: #f8fafc;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 13px;
  color: #64748b;
  font-weight: 600;
}

.meta-tag.highlight {
  background: #eff6ff;
  color: #2563eb;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.tech-tag {
  background: #f1f5f9;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  color: #475569;
  font-weight: 500;
}

/* --- 3. 技术文档导航 --- */
.docs-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
  margin-top: 40px;
}

.doc-card {
  background: #ffffff;
  border: 1px solid #f1f5f9;
  border-radius: 20px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
  position: relative;
}

.doc-card:hover {
  border-color: #3b82f6;
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.08);
}

.doc-card:hover .doc-arrow {
  opacity: 1;
  transform: translateX(5px);
}

.doc-icon {
  min-width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border-radius: 12px;
}

.doc-icon img {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.doc-content {
  flex: 1;
}

.doc-content h3 {
  font-size: 1.25rem;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 8px;
}

.doc-content p {
  color: #64748b;
  line-height: 1.5;
  font-size: 0.95rem;
  margin-bottom: 12px;
}

.doc-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.doc-tag {
  background: #f1f5f9;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  color: #475569;
  font-weight: 600;
}

.doc-arrow {
  opacity: 0;
  color: #3b82f6;
  transition: all 0.3s;
}

/* --- 4. 快速链接 --- */
.quick-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-top: 40px;
}

.quick-link-card {
  background: #ffffff;
  border: 1px solid #f1f5f9;
  border-radius: 16px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s;
}

.quick-link-card:hover {
  border-color: #3b82f6;
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
}

.link-icon {
  font-size: 32px;
  color: #3b82f6;
  margin-bottom: 16px;
}

.link-content h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.link-content p {
  color: #64748b;
  font-size: 0.9rem;
  line-height: 1.5;
}

/* --- 5. 技术栈展示 --- */
.tech-stack-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 40px;
  margin-top: 40px;
}

.tech-category {
  background: #ffffff;
  border: 1px solid #f1f5f9;
  border-radius: 20px;
  padding: 32px;
}

.tech-category h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f1f5f9;
}

.tech-icons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.tech-icon-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
  transition: all 0.3s;
  cursor: default;
}

.tech-icon-item:hover {
  background: #eff6ff;
  transform: translateY(-4px);
}

.tech-icon-item img {
  width: 40px;
  height: 40px;
}

.tech-icon-item .el-icon {
  font-size: 40px;
  color: #3b82f6;
}

.tech-icon-item span {
  font-size: 14px;
  font-weight: 600;
  color: #475569;
}

.tech-text {
  font-size: 40px;
}

/* --- 6. FAQ 样式 --- */
.faq-container {
  max-width: 800px;
  margin: 0 auto;
}
.custom-modern-collapse {
  border: none !important;
}

:deep(.el-collapse-item) {
  margin-bottom: 10px;
  border-radius: 16px;
  transition: all 0.3s ease;
  overflow: hidden;
  border-bottom: 1px solid #f1f5f9 !important;
}

:deep(.el-collapse-item:hover) {
  background-color: rgba(248, 250, 252, 0.8);
}

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

.faq-header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.faq-index {
  font-family: "JetBrains Mono", monospace;
  font-weight: 800;
  font-size: 14px;
  color: #cbd5e1;
  transition: color 0.3s;
}

.faq-question {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
}

:deep(.el-collapse-item.is-active) {
  background-color: #ffffff;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05);
  border-bottom-color: transparent !important;
}

:deep(.el-collapse-item.is-active) .faq-index {
  color: #2563eb;
}

:deep(.el-collapse-item.is-active) .faq-question {
  color: #2563eb;
}

.faq-answer-content {
  padding: 0 20px 30px 54px;
  line-height: 1.8;
  color: #64748b;
  font-size: 1rem;
}

/* --- 7. 动画系统 --- */
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

.before-enter {
  opacity: 0;
  will-change: transform, opacity;
}

.enter {
  animation: fadeInUp 1s cubic-bezier(0.33, 1, 0.68, 1) forwards;
}

/* --- 8. 响应式设计 --- */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .section-heading {
    font-size: 2rem;
  }

  .section-block {
    padding: 80px 24px;
  }

  .stats-pills {
    flex-direction: column;
    align-items: center;
  }

  .roadmap-wrapper {
    padding-left: 0;
  }

  .roadmap-line {
    display: none;
  }

  .node-marker {
    display: none;
  }

  .node-card {
    margin-left: 0;
  }

  .docs-grid,
  .quick-links,
  .tech-stack-container {
    grid-template-columns: 1fr;
  }

  .tech-icons {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }

  .section-heading {
    font-size: 1.75rem;
  }

  .doc-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .doc-icon {
    align-self: flex-start;
  }
}
</style>
