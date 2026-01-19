<template>
  <div class="home-page-scroller">
    <section class="hero-section-wrapper">
      <div class="hero-bg-shape"></div>
      <el-row :gutter="40" align="middle" class="hero-content">
        <el-col :xs="24" :md="12" class="text-side">
          <div class="badge-pill">
            <span class="dot"></span> 赶工中 别急......
          </div>
          <h1 class="main-title">
            <span class="gradient-text">解构魔方</span>
            <span class="block-text">重塑还原体验</span>
          </h1>
          <p class="sub-title">
            告别复杂的公式记忆。集成 <b>OpenCV</b> 视觉识别与 <b>Kociemba</b> 算法，
            为您提供从状态捕捉到 3D 演示的一站式还原方案。
          </p>

          <div class="action-group">
            <el-button type="primary" size="large" class="hero-btn primary-btn" :loading="loading" @click="handleEnterSolver">
              <el-icon class="mr-2"><Camera /></el-icon> 立即求解
            </el-button>
            <el-button size="large" class="hero-btn secondary-btn" @click="handleEnterPlayground">
              <el-icon class="mr-2"><Pointer /></el-icon> 自由练习
            </el-button>
          </div>

          <div class="tech-badges">
            <span class="tech-label">Powered by:</span>
            <el-tooltip content="前端框架" placement="top"><img src="/icons/logo_vue.svg" class="tech-icon"  alt="图标显示失败"/></el-tooltip>
            <el-tooltip content="3D 渲染引擎" placement="top"><img src="/icons/logo_threejs.svg" class="tech-icon"  alt="图标显示失败"/></el-tooltip>
            <el-tooltip content="计算机视觉" placement="top"><img src="/icons/logo_opencv.svg" class="tech-icon"  alt="图标显示失败"/></el-tooltip>
          </div>
        </el-col>

        <el-col :xs="24" :md="12" class="cube-side">
          <div class="cube-stage"
               @mousedown="handleMouseDown"
               @touchstart="handleTouchStart"
               @contextmenu.prevent>
            <div class="cube" :style="cubeStyle">
              <div v-for="face in ['front', 'back', 'left', 'right', 'top', 'bottom']"
                   :key="face"
                   :class="['cube-face', `face-${face}`]">
                <div v-for="i in 9" :key="i" class="cube-tile">
                  <div class="sticker"></div>
                </div>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </section>

    <section class="section-wrapper">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">不仅仅是求解器</h2>
          <p class="section-desc">我们将硬核算法封装在极简交互之下</p>
        </div>
        <el-row :gutter="24">
          <el-col :xs="24" :sm="8" v-for="(feat, idx) in features" :key="idx">
            <div class="feature-card-hover">
              <div class="icon-box" :class="feat.colorClass">
                <el-icon><component :is="feat.icon" /></el-icon>
              </div>
              <h3>{{ feat.title }}</h3>
              <p>{{ feat.desc }}</p>
            </div>
          </el-col>
        </el-row>
      </div>
    </section>

    <section class="section-wrapper bg-dots">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">构建你的魔方知识库</h2>
          <p class="section-desc">从零基础到竞速玩家，这里有你需要的进阶路径</p>
        </div>

        <el-row :gutter="30" justify="center">
          <el-col :xs="24" :sm="12" :md="8">
            <el-card class="course-card" shadow="hover">
              <div class="course-banner level-1">
                <span class="level-tag">入门</span>
                <el-icon class="course-icon"><Reading /></el-icon>
              </div>
              <div class="course-content">
                <h4>魔方基础结构与记号</h4>
                <p>了解中心块、棱块区别，掌握 U R F 等基础转动语言。</p>
                <div class="course-meta">
                  <span><el-icon><Timer /></el-icon> 10分钟</span>
                  <el-button text bg size="small" @click="handleEnterLearning">开始学习</el-button>
                </div>
              </div>
            </el-card>
          </el-col>

          <el-col :xs="24" :sm="12" :md="8">
            <el-card class="course-card" shadow="hover">
              <div class="course-banner level-2">
                <span class="level-tag">进阶</span>
                <el-icon class="course-icon"><DataLine /></el-icon>
              </div>
              <div class="course-content">
                <h4>层先法 (LBL) 详解</h4>
                <p>最经典的七步还原法，无需大量公式，逻辑清晰易上手。</p>
                <div class="course-meta">
                  <span><el-icon><Collection /></el-icon> 3 章节</span>
                  <el-button text bg size="small" @click="handleEnterLearning">查看课程</el-button>
                </div>
              </div>
            </el-card>
          </el-col>

          <el-col :xs="24" :sm="12" :md="8">
            <el-card class="course-card" shadow="hover">
              <div class="course-banner level-3">
                <span class="level-tag">竞速</span>
                <el-icon class="course-icon"><Trophy /></el-icon>
              </div>
              <div class="course-content">
                <h4>CFOP 高级算法预览</h4>
                <p>世界纪录保持者都在用的速拧方法，F2L/OLL/PLL 全解析。</p>
                <div class="course-meta">
                  <span><el-icon><Unlock /></el-icon> 待解锁</span>
                  <el-button text bg size="small" disabled>敬请期待</el-button>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <div class="mt-5">
          <el-button type="primary" plain round @click="handleEnterLearning">
            进入学习中心 <el-icon><ArrowRight /></el-icon>
          </el-button>
        </div>
      </div>
    </section>

    <section class="section-wrapper section-faq">
      <div class="container">
        <el-row :gutter="60" justify="center">
          <el-col :xs="24" :md="16">
            <h2 class="section-title">常见问题</h2>

            <el-collapse v-model="activeNames" class="custom-collapse" accordion>
              <el-collapse-item title="Q1: 识别魔方需要特殊的摄像头吗？" name="1">
                <div>不需要。使用电脑自带的摄像头即可。为了获得最佳效果，建议在光线均匀的环境下拍摄，避免魔方表面产生强烈反光。</div>
              </el-collapse-item>
              <el-collapse-item title="Q2: 为什么我的魔方总是识别失败？" name="2">
                <div>请检查是否有颜色贴纸破损或光线太暗。同时，CubeMaster 内置了手动修正功能，如果识别有误，您可以在 2D 展开图中点击色块进行手动调整。</div>
              </el-collapse-item>
              <el-collapse-item title="Q3: 自由练习模式支持计时吗？" name="3">
                <div>支持。自由探索模式集成了专业的计时器功能，您可以点击“开始挑战”来记录您的还原时间，并模拟真实的打乱过程。</div>
              </el-collapse-item>
              <el-collapse-item title="Q4: 这个项目是开源的吗？" name="4">
                <div>是的，这是一个基于 MIT 协议的开源项目。我们欢迎开发者参与贡献。</div>
              </el-collapse-item>
            </el-collapse>

            <div class="about-link-wrapper">
              <p>想要了解更多项目背后的故事或联系作者？</p>
              <router-link to="/about" class="about-link">
                查看关于页面 <el-icon><DArrowRight /></el-icon>
              </router-link>
            </div>
          </el-col>
        </el-row>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter, RouterLink} from 'vue-router';
