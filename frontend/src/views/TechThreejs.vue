<template>
  <div class="tech-doc-page threejs-doc">
    <div class="page-container">
      <!-- 返回 About 页面按钮 -->
      <header class="tech-doc-header">
        <button @click="goBackToAbout" class="minimal-back-btn">
          <el-icon><ArrowLeft /></el-icon>
          <span>BACK TO ABOUT</span>
        </button>
      </header>

      <!-- Hero Section -->
      <section class="hero-section" v-animate>
        <div class="glow-bg glow-top-right"></div>
        <div class="glow-bg glow-bottom-left"></div>

        <div class="hero-content">
          <div class="badge-pill">
            <span class="pulse-dot"></span>
            <span>3D 渲染 · 实时交互</span>
          </div>

          <h1 class="hero-title">
            Three.js 魔方渲染引擎<br />
            <span class="gradient-text">网页端实时 3D 交互实现</span>
          </h1>

          <p class="hero-subtitle">
            探索 CubeMaster 如何利用 Three.js 和 WebGL 在浏览器中实现流畅的 3D
            魔方渲染、 旋转动画和交互操作，提供沉浸式的学习体验。
          </p>

          <div class="stats-pills">
            <div class="stat-pill">
              <span class="dot-indicator blue"></span>
              <span>帧率：60 FPS (稳定)</span>
            </div>
            <div class="stat-pill">
              <span class="dot-indicator green"></span>
              <span>渲染对象：27 个立方体 + 54 个色块</span>
            </div>
            <div class="stat-pill">
              <span class="dot-indicator purple"></span>
              <span>加载时间：&lt; 1.5 秒</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Core Architecture -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">核心架构</h2>
        <div class="architecture-diagram">
          <div class="arch-layer">
            <div class="layer-header">
              <div class="layer-number">1</div>
              <h3>场景图 (Scene Graph)</h3>
            </div>
            <div class="layer-content">
              <p>层次化对象管理，父子关系定义魔方块的空间位置</p>
              <ul>
                <li><strong>Scene</strong>：根容器，包含所有渲染对象</li>
                <li><strong>Group</strong>：魔方整体容器，便于整体变换</li>
                <li>
                  <strong>Mesh</strong>：27 个立方体网格，每个代表一个小块
                </li>
                <li><strong>Material</strong>：PBR 材质，支持光泽和反射</li>
              </ul>
            </div>
          </div>

          <div class="arch-layer">
            <div class="layer-header">
              <div class="layer-number">2</div>
              <h3>渲染管线 (Render Pipeline)</h3>
            </div>
            <div class="layer-content">
              <p>WebGL 底层渲染优化，确保流畅性能</p>
              <ul>
                <li><strong>Renderer</strong>：WebGLRenderer，硬件加速</li>
                <li><strong>Camera</strong>：PerspectiveCamera，透视投影</li>
                <li><strong>Lighting</strong>：环境光 + 方向光 + 点光源</li>
                <li><strong>Shadow</strong>：软阴影映射，增强立体感</li>
              </ul>
            </div>
          </div>

          <div class="arch-layer">
            <div class="layer-header">
              <div class="layer-number">3</div>
              <h3>交互系统 (Interaction)</h3>
            </div>
            <div class="layer-content">
              <p>用户输入处理与动画系统</p>
              <ul>
                <li><strong>Raycaster</strong>：鼠标/触摸点击检测</li>
                <li><strong>OrbitControls</strong>：摄像机轨道控制</li>
                <li>
                  <strong>Animation Loop</strong>：requestAnimationFrame 循环
                </li>
                <li><strong>Tweening</strong>：GSAP 补间动画库</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- Cube Representation -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">魔方数据结构</h2>
        <div class="data-representation">
          <div class="data-card">
            <h3><span class="data-icon">🧊</span> 几何表示</h3>
            <div class="code-snippet">
              <pre><code>// 生成基础 3x3 离散点阵坐标系
const generateBaseCubies = () => {
  const positions = [];
  for (let x = -1; x <= 1; x++) {
    for (let y = -1; y <= 1; y++) {
      for (let z = -1; z <= 1; z++) {
        positions.push({ x, y, z, type: getCubieType(x, y, z) });
      }
    }
  }
  return positions;
};

