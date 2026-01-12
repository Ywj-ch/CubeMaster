<template>
  <div class="home-page-scroller">
    <section class="hero-section-wrapper">
      <el-row :gutter="40" align="middle" class="hero-section">
        <el-col :xs="24" :md="12" class="text-side">
          <div class="badge">V2.0 实时还原</div>
          <h1 class="main-title">
            <span class="gradient-text">算法驱动</span> <br />
            魔方还原可视化
          </h1>
          <p class="sub-title">
            集成 <b>OpenCV</b> 图像识别与 <b>Kociemba</b> 算法。支持实时 3D 步进演示，
            通过直观的交互让复杂的逻辑触手可及。
          </p>

          <div class="action-btns">
            <el-button type="primary" size="large" round :loading="loading" class="main-btn" @click="handleEnterSolver">
              进入求解器
            </el-button>
            <el-button size="large" round @click="handleEnterLearning">
              查看教程
            </el-button>
          </div>

          <el-divider content-position="left">核心技术</el-divider>
          <div class="tech-stack">
            <el-tag effect="plain" round>Vue 3</el-tag>
            <el-tag effect="plain" type="success" round>OpenCV</el-tag>
            <el-tag effect="plain" type="warning" round>Kociemba Algorithm</el-tag>
            <el-tag effect="plain" type="info" round>Three.js</el-tag>
          </div>
        </el-col>

        <el-col :xs="24" :md="12" class="cube-side">
          <div class="cube-display-card"
              @mousedown="handleMouseDown"
              @contextmenu.prevent>
            <div class="cube" :style="cubeStyle">
              <div v-for="face in ['front', 'back', 'left', 'right', 'top', 'bottom']"
                  :key="face"
                  :class="['cube-face', `face-${face}`]">
                <div v-for="i in 9" :key="i" class="cube-tile"></div>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </section>

    <section class="section-wrapper bg-light-gray">
      <el-row justify="center">
        <el-col :span="20">
          <h2 class="section-title">工作原理：三步还原魔方</h2>
          <p class="section-subtitle">从物理魔方到虚拟还原，每一步都清晰可见。</p>
          <el-timeline class="timeline-custom">
            <el-timeline-item timestamp="步骤一" placement="top">
              <el-card>
                <h4>图像识别</h4>
                <p>利用 <b>OpenCV</b> 强大的图像处理能力，精确识别您物理魔方每一面的颜色布局。上传图片或通过摄像头实时扫描，系统将自动分析并构建 3D 虚拟魔方模型。</p>
                <img src="/images/recognition.png" alt="图像识别" class="timeline-img">
              </el-card>
            </el-timeline-item>
            <el-timeline-item timestamp="步骤二" placement="top">
              <el-card>
                <h4>Kociemba 算法求解</h4>
                <p>将识别出的魔方状态输入到高性能的 <b>Kociemba 算法</b>中，该算法能够在极短时间内找到最少步数的解法。您将获得一个简洁高效的还原路径。</p>
                <img src="/images/algorithm.png" alt="算法求解" class="timeline-img">
              </el-card>
            </el-timeline-item>
            <el-timeline-item timestamp="步骤三" placement="top">
              <el-card>
                <h4>3D 可视化演示</h4>
                <p>在交互式 3D 魔方中，系统将根据算法结果一步步还原魔方。您可以暂停、播放、快进、回退，从任意角度观察魔方的每一个转动，深入理解还原过程。</p>
                <img src="/images/visualization.png" alt="3D 可视化" class="timeline-img">
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </el-col>
      </el-row>
    </section>

    <section class="section-wrapper">
      <el-row justify="center">
        <el-col :span="20">
          <h2 class="section-title">为什么选择 CubeMaster？</h2>
          <p class="section-subtitle">我们的优势，让您的学习和探索更轻松。</p>

          <el-row :gutter="30" class="feature-cards">
            <el-col :xs="24" :sm="12" :md="8">
              <el-card class="feature-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><Monitor /></el-icon>
                    <span>实时交互</span>
                  </div>
                </template>
                <p>物理魔方状态实时映射到 3D 模型，所见即所得的流畅体验。</p>
              </el-card>
            </el-col>
            <el-col :xs="24" :sm="12" :md="8">
              <el-card class="feature-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><Setting/></el-icon>
                    <span>智能算法</span>
                  </div>
                </template>
                <p>采用 Kociemba 最优解算法，提供高效且易于理解的还原步骤。</p>
              </el-card>
            </el-col>
            <el-col :xs="24" :sm="12" :md="8">
              <el-card class="feature-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><InfoFilled /></el-icon>
                    <span>直观学习</span>
                  </div>
                </template>
                <p>可视化每一步操作，助您轻松掌握魔方还原的底层逻辑。</p>
              </el-card>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
    </section>

    <section class="section-wrapper bg-dark-blue call-to-action-section">
      <el-row justify="center">
        <el-col :span="20" class="text-center">
          <h2 class="section-title text-white">立即体验魔方还原的奥秘</h2>
          <p class="section-subtitle text-white">无需下载，即刻开始您的探索之旅。</p>
          <el-button type="primary" size="large" round @click="handleEnterSolver">
            <el-icon class="mr-1"><Promotion /></el-icon>
            开始还原我的魔方
          </el-button>
        </el-col>
      </el-row>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const loading = ref(false); // 求解器按钮加载状态

