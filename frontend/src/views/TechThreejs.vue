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
            魔方渲染、旋转动画和交互操作，提供沉浸式的学习体验。
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
        <div class="architecture-grid">
          <div class="arch-card">
            <div class="arch-header">
              <div class="arch-number">01</div>
              <h3>场景图</h3>
            </div>
            <p class="arch-desc">
              层次化对象管理，父子关系定义魔方块的空间位置
            </p>
            <ul class="arch-list">
              <li><strong>Scene</strong>：根容器，包含所有渲染对象</li>
              <li><strong>Group</strong>：魔方整体容器，便于整体变换</li>
              <li><strong>Mesh</strong>：27 个立方体网格，每个代表一个小块</li>
              <li><strong>Material</strong>：PBR 材质，支持光泽和反射</li>
            </ul>
          </div>

          <div class="arch-card">
            <div class="arch-header">
              <div class="arch-number">02</div>
              <h3>渲染管线</h3>
            </div>
            <p class="arch-desc">WebGL 底层渲染优化，确保流畅性能</p>
            <ul class="arch-list">
              <li><strong>Renderer</strong>：WebGLRenderer，硬件加速</li>
              <li><strong>Camera</strong>：PerspectiveCamera，透视投影</li>
              <li><strong>Lighting</strong>：环境光 + 方向光 + 点光源</li>
              <li><strong>Shadow</strong>：软阴影映射，增强立体感</li>
            </ul>
          </div>

          <div class="arch-card">
            <div class="arch-header">
              <div class="arch-number">03</div>
              <h3>交互系统</h3>
            </div>
            <p class="arch-desc">用户输入处理与动画系统</p>
            <ul class="arch-list">
              <li><strong>Raycaster</strong>：鼠标/触摸点击检测</li>
              <li><strong>OrbitControls</strong>：摄像机轨道控制</li>
              <li>
                <strong>Animation Loop</strong>：requestAnimationFrame 循环
              </li>
              <li><strong>Tweening</strong>：GSAP 补间动画库</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Data Structure -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">魔方数据结构</h2>
        <div class="two-column-grid">
          <div class="content-card">
            <h3>几何表示</h3>
            <p class="card-desc">3x3 离散点阵坐标系生成基础魔方块位置</p>
            <CodeBlock
              language="javascript"
              title="魔方几何生成"
              :code="generateCubiesCode"
            />
          </div>

          <div class="content-card">
            <h3>颜色映射</h3>
            <p class="card-desc">标准配色方案，支持多种材质和纹理</p>
            <ul class="feature-list">
              <li>
                <strong>标准配色</strong
                >：白(U)、红(R)、橙(L)、绿(F)、蓝(B)、黄(D)
              </li>
              <li>
                <strong>材质系统</strong>：每个面独立 Material，支持高光和反光
              </li>
              <li>
                <strong>纹理选项</strong>：纯色、磨砂、光泽、半透明多种预设
              </li>
              <li><strong>状态同步</strong>：颜色数组与 3D 渲染实时同步</li>
            </ul>
            <div class="color-preview">
              <div class="color-swatch" style="background: #ffffff">U</div>
              <div class="color-swatch" style="background: #b71234">R</div>
              <div class="color-swatch" style="background: #ff5800">L</div>
              <div class="color-swatch" style="background: #009b48">F</div>
              <div class="color-swatch" style="background: #0046ad">B</div>
              <div class="color-swatch" style="background: #ffd500">D</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Customization System -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">魔方外观定制系统</h2>
        <p class="section-desc">
          通过 useCubeCustomization
          组合式函数，用户可以自定义魔方的材质、纹理、光照和几何参数，打造独特的视觉体验。
        </p>

        <div class="customization-grid">
          <div class="custom-card">
            <div class="custom-icon icon-blue"><PaintBrushIcon /></div>
            <h3>材质系统</h3>
            <p class="custom-desc">四种材质类型，满足不同视觉效果需求</p>
            <ul class="custom-list">
              <li><strong>Standard</strong>：标准材质，平衡性能与效果</li>
              <li><strong>Metal</strong>：金属材质，高反光质感</li>
              <li><strong>Glass</strong>：玻璃材质，半透明效果</li>
              <li><strong>Toon</strong>：卡通材质，漫画风格渲染</li>
            </ul>
          </div>

          <div class="custom-card">
            <div class="custom-icon icon-cyan"><PhotoIcon /></div>
            <h3>纹理系统</h3>
            <p class="custom-desc">内置纹理与自定义上传双重支持</p>
            <ul class="custom-list">
              <li><strong>内置纹理</strong>：木纹、碳纤维、金属拉丝等</li>
              <li><strong>自定义上传</strong>：支持 JPG/PNG 格式图片</li>
              <li><strong>Base64 转换</strong>：前端处理，无需后端存储</li>
              <li><strong>UV 映射</strong>：正确的纹理坐标映射</li>
            </ul>
          </div>

          <div class="custom-card">
            <div class="custom-icon icon-yellow"><LightBulbIcon /></div>
            <h3>光照配置</h3>
            <p class="custom-desc">动态调节光照参数，改变魔方视觉效果</p>
            <ul class="custom-list">
              <li><strong>环境光强度</strong>：控制整体亮度</li>
              <li><strong>方向光强度</strong>：主光源明暗调节</li>
              <li><strong>方向光颜色</strong>：支持自定义光源色温</li>
              <li><strong>实时预览</strong>：参数调整即时生效</li>
            </ul>
          </div>

          <div class="custom-card">
            <div class="custom-icon icon-green"><CubeTransparentIcon /></div>
            <h3>几何体参数</h3>
            <p class="custom-desc">调整魔方块形状，创造不同风格</p>
            <ul class="custom-list">
              <li><strong>圆角半径</strong>：0-0.5 可调节</li>
              <li><strong>方块间隙</strong>：控制块间缝隙大小</li>
              <li><strong>整体尺寸</strong>：缩放比例调节</li>
              <li><strong>比例保持</strong>：等比缩放防止变形</li>
            </ul>
          </div>
        </div>

        <div class="config-code">
          <h3>配置持久化</h3>
          <p class="code-desc">
            使用 localStorage 保存用户配置，刷新页面后自动恢复
          </p>
          <CodeBlock
            language="javascript"
            title="useCubeCustomization.js"
            :code="customizationCode"
          />
        </div>
      </section>

      <!-- Animation System -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">动画系统</h2>
        <div class="animation-layout">
          <div class="animation-main">
            <h3>旋转动画实现</h3>
            <p class="anim-desc">基于 requestAnimationFrame 的高性能旋转动画</p>
            <CodeBlock
              language="javascript"
              title="旋转动画实现"
              :code="rotateLayerCode"
            />
          </div>

          <div class="animation-side">
            <h3>性能优化</h3>
            <ul class="optimization-list">
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

      <!-- Interaction -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">交互实现</h2>
        <div class="interaction-list">
          <div class="interaction-item">
            <div class="item-number">1</div>
            <div class="item-content">
              <h3>点击检测</h3>
              <p>
                使用 Raycaster
                从鼠标位置发射射线，与魔方块求交，确定点击的面和层。
              </p>
              <CodeBlock
                language="javascript"
                title="点击检测"
                :foldable="false"
                :code="raycasterCode"
              />
            </div>
          </div>

          <div class="interaction-item">
            <div class="item-number">2</div>
            <div class="item-content">
              <h3>拖动识别</h3>
              <p>跟踪鼠标移动向量，确定旋转方向和层，阈值处理避免误操作。</p>
              <CodeBlock
                language="javascript"
                title="拖动识别"
                :foldable="false"
                :code="dragVectorCode"
              />
            </div>
          </div>

          <div class="interaction-item">
            <div class="item-number">3</div>
            <div class="item-content">
              <h3>动画队列</h3>
              <p>顺序执行旋转动画，支持撤销/重做，确保状态一致性。</p>
              <CodeBlock
                language="javascript"
                title="动画队列"
                :foldable="false"
                :code="animationQueueCode"
              />
            </div>
          </div>
        </div>
      </section>

      <!-- Performance -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">性能指标</h2>
        <div class="metrics-grid">
          <div class="metric-item">
            <div class="metric-value">60</div>
            <div class="metric-label">FPS</div>
            <div class="metric-desc">目标帧率 (vsync 同步)</div>
          </div>
          <div class="metric-item">
            <div class="metric-value">&lt; 16ms</div>
            <div class="metric-label">帧时间</div>
            <div class="metric-desc">每帧渲染时间</div>
          </div>
          <div class="metric-item">
            <div class="metric-value">27</div>
            <div class="metric-label">绘制调用</div>
            <div class="metric-desc">InstancedMesh 优化</div>
          </div>
        </div>

        <div class="optimization-tips-box">
          <h3>优化技巧</h3>
          <ul class="tips-list">
            <li>
              <strong>几何体合并</strong>：将多个 Mesh 合并为单个，减少 draw
              calls
            </li>
            <li>
              <strong>纹理图集</strong>：将多个小纹理合并为大图，减少纹理切换
            </li>
            <li>
              <strong>细节层次 (LOD)</strong>：远距离使用简化模型，提升渲染速度
            </li>
            <li><strong>视锥剔除</strong>：只渲染摄像机可见范围内的对象</li>
            <li>
              <strong>WebWorker</strong>：复杂计算移至 Worker 线程，避免阻塞渲染
            </li>
          </ul>
        </div>
      </section>

      <!-- Challenges -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">技术挑战</h2>
        <div class="challenges-grid">
          <div class="challenge-box">
            <div class="challenge-icon icon-cyan"><DevicePhoneMobileIcon /></div>
            <h3>移动端适配</h3>
            <p>
              <strong>问题</strong>：移动设备 GPU 性能有限，触摸交互精度要求高
            </p>
            <p>
              <strong>解决方案</strong
              >：响应式设计，简化阴影和反射，增大触摸热区
            </p>
          </div>
          <div class="challenge-box">
            <div class="challenge-icon icon-blue"><GlobeAltIcon /></div>
            <h3>浏览器兼容</h3>
            <p>
              <strong>问题</strong>：不同浏览器 WebGL 实现差异，扩展支持不一致
            </p>
            <p>
              <strong>解决方案</strong>：特性检测，渐进增强，提供降级方案 (CSS
              3D)
            </p>
          </div>
          <div class="challenge-box">
            <div class="challenge-icon icon-tool"><Cog6ToothIcon /></div>
            <h3>状态同步</h3>
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
            <div class="nav-icon icon-ai"><EyeIcon /></div>
            <h3>YOLOv8 视觉识别</h3>
            <p>魔方颜色检测技术详解</p>
          </router-link>
          <router-link to="/tech/kociemba" class="nav-card">
            <div class="nav-icon icon-learning"><PuzzlePieceIcon /></div>
            <h3>Kociemba 算法</h3>
            <p>魔方两阶段求解算法原理</p>
          </router-link>
          <router-link to="/tech/architecture" class="nav-card">
            <div class="nav-icon icon-tech"><BuildingOffice2Icon /></div>
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
import { 
  PaintBrushIcon,
  LightBulbIcon,
  DevicePhoneMobileIcon,
  GlobeAltIcon,
  EyeIcon,
  PuzzlePieceIcon,
  BuildingOffice2Icon,
  PhotoIcon,
  CubeTransparentIcon,
  Cog6ToothIcon
} from "@heroicons/vue/24/solid";
import CodeBlock from "../components/CodeBlock.vue";

