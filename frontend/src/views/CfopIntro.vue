<template>
  <div class="cfop-intro-page">
    <div class="page-container">
      <!-- ================= 1. Hero Section ================= -->
      <section class="hero-section" v-animate>
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

      <!-- ================= 2. 学习目标 ================= -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">你将学到</h2>
        <div class="learning-list-card">
          <ul class="check-list">
            <li v-for="(item, i) in learningPoints" :key="i">
              <el-icon class="check-icon"><Check /></el-icon>
              <span>{{ item }}</span>
            </li>
          </ul>

          <!-- 模拟器推广卡片 -->
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

      <!-- ================= 3. 决策树 ================= -->
      <section class="section-block" v-animate>
        <h2 class="section-heading text-center">我应该选择哪条路径？</h2>
        <p class="section-sub text-center">
          不确定从哪里开始？根据你的经验水平选择：
        </p>

        <div class="decision-grid">
          <div
            class="decision-card emerald"
            @click="goToCourse2Look('advanced')"
          >
            <div class="icon-box">🌱</div>
            <h3>我是 CFOP 新手</h3>
            <p>从 16 个基础算法开始 (2-Look)</p>
          </div>

          <!-- 中卡：电梯模式 -->
          <div class="decision-card blue" @click="scrollToId('full-roadmap')">
            <div class="icon-box"><ArrowTrendingUpIcon class="w-7 h-7 icon-blue" /></div>
            <h3>挑战完整 CFOP</h3>
            <p>分模块攻克 F2L + OLL + PLL</p>
          </div>

          <!-- 右卡：查表模式 -->
          <div class="decision-card purple" @click="scrollToId('full-roadmap')">
            <div class="icon-box"><BoltIcon class="w-7 h-7 icon-orange" /></div>
            <h3>我需要快速参考</h3>
            <p>查阅算法表与指法技巧</p>
          </div>
        </div>
      </section>

      <!-- ================= 4. CFOP 数据概览 ================= -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">CFOP 数据概览</h2>
        <div class="stats-grid">
          <div class="stat-box blue-theme">
            <div class="blob"></div>
            <div class="bg"></div>
            <div class="stat-content">
              <div class="stat-icon"><TrophyIcon class="w-6 h-6 icon-yellow" /></div>
              <div class="stat-num">4</div>
              <div class="stat-label">主要步骤</div>
            </div>
          </div>

          <div class="stat-box purple-theme">
            <div class="blob"></div>
            <div class="bg"></div>
            <div class="stat-content">
              <div class="stat-icon">🔄</div>
              <div class="stat-num">57</div>
              <div class="stat-label">OLL 情况</div>
            </div>
          </div>

          <div class="stat-box orange-theme">
            <div class="blob"></div>
            <div class="bg"></div>
            <div class="stat-content">
              <div class="stat-icon"><PuzzlePieceIcon class="w-6 h-6 icon-cyan" /></div>
              <div class="stat-num">21</div>
              <div class="stat-label">PLL 情况</div>
            </div>
          </div>

          <div class="stat-box emerald-theme">
            <div class="blob"></div>
            <div class="bg"></div>
            <div class="stat-content">
              <div class="stat-icon">🤝</div>
              <div class="stat-num">41</div>
              <div class="stat-label">F2L 情况</div>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= 5. 进步时间线 ================= -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">CFOP 进步时间线</h2>
        <p class="section-sub">掌握每个阶段后你可以期待的速度：</p>

        <div class="timeline-container">
          <div
            class="timeline-item"
            :class="time.colorClass"
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
      <section id="full-roadmap" class="section-block" v-animate>
        <h2 class="section-heading text-center">4 步 CFOP 详解与入口</h2>
        <p class="section-sub text-center">点击卡片进入对应的算法库：</p>

        <div class="roadmap-wrapper">
          <!-- 垂直连接线 -->
          <div class="roadmap-line"></div>

          <div
            class="roadmap-node"
            v-for="(step, idx) in cfopSteps"
            :key="idx"
            :class="{ 'is-clickable': step.route }"
            @click="handleStepClick(step)"
          >
            <!-- 左侧节点 -->
            <div class="node-marker">
              <div class="marker-circle">{{ idx + 1 }}</div>
            </div>

            <!-- 右侧卡片 -->
            <div class="node-card">
              <div class="card-header">
                <div class="header-left">
                  <span class="step-icon"><component :is="step.icon" class="w-6 h-6" :class="step.iconClass" /></span>
                  <h3 class="step-title">{{ step.title }}</h3>
                </div>
                <!-- 入口箭头 -->
                <div class="header-right" v-if="step.route">
                  <span class="enter-text">进入库</span>
                  <el-icon><ArrowRight /></el-icon>
                </div>
              </div>
              <div class="card-body">
                <p>{{ step.desc }}</p>
                <div class="step-meta">
                  <span class="meta-tag">目标: {{ step.goal }}</span>
                  <span class="meta-tag highlight"
                    >算法: {{ step.algCount }}</span
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= 7. 方法对比表 ================= -->
      <section class="section-block" v-animate>
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
      <section class="section-wrapper faq-modern-section">
        <div class="container">
          <!-- 标题：加入入场动画 -->
          <div class="section-header center animate-entry delay-1">
            <h2 class="section-title">常见问题</h2>
            <p class="section-desc">关于 CFOP，你想知道的都在这里</p>
          </div>

          <!-- 容器：移除默认边框 -->
          <div class="faq-list-container animate-entry delay-2">
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
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { Check, Monitor, ArrowRight } from "@element-plus/icons-vue";
import { 
  ArrowTrendingUpIcon,
  BoltIcon,
  TrophyIcon,
  PuzzlePieceIcon,
  Square3Stack3DIcon,
  ArrowsRightLeftIcon,
  FlagIcon
} from "@heroicons/vue/24/solid";

