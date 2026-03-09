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
            深入解析 CubeMaster 的服务架构、数据流设计和基础设施选择，
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
              <span>代码行数：30,000+ 行</span>
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
                <div class="component">模型文件 (.pt)</div>
                <div class="component">临时图像存储</div>
                <div class="component">配置/状态文件</div>
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
              <h3><PaintBrushIcon class="w-5 h-5 inline-block align-middle mr-2" /> UI 框架</h3>
              <ul>
                <li>
                  <strong>Vue 3 Composition API</strong
                  >：响应式数据绑定和组件逻辑
                </li>
                <li><strong>Element Plus</strong>：企业级 UI 组件库</li>
                <li><strong>Vue Router</strong>：SPA 路由管理，支持嵌套路由</li>
                <li><strong>Prism.js</strong>：代码语法高亮，支持多语言</li>
              </ul>
            </div>

            <div class="frontend-module">
              <h3><CubeIcon class="w-5 h-5 inline-block align-middle mr-2" /> 3D 引擎</h3>
              <ul>
                <li><strong>Three.js</strong>：WebGL 渲染库，核心 3D 功能</li>
                <li><strong>自定义控件</strong>：魔方专用交互系统</li>
                <li><strong>性能监控</strong>：帧率统计和内存管理</li>
              </ul>
            </div>

            <div class="frontend-module">
              <h3><CloudIcon class="w-5 h-5 inline-block align-middle mr-2" /> 网络层</h3>
              <ul>
                <li><strong>Axios</strong>：HTTP 客户端，拦截器和错误处理</li>
                <li><strong>请求队列</strong>：顺序处理，避免竞态条件</li>
                <li><strong>缓存策略</strong>：本地存储频繁访问数据</li>
              </ul>
            </div>

            <div class="frontend-module">
              <h3><CommandLineIcon class="w-5 h-5 inline-block align-middle mr-2" /> 构建工具</h3>
              <ul>
                <li><strong>Vite</strong>：极速构建工具，开发服务器</li>
                <li><strong>Sass</strong>：CSS 预处理器，增强样式可维护性</li>
                <li><strong>Vitest</strong>：现代化单元测试框架，Vite 原生集成</li>
                <li><strong>Prettier</strong>：代码格式化工具</li>
                <li><strong>构建与部署</strong>：Vite 静态构建，手动部署</li>
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
                <div class="service-icon">
                <MagnifyingGlassIcon class="w-8 h-8" />
              </div>
                <h3>视觉识别服务</h3>
              </div>
              <div class="service-details">
                <p>
                  <strong>职责</strong>：处理图像上传，运行 YOLOv8
                  推理，返回颜色检测结果
                </p>
                <CodeBlock
                  language="bash"
                  title="视觉识别 API"
                  :foldable="false"
                  :code="detectApiCode"
                />
                <p>
                  <strong>技术栈</strong>：FastAPI, PyTorch, OpenCV, Ultralytics
                  YOLOv8
                </p>
              </div>
            </div>

            <div class="service-card">
              <div class="service-header">
                <div class="service-icon">
                <PuzzlePieceIcon class="w-8 h-8" />
              </div>
                <h3>求解引擎服务</h3>
              </div>
              <div class="service-details">
                <p>
                  <strong>职责</strong>：接收魔方状态，调用 Kociemba
                  算法，返回解法步骤
                </p>
                <CodeBlock
                  language="bash"
                  title="求解引擎 API"
                  :foldable="false"
                  :code="solveApiCode"
                />
                <p>
                  <strong>技术栈</strong>：FastAPI, Python, twophase (Kociemba),
                  缓存机制
                </p>
              </div>
            </div>

            <div class="service-card">
              <div class="service-header">
                <div class="service-icon">
                <CloudIcon class="w-8 h-8" />
              </div>
                <h3>云端存储与并发考虑</h3>
              </div>
              <div class="service-details">
                <p>
                  <strong>挑战</strong>：云端部署时图像存储压力与多用户并发冲突
                </p>
                <CodeBlock
                  language="bash"
                  title="解决方案架构"
                  :foldable="false"
                  :code="solutionArchCode"
                />
                <p><strong>解决方案</strong>：</p>
                <ul>
                  <li>
                    <strong>临时存储</strong
                    >：使用服务器临时目录存储图像，处理完成后自动清理
                  </li>
                  <li>
                    <strong>并发隔离</strong
                    >：每个请求生成唯一session_id，确保文件操作隔离
                  </li>
                  <li>
                    <strong>资源优化</strong>：图像压缩、内存缓存减少服务器负载
                  </li>
                  <li><strong>请求管理</strong>：同步处理，避免并发冲突</li>
                </ul>
                <p>
                  <strong>技术栈</strong>：Python 并发库 (asyncio,
                  threading)，本地文件系统
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
          <div class="data-flow-image-container">
            <img
              src="/images/solver-data-flow.png"
              alt="求解器数据流图"
              class="data-flow-image"
              @click="openImagePreview('/images/solver-data-flow.png')"
              style="cursor: pointer"
            />
            <div class="image-caption">CubeMaster 求解器完整数据流示意图</div>
          </div>
          <div class="data-flow-description">
            <p>数据流清晰展示了从用户输入到3D可视化还原的完整过程：</p>
            <ul>
              <li>
                <strong>用户输入层</strong
                >：支持摄像头实时拍摄、手动输入、文件上传三种方式
              </li>
              <li>
                <strong>前端处理层</strong
                >：图像预处理、Base64编码、状态验证与API调用
              </li>
              <li>
                <strong>后端推理层</strong
                >：YOLOv8颜色识别、状态合法性验证、标准字符串生成
              </li>
              <li>
                <strong>求解计算层</strong
                >：Kociemba二阶段算法求解、解法优化与步骤分解
              </li>
              <li>
                <strong>3D可视化层</strong
                >：Three.js动画演示、步骤高亮、交互式控制
              </li>
            </ul>
            <p>
              各层之间通过定义良好的REST
              API接口通信，确保系统的可维护性和可扩展性。
            </p>
          </div>
        </div>
      </section>

      <!-- Deployment & DevOps -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">部署与运维</h2>
        <div class="deployment-grid">
          <div class="deploy-card">
            <h3><RocketLaunchIcon class="w-5 h-5 inline-block align-middle mr-2" /> 前端部署</h3>
            <ul>
              <li><strong>开发服务器</strong>：Vite 热重载开发环境</li>
              <li><strong>静态构建</strong>：Vite 生产构建，生成静态资源</li>
              <li><strong>版本管理</strong>：语义化版本，Git 分支策略</li>
              <li><strong>访问优化</strong>：浏览器缓存策略，资源压缩</li>
            </ul>
          </div>

          <div class="deploy-card">
            <h3><WrenchScrewdriverIcon class="w-5 h-5 inline-block align-middle mr-2" /> 后端部署</h3>
            <ul>
              <li>
                <strong>开发服务器</strong>：FastAPI + Uvicorn 本地开发服务
              </li>
              <li><strong>API 服务</strong>：RESTful API 接口，支持跨域请求</li>
              <li><strong>环境配置</strong>：Python 虚拟环境，依赖管理</li>
              <li><strong>生产部署考虑</strong>：可容器化或云服务部署</li>
            </ul>
          </div>

          <div class="deploy-card">
            <h3><Lock class="w-5 h-5 inline-block align-middle mr-2" /> 安全策略</h3>
            <ul>
              <li><strong>CORS 配置</strong>：严格限制允许的源和请求方法</li>
              <li><strong>速率限制</strong>：API 调用频率限制，防止滥用</li>
              <li><strong>输入验证</strong>：所有用户输入严格验证和清理</li>
              <li><strong>数据加密</strong>：HTTPS 传输，敏感数据加密存储</li>
              <li><strong>临时文件清理</strong>：定期清理服务器临时识别图像</li>
              <li>
                <strong>模型文件安全</strong>：保护训练模型，防止未授权访问
              </li>
            </ul>
          </div>

          <div class="deploy-card">
            <h3><ChartBarIcon class="w-5 h-5 inline-block align-middle mr-2" /> 日志与调试</h3>
            <ul>
              <li><strong>日志记录</strong>：Python 标准日志，控制台输出</li>
              <li><strong>错误追踪</strong>：前端控制台日志，网络请求监控</li>
              <li>
                <strong>性能监控</strong>：浏览器开发者工具，API 响应时间记录
              </li>
              <li><strong>调试工具</strong>：Vue DevTools，Python 调试器</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Scaling Considerations -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">扩展性设计</h2>
        <div class="scaling-considerations">
          <div class="scaling-card">
            <h3><DevicePhoneMobileIcon class="w-5 h-5 inline-block align-middle mr-2" /> 用户规模扩展</h3>
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
            <h3><CpuChipIcon class="w-5 h-5 inline-block align-middle mr-2" /> 算法功能扩展</h3>
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
            <h3><GlobeAltIcon class="w-5 h-5 inline-block align-middle mr-2" /> 国际化扩展</h3>
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
              <span class="stack-tag">Vue 3</span>
              <span class="stack-tag">Vite</span>
              <span class="stack-tag">Element Plus</span>
              <span class="stack-tag">Vue Router</span>
              <span class="stack-tag">Three.js</span>
              <span class="stack-tag">Axios</span>
              <span class="stack-tag">Prism.js</span>
            </div>
          </div>

          <div class="stack-category">
            <h3>后端技术栈</h3>
            <div class="stack-tags">
              <span class="stack-tag">FastAPI</span>
              <span class="stack-tag">Uvicorn</span>
              <span class="stack-tag">Python 3.10</span>
              <span class="stack-tag">PyTorch</span>
              <span class="stack-tag">YOLOv8</span>
              <span class="stack-tag">OpenCV</span>
              <span class="stack-tag">NumPy</span>
              <span class="stack-tag">Kociemba</span>
            </div>
          </div>

          <div class="stack-category">
            <h3>开发运维</h3>
            <div class="stack-tags">
              <span class="stack-tag">Git</span>
              <span class="stack-tag">Prettier</span>
              <span class="stack-tag">Docker</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Navigation -->
      <section class="section-block navigation-section" v-animate>
        <h2 class="section-heading text-center">深入技术细节</h2>
        <div class="nav-cards">
          <router-link to="/tech/yolo" class="nav-card">
            <EyeIcon class="nav-icon w-10 h-10" />
            <h3>YOLOv8 视觉识别</h3>
            <p>魔方颜色检测技术详解</p>
          </router-link>
          <router-link to="/tech/kociemba" class="nav-card">
            <PuzzlePieceIcon class="nav-icon w-10 h-10" />
            <h3>Kociemba 算法</h3>
            <p>魔方两阶段求解算法原理</p>
          </router-link>
          <router-link to="/tech/threejs" class="nav-card">
            <CubeIcon class="nav-icon w-10 h-10" />
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

    <!-- 图片预览模态框 -->
    <div v-if="showImageModal" class="image-modal" @click="closeImagePreview">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closeImagePreview">×</button>
        <img :src="currentImageSrc" alt="预览图片" class="modal-image" />
        <div class="image-caption-modal">CubeMaster 求解器完整数据流示意图</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useRouter } from "vue-router";