import {
  Camera, Pointer, ArrowRight, Reading, DataLine, Trophy, Timer, Collection, Unlock, DArrowRight
} from '@element-plus/icons-vue';

const router = useRouter();
const loading = ref(false);
const activeNames = ref("1");

// --- 优化后的 3D 魔方交互逻辑 ---
const rotateX = ref(-25);
const rotateY = ref(-35);
let isDragging = false;
let startX, startY;
let currentX = -25;
let currentY = -35;
let animationId = null;

const cubeStyle = computed(() => ({
  transform: `rotateX(${rotateX.value}deg) rotateY(${rotateY.value}deg)`
}));

// 自动旋转：使用增量，而不是绝对时间
const autoRotate = () => {
  if (!isDragging) {
    // 每一帧增加一点点角度，实现平滑自转
    rotateY.value += 0.2;
    // 同步更新 current 值，防止下次点击时跳变
    currentY = rotateY.value;
    currentX = rotateX.value;
  }
  animationId = requestAnimationFrame(autoRotate);
};

// 鼠标/触摸开始
const handleInteractionStart = (clientX, clientY) => {
  isDragging = true;
  startX = clientX;
  startY = clientY;
  // 记录按下时的当前角度，作为拖拽的基准
  currentX = rotateX.value;
  currentY = rotateY.value;
};

// 鼠标/触摸移动
const handleInteractionMove = (clientX, clientY) => {
  if (!isDragging) return;
  const deltaX = clientX - startX;
  const deltaY = clientY - startY;

  // 更新角度：基准 + 变化量
  // Y轴移动控制 rotateY, X轴移动控制 rotateX (注意正负号以符合直觉)
  rotateY.value = currentY + deltaX * 0.5;
  rotateX.value = currentX - deltaY * 0.5;
};

// 事件监听包装
const handleMouseDown = (e) => {
  if (e.button === 0) handleInteractionStart(e.clientX, e.clientY);
};
const handleMouseMove = (e) => handleInteractionMove(e.clientX, e.clientY);
const handleMouseUp = () => { isDragging = false; };

// 触摸屏支持
const handleTouchStart = (e) => handleInteractionStart(e.touches[0].clientX, e.touches[0].clientY);
const handleTouchMove = (e) => handleInteractionMove(e.touches[0].clientX, e.touches[0].clientY);
const handleTouchEnd = () => { isDragging = false; };