const router = useRouter();
const activeNames = ref("1");

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
    ); // 露出10%触发
    observer.observe(el);
  },
};

// === 核心逻辑：滚动触发动画 ===
onMounted(() => {
  const observerOptions = {
    threshold: 0.15, // 元素露出 15% 时触发
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        // 当元素进入视野，添加 is-visible 类触发 CSS 动画
        entry.target.classList.add("is-visible");
        // 触发后停止观察，保证动画只跑一次
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // 扫描所有需要入场动画的元素
  const animElements = document.querySelectorAll(
    ".animate-entry, .animate-entry-right",
  );
  animElements.forEach((el) => observer.observe(el));
});

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
    icon: Square3Stack3DIcon,
    iconClass: "icon-green",
    desc: "通过将棱块与中心块对齐，在底层完成一个十字。重点在于规划，尽量在 8 步内完成。",
    goal: "底层十字",
    algCount: "无",
    route: null,
  },
  {
    id: "f2l",
    title: "F2L (前两层)",
    icon: ArrowsRightLeftIcon,
    iconClass: "icon-cyan",
    desc: "同时还原底层角块和中间层棱块。这是 CFOP 中最慢但也最能提速的阶段。",
    goal: "前两层完成",
    algCount: "41",
    route: "/cfop/lib/f2l",
  },
  {
    id: "oll",
    title: "OLL (顶层定向)",
    icon: TrophyIcon,
    iconClass: "icon-yellow",
    desc: "将顶层所有颜色统一朝上。分为 2-Look (10个公式) 和 Full (57个公式)。",
    goal: "顶面复原",
    algCount: "57",
    route: "/cfop/lib/oll",
  },
  {
    id: "pll",
    title: "PLL (顶层排列)",
    icon: FlagIcon,
    iconClass: "icon-purple",
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
      "理解原理只需 15 分钟，但熟练掌握完整 119 个公式通常需要 1-3 个月的练习。",
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

// --- 逻辑方法 ---
const goPractice = () => router.push("/cube");
const goToCourse2Look = () => router.push("/learning/advanced");

const handleStepClick = (step) => {
  if (step.route) {
    router.push(step.route);
  } else {
    // 静态卡片不操作
  }
};

const scrollToId = (id) => {
  const element = document.getElementById(id);
  if (element) {
    element.scrollIntoView({ behavior: "smooth", block: "start" });
  }
};

// 页面加载时处理滚动状态（从 Library 返回）
onMounted(() => {
  const state = window.history.state;
  if (state && state.scrollTarget === "full-roadmap") {
    setTimeout(() => {
      scrollToId("full-roadmap");
      window.history.replaceState({ ...state, scrollTarget: null }, "");
    }, 100);
  }
});
</script>

<style scoped>
/* --- 页面基础 --- */
.cfop-intro-page {
  width: 100%;
  min-height: 100vh;
  background-color: #f8fafc;
  font-family: "Inter", sans-serif;
  color: #0f172a;
  padding-bottom: 100px;
  overflow-x: hidden; /* 避免动效横向溢出 */
}

.page-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 24px;
}