import { ArrowLeft, ArrowUp } from "@element-plus/icons-vue";
import { 
  PaintBrushIcon,
  CubeIcon,
  CloudIcon,
  CommandLineIcon,
  MagnifyingGlassIcon,
  PuzzlePieceIcon,
  RocketLaunchIcon,
  WrenchScrewdriverIcon,
  ChartBarIcon,
  CpuChipIcon,
  DevicePhoneMobileIcon,
  GlobeAltIcon,
  EyeIcon,
  ServerIcon
} from "@heroicons/vue/24/solid";
import { Lock } from "@element-plus/icons-vue";
import CodeBlock from "../components/CodeBlock.vue";

const router = useRouter();
const showBackToTop = ref(false);
const showImageModal = ref(false);
const currentImageSrc = ref("");

const detectApiCode = `POST /api/detect
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
}`;

const solveApiCode = `POST /api/solve
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
}`;

const solutionArchCode = `# 解决方案架构
1. 图片上传流程：
    前端 → 后端临时内存/磁盘存储 → 识别 → 自动清理

2. 并发处理机制：
    每个请求生成唯一 session_id
    线程安全处理，避免状态污染`;

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

// 图片预览功能
const openImagePreview = (src) => {
  currentImageSrc.value = src;
  showImageModal.value = true;
  // 禁止背景滚动
  document.body.style.overflow = "hidden";
};