// 路由跳转
const handleEnterSolver = () => router.push('/solver');
const handleEnterPlayground = () => router.push('/cube');
const handleEnterLearning = () => router.push('/learning');

// 数据定义
const features = [
  {
    title: '实时交互',
    desc: '物理魔方状态实时映射到 Web 端 3D 模型，零延迟的数字孪生体验。',
    icon: 'Monitor',
    colorClass: 'icon-blue'
  },
  {
    title: '智能算法',
    desc: '采用 Kociemba 二阶段算法，在 20 步之内解决任何打乱状态。',
    icon: 'Cpu',
    colorClass: 'icon-purple'
  },
  {
    title: '直观教学',
    desc: '抛弃晦涩的公式书。步骤分解演示，让逻辑清晰可见。',
    icon: 'VideoPlay',
    colorClass: 'icon-green'
  }
];

onMounted(() => {
  autoRotate();
  window.addEventListener('mousemove', handleMouseMove);
  window.addEventListener('mouseup', handleMouseUp);
  window.addEventListener('touchmove', handleTouchMove);
  window.addEventListener('touchend', handleTouchEnd);
});

onUnmounted(() => {
  cancelAnimationFrame(animationId);
  window.removeEventListener('mousemove', handleMouseMove);
  window.removeEventListener('mouseup', handleMouseUp);
  window.removeEventListener('touchmove', handleTouchMove);
  window.removeEventListener('touchend', handleTouchEnd);
});
</script>