// 小方块类型分类
const getCubieType = (x, y, z) => {
  const sum = Math.abs(x) + Math.abs(y) + Math.abs(z);
  if (sum === 3) return 'corner';     // 角块 (x,y,z 均不为 0)
  if (sum === 2) return 'edge';       // 棱块 (两个坐标不为 0)
  if (sum === 1) return 'center';     // 中心块 (一个坐标不为 0)
  return 'core';                      // 核心块 (0,0,0)
};</code></pre>
            </div>
          </div>

          <div class="data-card">
            <h3><span class="data-icon">🎨</span> 颜色映射</h3>
            <ul>
              <li>
                <strong>标准配色</strong
                >：白(U)、红(R)、蓝(B)、橙(O)、绿(G)、黄(D)
              </li>
              <li>
                <strong>材质系统</strong>：每个面独立 Material，支持高光和反光
              </li>
              <li>
                <strong>纹理选项</strong>：纯色、磨砂、光泽、半透明多种预设
              </li>
              <li><strong>状态同步</strong>：颜色数组 ↔ 3D 渲染实时同步</li>
            </ul>
            <div class="color-preview">
              <div class="color-swatch" style="background: #ffffff">U</div>
              <div class="color-swatch" style="background: #b71234">R</div>
              <div class="color-swatch" style="background: #0046ad">L</div>
              <div class="color-swatch" style="background: #ff5800">F</div>
              <div class="color-swatch" style="background: #009b48">B</div>
              <div class="color-swatch" style="background: #ffd500">D</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Animation System -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">动画系统</h2>
        <div class="animation-system">
          <div class="anim-card">
            <h3><span class="anim-icon">🔄</span> 旋转动画</h3>
            <div class="code-snippet">
              <pre><code>// 执行单层旋转动画
async function rotateLayer(layer, direction, angle = 90) {
  // 1. 确定受影响的小块
  const affectedCubies = getCubiesInLayer(layer);
  
  // 2. 创建父容器，统一变换
  const container = new THREE.Group();
  affectedCubies.forEach(cubie => container.add(cubie));
  scene.add(container);
  
  // 3. 执行动画
  return new Promise(resolve => {
    const duration = 300; // 毫秒
    const startTime = performance.now();
    
    function animate(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = easeOutCubic(progress);
      
      // 计算当前角度
      const currentAngle = angle * eased * (direction === 'clockwise' ? 1 : -1);
      
      // 应用旋转
      const axis = getAxisForLayer(layer);
      container.rotation[axis] = THREE.MathUtils.degToRad(currentAngle);
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        // 动画完成，更新逻辑状态
        updateCubeStateAfterRotation(layer, direction);
        scene.remove(container);
        resolve();
      }
    }
    
    requestAnimationFrame(animate);
  });
}</code></pre>
            </div>
          </div>

          <div class="anim-card">
            <h3><span class="anim-icon">⚡</span> 性能优化</h3>
            <ul>
              <li>
                <strong>对象复用</strong>：几何体和材质实例共享，减少内存占用
              </li>
              <li>
                <strong>批量渲染</strong>：使用 InstancedMesh 渲染相同几何体
              </li>
              <li><strong>帧率控制</strong>：防抖处理，避免过度渲染</li>
              <li><strong>内存管理</strong>：及时释放未使用的纹理和几何体</li>
              <li><strong>离屏渲染</strong>：预计算复杂场景，减少运行时开销</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Interaction Implementation -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">交互实现</h2>
        <div class="interaction-details">
          <div class="interaction-step">
            <div class="step-number">1</div>
            <div class="step-content">
              <h3>点击检测</h3>
              <p>
                使用 Raycaster
                从鼠标位置发射射线，与魔方块求交，确定点击的面和层。
              </p>
              <div class="code-snippet small">
                <pre><code>const raycaster = new THREE.Raycaster();
