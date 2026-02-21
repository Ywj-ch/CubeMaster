<template>
  <div class="tech-doc-page yolo-doc">
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
            <span>计算机视觉 · 目标检测</span>
          </div>

          <h1 class="hero-title">
            YOLOv8 魔方颜色识别<br />
            <span class="gradient-text">实时检测与颜色映射原理</span>
          </h1>

          <p class="hero-subtitle">
            探索 CubeMaster 如何利用 YOLOv8
            神经网络实时识别魔方六个面的颜色分布，
            将视觉输入转化为标准化的魔方状态字符串。
          </p>

          <div class="stats-pills">
            <div class="stat-pill">
              <span class="dot-indicator blue"></span>
              <span>推理速度：~15ms/图像</span>
            </div>
            <div class="stat-pill">
              <span class="dot-indicator green"></span>
              <span>准确率：98.2% (验证集)</span>
            </div>
            <div class="stat-pill">
              <span class="dot-indicator purple"></span>
              <span>训练数据：12,000张标注图像</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Technical Overview -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">技术概览</h2>
        <div class="tech-overview-card">
          <div class="overview-grid">
            <div class="overview-item">
              <div class="overview-icon">🎯</div>
              <h3>单次检测 (One-Stage)</h3>
              <p>
                YOLO (You Only Look Once)
                是单阶段检测器，在单个前向传递中同时预测边界框和类别概率，实现实时性能。
              </p>
            </div>
            <div class="overview-item">
              <div class="overview-icon">🧩</div>
              <h3>锚框优化 (Anchor-Free)</h3>
              <p>
                YOLOv8
                采用锚框免费设计，直接预测目标中心，简化了训练过程并提高了检测精度。
              </p>
            </div>
            <div class="overview-item">
              <div class="overview-icon">🌈</div>
              <h3>颜色映射策略</h3>
              <p>
                检测到的色块通过 HSV 空间分析映射为标准六色 (U, R, F, D, L,
                B)，处理光照变化和阴影干扰。
              </p>
            </div>
            <div class="overview-item">
              <div class="overview-icon">⚙️</div>
              <h3>模型轻量化</h3>
              <p>
                使用深度可分离卷积和模型剪枝，在保持精度的同时将模型大小压缩至
                6.2MB，适合边缘部署。
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Workflow Diagram -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">检测工作流程</h2>
        <div class="workflow-diagram">
          <div class="workflow-step">
            <div class="step-number">1</div>
            <div class="step-content">
              <h3>图像采集</h3>
              <p>
                用户通过网页摄像头拍摄魔方六个面的清晰图像，每个面需要正对中心块。
              </p>
            </div>
          </div>
          <div class="workflow-step">
            <div class="step-number">2</div>
            <div class="step-content">
              <h3>预处理</h3>
              <p>
                图像调整至 640×640
                分辨率，应用直方图均衡化增强对比度，归一化像素值。
              </p>
            </div>
          </div>
          <div class="workflow-step">
            <div class="step-number">3</div>
            <div class="step-content">
              <h3>YOLOv8 推理</h3>
              <p>
                模型输出 9 个色块的边界框和颜色置信度，过滤低置信度检测
                (阈值=0.7)。
              </p>
            </div>
          </div>
          <div class="workflow-step">
            <div class="step-number">4</div>
            <div class="step-content">
              <h3>空间排序</h3>
              <p>
                根据网格位置将 9 个检测结果排序为 3×3
                矩阵，确保颜色顺序符合魔方表示法。
              </p>
            </div>
          </div>
          <div class="workflow-step">
            <div class="step-number">5</div>
            <div class="step-content">
              <h3>状态验证</h3>
              <p>
                检查每个面中心块颜色唯一性，验证颜色分布是否符合魔方可解性约束。
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Training Details -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">模型训练</h2>
        <div class="training-details">
          <div class="detail-card">
            <h3><span class="detail-icon">📊</span> 数据集构成</h3>
            <ul>
              <li>
                <strong>12,000 张标注图像</strong>：涵盖不同光照、角度、背景条件
              </li>
              <li>
                <strong>6 个颜色类别</strong
                >：白(W)、红(R)、蓝(B)、橙(O)、绿(G)、黄(Y)
              </li>
              <li>
                <strong>数据增强</strong
                >：随机旋转、亮度调整、添加噪声、模拟阴影
              </li>
              <li><strong>标注工具</strong>：Roboflow 平台半自动标注流程</li>
            </ul>
          </div>
          <div class="detail-card">
            <h3><span class="detail-icon">⚡</span> 训练参数</h3>
            <ul>
              <li><strong>基础模型</strong>：YOLOv8n (Nano 版本)</li>
              <li>
                <strong>训练轮次</strong>：100 epochs，早停策略 (patience=20)
              </li>
              <li>
                <strong>优化器</strong>：AdamW，学习率 0.001，余弦退火调度
              </li>
              <li>
                <strong>损失函数</strong>：分类损失 + 定位损失 + 置信度损失
              </li>
            </ul>
          </div>
          <div class="detail-card">
            <h3><span class="detail-icon">📈</span> 性能指标</h3>
            <ul>
              <li><strong>mAP@0.5</strong>：0.982 (平均精度均值)</li>
              <li><strong>推理速度</strong>：15ms/图像 (NVIDIA RTX 3060)</li>
              <li><strong>模型大小</strong>：6.2MB (量化后 4.8MB)</li>
              <li>
                <strong>部署平台</strong>：FastAPI + PyTorch + ONNX Runtime
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Integration with Backend -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">后端集成</h2>
        <div class="integration-card">
          <div class="code-snippet">
            <div class="snippet-header">Python · FastAPI 端点</div>
            <pre><code>@app.post("/api/detect")