const closeImagePreview = () => {
  showImageModal.value = false;
  // 恢复背景滚动
  document.body.style.overflow = "";
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
  text-align: left;
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
  padding: 80px;
  border: 1px solid #e2e8f0;
}

.backend-services {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: auto auto;
  gap: 30px;
  align-items: stretch;
}

.service-card:nth-child(3) {
  grid-column: span 2;
  margin-top: 30px;
  align-self: start;
}

@media (max-width: 992px) {
  .backend-services {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .backend-services {
    grid-template-columns: 1fr;
  }

  .service-card:nth-child(3) {
    grid-column: auto;
    margin-top: 0;
    align-self: auto;
  }
}

.service-card {
  background: #f8fafc;
  border-radius: 20px;
  padding: 20px;
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
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

.service-details {
  text-align: left;
}

.service-details p {
  color: #64748b;
  margin-bottom: 16px;
  line-height: 1.6;
}

.service-details p strong {
  color: #1e293b;
}

.service-details ul {
  list-style: none;
  padding-left: 0;
  margin: 16px 0;
}

.service-details li {
  margin-bottom: 10px;
  color: #64748b;
  line-height: 1.5;
  padding-left: 0;
}

.service-details li strong {
  color: #1e293b;
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
  text-align: left;
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
  text-align: left;
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
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #1e293b;
}

/* 分组边框颜色 */
.stack-category:nth-child(1) .stack-tag {
  border-color: #42b883;
}
.stack-category:nth-child(2) .stack-tag {
  border-color: #3b82f6;
}
.stack-category:nth-child(3) .stack-tag {
  border-color: #8b5cf6;
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

/* 数据流图片样式 */
.data-flow-image-container {
  text-align: center;
  margin-bottom: 30px;
}

.data-flow-image {
  max-width: 100%;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  cursor: pointer;
}

.data-flow-image:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
}

.image-caption {
  margin-top: 12px;
  font-size: 14px;
  color: #64748b;
  font-style: italic;
}

.data-flow-description {
  background: #f8fafc;
  padding: 24px;
  border-radius: 16px;
  border-left: 4px solid #3b82f6;
  text-align: left;
}

.data-flow-description p {
  color: #475569;
  line-height: 1.6;
  margin-bottom: 16px;
}

.data-flow-description ul {
  list-style: none;
  padding-left: 20px;
  margin-bottom: 20px;
}

.data-flow-description li {
  margin-bottom: 8px;
  color: #475569;
  position: relative;
  padding-left: 24px;
}

.data-flow-description li:before {
  content: "→";
  color: #3b82f6;
  position: absolute;
  left: 0;
  font-weight: bold;
}

.data-flow-description li strong {
  color: #1e293b;
}

/* 图片预览模态框 */
.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(5px);
}

.modal-content {
  position: relative;
  max-width: 90%;
  max-height: 90%;
  background: #0f172a;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  animation: modalFadeIn 0.3s ease;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal-close {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 50%;
  color: white;
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.2);
}