raycaster.setFromCamera(mouse, camera);
const intersects = raycaster.intersectObjects(cubies);
if (intersects.length > 0) {
  const clickedCubie = intersects[0].object;
  const faceNormal = getClickedFace(intersects[0].face);
  return { cubie: clickedCubie, face: faceNormal };
}</code></pre>
              </div>
            </div>
          </div>

          <div class="interaction-step">
            <div class="step-number">2</div>
            <div class="step-content">
              <h3>拖动识别</h3>
              <p>跟踪鼠标移动向量，确定旋转方向和层，阈值处理避免误操作。</p>
              <div class="code-snippet small">
                <pre><code>const dragVector = new THREE.Vector2(
  currentMouse.x - startMouse.x,
  currentMouse.y - startMouse.y
);
if (dragVector.length() > DRAG_THRESHOLD) {
  const axis = determineRotationAxis(dragVector, clickedFace);
  const direction = determineRotationDirection(dragVector, axis);
  rotateLayer(getLayerFromAxisAndFace(axis, clickedFace), direction);
}</code></pre>
              </div>
            </div>
          </div>

          <div class="interaction-step">
            <div class="step-number">3</div>
            <div class="step-content">
              <h3>动画队列</h3>
              <p>顺序执行旋转动画，支持撤销/重做，确保状态一致性。</p>
              <div class="code-snippet small">
                <pre><code>class AnimationQueue {
  constructor() {
    this.queue = [];
    this.isAnimating = false;
  }
  
  async add(animation) {
    this.queue.push(animation);
    if (!this.isAnimating) this.process();
  }
  
  async process() {
    this.isAnimating = true;
    while (this.queue.length > 0) {
      const animation = this.queue.shift();
      await animation();
    }
    this.isAnimating = false;
  }
}</code></pre>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Performance Metrics -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">性能指标</h2>
        <div class="performance-metrics">
          <div class="metric-grid">
            <div class="metric-card">
              <div class="metric-value">60</div>
              <div class="metric-label">FPS</div>
              <div class="metric-desc">目标帧率 (vsync 同步)</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">&lt; 16ms</div>
              <div class="metric-label">帧时间</div>
              <div class="metric-desc">每帧渲染时间</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">27</div>
              <div class="metric-label">绘制调用</div>
              <div class="metric-desc">InstancedMesh 优化</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">12MB</div>
              <div class="metric-label">内存占用</div>
              <div class="metric-desc">几何体 + 纹理 + 程序</div>
            </div>
          </div>

          <div class="optimization-tips">
            <h3>优化技巧</h3>
            <ul>
              <li>
                <strong>几何体合并</strong>：将多个 Mesh 合并为单个，减少 draw
                calls
              </li>
              <li>
                <strong>纹理图集</strong>：将多个小纹理合并为大图，减少纹理切换
              </li>
              <li>
                <strong>细节层次 (LOD)</strong
                >：远距离使用简化模型，提升渲染速度
              </li>
              <li><strong>视锥剔除</strong>：只渲染摄像机可见范围内的对象</li>
              <li>
                <strong>WebWorker</strong>：复杂计算移至 Worker
                线程，避免阻塞渲染
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Challenges -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">技术挑战</h2>
        <div class="challenges-grid">
          <div class="challenge-card">
            <h3><span class="challenge-icon">📱</span> 移动端适配</h3>
            <p>
              <strong>问题</strong>：移动设备 GPU 性能有限，触摸交互精度要求高
            </p>
            <p>
              <strong>解决方案</strong
              >：响应式设计，简化阴影和反射，增大触摸热区
            </p>
          </div>
          <div class="challenge-card">
            <h3><span class="challenge-icon">🌐</span> 浏览器兼容</h3>
            <p>
              <strong>问题</strong>：不同浏览器 WebGL 实现差异，扩展支持不一致
            </p>
            <p>
              <strong>解决方案</strong>：特性检测，渐进增强，提供降级方案 (CSS
              3D)
            </p>
          </div>
          <div class="challenge-card">
            <h3><span class="challenge-icon">⚙️</span> 状态同步</h3>
            <p><strong>问题</strong>：3D 渲染状态与逻辑状态需要严格同步</p>
            <p>
              <strong>解决方案</strong>：单一数据源，状态变更通过中央控制器分发
            </p>
          </div>
        </div>
      </section>

      <!-- Navigation -->
      <section class="section-block navigation-section" v-animate>
        <h2 class="section-heading text-center">继续探索</h2>
        <div class="nav-cards">
          <router-link to="/tech/yolo" class="nav-card">
            <div class="nav-icon">👁️</div>
            <h3>YOLOv8 视觉识别</h3>
            <p>魔方颜色检测技术详解</p>
          </router-link>
          <router-link to="/tech/kociemba" class="nav-card">
            <div class="nav-icon">🧩</div>
            <h3>Kociemba 算法</h3>
            <p>魔方两阶段求解算法原理</p>
          </router-link>
          <router-link to="/tech/architecture" class="nav-card">
            <div class="nav-icon">🏗️</div>
            <h3>系统架构</h3>
            <p>前后端分离设计与数据流</p>
          </router-link>
        </div>
      </section>
    </div>

    <!-- 返回顶部按钮 -->
    <button
      @click="scrollToTop"
      class="back-to-top-btn"
      :class="{ visible: showBackToTop }"
    >
      <el-icon><ArrowUp /></el-icon>
    </button>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useRouter } from "vue-router";
