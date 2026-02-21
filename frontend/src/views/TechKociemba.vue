<template>
  <div class="tech-doc-page kociemba-doc">
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
            <span>求解算法 · 两阶段搜索</span>
          </div>

          <h1 class="hero-title">
            Kociemba 两阶段算法<br />
            <span class="gradient-text">魔方最优解的理论与实践</span>
          </h1>

          <p class="hero-subtitle">
            深入解析 Herbert Kociemba 于 1992 年提出的两阶段算法，该算法能在平均
            20 步内求解任意魔方状态， 是 CubeMaster 求解引擎的核心。
          </p>

          <div class="stats-pills">
            <div class="stat-pill">
              <span class="dot-indicator blue"></span>
              <span>平均解长度：19.5 步</span>
            </div>
            <div class="stat-pill">
              <span class="dot-indicator green"></span>
              <span>求解时间：&lt; 0.1 秒</span>
            </div>
            <div class="stat-pill">
              <span class="dot-indicator purple"></span>
              <span>状态空间：4.3×10¹⁹ 种</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Algorithm Introduction -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">算法核心思想</h2>
        <div class="intro-card">
          <div class="intro-grid">
            <div class="intro-item">
              <div class="intro-icon">🎯</div>
              <h3>两阶段分解</h3>
              <p>
                将魔方还原问题分解为两个更简单的子问题：先还原到子群 H
                (U,D,R2,L2,F2,B2)，再完全还原。
              </p>
            </div>
            <div class="intro-item">
              <div class="intro-icon">🧩</div>
              <h3>对称性剪枝</h3>
              <p>
                利用魔方对称群 (48 种对称) 将搜索空间减少 48
                倍，大幅提升搜索效率。
              </p>
            </div>
            <div class="intro-item">
              <div class="intro-icon">📊</div>
              <h3>预计算表</h3>
              <p>
                使用 IDA* 搜索配合预计算的模式数据库，快速评估到目标状态的距离。
              </p>
            </div>
            <div class="intro-item">
              <div class="intro-icon">⚡</div>
              <h3>启发式搜索</h3>
              <p>
                结合曼哈顿距离和模式数据库的启发函数，引导搜索向最优解方向前进。
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Phase Details -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">两阶段详解</h2>
        <div class="phase-diagram">
          <div class="phase-step phase-1">
            <div class="phase-header">
              <div class="phase-badge">阶段 1</div>
              <h3>还原到子群 H</h3>
            </div>
            <div class="phase-content">
              <p>
                <strong>目标</strong>：将魔方还原到子群 H = ⟨U, D, R², L², F²,
                B²⟩
              </p>
              <ul>
                <li>所有棱块方向正确 (可仅用 U,D,R2,L2,F2,B2 还原)</li>
                <li>角块位置正确 (不考虑方向)</li>
                <li>搜索深度通常 ≤ 12 步</li>
              </ul>
              <div class="phase-note">
                <strong>技术细节</strong>：使用剪枝表 pruning table
                存储每个状态到子群 H 的最少步数。
              </div>
            </div>
          </div>

          <div class="phase-arrow">→</div>

          <div class="phase-step phase-2">
            <div class="phase-header">
              <div class="phase-badge">阶段 2</div>
              <h3>完全还原</h3>
            </div>
            <div class="phase-content">
              <p><strong>目标</strong>：从子群 H 状态完全还原魔方</p>
              <ul>
                <li>仅使用子群 H 的生成元移动 (U,D,R2,L2,F2,B2)</li>
                <li>角块方向调整完成</li>
                <li>搜索深度通常 ≤ 18 步</li>
              </ul>
              <div class="phase-note">
                <strong>技术细节</strong
                >：使用第二阶段剪枝表，结合对称性减少搜索分支。
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Implementation -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">CubeMaster 实现</h2>
        <div class="implementation-details">
          <div class="impl-card">
            <h3><span class="impl-icon">🐍</span> Python 集成</h3>
            <div class="code-snippet">
              <pre><code>from twophase.solver import solve