const router = useRouter();
const showBackToTop = ref(false);

const generateCubiesCode = `// 生成基础 3x3 离散点阵坐标系
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
  if (sum === 3) return 'corner';     // 角块
  if (sum === 2) return 'edge';       // 棱块
  if (sum === 1) return 'center';     // 中心块
  return 'core';                      // 核心块
};`;

const customizationCode = `// useCubeCustomization.js
export function useCubeCustomization() {
  const config = ref(loadConfig()); // 从 localStorage 加载
  
  // 自动保存（防抖）
  watch(config, () => {
    if (saveTimeout) clearTimeout(saveTimeout);
    saveTimeout = setTimeout(() => {
      saveConfig(config.value);
    }, 1000);
  }, { deep: true });
  
  return {
    config,
    updateConfig,
    resetToDefault,
    uploadCustomTexture,
    // ... 其他方法
  };
}`;

const rotateLayerCode = `// 执行单层旋转动画
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
      
      const currentAngle = angle * eased * (direction === 'clockwise' ? 1 : -1);
      const axis = getAxisForLayer(layer);
      container.rotation[axis] = THREE.MathUtils.degToRad(currentAngle);
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        updateCubeStateAfterRotation(layer, direction);
        scene.remove(container);
        resolve();
      }
    }
    
    requestAnimationFrame(animate);
  });
}`;

