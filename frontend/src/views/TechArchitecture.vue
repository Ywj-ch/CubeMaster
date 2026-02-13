<template>
  <div class="tech-doc-page architecture-doc">
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
            <span>系统设计 · 前后端分离</span>
          </div>

          <h1 class="hero-title">
            CubeMaster 系统架构<br />
            <span class="gradient-text">现代 Web 应用的全栈设计</span>
          </h1>

          <p class="hero-subtitle">
            深入解析 CubeMaster 的微服务架构、数据流设计和基础设施选择，
            展示如何将计算机视觉、求解算法和 3D 渲染无缝集成到统一应用。
          </p>

          <div class="stats-pills">
            <div class="stat-pill">
              <span class="dot-indicator blue"></span>
              <span>响应时间：&lt; 200ms</span>
            </div>
            <div class="stat-pill">
              <span class="dot-indicator green"></span>
              <span>可用性：99.9% (设计目标)</span>
            </div>
            <div class="stat-pill">
              <span class="dot-indicator purple"></span>
              <span>代码行数：~15,000 行</span>
            </div>
          </div>
        </div>
      </section>

      <!-- System Overview -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">系统概览</h2>
        <div class="system-overview">
          <div class="overview-diagram">
            <div class="layer frontend-layer">
              <div class="layer-title">前端层 (Vue 3)</div>
              <div class="layer-components">
                <div class="component">UI 组件库</div>
                <div class="component">3D 渲染引擎</div>
                <div class="component">状态管理</div>
                <div class="component">路由导航</div>
              </div>
            </div>

            <div class="layer arrow-layer">⇅ HTTP/WebSocket</div>

            <div class="layer backend-layer">
              <div class="layer-title">后端层 (FastAPI)</div>
              <div class="layer-components">
                <div class="component">REST API</div>
                <div class="component">YOLOv8 推理</div>
                <div class="component">求解引擎</div>
                <div class="component">文件服务</div>
              </div>
            </div>

            <div class="layer arrow-layer">⇅ 模型文件</div>

            <div class="layer data-layer">
              <div class="layer-title">数据层</div>
              <div class="layer-components">
                <div class="component">SQLite 数据库</div>
                <div class="component">模型文件 (.pt)</div>
                <div class="component">静态资源</div>
              </div>
            </div>
          </div>

          <div class="overview-description">
            <p>
              <strong>前后端分离架构</strong>：前端独立部署，通过 REST API
              与后端通信，实现关注点分离和独立扩展。
            </p>
            <p>
              <strong>无状态设计</strong
              >：后端服务无状态，支持水平扩展，通过负载均衡处理高并发请求。
            </p>
            <p>
              <strong>渐进增强</strong
              >：核心功能在所有浏览器可用，高级特性（WebGL、WebRTC）作为增强。
            </p>
          </div>
        </div>
      </section>

      <!-- Frontend Architecture -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">前端架构</h2>
        <div class="frontend-architecture">
          <div class="frontend-grid">
            <div class="frontend-module">
              <h3><span class="module-icon">🎨</span> UI 框架</h3>
              <ul>
                <li>
                  <strong>Vue 3 Composition API</strong
                  >：响应式数据绑定和组件逻辑
                </li>
                <li><strong>Element Plus</strong>：企业级 UI 组件库</li>
                <li><strong>Vue Router</strong>：SPA 路由管理，支持嵌套路由</li>
                <li><strong>Pinia</strong>：状态管理，替代 Vuex 的轻量方案</li>
              </ul>
            </div>

            <div class="frontend-module">
              <h3><span class="module-icon">🎮</span> 3D 引擎</h3>
              <ul>
                <li><strong>Three.js</strong>：WebGL 渲染库，核心 3D 功能</li>
                <li><strong>GSAP</strong>：动画库，流畅的补间动画</li>
                <li><strong>自定义控件</strong>：魔方专用交互系统</li>
                <li><strong>性能监控</strong>：帧率统计和内存管理</li>
              </ul>
            </div>

            <div class="frontend-module">
              <h3><span class="module-icon">🔌</span> 网络层</h3>
              <ul>
                <li><strong>Axios</strong>：HTTP 客户端，拦截器和错误处理</li>
                <li><strong>WebSocket</strong>：实时通信（未来扩展）</li>
                <li><strong>请求队列</strong>：顺序处理，避免竞态条件</li>
                <li><strong>缓存策略</strong>：本地存储频繁访问数据</li>
              </ul>
            </div>

            <div class="frontend-module">
              <h3><span class="module-icon">📱</span> 构建工具</h3>
              <ul>
                <li><strong>Vite</strong>：极速构建工具，开发服务器</li>
                <li><strong>TypeScript</strong>：类型安全，代码提示</li>
                <li><strong>ESLint + Prettier</strong>：代码规范和格式化</li>
                <li><strong>自动部署</strong>：GitHub Actions + Vercel</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- Backend Architecture -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">后端架构</h2>
        <div class="backend-architecture">
          <div class="backend-services">
            <div class="service-card">
              <div class="service-header">
                <div class="service-icon">🔍</div>
                <h3>视觉识别服务</h3>
              </div>
              <div class="service-details">
                <p>
                  <strong>职责</strong>：处理图像上传，运行 YOLOv8
                  推理，返回颜色检测结果
                </p>
                <div class="code-snippet small">
                  <pre><code>POST /api/detect
