<template>
  <div class="cfop-intro-page">
    <div class="page-container">
      <!-- ================= 1. Hero Section (顶部大卡片) ================= -->
      <section class="hero-section">
        <!-- 背景光晕装饰 -->
        <div class="glow-bg glow-top-right"></div>
        <div class="glow-bg glow-bottom-left"></div>

        <div class="hero-content">
          <div class="badge-pill">
            <span class="pulse-dot"></span>
            <span>使用 CFOP 将你的还原时间减半</span>
          </div>

          <h1 class="hero-title">
            CFOP 方法教程：<br />
            <span class="gradient-text">十字、F2L、OLL 和 PLL</span>
          </h1>

          <p class="hero-subtitle">
            深入了解高级 CFOP 方法——在约 15
            分钟的阅读时间内，学习世界纪录保持者如何在 5 秒内还原魔方！
          </p>

          <!-- 统计数据胶囊 -->
          <div class="stats-pills">
            <div class="stat-pill">
              <span class="dot-indicator blue"></span>
              <span>50,000+ 学习者</span>
            </div>
            <div class="stat-pill">
              <span class="dot-indicator green"></span>
              <span>平均提升：2分钟 → 30秒</span>
            </div>
            <div class="stat-pill">
              <span class="dot-indicator purple"></span>
              <span>仅需16个算法即可入门</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= 2. 学习目标 (What you'll learn) ================= -->
      <section class="section-block">
        <h2 class="section-heading">你将学到</h2>
        <div class="learning-list-card">
          <ul class="check-list">
            <li v-for="(item, i) in learningPoints" :key="i">
              <el-icon class="check-icon"><Check /></el-icon>
              <span>{{ item }}</span>
            </li>
          </ul>

          <!-- 模拟器推广卡片 (静态展示) -->
          <div class="simulator-promo">
            <div class="promo-icon">
              <el-icon><Monitor /></el-icon>
            </div>
            <div class="promo-text">
              <strong>想试试手？</strong>
              <p>在阅读完理论后，进入自由练习模式尝试这些步骤。</p>
            </div>
            <el-button type="primary" plain round @click="goPractice"
              >前往练习</el-button
            >
          </div>
        </div>
      </section>

      <!-- ================= 3. 决策树 (Which path?) ================= -->
      <section class="section-block">
        <h2 class="section-heading">我应该选择哪条路径？</h2>
        <p class="section-sub">不确定从哪里开始？根据你的经验水平选择：</p>

        <div class="decision-grid">
          <!-- 左卡：跳转到 2-Look 课程 -->
          <div
            class="decision-card emerald"
            @click="goToCourse2Look('advanced')"
          >
            <div class="icon-box">🌱</div>
            <h3>我是 CFOP 新手</h3>
            <p>从 16 个基础算法开始 (2-Look)</p>
          </div>

          <!-- 中卡：电梯模式，滚动到下方 Roadmap -->
          <div class="decision-card blue" @click="scrollToId('full-roadmap')">
            <div class="icon-box">📈</div>
            <h3>挑战完整 CFOP</h3>
            <p>分模块攻克 F2L + OLL + PLL</p>
          </div>

          <!-- 右卡：同样滚动到下方，或未来做全局搜索 -->
          <div class="decision-card purple" @click="scrollToId('full-roadmap')">
            <div class="icon-box">⚡</div>
            <h3>我需要快速参考</h3>
            <p>查阅算法表与指法技巧</p>
          </div>
        </div>
      </section>

      <!-- ================= 4. CFOP 数据概览 (Stats) ================= -->
      <section class="section-block">
        <h2 class="section-heading">CFOP 数据概览</h2>
        <div class="stats-grid">
          <div class="stat-box blue-theme">
            <div class="stat-icon">🎯</div>
            <div class="stat-num">4</div>
            <div class="stat-label">主要步骤</div>
          </div>
          <div class="stat-box purple-theme">
            <div class="stat-icon">🔄</div>
            <div class="stat-num">57</div>
            <div class="stat-label">OLL 情况</div>
          </div>
          <div class="stat-box orange-theme">
            <div class="stat-icon">🧩</div>
            <div class="stat-num">21</div>
            <div class="stat-label">PLL 情况</div>
          </div>
          <div class="stat-box emerald-theme">
            <div class="stat-icon">🤝</div>
            <div class="stat-num">41</div>
            <div class="stat-label">F2L 情况</div>
          </div>
        </div>
      </section>

      <!-- ================= 5. 进步时间线 (Timeline) ================= -->
      <section class="section-block">
        <h2 class="section-heading">CFOP 进步时间线</h2>
        <p class="section-sub">掌握每个阶段后你可以期待的速度：</p>

        <div class="timeline-container">
          <div
            class="timeline-item"
            v-for="(time, idx) in timelineData"
            :key="idx"
          >
            <div class="time-badge" :class="time.colorClass">
              {{ time.time }}
            </div>
            <div class="time-content">
              <h3>{{ time.title }}</h3>
              <p>{{ time.desc }}</p>
            </div>
            <div class="progress-bar-wrap">
              <div
                class="progress-bar"
                :class="time.colorClass"
                :style="{ width: time.percent }"
              ></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= 6. 4步路线图 ================= -->
      <section id="full-roadmap" class="section-block">
        <h2 class="section-heading">4 步 CFOP 详解与入口</h2>
        <p class="section-sub">点击卡片进入对应的算法库：</p>

        <div class="steps-container">
          <div
            class="step-card"
            v-for="(step, idx) in cfopSteps"
            :key="idx"
            :class="{ 'is-clickable': step.route }"
            @click="handleStepClick(step)"
          >
            <div class="step-header">
              <div class="step-number">{{ idx + 1 }}</div>
              <div class="step-title">{{ step.title }}</div>
              <div class="step-icon">{{ step.icon }}</div>
            </div>
            <div class="step-body">
              <p>{{ step.desc }}</p>
              <div class="step-meta">
                <span class="meta-tag">目标: {{ step.goal }}</span>
                <span class="meta-tag highlight"
                  >算法数: {{ step.algCount }}</span
                >
              </div>

              <!-- 仅当有路由时显示“进入”箭头 -->
              <div v-if="step.route" class="enter-hint">
                <span>进入库</span>
                <el-icon><ArrowRight /></el-icon>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= 7. 方法对比表 (Comparison) ================= -->
      <section class="section-block">
        <h2 class="section-heading">为什么选择 CFOP？</h2>
        <div class="table-wrapper">
          <table class="comparison-table">
            <thead>
              <tr>
                <th>方法</th>
                <th>平均步数</th>
                <th>算法数</th>
                <th>难度</th>
                <th>速度潜力</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>初学者方法</td>
                <td>110-120</td>
                <td>7-10</td>
                <td><span class="tag simple">简单</span></td>
                <td>60+ 秒</td>
              </tr>
              <tr class="highlight-row">
                <td>
                  <strong>CFOP</strong> <span class="rec-badge">推荐</span>
                </td>
                <td><strong>55-60</strong></td>
                <td><strong>78</strong> (两步16)</td>
                <td><span class="tag medium">中等</span></td>
                <td><strong>10-20 秒</strong></td>
              </tr>
              <tr>
                <td>Roux</td>
                <td>45-50</td>
                <td>10-15</td>
                <td><span class="tag hard">困难</span></td>
                <td>10-15 秒</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- ================= 8. FAQ (常见问题) ================= -->
      <section class="section-block">
        <h2 class="section-heading text-center">常见问题</h2>
        <div class="faq-container">
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
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { Check, Monitor, ArrowRight } from "@element-plus/icons-vue";

const router = useRouter();
const activeNames = ref("1");

// --- 数据区 ---
const learningPoints = [
  "高效的十字规划 (Cross) 和盲拧执行",
  "直观理解 F2L 配对逻辑，减少旋转",
  "一步定向顶层 (OLL) 的识别与执行",
  "排列顶层块 (PLL) 完成还原",
  "专家级指法技巧 (Finger Tricks)",
];

const timelineData = [
  {
    time: "60秒",
    title: "初学者方法",
    desc: "你的起点（层先法）",
    percent: "100%",
    colorClass: "green",
  },
  {
    time: "30秒",
    title: "两步 CFOP",
    desc: "十字: 5s | F2L: 20s | 2-Look OLL/PLL: 5s",
    percent: "75%",
    colorClass: "blue",
  },
  {
    time: "20秒",
    title: "完整 CFOP",
    desc: "熟练掌握 78 个算法",
    percent: "50%",
    colorClass: "purple",
  },
  {
    time: "10秒",
    title: "世界级水平",
    desc: "完美执行 + 预判 (Lookahead)",
    percent: "25%",
    colorClass: "orange",
  },
];

const cfopSteps = [
  {
    id: "cross",
    title: "十字 (Cross)",
    icon: "🔲",
    desc: "通过将棱块与中心块对齐，在底层完成一个十字。重点在于规划，尽量在 8 步内完成。",
    goal: "底层十字",
    algCount: "无",
    route: null,
  },
  {
    id: "f2l",
    title: "F2L (前两层)",
    icon: "🤝",
    desc: "同时还原底层角块和中间层棱块。这是 CFOP 中最慢但也最能提速的阶段。",
    goal: "前两层完成",
    algCount: "41",
    route: "/cfop/lib/f2l",
  },
  {
    id: "oll",
    title: "OLL (顶层定向)",
    icon: "🎯",
    desc: "将顶层所有颜色统一朝上。分为 2-Look (10个公式) 和 Full (57个公式)。",
    goal: "顶面复原",
    algCount: "57",
    route: "/cfop/lib/oll",
  },
  {
    id: "pll",
    title: "PLL (顶层排列)",
    icon: "🏁",
    desc: "交换顶层块的位置以复原魔方。分为 2-Look (6个公式) 和 Full (21个公式)。",
    goal: "魔方还原",
    algCount: "21",
    route: "/cfop/lib/pll",
  },
];

const faqs = [
  {
    id: "1",
    title: "什么是 CFOP？",
    content:
      "CFOP 是 Cross, F2L, OLL, PLL 的缩写，是目前世界上最流行的速拧还原方法。",
  },
  {
    id: "2",
    title: "学习 CFOP 需要多久？",
    content:
      "理解原理只需 15 分钟，但熟练掌握完整 78 个公式通常需要 1-3 个月的练习。",
  },
  {
    id: "3",
    title: "必须背完所有公式吗？",
    content:
      "不需要！你可以从 '2-Look OLL' 和 '2-Look PLL' 开始，仅需记忆 16 个公式即可达到 30 秒以内的速度。",
  },
  {
    id: "4",
    title: "F2L 很难理解怎么办？",
    content:
      "F2L 初期建议使用'直观法'（理解块的配对逻辑）而不是死记公式。随着熟练度提高，再记忆特殊情况的算法。",
  },
];

// --- 方法区 ---
const goPractice = () => {
  router.push("/cube");
};

const goToCourse2Look = () => {
  router.push("/learning/advanced");
};

const handleStepClick = (step) => {
  // 直接检查对象中是否有有效路由
  if (step.route) {
    console.log("正在跳转到:", step.route);
    router.push(step.route);
  } else {
    // 针对没有路由的步骤（如 Cross）
    console.log("该步骤暂无算法库");
  }
};

const scrollToId = (id) => {
  const element = document.getElementById(id);
  if (element) {
    element.scrollIntoView({
      behavior: "smooth", // 平滑滚动效果
      block: "start", // 滚动到元素顶部
    });
  } else {
    console.warn(`未找到 ID 为 ${id} 的元素`);
  }
};
</script>

<style scoped>
/* --- 基础设置 --- */
.cfop-intro-page {
  width: 100%;
  min-height: 100vh;
  background-color: #f8fafc;
  font-family: "Inter", sans-serif;
  color: #0f172a;
  padding-bottom: 80px;
}

.page-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 24px;
}