const raycasterCode = `const raycaster = new THREE.Raycaster();
raycaster.setFromCamera(mouse, camera);
const intersects = raycaster.intersectObjects(cubies);
if (intersects.length > 0) {
  const clickedCubie = intersects[0].object;
  const faceNormal = getClickedFace(intersects[0].face);
}`;

const dragVectorCode = `const dragVector = new THREE.Vector2(
  currentMouse.x - startMouse.x,
  currentMouse.y - startMouse.y
);
if (dragVector.length() > DRAG_THRESHOLD) {
  const axis = determineRotationAxis(dragVector, clickedFace);
  rotateLayer(getLayerFromAxisAndFace(axis, clickedFace), direction);
}`;

const animationQueueCode = `class AnimationQueue {
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
      await this.queue.shift()();
    }
    this.isAnimating = false;
  }
}`;

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
  router.push({ path: "/about", state: { scrollTarget: "tech-docs" } });
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
  handleScroll();
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});
</script>

<style scoped>
/* 基础样式 */
.tech-doc-page {
  width: 100%;
  min-height: 100vh;
  background-color: #f8fafc;
  font-family:
    "Inter",
    -apple-system,
    BlinkMacSystemFont,
    sans-serif;
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
  text-align: center;
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
  justify-content: center;
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
  margin-bottom: 24px;
}
.section-desc {
  font-size: 1.125rem;
  color: #64748b;
  margin-bottom: 40px;
  line-height: 1.6;
}
.text-center {
  text-align: center;
}