Content-Type: multipart/form-data

{
  "images": ["base64_front", "base64_right", ...],
  "confidence_threshold": 0.7
}

Response:
{
  "status": "success",
  "cube_state": "UUUUUUUUURRR...",
  "processing_time": 0.15
}</code></pre>
                </div>
                <p>
                  <strong>技术栈</strong>：FastAPI, PyTorch, OpenCV, Ultralytics
                  YOLOv8
                </p>
              </div>
            </div>

            <div class="service-card">
              <div class="service-header">
                <div class="service-icon">🧩</div>
                <h3>求解引擎服务</h3>
              </div>
              <div class="service-details">
                <p>
                  <strong>职责</strong>：接收魔方状态，调用 Kociemba
                  算法，返回解法步骤
                </p>
                <div class="code-snippet small">
                  <pre><code>POST /api/solve
Content-Type: application/json

{
  "cube_state": "UUUUUUUUURRR...",
  "max_depth": 24,
  "timeout": 5
}

Response:
{
  "solution": "U R' F2 D2 L",
  "move_count": 19,
  "solve_time": 0.08
}</code></pre>
                </div>
                <p>
                  <strong>技术栈</strong>：FastAPI, Python, twophase (Kociemba),
                  缓存机制
                </p>
              </div>
            </div>

            <div class="service-card">
              <div class="service-header">
                <div class="service-icon">📊</div>
                <h3>数据持久化服务</h3>
              </div>
              <div class="service-details">
                <p>
                  <strong>职责</strong>：用户进度保存，算法学习记录，统计分析
                </p>
                <div class="code-snippet small">
                  <pre><code># SQLite 数据库设计