const rotateX = ref(30);
const rotateY = ref(30);
let isDragging = false;
let lastX, lastY;
let animationId = null;

const cubeStyle = computed(() => ({
  transform: `rotateX(${rotateX.value}deg) rotateY(${rotateY.value}deg)`
}));

// 自动旋转逻辑
const autoRotate = () => {
  if (!isDragging) {
    rotateY.value += 0.3; // 自动旋转的速度
    rotateX.value += 0.1;
  }
  animationId = requestAnimationFrame(autoRotate);
};

const handleMouseDown = (e) => {
  if (e.button === 0) {
    isDragging = true;
    lastX = e.clientX;
    lastY = e.clientY;
  }
};

const handleMouseMove = (e) => {
  if (!isDragging) return;
  const deltaX = e.clientX - lastX;
  const deltaY = e.clientY - lastY;
  rotateY.value += deltaX * 0.5;
  rotateX.value -= deltaY * 0.5;
  lastX = e.clientX;
  lastY = e.clientY;
};

const handleMouseUp = () => { isDragging = false; };

const handleEnterSolver = () => {
  loading.value = true;
  setTimeout(() => {
    router.push('/solver');
  }, 1000); // 模拟加载1秒
};

const handleEnterLearning = () => {
  router.push('/learning');
};


onMounted(() => {
  autoRotate();
  window.addEventListener('mousemove', handleMouseMove);
  window.addEventListener('mouseup', handleMouseUp);
});

onUnmounted(() => {
  cancelAnimationFrame(animationId);
  window.removeEventListener('mousemove', handleMouseMove);
  window.removeEventListener('mouseup', handleMouseUp);
});
</script>

<style scoped>
/* 全局布局 */
.home-page-scroller {
  width: 100%;
  overflow-x: hidden; /* 防止水平滚动条 */
}

.section-wrapper {
  padding: 100px 20px;
  text-align: center;
  max-width: 1200px;
  margin: 0 auto;
}