import { ArrowLeft, ArrowUp } from "@element-plus/icons-vue";

const router = useRouter();
const showBackToTop = ref(false);

// 滚动动画指令
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

// 返回 About 页面
const goBackToAbout = () => {
  router.push("/about");
};

// 返回顶部
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
};

// 监听滚动显示返回顶部按钮
const handleScroll = () => {
  showBackToTop.value = window.scrollY > 300;
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll);
  // 初始检查
  handleScroll();
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});
</script>

<style scoped>
/* === 基础样式 (从 TechYolo.vue 复制) === */
.tech-doc-page {
  width: 100%;
  min-height: 100vh;
  background-color: #f8fafc;
  font-family: "Inter", sans-serif;
  color: #0f172a;
  padding-bottom: 100px;
  overflow-x: hidden;
}

.page-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 24px;
}

/* 动画类 */
.before-enter {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.enter {
  opacity: 1;
  transform: translateY(0);
}

/* Hero Section */
.hero-section {
  position: relative;
  padding: 80px 0 60px;
  overflow: hidden;
  border-radius: 32px;
  margin-bottom: 60px;
}

.glow-bg {
  position: absolute;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
  z-index: 0;
}
.glow-top-right {
  top: -100px;
  right: -100px;
  background: #3b82f6;
}
.glow-bottom-left {
  bottom: -100px;
  left: -100px;
  background: #10b981;
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
}

.badge-pill {
  display: inline-flex;
  align-items: center;
  padding: 6px 16px;
  background: rgba(37, 99, 235, 0.1);
  color: #2563eb;
  border-radius: 100px;
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 24px;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background: #2563eb;
  border-radius: 50%;
  margin-right: 8px;
  box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.7);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.4);
  }
  70% {
    box-shadow: 0 0 0 6px rgba(37, 99, 235, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(37, 99, 235, 0);
  }
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 24px;
  letter-spacing: -0.02em;
}

.gradient-text {
  background: linear-gradient(135deg, #1e293b 0%, #3b82f6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 40px;
}

.stats-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.stat-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
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

/* 通用 Section */
.section-block {
  margin-bottom: 100px;
}
.section-heading {
  font-size: 2rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 40px;
}
.text-center {
  text-align: center;
}

/* 技术概览网格 */
.tech-overview-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
}

@media (max-width: 768px) {
  .overview-grid {
    grid-template-columns: 1fr;
  }
}

.overview-item {
  text-align: center;
}

.overview-icon {
  font-size: 2.5rem;
  margin-bottom: 16px;
}

.overview-item h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #1e293b;
}

.overview-item p {
  color: #64748b;
  line-height: 1.6;
}

/* 工作流程 */
.workflow-diagram {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
}

.workflow-step {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 30px;
  padding-bottom: 30px;
  border-bottom: 1px solid #f1f5f9;
}
.workflow-step:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.step-number {
  width: 50px;
  height: 50px;
  background: #3b82f6;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 800;
  flex-shrink: 0;
}

.step-content h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 8px;
  color: #1e293b;
}

.step-content p {
  color: #64748b;
  line-height: 1.6;
}

/* 训练详情 */
.training-details {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

@media (max-width: 992px) {
  .training-details {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .training-details {
    grid-template-columns: 1fr;
  }
}

.detail-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
}

.detail-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 10px;
}

.detail-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.detail-card li {
  margin-bottom: 12px;
  color: #64748b;
  line-height: 1.6;
  padding-left: 0;
}

.detail-card li strong {
  color: #1e293b;
}

/* 集成卡片 */
.integration-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}

.code-snippet {
  background: #0f172a;
  border-radius: 16px;
  overflow: hidden;
}

.snippet-header {
  background: #1e293b;
  color: #cbd5e1;
  padding: 16px 24px;
  font-size: 14px;
  font-weight: 600;
}

.code-snippet pre {
  margin: 0;
  padding: 24px;
  overflow-x: auto;
}

.code-snippet code {
  font-family: "JetBrains Mono", monospace;
  font-size: 14px;
  color: #e2e8f0;
  line-height: 1.6;
}

.integration-note h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #1e293b;
}

.integration-note ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.integration-note li {
  margin-bottom: 12px;
  color: #64748b;
  line-height: 1.6;
  padding-left: 0;
}

.integration-note li strong {
  color: #1e293b;
}

/* 挑战网格 */
.challenges-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

@media (max-width: 992px) {
  .challenges-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .challenges-grid {
    grid-template-columns: 1fr;
  }
}