CREATE TABLE user_progress (
  id INTEGER PRIMARY KEY,
  user_id TEXT,
  algorithm TEXT,
  solve_times JSON,
  best_time REAL,
  created_at TIMESTAMP
);</code></pre>
                </div>
                <p>
                  <strong>技术栈</strong>：SQLAlchemy, SQLite, Alembic (迁移),
                  JWT 认证
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Data Flow -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">数据流设计</h2>
        <div class="data-flow-diagram">
          <div class="flow-step">
            <div class="step-number">1</div>
            <div class="step-content">
              <h3>用户输入</h3>
              <p>用户通过摄像头拍摄魔方六面图像，或手动输入魔方状态。</p>
              <div class="step-tags">
                <span class="tag">WebRTC 摄像头</span>
                <span class="tag">手动输入界面</span>
                <span class="tag">文件上传</span>
              </div>
            </div>
          </div>

          <div class="flow-arrow">↓</div>

          <div class="flow-step">
            <div class="step-number">2</div>
            <div class="step-content">
              <h3>前端处理</h3>
              <p>图像预处理、Base64 编码、状态验证，通过 HTTP 发送到后端。</p>
              <div class="step-tags">
                <span class="tag">Canvas 图像处理</span>
                <span class="tag">Base64 编码</span>
                <span class="tag">状态验证</span>
              </div>
            </div>
          </div>

          <div class="flow-arrow">↓</div>

          <div class="flow-step">
            <div class="step-number">3</div>
            <div class="step-content">
              <h3>后端推理</h3>
              <p>YOLOv8 识别颜色，验证状态合法性，返回标准魔方字符串。</p>
              <div class="step-tags">
                <span class="tag">YOLOv8 推理</span>
                <span class="tag">颜色映射</span>
                <span class="tag">状态验证</span>
              </div>
            </div>
          </div>

          <div class="flow-arrow">↓</div>

          <div class="flow-step">
            <div class="step-number">4</div>
            <div class="step-content">
              <h3>求解计算</h3>
              <p>Kociemba 算法求解，优化解法步骤，返回人类可读的解法。</p>
              <div class="step-tags">
                <span class="tag">Kociemba 算法</span>
                <span class="tag">解法优化</span>
                <span class="tag">步骤分解</span>
              </div>
            </div>
          </div>

          <div class="flow-arrow">↓</div>

          <div class="flow-step">
            <div class="step-number">5</div>
            <div class="step-content">
              <h3>3D 可视化</h3>
              <p>前端接收解法，通过 Three.js 逐步动画演示还原过程。</p>
              <div class="step-tags">
                <span class="tag">Three.js 动画</span>
                <span class="tag">步骤高亮</span>
                <span class="tag">交互控制</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Deployment & DevOps -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">部署与运维</h2>
        <div class="deployment-grid">
          <div class="deploy-card">
            <h3><span class="deploy-icon">🚀</span> 前端部署</h3>
            <ul>
              <li>
                <strong>静态托管</strong>：Vercel / Netlify / GitHub Pages
              </li>
              <li><strong>CDN 加速</strong>：Cloudflare CDN 全球分发</li>
              <li><strong>版本管理</strong>：语义化版本，自动更新提示</li>
              <li>
                <strong>监控指标</strong>：Google Analytics, Sentry 错误追踪
              </li>
            </ul>
          </div>

          <div class="deploy-card">
            <h3><span class="deploy-icon">🛠️</span> 后端部署</h3>
            <ul>
              <li><strong>容器化</strong>：Docker + Docker Compose</li>
              <li><strong>云服务</strong>：AWS EC2 / Google Cloud Run</li>
              <li><strong>负载均衡</strong>：Nginx 反向代理，SSL 终止</li>
              <li>
                <strong>自动扩缩</strong>：基于 CPU/内存使用率自动调整实例
              </li>
            </ul>
          </div>

          <div class="deploy-card">
            <h3><span class="deploy-icon">🔒</span> 安全策略</h3>
            <ul>
              <li><strong>CORS 配置</strong>：严格限制允许的源和请求方法</li>
              <li><strong>速率限制</strong>：API 调用频率限制，防止滥用</li>
              <li><strong>输入验证</strong>：所有用户输入严格验证和清理</li>
              <li><strong>数据加密</strong>：HTTPS 传输，敏感数据加密存储</li>
            </ul>
          </div>

          <div class="deploy-card">
            <h3><span class="deploy-icon">📈</span> 监控告警</h3>
            <ul>
              <li><strong>性能监控</strong>：响应时间、错误率、资源使用率</li>
              <li>
                <strong>日志聚合</strong>：ELK Stack (Elasticsearch, Logstash,
                Kibana)
              </li>
              <li><strong>健康检查</strong>：定时端点检查，自动重启失败服务</li>
              <li><strong>告警系统</strong>：Slack/Email 通知关键指标异常</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Scaling Considerations -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">扩展性设计</h2>
        <div class="scaling-considerations">
          <div class="scaling-card">
            <h3><span class="scaling-icon">📱</span> 用户规模扩展</h3>
            <p><strong>挑战</strong>：同时在线用户数从 100 扩展到 10,000+</p>
            <p><strong>解决方案</strong>：</p>
            <ul>
              <li>前端静态资源 CDN 分发</li>
              <li>后端微服务化，独立扩展计算密集型服务</li>
              <li>数据库读写分离，缓存层 (Redis) 减轻负载</li>
              <li>异步任务队列处理批量求解请求</li>
            </ul>
          </div>

          <div class="scaling-card">
            <h3><span class="scaling-icon">🧠</span> 算法功能扩展</h3>
            <p><strong>挑战</strong>：支持更多魔方类型 (4×4, 5×5, 异形)</p>
            <p><strong>解决方案</strong>：</p>
            <ul>
              <li>插件化算法架构，支持动态加载求解器</li>
              <li>统一状态表示接口，适配不同魔方类型</li>
              <li>3D 渲染引擎参数化，支持不同几何结构</li>
              <li>训练数据 pipeline 自动化，快速适配新魔方</li>
            </ul>
          </div>

          <div class="scaling-card">
            <h3><span class="scaling-icon">🌐</span> 国际化扩展</h3>
            <p><strong>挑战</strong>：支持多语言界面和本地化内容</p>
            <p><strong>解决方案</strong>：</p>
            <ul>
              <li>Vue I18n 国际化框架</li>
              <li>内容与代码分离，支持动态语言切换</li>
              <li>本地化算法名称和说明文档</li>
              <li>区域特定的配色方案和 UI 偏好</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Technology Stack -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">技术栈总结</h2>
        <div class="tech-stack-summary">
          <div class="stack-category">
            <h3>前端技术栈</h3>
            <div class="stack-tags">
              <span class="stack-tag vue">Vue 3</span>
              <span class="stack-tag vite">Vite</span>
              <span class="stack-tag typescript">TypeScript</span>
              <span class="stack-tag element">Element Plus</span>
              <span class="stack-tag threejs">Three.js</span>
              <span class="stack-tag pinia">Pinia</span>
              <span class="stack-tag axios">Axios</span>
              <span class="stack-tag gsap">GSAP</span>
            </div>
          </div>

          <div class="stack-category">
            <h3>后端技术栈</h3>
            <div class="stack-tags">
              <span class="stack-tag fastapi">FastAPI</span>
              <span class="stack-tag python">Python 3.10</span>
              <span class="stack-tag pytorch">PyTorch</span>
              <span class="stack-tag yolov8">YOLOv8</span>
              <span class="stack-tag opencv">OpenCV</span>
              <span class="stack-tag kociemba">Kociemba</span>
              <span class="stack-tag sqlalchemy">SQLAlchemy</span>
              <span class="stack-tag docker">Docker</span>
            </div>
          </div>

          <div class="stack-category">
            <h3>开发运维</h3>
            <div class="stack-tags">
              <span class="stack-tag git">Git</span>
              <span class="stack-tag github">GitHub Actions</span>
              <span class="stack-tag eslint">ESLint</span>
              <span class="stack-tag prettier">Prettier</span>
              <span class="stack-tag vercel">Vercel</span>
              <span class="stack-tag nginx">Nginx</span>
              <span class="stack-tag sentry">Sentry</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Navigation -->
      <section class="section-block navigation-section" v-animate>
        <h2 class="section-heading text-center">深入技术细节</h2>
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
          <router-link to="/tech/threejs" class="nav-card">
            <div class="nav-icon">🎮</div>
            <h3>Three.js 3D渲染</h3>
            <p>网页端实时3D魔方交互实现</p>
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