/* 核心架构 - 3列网格 */
.architecture-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.arch-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.arch-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.arch-number {
  width: 36px;
  height: 36px;
  background: #3b82f6;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 800;
  flex-shrink: 0;
}

.arch-header h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.arch-desc {
  color: #64748b;
  margin-bottom: 20px;
  line-height: 1.5;
}

.arch-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.arch-list li {
  color: #64748b;
  margin-bottom: 8px;
  line-height: 1.5;
}

.arch-list li strong {
  color: #1e293b;
}

/* 两列布局 */
.two-column-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
}

.content-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.content-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 12px;
}

.card-desc {
  color: #64748b;
  margin-bottom: 20px;
  line-height: 1.5;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0 0 20px 0;
}

.feature-list li {
  color: #64748b;
  margin-bottom: 12px;
  line-height: 1.5;
}

.feature-list li strong {
  color: #1e293b;
}

/* 颜色预览 */
.color-preview {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.color-swatch {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.7);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.8);
}

/* 定制系统 - 4列网格 */
.customization-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 40px;
}

.custom-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 24px;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.custom-icon {
  width: 32px;
  height: 32px;
  margin-bottom: 16px;
  flex-shrink: 0;
}

.custom-card h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.custom-desc {
  color: #64748b;
  font-size: 0.875rem;
  margin-bottom: 16px;
  line-height: 1.5;
}

.custom-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.custom-list li {
  color: #64748b;
  font-size: 0.875rem;
  margin-bottom: 6px;
  line-height: 1.4;
}

.custom-list li strong {
  color: #1e293b;
}