.challenge-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
}

.challenge-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.challenge-emoji {
  font-size: 2rem;
}

.challenge-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.challenge-card p {
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 12px;
}

/* 导航卡片 */
.navigation-section {
  margin-top: 80px;
}

.nav-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

@media (max-width: 768px) {
  .nav-cards {
    grid-template-columns: 1fr;
  }
}

.nav-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s;
  text-align: center;
}

.nav-card:hover {
  transform: translateY(-5px);
  border-color: #3b82f6;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.nav-icon {
  font-size: 2.5rem;
  margin-bottom: 16px;
}

.nav-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 8px;
  color: #1e293b;
}

.nav-card p {
  color: #64748b;
  font-size: 0.95rem;
}

/* 响应式基础 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  .integration-card {
    grid-template-columns: 1fr;
  }
}

/* === 特定于 Three.js 页面的样式 === */

/* 架构图示 */
.architecture-diagram {
  display: flex;
  flex-direction: column;
  gap: 24px;
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
}

.arch-layer {
  display: flex;
  gap: 24px;
  padding: 30px;
  background: #f8fafc;
  border-radius: 20px;
  border-left: 4px solid #3b82f6;
}

.layer-header {
  display: flex;
  align-items: center;
  gap: 16px;
  min-width: 200px;
}

.layer-number {
  width: 40px;
  height: 40px;
  background: #3b82f6;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 800;
  flex-shrink: 0;
}

.layer-header h3 {
  font-size: 1.25rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
}

.layer-content {
  flex: 1;
}

.layer-content p {
  color: #64748b;
  margin-bottom: 16px;
  font-weight: 600;
}

.layer-content ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.layer-content li {
  color: #64748b;
  margin-bottom: 8px;
  padding-left: 0;
}

.layer-content li strong {
  color: #1e293b;
}

/* 数据表示 */
.data-representation {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 40px;
}

.data-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
}

.data-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 10px;
}

.code-snippet {
  background: #0f172a;
  border-radius: 16px;
  overflow: hidden;
}

.code-snippet pre {
  margin: 0;
  padding: 24px;
  overflow-x: auto;
}

.code-snippet code {
  font-family: "JetBrains Mono", monospace;
  font-size: 14px;
  color: #e2e8f0;
  line-height: 1.6;
}

.data-card ul {
  list-style: none;
  padding: 0;
  margin: 0 0 20px 0;
}

.data-card li {
  margin-bottom: 12px;
  color: #64748b;
  line-height: 1.6;
  padding-left: 0;
}

.data-card li strong {
  color: #1e293b;
}

.color-preview {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.color-swatch {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  color: rgba(0, 0, 0, 0.7);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.8);
}

/* 动画系统 */
.animation-system {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 40px;
}

.anim-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
}

.anim-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 10px;
}

/* 交互步骤 */
.interaction-details {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
}

.interaction-step {
  display: flex;
  gap: 24px;
  margin-bottom: 40px;
  padding-bottom: 40px;
  border-bottom: 1px solid #f1f5f9;
}
.interaction-step:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.step-number {
  width: 50px;
  height: 50px;
  background: #3b82f6;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 800;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-content h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #1e293b;
}

.step-content p {
  color: #64748b;
  margin-bottom: 20px;
  line-height: 1.6;
}

.code-snippet.small {
  background: #0f172a;
  border: 1px solid #334155;
}

.code-snippet.small pre {
  padding: 16px;
}

.code-snippet.small code {
  color: #e2e8f0;
  font-size: 13px;
}

/* 性能指标 */
.performance-metrics {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 40px;
}

.metric-card {
  background: #f8fafc;
  border-radius: 16px;
  padding: 30px;
  text-align: center;
  border: 1px solid #e2e8f0;
}

.metric-value {
  font-size: 2.5rem;
  font-weight: 800;
  color: #3b82f6;
  margin-bottom: 8px;
}

.metric-label {
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.metric-desc {
  font-size: 0.9rem;
  color: #64748b;
}

.optimization-tips h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #1e293b;
}

.optimization-tips ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

@media (max-width: 768px) {
  .optimization-tips ul {
    grid-template-columns: 1fr;
  }
}

.optimization-tips li {
  color: #64748b;
  line-height: 1.6;
  padding-left: 24px;
  position: relative;
}

.optimization-tips li:before {
  content: "✓";
  color: #10b981;
  position: absolute;
  left: 0;
  font-weight: bold;
}