/* --- 动效类 --- */
.before-enter {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.enter {
  opacity: 1;
  transform: translateY(0);
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

/* --- 通用 Section --- */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.section-block {
  margin-bottom: 100px;
}
.section-heading {
  font-size: 2rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 40px;
}
.section-sub {
  font-size: 1.1rem;
  color: #64748b;
  margin-bottom: 50px;
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
  text-align: center;
}
.decision-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}
.decision-card .icon-box {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin: 0 auto 20px;
}

.decision-card .icon-box svg {
  width: 28px;
  height: 28px;
}
.decision-card h3 {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 8px;
}
.decision-card p {
  font-size: 0.95rem;
  color: #64748b;
}

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
  margin-top: 20px;
}

.stat-box {
  position: relative;
  width: 100%;
  height: 220px;
  border-radius: 20px;
  z-index: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
  cursor: pointer;
}

/* 1. 顶部彩色装饰线 */
.stat-box::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px; /* 线条粗细 */
  background: var(--theme-color);
  z-index: 10; /* 确保在最上层 */
}

/* 2. 内部磨砂背景层 */
.stat-box .bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(30px);
  transition: all 0.5s ease;
}

/* 3. 动态色斑 (默认隐藏) */
.stat-box .blob {
  position: absolute;
  z-index: 1;
  top: 10%;
  left: 10%;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background-color: var(--theme-color);
  opacity: 0;
  filter: blur(20px);
  transition: all 0.6s ease;
  animation: blob-bounce 6s infinite ease;
}

/* --- 悬浮激活逻辑 --- */
.stat-box:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  border-color: var(--theme-color); /* 边框变色 */
}

.stat-box:hover .bg {
  background: rgba(255, 255, 255, 0.7);
}

.stat-box:hover .blob {
  opacity: 0.6;
  transform: scale(1.3);
}

/* 4. 实际内容层 */
.stat-content {
  position: relative;
  z-index: 5; /* 确保在所有层级之上 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.stat-icon {
  font-size: 26px;
  margin-bottom: 12px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.stat-icon svg {
  width: 24px;
  height: 24px;
}

.stat-num {
  font-size: 2.8rem;
  font-weight: 900;
  color: #1e293b;
  line-height: 1;
  margin-bottom: 8px;
  letter-spacing: -1px;
}

.stat-label {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* 颜色主题配置 */
.stat-box.blue-theme {
  --theme-color: #3b82f6;
}
.stat-box.purple-theme {
  --theme-color: #8b5cf6;
}
.stat-box.orange-theme {
  --theme-color: #f59e0b;
}
.stat-box.emerald-theme {
  --theme-color: #10b981;
}

/* 动画关键帧保持逻辑 */
@keyframes blob-bounce {
  0% {
    transform: translate(-80%, -80%);
  }
  25% {
    transform: translate(20%, -80%);
  }
  50% {
    transform: translate(20%, 20%);
  }
  75% {
    transform: translate(-80%, 20%);
  }
  100% {
    transform: translate(-80%, -80%);
  }
}

/* 响应式 */
@media (max-width: 992px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 500px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}

/* --- 5. 进步时间线 --- */
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
  padding: 24px 30px; /* 稍微增加内边距 */
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  position: relative; /* 必须 */
  overflow: hidden; /* 必须 */
}

.timeline-item:hover {
  box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.05);
  transform: translateX(8px); /* 悬浮时轻微右移，配合左侧线条更有质感 */
}

/* 左侧装饰线条通用样式 */
.timeline-item::before {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 4px; /* 线条宽度 */
  background: var(--timeline-color);
}

/* 根据 Template 传入的类名分配颜色 */
.timeline-item.green {
  --timeline-color: #10b981;
}
.timeline-item.blue {
  --timeline-color: #3b82f6;
}
.timeline-item.purple {
  --timeline-color: #8b5cf6;
}
.timeline-item.orange {
  --timeline-color: #f59e0b;
}

.time-badge {
  font-size: 1.5rem;
  font-weight: 800;
  width: 100px;
  text-align: center;
  /* 颜色跟随父级变量，保持一致性 */
  color: var(--timeline-color);
}

.time-content {
  flex: 1;
}

.time-content h3 {
  font-size: 1.15rem;
  font-weight: 800;
  margin-bottom: 6px;
  color: #1e293b;
}

.time-content p {
  font-size: 0.95rem;
  color: #64748b;
}

.progress-bar-wrap {
  width: 180px;
  height: 8px;
  background: #f1f5f9;
  border-radius: 10px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: 10px;
}

/* 进度条也改用变量，简化代码 */
.progress-bar {
  background: var(--timeline-color);
  opacity: 0.8;
}

/* --- 6. 垂直时间轴 (Roadmap) --- */
.roadmap-wrapper {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  padding-left: 40px; /* 留出左侧空间 */
}