/* === 特定于架构页面的样式 === */

/* 系统概览 */
.system-overview {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
}

.overview-diagram {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 30px;
}

.layer {
  padding: 24px;
  border-radius: 16px;
  text-align: center;
}

.frontend-layer {
  background: linear-gradient(135deg, #42b883 0%, #35495e 100%);
  color: white;
}

.backend-layer {
  background: linear-gradient(135deg, #009688 0%, #004d40 100%);
  color: white;
}

.data-layer {
  background: linear-gradient(135deg, #ff9800 0%, #e65100 100%);
  color: white;
}

.arrow-layer {
  color: #64748b;
  font-size: 1.5rem;
  font-weight: 300;
}

.layer-title {
  font-size: 1.25rem;
  font-weight: 800;
  margin-bottom: 16px;
}

.layer-components {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
}

.component {
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.overview-description p {
  color: #64748b;
  margin-bottom: 12px;
  line-height: 1.6;
}

/* 前端架构 */
.frontend-architecture {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
}

.frontend-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
}

@media (max-width: 768px) {
  .frontend-grid {
    grid-template-columns: 1fr;
  }
}

.frontend-module {
  padding: 24px;
  background: #f8fafc;
  border-radius: 16px;
  border-left: 4px solid #42b883;
}

.frontend-module h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 10px;
}

.frontend-module ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.frontend-module li {
  margin-bottom: 12px;
  color: #64748b;
  line-height: 1.6;
  padding-left: 0;
}

.frontend-module li strong {
  color: #1e293b;
}

/* 后端服务 */
.backend-architecture {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
}

.backend-services {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
}

@media (max-width: 768px) {
  .backend-services {
    grid-template-columns: 1fr;
  }
}

.service-card {
  background: #f8fafc;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
}

.service-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.service-icon {
  font-size: 2rem;
}

.service-card h3 {
  font-size: 1.25rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
}

.service-details p {
  color: #64748b;
  margin-bottom: 16px;
  line-height: 1.6;
}

.service-details p strong {
  color: #1e293b;
}

.code-snippet.small {
  background: #0f172a;
  border-radius: 12px;
  overflow: hidden;
  margin: 16px 0;
}

.code-snippet.small pre {
  margin: 0;
  padding: 16px;
  overflow-x: auto;
}

.code-snippet.small code {
  font-family: "JetBrains Mono", monospace;
  font-size: 12px;
  color: #e2e8f0;
  line-height: 1.5;
}

/* 数据流 */
.data-flow-diagram {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
}

.flow-step {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 20px;
  padding: 24px;
  background: #f8fafc;
  border-radius: 16px;
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
  margin-bottom: 16px;
  line-height: 1.6;
}

.step-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background: rgba(59, 130, 246, 0.1);
  color: #2563eb;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.flow-arrow {
  text-align: center;
  font-size: 1.5rem;
  color: #94a3b8;
  font-weight: 300;
  margin: 10px 0;
}

/* 部署网格 */
.deployment-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

@media (max-width: 768px) {
  .deployment-grid {
    grid-template-columns: 1fr;
  }
}

.deploy-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
}