def solve_cube(cube_state):
    """
    输入: 54字符魔方状态字符串
    返回: 解法字符串 (如 "U R' F2 D2 L")
    """
    # 验证状态有效性
    if not is_valid_state(cube_state):
        raise ValueError("无效的魔方状态")
    
    # 调用 Kociemba 求解器
    solution = solve(cube_state, max_depth=24, timeout=5)
    
    # 优化解法 (移除冗余步骤)
    optimized = optimize_moves(solution)
    
    return {
        "raw_solution": solution,
        "optimized": optimized,
        "move_count": len(optimized.split()),
        "time_taken": get_solve_time()
    }</code></pre>
            </div>
            <div class="impl-desc">
              <p>
                <strong>twophase 库</strong>：基于 C 扩展的 Python
                实现，提供毫秒级求解能力。
              </p>
              <p>
                <strong>错误处理</strong>：自动检测无效状态，返回可读错误信息。
              </p>
            </div>
          </div>

          <div class="impl-card">
            <h3><span class="impl-icon">🔧</span> 性能优化</h3>
            <ul>
              <li>
                <strong>缓存机制</strong
                >：频繁出现的状态缓存求解结果，减少重复计算
              </li>
              <li>
                <strong>并行搜索</strong
                >：多线程同时探索不同分支，加速第一阶段求解
              </li>
              <li>
                <strong>内存管理</strong>：剪枝表使用内存映射文件，减少 RAM 占用
              </li>
              <li>
                <strong>提前终止</strong>：找到 ≤20
                步解后立即返回，不追求绝对最优
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Mathematical Foundation -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">数学基础</h2>
        <div class="math-grid">
          <div class="math-card">
            <h3>群论应用</h3>
            <p>魔方状态构成群 G，子群 H 是 G 的子集，满足：</p>
            <div class="math-formula">
              H = {g ∈ G | 棱块方向正确 ∧ 角块位置正确}
            </div>
            <p>第一阶段是寻找最短路径 g₁ 使 s·g₁ ∈ H</p>
          </div>
          <div class="math-card">
            <h3>状态表示</h3>
            <p>使用坐标表示法压缩状态空间：</p>
            <ul>
              <li><strong>角块位置</strong>：8! × 3⁷ = 88,179,840 种</li>
              <li><strong>棱块位置</strong>：12! × 2¹¹ = 42,577,920 种</li>
              <li><strong>组合总数</strong>：~4.3×10¹⁹ 种可能状态</li>
            </ul>
          </div>
          <div class="math-card">
            <h3>对称性群</h3>
            <p>魔方有 48 种空间对称 (旋转+反射)：</p>
            <div class="math-formula">
              S = {r_x^a ∘ r_y^b ∘ r_z^c | a,b,c ∈ {0,1,2,3}}
            </div>
            <p>利用对称性将状态空间减少 48 倍，加速搜索。</p>
          </div>
        </div>
      </section>

      <!-- Comparison with Other Algorithms -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">算法对比</h2>
        <div class="comparison-table-wrapper">
          <table class="algorithm-comparison">
            <thead>
              <tr>
                <th>算法</th>
                <th>平均步数</th>
                <th>求解时间</th>
                <th>内存需求</th>
                <th>实现难度</th>
                <th>适用场景</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Kociemba 两阶段</strong></td>
                <td>19-21</td>
                <td>&lt; 0.1s</td>
                <td>10-100MB</td>
                <td><span class="tag medium">中等</span></td>
                <td>实时求解，通用应用</td>
              </tr>
              <tr>
                <td>Thistlethwaite 四阶段</td>
                <td>45-52</td>
                <td>0.5-2s</td>
                <td>1-10MB</td>
                <td><span class="tag simple">简单</span></td>
                <td>教学演示，历史研究</td>
              </tr>
              <tr>
                <td>IDA* + 模式数据库</td>
                <td>18-20 (最优)</td>
                <td>1-30s</td>
                <td>1GB+</td>
                <td><span class="tag hard">困难</span></td>
                <td>理论研究，最优解搜索</td>
              </tr>
              <tr>
                <td>神经网络求解</td>
                <td>25-35</td>
                <td>0.01s (推理)</td>
                <td>50-200MB</td>
                <td><span class="tag hard">困难</span></td>
                <td>AI 研究，端到端学习</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Limitations -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">局限性 & 改进</h2>
        <div class="limitations-grid">
          <div class="limit-card">
            <h3><span class="limit-icon">⏱️</span> 非最优性</h3>
            <p>
              <strong>问题</strong>：两阶段算法不保证找到全局最优解 (God's
              Number = 20)
            </p>
            <p>
              <strong>改进方向</strong>：结合 IDA*
              深度搜索，在允许时间内寻找更优解
            </p>
          </div>
          <div class="limit-card">
            <h3><span class="limit-icon">💾</span> 内存占用</h3>
            <p><strong>问题</strong>：剪枝表需要大量内存 (原始实现约 100MB)</p>
            <p><strong>改进方向</strong>：使用压缩表、按需加载、共享内存技术</p>
          </div>
          <div class="limit-card">
            <h3><span class="limit-icon">🔢</span> 大魔方扩展</h3>
            <p><strong>问题</strong>：算法专为 3×3 设计，难以扩展到 4×4+</p>
            <p>
              <strong>改进方向</strong>：分层降阶法，结合 Kociemba 处理 3×3 阶段
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

/* 算法核心思想卡片 */
.intro-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
  margin-top: 20px;
}

.intro-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
}

@media (max-width: 768px) {
  .intro-grid {
    grid-template-columns: 1fr;
  }
}

.intro-item {
  background: #f8fafc;
  border-radius: 20px;
  padding: 24px;
  transition: all 0.3s;
}

.intro-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.intro-icon {
  font-size: 2.5rem;
  margin-bottom: 16px;
}

.intro-item h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #1e293b;
}