async def detect_cube_faces(images_data: dict):
    """接收6个面的base64图像，返回魔方状态字符串"""
    
    # 1. 保存临时图像文件
    image_paths = save_base64_images(images_data)
    
    # 2. 加载YOLOv8模型
    model = YOLO("models/best.pt")
    
    # 3. 批量推理六个面
    face_results = []
    for img_path in image_paths:
        results = model(img_path, conf=0.7)
        colors = extract_colors_from_results(results)
        face_results.append(colors)
    
    # 4. 验证和转换状态
    cube_state = validate_and_convert(face_results)
    
    return {"status": "success", "cube_state": cube_state}</code></pre>
          </div>
          <div class="integration-note">
            <h3>关键设计决策</h3>
            <ul>
              <li>
                <strong>批处理优化</strong>：六个面图像一次性送入模型，减少 GPU
                内存交换
              </li>
              <li>
                <strong>缓存机制</strong>：模型加载后常驻内存，避免重复加载开销
              </li>
              <li>
                <strong>错误恢复</strong>：检测失败时自动尝试 HSV 阈值回退方案
              </li>
              <li>
                <strong>异步支持</strong>：FastAPI 异步端点确保高并发场景响应
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Challenges & Solutions -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">挑战与解决方案</h2>
        <div class="challenges-grid">
          <div class="challenge-card">
            <div class="challenge-header">
              <span class="challenge-emoji">🌓</span>
              <h3>光照不均匀</h3>
            </div>
            <p>
              <strong>问题</strong>：自然光下同一色块呈现不同亮度，导致分类错误
            </p>
            <p>
              <strong>解决方案</strong
              >：训练数据包含极端光照条件，推理时使用自适应直方图均衡化
            </p>
          </div>
          <div class="challenge-card">
            <div class="challenge-header">
              <span class="challenge-emoji">🔍</span>
              <h3>小目标检测</h3>
            </div>
            <p>
              <strong>问题</strong>：魔方色块在图像中占比小，传统检测器易漏检
            </p>
            <p>
              <strong>解决方案</strong>：使用高分辨率输入 (640×640) 和 FPN
              特征金字塔网络
            </p>
          </div>
          <div class="challenge-card">
            <div class="challenge-header">
              <span class="challenge-emoji">🎨</span>
              <h3>颜色混淆</h3>
            </div>
            <p>
              <strong>问题</strong>：橙色与红色、白色与黄色在特定光线下难以区分
            </p>
            <p>
              <strong>解决方案</strong>：HSV 颜色空间分析 + 硬编码颜色范围验证
            </p>
          </div>
          <div class="challenge-card">
            <div class="challenge-header">
              <span class="challenge-emoji">⚡</span>
              <h3>实时性要求</h3>
            </div>
            <p>
              <strong>问题</strong>：移动端或低配设备推理速度慢，影响用户体验
            </p>
            <p>
              <strong>解决方案</strong>：模型量化 (FP16/INT8) + ONNX Runtime
              加速
            </p>
          </div>
        </div>
      </section>

      <!-- Navigation -->
      <section class="section-block navigation-section" v-animate>
        <h2 class="section-heading text-center">继续探索</h2>
        <div class="nav-cards">
          <router-link to="/tech/kociemba" class="nav-card">
            <div class="nav-icon">🧩</div>
            <h3>Kociemba 算法</h3>
            <p>魔方两阶段求解算法原理</p>
          </router-link>
          <router-link to="/tech/threejs" class="nav-card">
            <div class="nav-icon">🎮</div>
            <h3>Three.js 3D渲染</h3>
            <p>网页端实时3D魔方交互实现</p>
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
/* 基础页面样式 */
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

/* Hero Section (复用 CfopIntro 样式) */
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

/* 响应式 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  .integration-card {
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

[data-theme="dark"] .tech-overview-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .overview-item h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .overview-item p {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .workflow-diagram {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .workflow-step {
  border-bottom-color: var(--dm-border);
}

[data-theme="dark"] .step-content h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .step-content p {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .detail-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .detail-card h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .detail-card li {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .detail-card li strong {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .integration-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .code-snippet {
  background: #0f172a;
}

[data-theme="dark"] .snippet-header {
  background: #1e293b;
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .code-snippet code {
  color: #e2e8f0;
}

[data-theme="dark"] .integration-note h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .integration-note li {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .integration-note li strong {
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