.optimization-tips li strong {
  color: #1e293b;
}

/* 挑战网格 */
.challenges-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

@media (max-width: 992px) {
  .challenges-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .challenges-grid {
    grid-template-columns: 1fr;
  }
}

.challenge-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
}

.challenge-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 10px;
}

.challenge-card p {
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 12px;
}

/* 导航卡片 */
.navigation-section {
  margin-top: 80px;
}

.nav-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

@media (max-width: 768px) {
  .nav-cards {
    grid-template-columns: 1fr;
  }
}

.nav-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s;
  text-align: center;
}

.nav-card:hover {
  transform: translateY(-5px);
  border-color: #3b82f6;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.nav-icon {
  font-size: 2.5rem;
  margin-bottom: 16px;
}

.nav-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 8px;
  color: #1e293b;
}

.nav-card p {
  color: #64748b;
  font-size: 0.95rem;
}

/* 响应式 */
@media (max-width: 992px) {
  .architecture-diagram {
    padding: 24px;
  }
  .arch-layer {
    flex-direction: column;
    gap: 16px;
  }
  .data-representation,
  .animation-system {
    grid-template-columns: 1fr;
  }
  .metric-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .challenges-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 576px) {
  .metric-grid {
    grid-template-columns: 1fr;
  }
}

/* 技术文档头部和返回按钮 */
.tech-doc-header {
  margin-top: 30px;
  margin-bottom: 20px;
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

/* 返回顶部按钮 */
.back-to-top-btn {
  position: fixed;
  bottom: 40px;
  right: 40px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #3b82f6;
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.3s ease;
  z-index: 1000;
}
.back-to-top-btn.visible {
  opacity: 1;
  transform: translateY(0);
}
.back-to-top-btn:hover {
  background: #2563eb;
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
}

/* 移动端适配 */
@media (max-width: 768px) {
  .back-to-top-btn {
    bottom: 20px;
    right: 20px;
    width: 45px;
    height: 45px;
  }
}

/* ==================== Dark Mode Styles ==================== */
[data-theme="dark"] .tech-doc-page {
  background-color: var(--dm-bg-page);
  color: var(--dm-text-primary);
}

[data-theme="dark"] .hero-section {
  background: transparent;
}

[data-theme="dark"] .badge-pill {
  background: rgba(59, 130, 246, 0.15);
  color: var(--dm-accent);
}

[data-theme="dark"] .pulse-dot {
  background: var(--dm-accent);
}

[data-theme="dark"] .hero-title {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .gradient-text {
  background: linear-gradient(
    135deg,
    var(--dm-text-primary) 0%,
    var(--dm-accent) 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

[data-theme="dark"] .hero-subtitle {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .stat-pill {
  background: var(--dm-glass-bg);
  border-color: var(--dm-glass-border);
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .section-heading {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .architecture-diagram {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .arch-layer {
  background: var(--dm-bg-hover);
  border-left-color: var(--dm-accent);
}

[data-theme="dark"] .layer-header h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .layer-content p {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .layer-content li {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .data-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .data-card h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .code-snippet {
  background: #0f172a;
}

[data-theme="dark"] .code-snippet code {
  color: #e2e8f0;
}

[data-theme="dark"] .data-card li {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .data-card li strong {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .color-swatch {
  border-color: var(--dm-border);
}

[data-theme="dark"] .anim-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .anim-card h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .interaction-details {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .interaction-step {
  border-bottom-color: var(--dm-border);
}

[data-theme="dark"] .step-content h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .step-content p {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .code-snippet.small {
  background: #0f172a;
  border-color: var(--dm-border);
}

[data-theme="dark"] .performance-metrics {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .metric-card {
  background: var(--dm-bg-hover);
  border-color: var(--dm-border);
}

[data-theme="dark"] .metric-value {
  color: var(--dm-accent);
}

[data-theme="dark"] .metric-label {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .metric-desc {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .optimization-tips h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .optimization-tips li {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .optimization-tips li:before {
  color: #34d399;
}

[data-theme="dark"] .optimization-tips li strong {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .challenge-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .challenge-card h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .challenge-card p {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .nav-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .nav-card:hover {
  border-color: var(--dm-accent);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .nav-card h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .nav-card p {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .minimal-back-btn {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .minimal-back-btn:hover {
  color: var(--dm-accent);
}

[data-theme="dark"] .back-to-top-btn {
  background: var(--dm-accent);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

[data-theme="dark"] .back-to-top-btn:hover {
  background: var(--dm-accent-hover);
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
}
</style>