/* 贯穿线 */
.roadmap-line {
  position: absolute;
  left: 19px; /* 圆点中心 */
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

.node-marker {
  position: absolute;
  left: -40px;
  top: 24px; /* 对齐卡片顶部 */
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
  color: #94a3b8;
  transition: all 0.3s;
}

/* 激活状态 (悬浮或点击) */
.roadmap-node.is-clickable {
  cursor: pointer;
}
.roadmap-node:hover .marker-circle,
.roadmap-node.is-clickable:hover .marker-circle {
  border-color: #3b82f6;
  color: #3b82f6;
  transform: scale(1.1);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.node-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 24px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

/* 悬浮动效 */
.roadmap-node.is-clickable:hover .node-card {
  border-color: #3b82f6;
  transform: translateX(10px); /* 向右微动，增强连接感 */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}
/* 静态卡片视觉弱化 */
.roadmap-node:not(.is-clickable) .node-card {
  background: #f8fafc;
  opacity: 0.9;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.step-icon {
  font-size: 1.5rem;
}

.step-icon svg {
  width: 24px;
  height: 24px;
}
.step-title {
  font-size: 1.25rem;
  font-weight: 800;
  margin: 0;
  color: #1e293b;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #3b82f6;
  font-size: 14px;
  font-weight: 700;
  opacity: 0;
  transition: opacity 0.3s;
}
.roadmap-node.is-clickable:hover .header-right {
  opacity: 1;
}

.card-body p {
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 16px;
}
.tags-row {
  display: flex;
  gap: 12px;
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
  padding: 20px;
  text-align: left;
  font-weight: 700;
  color: #475569;
  border-bottom: 1px solid #e2e8f0;
}
.comparison-table td {
  padding: 20px;
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

/* --- 8. FAQ Section 整体布局 --- */
.faq-modern-section {
  padding-top: 80px;
  padding-bottom: 80px;
}

.faq-list-container {
  max-width: 800px;
  margin: 0 auto;
}

/* Section标题样式 */
.section-header.center {
  text-align: center;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 16px;
  letter-spacing: -1px;
}

.section-desc {
  font-size: 1.15rem;
  color: #64748b;
}

/* === 入场动画系统 === */

/* 1. 定义动画关键帧 */
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

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 2. 修改动画类：默认不执行动画，只设置初始隐藏状态 */
.animate-entry,
.animate-entry-right {
  opacity: 0;
  will-change: transform, opacity;
}

/* 3. 激活类：大幅度拉长时间，并使用更平滑的曲线 */
.animate-entry.is-visible {
  animation: fadeInUp 1s cubic-bezier(0.33, 1, 0.68, 1) forwards;
}

.animate-entry-right.is-visible {
  animation: fadeInRight 1s cubic-bezier(0.33, 1, 0.68, 1) forwards;
}

/* 4. 延迟梯度 */
.delay-1 {
  animation-delay: 0.5s;
}
.delay-2 {
  animation-delay: 1s;
}
.delay-3 {
  animation-delay: 1.5s;
}
.delay-4 {
  animation-delay: 2s;
}
.delay-5 {
  animation-delay: 2.5s;
}

/* --- 深度重塑 Element Collapse --- */
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
[data-theme="light"] :deep(.el-collapse-item:hover) {
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
[data-theme="light"] :deep(.el-collapse-item.is-active) {
  background-color: #ffffff;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05);
  border-bottom-color: #f1f5f9 !important;
}

[data-theme="light"] :deep(.el-collapse-item.is-active) .faq-index {
  color: #2563eb; /* 展开时序号变蓝 */
}

[data-theme="light"] :deep(.el-collapse-item.is-active) .faq-question {
  color: #2563eb;
}

/* 回答内容的排版 */
.faq-answer-content {
  padding: 20px 0 10px 54px;
  line-height: 1.8;
  color: #64748b;
  font-size: 1rem;
  text-align: left;
}

/* 响应式 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  .decision-grid,
  .stats-grid,
  .milestone-grid {
    grid-template-columns: 1fr;
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
}

/* ==================== Dark Mode Styles ==================== */
[data-theme="dark"] .cfop-intro-page {
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

[data-theme="dark"] .section-sub {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .learning-list-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .check-list li {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .simulator-promo {
  background: var(--dm-bg-hover);
  border-color: var(--dm-border);
}

[data-theme="dark"] .promo-icon {
  background: rgba(59, 130, 246, 0.15);
  color: var(--dm-accent);
}

[data-theme="dark"] .promo-text {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .promo-text strong {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .decision-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
  box-shadow: var(--dm-shadow-md);
}

[data-theme="dark"] .decision-card:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .decision-card p {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .decision-card.emerald {
  background: linear-gradient(
    to bottom right,
    rgba(16, 185, 129, 0.1),
    var(--dm-bg-card)
  );
  border-color: rgba(16, 185, 129, 0.3);
}

[data-theme="dark"] .decision-card.blue {
  background: linear-gradient(
    to bottom right,
    rgba(59, 130, 246, 0.1),
    var(--dm-bg-card)
  );
  border-color: rgba(59, 130, 246, 0.3);
}

[data-theme="dark"] .decision-card.purple {
  background: linear-gradient(
    to bottom right,
    rgba(139, 92, 246, 0.1),
    var(--dm-bg-card)
  );
  border-color: rgba(139, 92, 246, 0.3);
}

[data-theme="dark"] .stat-box {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .stat-box .bg {
  background: rgba(30, 41, 59, 0.95);
}

[data-theme="dark"] .stat-box:hover .bg {
  background: rgba(30, 41, 59, 0.7);
}

[data-theme="dark"] .stat-num {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .stat-label {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .timeline-item {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .time-content h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .time-content p {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .progress-bar-wrap {
  background: var(--dm-bg-hover);
}

[data-theme="dark"] .roadmap-line {
  background: var(--dm-border);
}

[data-theme="dark"] .marker-circle {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
  color: var(--dm-text-muted);
}

[data-theme="dark"] .roadmap-node:hover .marker-circle {
  border-color: var(--dm-accent);
  color: var(--dm-accent);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}

[data-theme="dark"] .node-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .roadmap-node.is-clickable:hover .node-card {
  border-color: var(--dm-accent);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .roadmap-node:not(.is-clickable) .node-card {
  background: var(--dm-bg-hover);
}

[data-theme="dark"] .step-title {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .header-right {
  color: var(--dm-accent);
}

[data-theme="dark"] .card-body p {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .meta-tag {
  background: var(--dm-bg-hover);
  color: var(--dm-text-muted);
}

[data-theme="dark"] .meta-tag.highlight {
  background: rgba(59, 130, 246, 0.15);
  color: var(--dm-accent);
}

[data-theme="dark"] .table-wrapper {
  border-color: var(--dm-border);
}

[data-theme="dark"] .comparison-table {
  background: var(--dm-bg-card);
}

[data-theme="dark"] .comparison-table th {
  background: var(--dm-bg-hover);
  color: var(--dm-text-secondary);
  border-bottom-color: var(--dm-border);
}

[data-theme="dark"] .comparison-table td {
  border-bottom-color: var(--dm-border);
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .highlight-row {
  background: rgba(59, 130, 246, 0.1);
}

[data-theme="dark"] .rec-badge {
  background: var(--dm-text-primary);
  color: var(--dm-bg-page);
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

/* FAQ 部分深色模式 */
html[data-theme="dark"] .faq-modern-section {
  /* 移除背景和边框，让FAQ融入页面背景 */
}

[data-theme="dark"] .section-title {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .section-desc {
  color: var(--dm-text-muted);
}

html[data-theme="dark"] :deep(.el-collapse-item) {
  border-bottom-color: var(--dm-border) !important;
  transition: all 0.3s ease;
}

html[data-theme="dark"] :deep(.el-collapse-item:hover) {
  /* 移除背景色，让内容融入页面背景 */
}

html[data-theme="dark"] :deep(.el-collapse-item__header) {
  background-color: var(--dm-bg-card) !important;
  color: var(--dm-text-primary);
  border: none !important;
  transition: all 0.3s;
}

html[data-theme="dark"] :deep(.el-collapse-item__wrap) {
  background-color: transparent;
  border: none !important;
}

html[data-theme="dark"] :deep(.el-collapse-item__content) {
  background-color: transparent;
  color: var(--dm-text-secondary);
}

html[data-theme="dark"] .faq-index {
  color: var(--dm-text-muted);
}

html[data-theme="dark"] .faq-question {
  color: var(--dm-text-primary);
}

html[data-theme="dark"] :deep(.el-collapse-item.is-active) {
  background-color: var(--dm-bg-card);
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.3);
  border-bottom-color: var(--dm-border) !important;
}

html[data-theme="dark"] :deep(.el-collapse-item.is-active) .faq-index,
html[data-theme="dark"] :deep(.el-collapse-item.is-active) .faq-question {
  color: var(--dm-accent);
}

html[data-theme="dark"] .faq-answer-content {
  color: var(--dm-text-secondary);
  text-align: left;
}
</style>