.deploy-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 10px;
}

.deploy-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.deploy-card li {
  margin-bottom: 12px;
  color: #64748b;
  line-height: 1.6;
  padding-left: 0;
}

.deploy-card li strong {
  color: #1e293b;
}

/* 扩展性考虑 */
.scaling-considerations {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
}

.scaling-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
}

.scaling-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 10px;
}

.scaling-card p {
  color: #64748b;
  margin-bottom: 12px;
  line-height: 1.6;
}

.scaling-card p strong {
  color: #1e293b;
}

.scaling-card ul {
  list-style: none;
  padding: 0;
  margin: 16px 0 0 0;
}

.scaling-card li {
  color: #64748b;
  margin-bottom: 8px;
  padding-left: 20px;
  position: relative;
}

.scaling-card li:before {
  content: "•";
  color: #3b82f6;
  position: absolute;
  left: 0;
}

/* 技术栈总结 */
.tech-stack-summary {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
}

.stack-category {
  margin-bottom: 40px;
}
.stack-category:last-child {
  margin-bottom: 0;
}

.stack-category h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #1e293b;
}

.stack-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.stack-tag {
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: white;
}

.stack-tag.vue {
  background: #42b883;
}
.stack-tag.vite {
  background: #646cff;
}
.stack-tag.typescript {
  background: #3178c6;
}
.stack-tag.element {
  background: #409eff;
}
.stack-tag.threejs {
  background: #000000;
}
.stack-tag.pinia {
  background: #ffd859;
  color: #333;
}
.stack-tag.axios {
  background: #5a29e4;
}
.stack-tag.gsap {
  background: #88ce02;
  color: #333;
}

.stack-tag.fastapi {
  background: #009688;
}
.stack-tag.python {
  background: #3776ab;
}
.stack-tag.pytorch {
  background: #ee4c2c;
}
.stack-tag.yolov8 {
  background: #000000;
}
.stack-tag.opencv {
  background: #5c3ee8;
}
.stack-tag.kociemba {
  background: #1e88e5;
}
.stack-tag.sqlalchemy {
  background: #d71f49;
}
.stack-tag.docker {
  background: #2496ed;
}

.stack-tag.git {
  background: #f05032;
}
.stack-tag.github {
  background: #181717;
}
.stack-tag.eslint {
  background: #4b32c3;
}
.stack-tag.prettier {
  background: #f7b93e;
  color: #333;
}
.stack-tag.vercel {
  background: #000000;
}
.stack-tag.nginx {
  background: #269539;
}
.stack-tag.sentry {
  background: #362d59;
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
  .overview-diagram {
    gap: 12px;
  }
  .layer-components {
    flex-direction: column;
    align-items: center;
  }
  .backend-services {
    grid-template-columns: 1fr;
  }
  .data-flow-diagram {
    padding: 24px;
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
</style>