<style scoped>
/* 核心变量 */
:root {
  --primary-color: #409eff;
  --bg-dots: radial-gradient(#e5e7eb 1px, transparent 1px);
}

.home-page-scroller {
  width: 100%;
  overflow-x: hidden;
  font-family: 'Inter', system-ui, sans-serif;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.mt-5 { margin-top: 3rem; }

/* --- Hero Section --- */
.hero-section-wrapper {
  position: relative;
  min-height: 85vh; /* 稍微减小高度 */
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  overflow: hidden;
}

.hero-bg-shape {
  position: absolute;
  top: -10%; right: -10%;
  width: 50vw; height: 50vw;
  background: radial-gradient(circle, rgba(64,158,255,0.1) 0%, rgba(255,255,255,0) 70%);
  border-radius: 50%;
  z-index: 0;
  pointer-events: none;
}

.hero-content {
  width: 100%;
  max-width: 1200px;
  z-index: 1;
  padding: 0 20px;
}

/* 文本区域样式同上个版本，略 */
.badge-pill {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  background: white;
  border-radius: 20px;
  font-size: 15px;
  font-weight: 600;
  color: #409eff;
  box-shadow: 0 2px 10px rgba(64,158,255,0.15);
  margin-bottom: 24px;
}
.dot { width: 6px; height: 6px; background: #409eff; border-radius: 50%; margin-right: 8px; }

.main-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 24px;
  color: #1a202c;
}
.gradient-text {
  background: linear-gradient(120deg, #2b6cb0, #4299e1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.block-text { display: block; }

.sub-title {
  font-size: 1.15rem;
  color: #4a5568;
  line-height: 1.7;
  max-width: 500px;
  margin-bottom: 40px;
}

.action-group { display: flex; gap: 16px; margin-bottom: 40px; }
.hero-btn { height: 50px; padding: 0 30px; font-size: 16px; border-radius: 12px; font-weight: 600; }
.primary-btn { box-shadow: 0 10px 20px rgba(64,158,255,0.3); }
.secondary-btn { background: white; border: 1px solid #e2e8f0; color: #4a5568; }

.tech-badges { display: flex; align-items: center; gap: 15px; opacity: 0.8; }
.tech-label { font-size: 14px; color: rgb(29, 197, 185); font-weight: 600; text-transform: uppercase; }
.tech-icon { width: 24px; height: 24px; filter: grayscale(100%); transition: 0.3s; cursor: help; }
.tech-icon:hover { filter: grayscale(0%); transform: scale(1.1); }

/* --- Cube Stage (交互修复版) --- */
.cube-stage {
  width: 100%;
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
  perspective: 1000px;
  cursor: grab;
  position: relative;
}
.cube-stage:active { cursor: grabbing; }

.cube {
  width: 200px;
  height: 200px;
  position: relative;
  transform-style: preserve-3d;
}

/* Cube Faces & Tiles 样式保持不变 */
.cube-face {
  position: absolute;
  width: 200px;
  height: 200px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4px;
  padding: 4px;
  background: #1a202c;
  border-radius: 8px;
  box-shadow: inset 0 0 15px rgba(0,0,0,0.5);
}
.cube-tile { border-radius: 4px; position: relative; overflow: hidden; }
.sticker { width: 100%; height: 100%; background: inherit; position: relative; }
.sticker::after {
  content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0) 50%);
}
.face-front .cube-tile { background: #345bf8; }
.face-back .cube-tile { background: #15ee1e; }
.face-left .cube-tile { background: #ff9800; }
.face-right .cube-tile { background: #ee1c1c; }
.face-top .cube-tile { background: #ffffff; }
.face-bottom .cube-tile { background: #f5f5f5; }

.face-front { transform: translateZ(100px); }
.face-back { transform: rotateY(180deg) translateZ(100px); }
.face-left { transform: rotateY(-90deg) translateZ(100px); }
.face-right { transform: rotateY(90deg) translateZ(100px); }
.face-top { transform: rotateX(90deg) translateZ(100px); }
.face-bottom { transform: rotateX(-90deg) translateZ(100px); }

/* --- 通用 Section --- */
.section-wrapper { padding: 100px 0; }
.section-header { margin-bottom: 50px; }
.section-title { font-size: 2.2rem; font-weight: 700; color: #1a202c; margin-bottom: 10px; }
.section-desc { font-size: 1.1rem; color: #718096; }

/* --- Features (卡片) --- */
.feature-card-hover {
  background: white;
  padding: 40px 30px;
  border-radius: 16px;
  border: 1px solid #edf2f7;
  transition: all 0.3s ease;
  height: 100%;
}
.feature-card-hover:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.06);
}
.icon-box {
  width: 60px; height: 60px;
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 28px;
  margin-bottom: 24px;
}
.icon-blue { background: rgba(66, 153, 225, 0.1); color: #4299e1; }
.icon-purple { background: rgba(159, 122, 234, 0.1); color: #9f7aea; }
.icon-green { background: rgba(72, 187, 120, 0.1); color: #48bb78; }
.feature-card-hover h3 { font-size: 1.25rem; margin-bottom: 12px; color: #2d3748; }
.feature-card-hover p { color: #718096; line-height: 1.6; font-size: 0.95rem; }

/* --- Learning Section (课程卡片) --- */
.bg-dots {
  background-color: #f9fafb;
  background-image: var(--bg-dots);
  background-size: 20px 20px;
}
.course-card {
  border: none;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s;
  height: 100%;
}
.course-card:hover { transform: translateY(-5px); }

.course-banner {
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  color: white;
}
.level-1 { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.level-2 { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.level-3 { background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%); }

.course-icon { font-size: 48px; opacity: 0.9; }
.level-tag {
  position: absolute;
  top: 10px; right: 10px;
  background: rgba(0,0,0,0.2);
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.course-content { padding: 20px; }
.course-content h4 { font-size: 1.1rem; margin-bottom: 8px; color: #2d3748; }
.course-content p { font-size: 0.9rem; color: #718096; line-height: 1.5; margin-bottom: 20px; height: 40px; overflow: hidden; }

.course-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  color: #a0aec0;
}

/* --- FAQ / About --- */
.section-faq {
  background: white;
  border-top: 1px solid #f0f0f0;
}
.custom-collapse {
  border-top: none;
  border-bottom: none;
}
.custom-collapse :deep(.el-collapse-item__header) {
  font-size: 1rem;
  transition: all 0.3s ease;
  border-bottom: 1px solid #edf2f7;
  padding: 10px 0;
}
.custom-collapse :deep(.el-collapse-item.is-active) .el-collapse-item__header {
  font-size: 1.1rem;
  font-weight: 500;
  color: #428be8; /* 使用你项目中的魔方蓝色 */
  padding-left: 15px; /* 为侧边条腾出空间 */
  border-left: 4px solid #0051BA; /* 魔方主题色高亮条 */
  background-color: #f8fbff; /* 淡淡的蓝色背景 */
}
.custom-collapse :deep(.el-collapse-item__content) {
  font-size: 0.95rem;
  color: #718096;
  line-height: 1.6;
  padding: 20px 15px;
  background-color: #f8fbff;
  border-bottom: 1px solid #edf2f7;
}

.about-link-wrapper {
  margin-top: 200px;
  text-align: center;
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
}
.about-link-wrapper p { color: #64748b; margin-bottom: 10px; }
.about-link {
  color: #409eff;
  text-decoration: none;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: gap 0.2s;
}
.about-link:hover { gap: 10px; }

/* --- Responsive --- */
@media (max-width: 992px) {
  .hero-content { flex-direction: column; text-align: center; padding-top: 40px; }
  .text-side { margin-bottom: 40px; }
  .action-group { justify-content: center; }
  .cube-stage { height: 350px; }
}
@media (max-width: 768px) {
  .main-title { font-size: 2.5rem; }
  .section-title { font-size: 1.8rem; }
  .feature-card-hover { margin-bottom: 20px; }
  .course-card { margin-bottom: 20px; }
}
</style>