.config-code {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.config-code h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.code-desc {
  color: #64748b;
  margin-bottom: 20px;
}

/* 动画系统 */
.animation-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

.animation-main {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.animation-main h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.anim-desc {
  color: #64748b;
  margin-bottom: 20px;
}

.animation-side {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.animation-side h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 20px;
}

.optimization-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.optimization-list li {
  color: #64748b;
  margin-bottom: 12px;
  line-height: 1.5;
}

.optimization-list li strong {
  color: #1e293b;
}

/* 交互实现 - 垂直列表 */
.interaction-list {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.interaction-item {
  display: flex;
  gap: 24px;
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.item-number {
  width: 36px;
  height: 36px;
  background: #3b82f6;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
  font-weight: 700;
  flex-shrink: 0;
}

.item-content {
  flex: 1;
}

.item-content h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 12px;
}

.item-content p {
  color: #64748b;
  margin-bottom: 16px;
  line-height: 1.5;
}

/* 性能指标 */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 40px;
}

.metric-item {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
  text-align: center;
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
  font-size: 0.875rem;
  color: #64748b;
}

.optimization-tips-box {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.optimization-tips-box h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 20px;
}

.tips-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.tips-list li {
  color: #64748b;
  line-height: 1.5;
  padding-left: 24px;
  position: relative;
}

.tips-list li:before {
  content: "✓";
  color: #10b981;
  position: absolute;
  left: 0;
  font-weight: bold;
}

.tips-list li strong {
  color: #1e293b;
}

/* 技术挑战 */
.challenges-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.challenge-box {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.challenge-icon {
  width: 32px;
  height: 32px;
  margin-bottom: 16px;
  flex-shrink: 0;
}

.challenge-box h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 16px;
}

.challenge-box p {
  color: #64748b;
  margin-bottom: 12px;
  line-height: 1.5;
}

.challenge-box p strong {
  color: #1e293b;
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
  width: 40px;
  height: 40px;
  margin-bottom: 16px;
  flex-shrink: 0;
}

.nav-icon svg {
  width: 40px;
  height: 40px;
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

/* 返回按钮 */
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

/* 响应式 */
@media (max-width: 992px) {
  .architecture-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .customization-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .animation-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  .architecture-grid {
    grid-template-columns: 1fr;
  }
  .two-column-grid {
    grid-template-columns: 1fr;
  }
  .customization-grid {
    grid-template-columns: 1fr;
  }
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  .challenges-grid {
    grid-template-columns: 1fr;
  }
  .nav-cards {
    grid-template-columns: 1fr;
  }
  .tips-list {
    grid-template-columns: 1fr;
  }
  .stats-pills {
    flex-direction: column;
    align-items: center;
  }
}

@media (max-width: 576px) {
  .hero-title {
    font-size: 2rem;
  }
  .interaction-item {
    flex-direction: column;
  }
  .item-number {
    width: 32px;
    height: 32px;
    font-size: 1rem;
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

[data-theme="dark"] .section-desc {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .arch-card,
[data-theme="dark"] .content-card,
[data-theme="dark"] .custom-card,
[data-theme="dark"] .config-code,
[data-theme="dark"] .animation-main,
[data-theme="dark"] .animation-side,
[data-theme="dark"] .interaction-item,
[data-theme="dark"] .metric-item,
[data-theme="dark"] .optimization-tips-box,
[data-theme="dark"] .challenge-box,
[data-theme="dark"] .nav-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .arch-header h3,
[data-theme="dark"] .content-card h3,
[data-theme="dark"] .custom-card h3,
[data-theme="dark"] .config-code h3,
[data-theme="dark"] .animation-main h3,
[data-theme="dark"] .animation-side h3,
[data-theme="dark"] .item-content h3,
[data-theme="dark"] .optimization-tips-box h3,
[data-theme="dark"] .challenge-box h3,
[data-theme="dark"] .nav-card h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .arch-desc,
[data-theme="dark"] .card-desc,
[data-theme="dark"] .custom-desc,
[data-theme="dark"] .code-desc,
[data-theme="dark"] .anim-desc,
[data-theme="dark"] .item-content p,
[data-theme="dark"] .challenge-box p {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .arch-list li,
[data-theme="dark"] .feature-list li,
[data-theme="dark"] .custom-list li,
[data-theme="dark"] .optimization-list li,
[data-theme="dark"] .tips-list li {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .arch-list li strong,
[data-theme="dark"] .feature-list li strong,
[data-theme="dark"] .custom-list li strong,
[data-theme="dark"] .optimization-list li strong,
[data-theme="dark"] .tips-list li strong,
[data-theme="dark"] .challenge-box p strong {
  color: var(--dm-text-primary);
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

[data-theme="dark"] .color-swatch {
  border-color: var(--dm-border);
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

[data-theme="dark"] .nav-card:hover {
  border-color: var(--dm-accent);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .nav-card p {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .tips-list li:before {
  color: #34d399;
}
</style>