.bg-light-gray { background-color: #f7fafc; }
.bg-dark-blue { background-color: #2d3748; }

.section-title {
  font-size: 3rem;
  font-weight: bold;
  color: #2d3748;
  margin-bottom: 20px;
}
.section-title.text-white { color: white; }

.section-subtitle {
  font-size: 1.2rem;
  color: #4a5568;
  margin-bottom: 60px;
}
.section-subtitle.text-white { color: #e2e8f0; }

/* --- Hero Section (第一屏) --- */
.hero-section-wrapper {
  min-height: calc(100vh - 80px); /* 减去 Header 高度 */
  display: flex;
  align-items: center;
  padding: 0 20px;
  max-width: 1400px; /* 稍微宽一点 */
  margin: 0 auto;
}
.hero-section {
  width: 100%;
}

.badge {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(66, 153, 225, 0.1);
  color: #4299E1;
  border-radius: 20px;
  font-weight: bold;
  font-size: 14px;
  margin-bottom: 20px;
}

.main-title {
  font-size: 3.8rem; /* 更大 */
  line-height: 1.1;
  color: #1a202c;
  margin-bottom: 20px;
}

.gradient-text {
  background: linear-gradient(90deg, #4299e1, #667eea);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.sub-title {
  font-size: 1.3rem; /* 更大 */
  color: #4a5568;
  line-height: 1.8;
  margin-bottom: 40px;
}

.action-btns .el-button {
  margin-right: 20px; /* 按钮间距 */
}

.tech-stack {
  display: flex;
  flex-wrap: wrap; /* 自动换行 */
  gap: 10px;
  margin-top: 20px;
}

.cube-side {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  min-height: 500px; /* 确保右侧高度足够 */
}

.cube-display-card {
  width: 100%; /* 占据可用宽度 */
  max-width: 500px; /* 最大宽度 */
  height: 500px;
  background: white;
  border-radius: 30px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.08);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: grab;
  position: relative;
  overflow: hidden;
}

.cube-display-card:active { cursor: grabbing; }

/* 3D Cube 基础样式与之前相同，但优化细节 */
.cube {
  width: 250px; /* 稍微大一点 */
  height: 250px;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.1s linear;
}

.cube-face {
  position: absolute;
  width: 250px;
  height: 250px;
  border: 2px solid rgba(0,0,0,0.8);
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2px;
  background: #2d3748;
}

.cube-tile {
  border-radius: 4px;
}

/* 颜色分配 */
.face-front .cube-tile { background: #e53e3e; } /* 红 */
.face-back .cube-tile { background: #38a169; } /* 绿 */
.face-left .cube-tile { background: #ed8936; } /* 橙 */
.face-right .cube-tile { background: #3182ce; } /* 蓝 */
.face-top .cube-tile { background: #ecc94b; } /* 黄 */
.face-bottom .cube-tile { background: #f7fafc; } /* 白 */

/* 3D 转换 */
.face-front { transform: translateZ(125px); }
.face-back { transform: rotateY(180deg) translateZ(125px); }
.face-left { transform: rotateY(-90deg) translateZ(125px); }
.face-right { transform: rotateY(90deg) translateZ(125px); }
.face-top { transform: rotateX(90deg) translateZ(125px); }
.face-bottom { transform: rotateX(-90deg) translateZ(125px); }


/* --- 第二屏: 工作原理 --- */
.timeline-custom {
  max-width: 800px;
  margin: 60px auto;
  text-align: left;
}
.timeline-custom h4 {
  font-size: 1.5rem;
  color: #2d3748;
  margin-bottom: 10px;
}
.timeline-custom p {
  font-size: 1rem;
  color: #4a5568;
  line-height: 1.6;
}
.timeline-img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin-top: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* --- 第三屏: 核心优势 --- */
.feature-cards {
  margin-top: 60px;
}
.feature-card {
  margin-bottom: 30px;
  text-align: left;
  min-height: 250px;
}
.feature-card .card-header {
  display: flex;
  align-items: center;
  font-size: 1.4rem;
  font-weight: bold;
  color: #2d3748;
}
.feature-card .el-icon {
  margin-right: 10px;
  font-size: 28px;
  color: #4299E1;
}
.feature-card p {
  font-size: 1rem;
  color: #4a5568;
  line-height: 1.6;
  margin-top: 15px;
}

/* --- 第四屏: 行动召唤 --- */
.call-to-action-section {
  padding: 80px 20px;
}
.call-to-action-section .el-button {
  margin-top: 30px;
}

/* --- 响应式适配 --- */
@media (max-width: 992px) {
  .main-title { font-size: 3rem; }
  .section-title { font-size: 2.5rem; }
  .cube-display-card { max-width: 400px; height: 400px; }
  .cube, .cube-face { width: 200px; height: 200px; }
  .face-front, .face-back, .face-left, .face-right, .face-top, .face-bottom { transform: translateZ(100px); }
}

@media (max-width: 768px) {
  .hero-section-wrapper {
    flex-direction: column;
    text-align: center;
    padding-top: 40px;
  }
  .text-side, .cube-side {
    max-width: 100%;
  }
  .cube-side {
    order: -1; /* 魔方在小屏幕上放到文字上方 */
    margin-bottom: 40px;
  }
  .main-title { font-size: 2.2rem; }
  .sub-title { font-size: 1rem; }
  .action-btns .el-button { margin-right: 0; margin-bottom: 15px; width: 80%; }
  .tech-stack { justify-content: center; }

  .section-title { font-size: 2rem; }
  .section-subtitle { font-size: 1rem; }
  .timeline-custom { margin: 30px auto; }
  .feature-card { min-height: auto; }
}

@media (max-width: 576px) {
  .hero-section-wrapper { padding-left: 10px; padding-right: 10px; }
  .main-title { font-size: 1.8rem; }
  .sub-title { font-size: 0.9rem; }
  .section-title { font-size: 1.8rem; }
  .cube-display-card { height: 300px; }
  .cube, .cube-face { width: 150px; height: 150px; }
  .face-front, .face-back, .face-left, .face-right, .face-top, .face-bottom { transform: translateZ(75px); }
}
</style>