.intro-item p {
  color: #64748b;
  line-height: 1.6;
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

/* === 特定于 Kociemba 页面的样式 === */

/* 阶段图示 */
.phase-diagram {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 40px;
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
}

.phase-step {
  flex: 1;
  background: #f8fafc;
  border-radius: 20px;
  padding: 30px;
}

.phase-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.phase-badge {
  background: #3b82f6;
  color: white;
  padding: 6px 16px;
  border-radius: 100px;
  font-size: 14px;
  font-weight: 700;
}

.phase-step h3 {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
}

.phase-content p {
  color: #64748b;
  margin-bottom: 16px;
}

.phase-content ul {
  list-style: none;
  padding: 0;
  margin: 16px 0;
}

.phase-content li {
  color: #64748b;
  margin-bottom: 8px;
  padding-left: 20px;
  position: relative;
}

.phase-content li:before {
  content: "•";
  color: #3b82f6;
  position: absolute;
  left: 0;
}

.phase-note {
  background: rgba(59, 130, 246, 0.1);
  border-left: 4px solid #3b82f6;
  padding: 16px;
  margin-top: 20px;
  border-radius: 0 8px 8px 0;
}

.phase-arrow {
  font-size: 2.5rem;
  color: #94a3b8;
  font-weight: 300;
}

/* 实现详情 */
.implementation-details {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 40px;
}

.impl-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
}

.impl-card h3 {
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
  margin-bottom: 20px;
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

.impl-desc p {
  color: #64748b;
  margin-bottom: 12px;
}

.impl-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.impl-card li {
  margin-bottom: 12px;
  color: #64748b;
  line-height: 1.6;
  padding-left: 0;
}

.impl-card li strong {
  color: #1e293b;
}

/* 数学网格 */
.math-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

@media (max-width: 768px) {
  .math-grid {
    grid-template-columns: 1fr;
  }
}

.math-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
}

.math-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #1e293b;
}

.math-card p {
  color: #64748b;
  margin-bottom: 16px;
}

.math-formula {
  font-family: "JetBrains Mono", monospace;
  background: #f8fafc;
  padding: 16px;
  border-radius: 12px;
  margin: 16px 0;
  color: #1e293b;
  text-align: left;
  font-size: 14px;
}

.math-card ul {
  list-style: none;
  padding: 0;
  margin: 16px 0;
}

.math-card li {
  color: #64748b;
  margin-bottom: 8px;
  padding-left: 0;
}

/* 算法对比表 */
.comparison-table-wrapper {
  overflow-x: auto;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
}

.algorithm-comparison {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  min-width: 800px;
}

.algorithm-comparison th {
  background: #f8fafc;
  padding: 20px;
  text-align: left;
  font-weight: 700;
  color: #475569;
  border-bottom: 1px solid #e2e8f0;
}

.algorithm-comparison td {
  padding: 20px;
  border-bottom: 1px solid #f1f5f9;
  color: #334155;
}

.tag {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}
.tag.simple {
  background: #ecfdf5;
  color: #047857;
}
.tag.medium {
  background: #eff6ff;
  color: #1d4ed8;
}
.tag.hard {
  background: #fef2f2;
  color: #b91c1c;
}

/* 局限性网格 */
.limitations-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

@media (max-width: 768px) {
  .limitations-grid {
    grid-template-columns: 1fr;
  }
}

.limit-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 30px;
  border: 1px solid #e2e8f0;
}

.limit-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 10px;
}

.limit-card p {
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 12px;
}

/* 导航卡片 (复用 YOLO 样式) */
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
  .phase-diagram {
    flex-direction: column;
    gap: 30px;
  }
  .phase-arrow {
    transform: rotate(90deg);
  }
  .implementation-details {
    grid-template-columns: 1fr;
  }
  .math-grid,
  .limitations-grid {
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

[data-theme="dark"] .intro-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .intro-item {
  background: var(--dm-bg-hover);
}

[data-theme="dark"] .intro-item h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .intro-item p {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .phase-diagram {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .phase-step {
  background: var(--dm-bg-hover);
}

[data-theme="dark"] .phase-step h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .phase-content p {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .phase-content li {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .phase-note {
  background: rgba(59, 130, 246, 0.1);
  border-left-color: var(--dm-accent);
}

[data-theme="dark"] .phase-arrow {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .impl-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .impl-card h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .code-snippet {
  background: #0f172a;
}

[data-theme="dark"] .code-snippet code {
  color: #e2e8f0;
}

[data-theme="dark"] .impl-desc p {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .impl-card li {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .impl-card li strong {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .math-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .math-card h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .math-card p {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .math-formula {
  background: var(--dm-bg-hover);
  color: var(--dm-text-primary);
}

[data-theme="dark"] .math-card li {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .comparison-table-wrapper {
  border-color: var(--dm-border);
}

[data-theme="dark"] .algorithm-comparison {
  background: var(--dm-bg-card);
}

[data-theme="dark"] .algorithm-comparison th {
  background: var(--dm-bg-hover);
  color: var(--dm-text-secondary);
  border-bottom-color: var(--dm-border);
}

[data-theme="dark"] .algorithm-comparison td {
  border-bottom-color: var(--dm-border);
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .tag.simple {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

[data-theme="dark"] .tag.medium {
  background: rgba(59, 130, 246, 0.15);
  color: var(--dm-accent);
}

[data-theme="dark"] .tag.hard {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

[data-theme="dark"] .limit-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .limit-card h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .limit-card p {
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