.modal-image {
  max-width: 100%;
  max-height: calc(90vh - 100px);
  border-radius: 8px;
  display: block;
  margin: 0 auto;
}

.image-caption-modal {
  text-align: center;
  color: #cbd5e1;
  margin-top: 15px;
  font-size: 14px;
  font-style: italic;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .back-to-top-btn {
    bottom: 20px;
    right: 20px;
    width: 45px;
    height: 45px;
  }

  .modal-content {
    padding: 15px;
    max-width: 95%;
    max-height: 85%;
  }

  .modal-close {
    width: 36px;
    height: 36px;
    font-size: 20px;
  }

  .modal-image {
    max-height: calc(85vh - 80px);
  }

  .image-caption-modal {
    font-size: 13px;
    margin-top: 10px;
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

[data-theme="dark"] .system-overview {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .overview-description p {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .frontend-architecture,
[data-theme="dark"] .backend-architecture {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .frontend-module {
  background: var(--dm-bg-hover);
  text-align: left;
}

[data-theme="dark"] .frontend-module h3,
[data-theme="dark"] .service-card h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .frontend-module li,
[data-theme="dark"] .service-details p,
[data-theme="dark"] .service-details li {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .service-card {
  background: var(--dm-bg-hover);
  border-color: var(--dm-border);
}

[data-theme="dark"] .data-flow-diagram {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .data-flow-description {
  background: var(--dm-bg-hover);
  border-left-color: var(--dm-accent);
  text-align: left;
}

[data-theme="dark"] .data-flow-description p,
[data-theme="dark"] .data-flow-description li {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .data-flow-image {
  border-color: var(--dm-border);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .image-caption {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .deploy-card,
[data-theme="dark"] .scaling-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
  text-align: left;
}

[data-theme="dark"] .deploy-card h3,
[data-theme="dark"] .scaling-card h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .deploy-card li,
[data-theme="dark"] .scaling-card p,
[data-theme="dark"] .scaling-card li {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .tech-stack-summary {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .stack-category h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .stack-tag {
  background: var(--dm-bg-hover);
  border-color: var(--dm-border);
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

[data-theme="dark"] .image-modal {
  background: rgba(0, 0, 0, 0.9);
}

[data-theme="dark"] .modal-content {
  background: var(--dm-bg-card);
}

[data-theme="dark"] .modal-close {
  background: var(--dm-bg-hover);
  color: var(--dm-text-primary);
}

[data-theme="dark"] .modal-close:hover {
  background: var(--dm-border);
}

[data-theme="dark"] .image-caption-modal {
  color: var(--dm-text-muted);
}

/* 修复 strong 标签在暗色模式下的颜色 */
[data-theme="dark"] .frontend-module li strong,
[data-theme="dark"] .service-details p strong,
[data-theme="dark"] .service-details li strong,
[data-theme="dark"] .overview-description p strong,
[data-theme="dark"] .deploy-card li strong,
[data-theme="dark"] .scaling-card p strong,
[data-theme="dark"] .data-flow-description li strong {
  color: var(--dm-text-primary);
}

/* 修复代码块居中问题 */
[data-theme="dark"] .service-details,
[data-theme="dark"] .service-details .code-snippet {
  text-align: left;
}
</style>