/* --- 1. Hero Section --- */
.hero-section {
  position: relative;
  padding: 80px 0 60px;
  overflow: hidden;
  border-radius: 32px;
  margin-bottom: 60px;
}

/* 氛围光晕 */
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
  font-size: 3.5rem;
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

/* --- 通用 Section 样式 --- */
.section-block {
  margin-bottom: 80px;
}

.section-heading {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 16px;
  color: #0f172a;
}
.section-heading.text-center {
  text-align: center;
}

.section-sub {
  font-size: 1.1rem;
  color: #64748b;
  margin-bottom: 40px;
}

/* --- 2. 学习目标 --- */
.learning-list-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.check-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.check-list li {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.1rem;
  color: #334155;
}

.check-icon {
  color: #10b981;
  font-weight: bold;
}

.simulator-promo {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.promo-icon {
  width: 48px;
  height: 48px;
  background: #eff6ff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
  font-size: 24px;
}

.promo-text {
  flex: 1;
  font-size: 14px;
  color: #64748b;
}
.promo-text strong {
  display: block;
  color: #0f172a;
  margin-bottom: 4px;
  font-size: 15px;
}

/* --- 3. 决策树 --- */
.decision-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.decision-card {
  background: #fff;
  border: 2px solid transparent;
  border-radius: 20px;
  padding: 30px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.decision-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.decision-card .icon-box {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-bottom: 20px;
}

.decision-card h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 8px;
}
.decision-card p {
  font-size: 0.9rem;
  color: #64748b;
}

/* 颜色主题 */
.decision-card.emerald {
  background: linear-gradient(to bottom right, #ecfdf5, #fff);
  border-color: #d1fae5;
}
.decision-card.emerald:hover {
  border-color: #10b981;
}
.decision-card.emerald .icon-box {
  background: rgba(16, 185, 129, 0.1);
}

.decision-card.blue {
  background: linear-gradient(to bottom right, #eff6ff, #fff);
  border-color: #dbeafe;
}
.decision-card.blue:hover {
  border-color: #3b82f6;
}
.decision-card.blue .icon-box {
  background: rgba(59, 130, 246, 0.1);
}

.decision-card.purple {
  background: linear-gradient(to bottom right, #f5f3ff, #fff);
  border-color: #ede9fe;
}
.decision-card.purple:hover {
  border-color: #8b5cf6;
}
.decision-card.purple .icon-box {
  background: rgba(139, 92, 246, 0.1);
}

/* --- 4. 统计 Grid --- */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}
@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.stat-box {
  background: #fff;
  border-radius: 20px;
  padding: 24px;
  text-align: center;
  border: 1px solid #e2e8f0;
  transition: transform 0.3s;
}
.stat-box:hover {
  transform: scale(1.05);
}

.stat-icon {
  font-size: 24px;
  margin-bottom: 12px;
}
.stat-num {
  font-size: 2.5rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1;
  margin-bottom: 8px;
}
.stat-label {
  font-size: 0.9rem;
  color: #64748b;
}

/* --- 5. 时间线 --- */
.timeline-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.timeline-item {
  display: flex;
  align-items: center;
  gap: 20px;
  background: #fff;
  padding: 20px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s;
}
.timeline-item:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
}

.time-badge {
  font-size: 1.5rem;
  font-weight: 800;
  width: 100px;
  text-align: center;
}
.time-badge.green {
  color: #10b981;
}
.time-badge.blue {
  color: #3b82f6;
}
.time-badge.purple {
  color: #8b5cf6;
}
.time-badge.orange {
  color: #f59e0b;
}

.time-content {
  flex: 1;
}
.time-content h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 4px;
}
.time-content p {
  font-size: 0.9rem;
  color: #64748b;
}

.progress-bar-wrap {
  width: 150px;
  height: 8px;
  background: #f1f5f9;
  border-radius: 4px;
  overflow: hidden;
}
.progress-bar {
  height: 100%;
  border-radius: 4px;
}
.progress-bar.green {
  background: linear-gradient(to right, #10b981, #34d399);
}
.progress-bar.blue {
  background: linear-gradient(to right, #3b82f6, #60a5fa);
}
.progress-bar.purple {
  background: linear-gradient(to right, #8b5cf6, #a78bfa);
}
.progress-bar.orange {
  background: linear-gradient(to right, #f59e0b, #fbbf24);
}

/* --- 6. 步骤卡片 --- */
.steps-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.step-card {
  background: #fff;
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); /* 更平滑的曲线 */
  position: relative;
}

/* 只有带路由的卡片才有悬浮效果 */
.step-card.is-clickable {
  cursor: pointer;
}

.step-card.is-clickable:hover {
  transform: translateY(-4px) scale(1.01); /* 微微上浮放大 */
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.1);
  border-color: #3b82f6; /* 边框变蓝 */
}

.step-header {
  background: #f8fafc;
  padding: 20px 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  border-bottom: 1px solid #f1f5f9;
  transition: background 0.3s;
}

/* 悬浮时 Header 变色 */
.step-card.is-clickable:hover .step-header {
  background: #eff6ff;
}

.step-number {
  width: 32px;
  height: 32px;
  background: #0f172a;
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
}

.step-title {
  font-size: 1.25rem;
  font-weight: 800;
  flex: 1;
  color: #1e293b;
}
.step-icon {
  font-size: 1.5rem;
}

.step-body {
  padding: 24px;
  position: relative;
}
.step-body p {
  color: #475569;
  line-height: 1.6;
  margin-bottom: 16px;
  max-width: 90%;
}

.step-meta {
  display: flex;
  gap: 12px;
}
.meta-tag {
  background: #f1f5f9;
  color: #64748b;
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 6px;
  font-weight: 600;
}
.meta-tag.highlight {
  background: #f0fdf4;
  color: #166534;
  border: 1px solid #dcfce7;
}

/* 箭头入口提示 */
.enter-hint {
  position: absolute;
  right: 24px;
  bottom: 24px;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 700;
  color: #3b82f6;
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.3s ease;
}

.step-card.is-clickable:hover .enter-hint {
  opacity: 1;
  transform: translateX(0);
}

/* --- 7. 对比表 --- */
.table-wrapper {
  overflow-x: auto;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
}

.comparison-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  min-width: 600px;
}

.comparison-table th {
  background: #f8fafc;
  padding: 16px;
  text-align: left;
  font-weight: 700;
  color: #475569;
  border-bottom: 1px solid #e2e8f0;
}

.comparison-table td {
  padding: 16px;
  border-bottom: 1px solid #f1f5f9;
  color: #334155;
}

.highlight-row {
  background: #f0f9ff;
}
.rec-badge {
  background: #0f172a;
  color: #fff;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: 8px;
  vertical-align: middle;
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

/* --- 8. FAQ --- */
.faq-container {
  max-width: 800px;
  margin: 0 auto;
}
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

/* 响应式微调 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }
  .timeline-item {
    flex-direction: column;
    align-items: flex-start;
  }
  .progress-bar-wrap {
    width: 100%;
  }
}
</style>
