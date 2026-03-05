<template>
  <div class="tech-doc-page kociemba-doc">
    <div class="page-container">
      <!-- 返回 About 页面按钮 -->
      <header class="tech-doc-header">
        <button @click="goBackToAbout" class="minimal-back-btn">
          <el-icon><ArrowLeft /></el-icon>
          <span>BACK TO ABOUT</span>
        </button>

        <!-- 面包屑导航 -->
        <nav class="breadcrumb-nav">
          <div class="breadcrumb-links">
            <a
              v-for="section in sections"
              :key="section.id"
              @click="scrollToSection(section.id)"
              class="breadcrumb-link"
              :class="{ active: activeSection === section.id }"
            >
              {{ section.title }}
            </a>
          </div>
        </nav>
      </header>

      <!-- Hero Section -->
      <section id="background" class="hero-section" v-animate>
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
            深入解析 Herbert Kociemba 于 1992 年提出的两阶段算法，该算法能在约
            19 步内求解任意魔方状态，是 CubeMaster 求解引擎的核心。
          </p>

          <div class="stats-pills left-align">
            <div class="stat-pill">
              <span class="dot-indicator blue"></span>
              <span>平均解长度：约 18-20 步</span>
            </div>
            <div class="stat-pill">
              <span class="dot-indicator green"></span>
              <span>求解时间：约 1 秒内</span>
            </div>
            <div class="stat-pill">
              <span class="dot-indicator purple"></span>
              <span>存储需求：约 67 MB</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 第1节：算法背景与核心思想 -->
      <section id="background" class="section-block" v-animate>
        <h2 class="section-heading">1. 算法背景与核心思想</h2>

        <div class="content-card">
          <h3 class="subsection-heading">1.1 什么是 Kociemba 算法？</h3>
          <p class="paragraph">
            Kociemba 算法（又称二阶段算法）是由德国数学家 Herbert Kociemba 于
            1992 年提出的高效魔方求解算法。
          </p>

          <p class="paragraph highlight"><strong>核心特性：</strong></p>

          <div class="feature-table-wrapper">
            <table class="feature-table">
              <thead>
                <tr>
                  <th>特性</th>
                  <th>数值</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>平均求解步数</td>
                  <td><strong>约 18-20 步</strong></td>
                </tr>
                <tr>
                  <td>最坏情况</td>
                  <td><strong>约 20 步</strong>（上帝数）</td>
                </tr>
                <tr>
                  <td>求解时间</td>
                  <td><strong>约 1 秒内</strong>（普通 CPU）</td>
                </tr>
                <tr>
                  <td>存储需求</td>
                  <td><strong>约 67 MB</strong>（所有表文件）</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="content-card">
          <h3 class="subsection-heading">1.2 两阶段分解原理</h3>

          <div class="phase-section">
            <h4>阶段一：初始状态到 G1 子群</h4>
            <p class="paragraph">
              <strong>目标：</strong>将魔方从任意状态变换至 G1 子群状态。
            </p>

            <p class="paragraph"><strong>G1 子群定义：</strong></p>
            <ul class="feature-list">
              <li>角块方向正确：所有角块方向值之和等于 0 (mod 3)</li>
              <li>棱块方向正确：所有棱块方向值之和等于 0 (mod 2)</li>
              <li>中层棱块归位：FR、FL、BL、BR 四个棱块全部回到中层槽位</li>
            </ul>

            <p class="paragraph">
              <strong>状态空间（用于建立剪枝表）：</strong>
            </p>
            <div class="code-block-text">
              角块方向：3^7 = 2,187 种状态 棱块方向：2^11 = 2,048 种状态
              中层棱块位置：C(12,4) = 495 种状态 总计：约 22 亿种状态
            </div>
          </div>

          <div class="phase-section">
            <h4>阶段二：G1 子群到还原状态</h4>
            <p class="paragraph">
              <strong>可用操作：</strong>{ U, D, L2, R2, F2, B2
              }（这些操作能保持 G1 的特征不被破坏）
            </p>
            <p class="paragraph">
              <strong>目标：</strong
              >在不改变块方向的前提下，通过位置置换完成还原。
            </p>
            <p class="paragraph"><strong>状态空间：</strong></p>
            <div class="code-block-text">
              角块位置：8! = 40,320 种状态 棱块位置：8! = 40,320 种状态
              中层棱块：4! = 24 种状态 总计：约 195 亿种状态（考虑奇偶性限制）
            </div>
          </div>
        </div>

        <div class="content-card">
          <h3 class="subsection-heading">1.3 算法划分的理论依据与技术优势</h3>

          <h4>状态空间的指数级降维</h4>
          <p class="paragraph">
            魔方的全状态空间高达约 4.33 × 10^19
            种，直接建立索引或启发式表在计算上是不可行的。
          </p>
          <ul class="feature-list">
            <li>
              <strong>分阶段处理：</strong>通过引入 G1
              子群作为中间目标，将复杂问题拆解为两个规模可控的子问题
            </li>
            <li>
              <strong>剪枝表可行性：</strong>阶段二最大的独立子空间为 8!（约
              40,320），使得算法可以预先计算并存储所有可能的距离值
            </li>
          </ul>

          <h4>算子集对子群性质的保持</h4>
          <p class="paragraph">
            在阶段二中，操作集限定为 G1 = &#10216;U, D, L2, R2, F2, B2&#10217;：
          </p>
          <ul class="feature-list">
            <li>
              <strong>方向不变性：</strong>上述算子属于 G1
              子群的生成元，不会改变棱块和角块的方向
            </li>
            <li>
              <strong>轨道闭合性：</strong
              >中层棱块与顶底层棱块形成互相独立的置换轨道，确保中层棱块在阶段二中不会移出
              E 层槽位
            </li>
          </ul>

          <h4>搜索效率的优化</h4>
          <p class="paragraph">这种划分极大缩短了搜索树的深度：</p>
          <ul class="feature-list">
            <li>
              <strong>阶段一：</strong
              >侧重于定性约束（方向与层归属），搜索目标明确，路径较短
            </li>
            <li>
              <strong>阶段二：</strong
              >侧重于定量排列（位置置换），启发式估值函数相互独立且高度优化
            </li>
          </ul>
        </div>
      </section>

      <!-- 第2节：文件结构总览 -->
      <section id="file-structure" class="section-block" v-animate>
        <h2 class="section-heading">2. 文件结构总览</h2>

        <div class="content-card">
          <h3 class="subsection-heading">2.1 核心算法文件</h3>

          <p class="paragraph">
            以下是 twophase 目录下的核心算法文件，这些文件实现了 Kociemba
            算法的完整功能：
          </p>

          <div class="feature-table-wrapper">
            <table class="feature-table core-files">
              <thead>
                <tr>
                  <th>文件名</th>
                  <th>行数</th>
                  <th>核心功能</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>solver.py</code></td>
                  <td>311</td>
                  <td>两阶段搜索算法主逻辑，IDA* 实现</td>
                </tr>
                <tr>
                  <td><code>pruning.py</code></td>
                  <td>332</td>
                  <td>剪枝表生成与查询，启发式函数</td>
                </tr>
                <tr>
                  <td><code>moves.py</code></td>
                  <td>210</td>
                  <td>移动表，坐标转换核心数据结构</td>
                </tr>
                <tr>
                  <td><code>cubie.py</code></td>
                  <td>561</td>
                  <td>魔方块层次表示，基本数据结构</td>
                </tr>
                <tr>
                  <td><code>coord.py</code></td>
                  <td>223</td>
                  <td>坐标层次表示，状态编码</td>
                </tr>
                <tr>
                  <td><code>symmetries.py</code></td>
                  <td>-</td>
                  <td>对称性处理，减少搜索空间</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="content-card">
          <h3 class="subsection-heading">2.2 辅助文件</h3>

          <div class="feature-table-wrapper">
            <table class="feature-table">
              <thead>
                <tr>
                  <th>文件名</th>
                  <th>功能</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>defs.py</code></td>
                  <td>常量定义（状态空间大小等）</td>
                </tr>
                <tr>
                  <td><code>enums.py</code></td>
                  <td>枚举类型（角块、棱块、颜色、移动等）</td>
                </tr>
                <tr>
                  <td><code>face.py</code></td>
                  <td>面层次表示（颜色编码）</td>
                </tr>
                <tr>
                  <td><code>misc.py</code></td>
                  <td>工具函数（排列组合等）</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="content-card">
          <h3 class="subsection-heading">2.3 非核心文件</h3>

          <p class="paragraph">
            以下文件主要用于 GUI、计算机视觉和网络通信，与核心算法无关：
          </p>

          <div class="tag-list">
            <span class="tag">client_gui.py</span>
            <span class="tag">client_gui2.py</span>
            <span class="tag">computer_vision.py</span>
            <span class="tag">vision2.py</span>
            <span class="tag">server.py</span>
            <span class="tag">sockets.py</span>
            <span class="tag">performance.py</span>
          </div>
        </div>
      </section>

      <!-- 第3节：核心文件详解 -->
      <section id="core-files" class="section-block" v-animate>
        <h2 class="section-heading">3. 核心文件详解</h2>

        <!-- solver.py -->
        <div class="content-card">
          <div class="file-header">
            <div class="file-icon">
              <span class="file-icon-text">Py</span>
            </div>
            <div class="file-title-group">
              <h3>solver.py</h3>
              <div class="file-meta">311 行 · 算法核心</div>
            </div>
          </div>

          <p class="paragraph">
            solver.py 是整个算法的核心，实现了两阶段搜索算法和 IDA*
            搜索。包含多线程求解器， 支持正向和逆向搜索，能够在约 1
            秒内找到最优解。
          </p>

          <div class="method-list">
            <h4>关键方法</h4>
            <ul>
              <li>
                <code>SolverThread.search()</code>
                <span>阶段一：IDA* 搜索，从初始状态到 G1 子群</span>
              </li>
              <li>
                <code>SolverThread.search_phase2()</code>
                <span>阶段二：在 G1 子群内搜索到还原状态</span>
              </li>
              <li>
                <code>solve()</code>
                <span>主入口：多线程求解魔方，启动 6 个线程并行搜索</span>
              </li>
            </ul>
          </div>

          <CodeBlock
            language="python"
            title="SolverThread 核心搜索逻辑"
            :code="solverCode"
          />
        </div>

        <!-- pruning.py -->
        <div class="content-card">
          <div class="file-header">
            <div class="file-icon">
              <span class="file-icon-text">Py</span>
            </div>
            <div class="file-title-group">
              <h3>pruning.py</h3>
              <div class="file-meta">332 行 · 剪枝表生成</div>
            </div>
          </div>

          <p class="paragraph">
            pruning.py 负责生成和查询剪枝表。通过位压缩技术（每个状态仅 2
            bit）， 将约 240 MB 的原始数据压缩到约 61 MB，实现高效的启发式评估。
          </p>

          <div class="method-list">
            <h4>关键方法</h4>
            <ul>
              <li>
                <code>create_phase1_prun_table()</code>
                <span>生成阶段一剪枝表（BFS + 对称性约减）</span>
              </li>
              <li>
                <code>create_phase2_prun_table()</code>
                <span>生成阶段二剪枝表</span>
              </li>
              <li>
                <code>get_flipslice_twist_depth3()</code>
                <span>查询状态到目标的距离（mod 3）</span>
              </li>
            </ul>
          </div>

          <CodeBlock
            language="python"
            title="位压缩查询实现"
            :code="pruningCode"
          />
        </div>

        <!-- moves.py -->
        <div class="content-card">
          <div class="file-header">
            <div class="file-icon">
              <span class="file-icon-text">Py</span>
            </div>
            <div class="file-title-group">
              <h3>moves.py</h3>
              <div class="file-meta">210 行 · 移动表</div>
            </div>
          </div>

          <p class="paragraph">
            moves.py 预计算所有可能的移动结果，实现 O(1) 时间的状态转移查询。
            包含 twist_move、flip_move、corners_move 等核心移动表。
          </p>

          <div class="method-list">
            <h4>关键数据结构</h4>
            <ul>
              <li>
                <code>twist_move[]</code>
                <span>角块方向移动表（2187 × 18）</span>
              </li>
              <li>
                <code>flip_move[]</code>
                <span>棱块方向移动表（2048 × 18）</span>
              </li>
              <li>
                <code>corners_move[]</code>
                <span>角块位置移动表（40320 × 18）</span>
              </li>
            </ul>
          </div>
        </div>

        <!-- cubie.py -->
        <div class="content-card">
          <div class="file-header">
            <div class="file-icon">
              <span class="file-icon-text">Py</span>
            </div>
            <div class="file-title-group">
              <h3>cubie.py</h3>
              <div class="file-meta">561 行 · 魔方块表示</div>
            </div>
          </div>

          <p class="paragraph">
            cubie.py 定义了魔方的基本数据结构：CubieCube 类。 使用
            cp、co、ep、eo 数组表示角块和棱块的位置与方向。
          </p>

          <CodeBlock
            language="python"
            title="CubieCube 核心结构"
            :code="cubieCode"
          />
        </div>

        <!-- coord.py -->
        <div class="content-card">
          <div class="file-header">
            <div class="file-icon">
              <span class="file-icon-text">Py</span>
            </div>
            <div class="file-title-group">
              <h3>coord.py</h3>
              <div class="file-meta">223 行 · 坐标表示</div>
            </div>
          </div>

          <p class="paragraph">
            coord.py 实现了魔方的坐标表示，将复杂的状态映射为数字索引，
            便于剪枝表查询和状态比较。
          </p>
        </div>

        <!-- defs.py -->
        <div class="content-card">
          <div class="file-header">
            <div class="file-icon">
              <span class="file-icon-text">Py</span>
            </div>
            <div class="file-title-group">
              <h3>defs.py</h3>
              <div class="file-meta">45 行 · 常量定义</div>
            </div>
          </div>

          <p class="paragraph">
            defs.py
            定义了算法中使用的所有常量：状态空间大小、对称性数量、文件路径等。
          </p>

          <CodeBlock language="python" title="关键常量定义" :code="defsCode" />
        </div>
      </section>

      <!-- 第4节：学习路径推荐 -->
      <section id="learning-path" class="section-block" v-animate>
        <h2 class="section-heading">4. 学习路径推荐</h2>

        <div class="roadmap-wrapper">
          <!-- 垂直连接线 -->
          <div class="roadmap-line"></div>

          <div
            class="roadmap-node"
            v-for="(stage, idx) in learningStages"
            :key="idx"
          >
            <!-- 左侧节点 -->
            <div class="node-marker">
              <div class="marker-circle">{{ idx + 1 }}</div>
            </div>

            <!-- 右侧卡片 -->
            <div class="node-card">
              <div class="card-header">
                <div class="header-left">
                  <span class="step-icon">{{ stage.icon }}</span>
                  <h3 class="step-title">{{ stage.title }}</h3>
                </div>
                <div class="header-right">
                  <span class="meta-tag highlight"
                    >预计 {{ stage.duration }}</span
                  >
                </div>
              </div>
              <div class="card-body">
                <div class="reading-path">{{ stage.path }}</div>
                <ul class="checklist">
                  <li v-for="item in stage.items" :key="item">{{ item }}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 第5节：关键代码段解析 -->
      <section id="code-analysis" class="section-block" v-animate>
        <h2 class="section-heading">5. 关键代码段解析</h2>

        <div class="content-card">
          <h3 class="subsection-heading">5.1 阶段一搜索核心</h3>

          <p class="paragraph">
            位置：solver.py:150-179。核心逻辑：应用移动 → 查询剪枝表 → 剪枝判断
            → 递归搜索
          </p>

          <CodeBlock
            language="python"
            title="阶段一 IDA* 搜索实现"
            :code="phase1SearchCode"
          />
        </div>

        <div class="content-card">
          <h3 class="subsection-heading">5.2 位压缩技术详解</h3>

          <p class="paragraph">
            通过位运算将每个状态压缩到 2 bit，相比 1 字节存储节省约 4 倍空间（约
            75%）
          </p>

          <CodeBlock
            language="python"
            title="剪枝表位压缩查询"
            :code="bitCompressionCode"
          />
        </div>

        <div class="content-card">
          <h3 class="subsection-heading">5.3 多线程并行搜索</h3>

          <p class="paragraph">
            启动 6 个线程：3 个方向（0°、120°、240°）× 正逆各 1 次，平均加速约
            12 倍
          </p>

          <CodeBlock
            language="python"
            title="多线程求解实现"
            :code="multithreadCode"
          />
        </div>
      </section>

      <!-- 第6节：性能分析 -->
      <section id="performance" class="section-block" v-animate>
        <h2 class="section-heading">6. 性能分析</h2>

        <div class="content-card">
          <h3 class="subsection-heading">6.1 存储需求</h3>

          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-value">34 MB</div>
              <div class="stat-label">阶段一剪枝表</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">27 MB</div>
              <div class="stat-label">阶段二剪枝表</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">5 MB</div>
              <div class="stat-label">移动表文件</div>
            </div>
            <div class="stat-card highlight">
              <div class="stat-value">67 MB</div>
              <div class="stat-label">总计</div>
            </div>
          </div>

          <div class="info-box success">
            <h4>位压缩技术</h4>
            <p>
              通过位运算将每个状态压缩到 2 bit，相比 1 字节存储节省约 4 倍空间：
            </p>
            <ul>
              <li>未压缩：约 140,893,410 状态 × 1 字节 = 约 134 MB</li>
              <li>压缩后：约 140,893,410 状态 ÷ 16 × 4 字节 = 约 33.6 MB</li>
              <li>节省空间：约 75%</li>
            </ul>
          </div>
        </div>

        <div class="content-card">
          <h3 class="subsection-heading">6.2 时间性能</h3>

          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-value">约 1 秒</div>
              <div class="stat-label">平均求解时间</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">约 3 秒</div>
              <div class="stat-label">最坏情况</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">12×</div>
              <div class="stat-label">多线程加速</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">18-19</div>
              <div class="stat-label">平均步数</div>
            </div>
          </div>
        </div>

        <div class="content-card">
          <h3 class="subsection-heading">6.3 算法对比</h3>

          <div class="feature-table-wrapper">
            <table class="feature-table comparison">
              <thead>
                <tr>
                  <th>算法</th>
                  <th>阶段数</th>
                  <th>平均步数</th>
                  <th>计算速度</th>
                </tr>
              </thead>
              <tbody>
                <tr class="highlight-row">
                  <td><strong>Kociemba</strong></td>
                  <td>2 阶段</td>
                  <td>约 18-20 步</td>
                  <td>快（毫秒级）</td>
                </tr>
                <tr>
                  <td>Thistlethwaite</td>
                  <td>4 阶段</td>
                  <td>约 52 步</td>
                  <td>较慢</td>
                </tr>
                <tr>
                  <td>CFOP（人类）</td>
                  <td>4 阶段</td>
                  <td>约 50-60 步</td>
                  <td>极慢（人工）</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- 第7节：实践建议 -->
      <section id="practice" class="section-block" v-animate>
        <h2 class="section-heading">7. 实践建议</h2>

        <div class="content-card">
          <h3 class="subsection-heading">对于初学者</h3>

          <div class="practice-grid">
            <div class="practice-item">
              <h4>第一步：运行代码</h4>
              <p>先运行 solve() 函数，观察输出，建立直观感受</p>
            </div>
            <div class="practice-item">
              <h4>第二步：逐步调试</h4>
              <p>在 search() 和 search_phase2() 设置断点，跟踪执行流程</p>
            </div>
            <div class="practice-item">
              <h4>第三步：理解坐标</h4>
              <p>手动计算简单魔方状态的 twist、flip、slice 值</p>
            </div>
          </div>
        </div>

        <div class="content-card">
          <h3 class="subsection-heading">对于进阶学习者</h3>

          <div class="practice-grid">
            <div class="practice-item">
              <h4>绘制流程图</h4>
              <p>画出两阶段搜索的完整流程，标注关键决策点</p>
            </div>
            <div class="practice-item">
              <h4>手动跟踪</h4>
              <p>选择一个简单打乱（3-5步），手动跟踪代码执行</p>
            </div>
            <div class="practice-item">
              <h4>尝试优化</h4>
              <p>修改 max_length 和 timeout 参数，观察效果变化</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 第8节：常见问题 -->
      <section id="faq" class="section-block" v-animate>
        <h2 class="section-heading">8. 常见问题</h2>

        <div class="faq-list-container">
          <el-collapse
            v-model="activeFaq"
            accordion
            class="custom-modern-collapse"
          >
            <el-collapse-item
              v-for="(faq, index) in faqs"
              :key="faq.id"
              :name="faq.id"
              class="faq-item"
            >
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

      <!-- 第9节：参考资源 -->
      <section id="resources" class="section-block" v-animate>
        <h2 class="section-heading">9. 参考资源</h2>

        <div class="resource-grid">
          <a
            href="https://kociemba.org/cube.htm"
            target="_blank"
            class="resource-card"
          >
            <div class="resource-icon">🌐</div>
            <h4>Kociemba 官方网站</h4>
            <p>算法原作者的官方文档和 Cube Explorer 软件</p>
          </a>

          <a
            href="https://github.com/hkociemba/RubiksCube-TwophaseSolver"
            target="_blank"
            class="resource-card"
          >
            <div class="resource-icon">📦</div>
            <h4>GitHub 仓库</h4>
            <p>官方 Python 实现源码</p>
          </a>

          <a
            href="https://zhuanlan.zhihu.com/p/386717204"
            target="_blank"
            class="resource-card"
          >
            <div class="resource-icon">📖</div>
            <h4>知乎教程</h4>
            <p>中文深入浅出的算法讲解</p>
          </a>

          <div class="resource-card">
            <div class="resource-icon">📄</div>
            <h4>学术论文</h4>
            <p>The Two-Phase Algorithm by Herbert Kociemba（1992）</p>
          </div>
        </div>
      </section>

      <!-- 底部导航：继续探索 -->
      <section class="section-block navigation-section" v-animate>
        <h2 class="section-heading text-center">继续探索</h2>
        <div class="nav-cards">
          <router-link to="/tech/yolo" class="nav-card">
            <div class="nav-icon">👁️</div>
            <h3>YOLO 目标检测</h3>
            <p>计算机视觉魔方识别</p>
          </router-link>
          <router-link to="/tech/threejs" class="nav-card">
            <div class="nav-icon">🎮</div>
            <h3>Three.js 3D渲染</h3>
            <p>网页端实时3D魔方交互</p>
          </router-link>
          <router-link to="/tech/architecture" class="nav-card">
            <div class="nav-icon">🏗️</div>
            <h3>系统架构</h3>
            <p>前后端分离设计与数据流</p>
          </router-link>
        </div>
      </section>

      <!-- 返回顶部按钮 -->
      <button
        @click="scrollToTop"
        class="back-to-top-btn"
        :class="{ visible: showBackToTop }"
      >
        <el-icon><ArrowUp /></el-icon>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { ArrowLeft, ArrowUp } from "@element-plus/icons-vue";
import CodeBlock from "../components/CodeBlock.vue";

// 代码示例数据
const solverCode = `class SolverThread:
    def search(self, flip, twist, slice_sorted, dist, togo_phase1):
        if self.terminated.is_set():
            return
            
        if togo_phase1 == 0:  # 阶段一完成
            self.start_phase2()
            return
            
        for m in Move:  # 遍历18种移动
            # 应用移动，更新坐标
            flip_new = mv.flip_move[18 * flip + m]
            twist_new = mv.twist_move[18 * twist + m]
            slice_sorted_new = mv.slice_sorted_move[18 * slice_sorted + m]
            
            # 查询剪枝表，获取启发式距离
            dist_new = pr.get_distance(dist, flip_new, twist_new, slice_sorted_new)
            
            # 剪枝判断
            if dist_new >= togo_phase1:
                continue
            
            # 递归搜索
            self.sofar_phase1.append(m)
            self.search(flip_new, twist_new, slice_sorted_new, 
                       dist_new, togo_phase1 - 1)
            self.sofar_phase1.pop(-1)`;

const pruningCode = `def get_flipslice_twist_depth3(ix):
    """查询状态 ix 到目标的距离（mod 3）"""
    # 定位到包含该状态的 uint32
    y = flipslice_twist_depth3[ix // 16]
    
    # 右移到正确位置（每个状态占2bit）
    y >>= (ix % 16) * 2
    
    # 提取2bit的值（0-3）
    return y & 3

# 压缩效果：
# 未压缩：约 140,893,410 状态 × 1 字节 = 约 134 MB
# 压缩后：约 140,893,410 ÷ 16 × 4 字节 = 约 33.6 MB
# 节省空间：约 75%`;

const cubieCode = `class CubieCube:
    """魔方块层次表示"""
    def __init__(self, cp=None, co=None, ep=None, eo=None):
        # 角块位置（Corner Permutation）
        self.cp = cp or [Co(i) for i in range(8)]
        
        # 角块方向（Corner Orientation）：0/1/2
        self.co = co or [0] * 8
        
        # 棱块位置（Edge Permutation）
        self.ep = ep or [Ed(i) for i in range(12)]
        
        # 棱块方向（Edge Orientation）：0/1
        self.eo = eo or [0] * 12
    
    def corner_multiply(self, other):
        """角块乘法：状态转移"""
        for i in range(8):
            self.co[i] = (self.co[i] + other.co[self.cp[i]]) % 3
            self.cp[i] = other.cp[self.cp[i]]`;

const defsCode = `# 阶段一状态空间
N_TWIST = 2187           # 3^7 角块方向数
N_FLIP = 2048            # 2^11 棱块方向数
N_SLICE_SORTED = 11880   # 12×11×10×9 中层棱块位置数

# 阶段二状态空间
N_CORNERS = 40320        # 8! 角块排列数
N_UD_EDGES = 40320       # 8! UD棱块排列数

# 对称性约减
N_FLIPSLICE_CLASS = 64430  # 对称性约减后的类数
N_CORNERS_CLASS = 2768     # 对称性约减后的类数
N_SYM_D4h = 16             # D4h对称群数量`;

const phase1SearchCode = `for m in Move:  # 遍历18种移动
    # 1. 应用移动，更新坐标
    flip_new = mv.flip_move[18 * flip + m]
    twist_new = mv.twist_move[18 * twist + m]
    slice_sorted_new = mv.slice_sorted_move[18 * slice_sorted + m]
    
    # 2. 计算 flipslice 索引
    flipslice = 2048 * (slice_sorted_new // 24) + flip_new
    classidx = sy.flipslice_classidx[flipslice]
    sym = sy.flipslice_sym[flipslice]
    
    # 3. 查询剪枝表，获取启发式距离
    dist_new_mod3 = pr.get_flipslice_twist_depth3(
        2187 * classidx + sy.twist_conj[(twist_new << 4) + sym]
    )
    dist_new = pr.distance[3 * dist + dist_new_mod3]
    
    # 4. 剪枝判断
    if dist_new >= togo_phase1:
        continue
    
    # 5. 递归搜索
    self.sofar_phase1.append(m)
    self.search(flip_new, twist_new, slice_sorted_new, 
               dist_new, togo_phase1 - 1)
    self.sofar_phase1.pop(-1)`;

const bitCompressionCode = `def get_flipslice_twist_depth3(ix):
    """查询状态 ix 到目标的距离（mod 3）"""
    y = flipslice_twist_depth3[ix // 16]  # 定位uint32
    y >>= (ix % 16) * 2                    # 右移（2bit/状态）
    return y & 3                           # 提取值

# 存储效率对比：
# ┌─────────────┬────────────┬──────────┐
# │    类型     │   原始大小  │  压缩后   │
# ├─────────────┼────────────┼──────────┤
# │ 阶段一剪枝表 │   约 134 MB │  34 MB   │
# │ 阶段二剪枝表 │   约 106 MB │  27 MB   │
# │ 总计        │   约 240 MB │  61 MB   │
# └─────────────┴────────────┴──────────┘
# 节省空间：约 75%`;

const multithreadCode = `# 启动 6 个线程并行搜索
for i in range(6):
    # rot: 0=0°, 1=120°, 2=240°
    # inv: 0=正向, 1=逆向
    rot, inv = i % 3, i // 3
    
    th = SolverThread(
        cc, rot, inv, 
        max_length, timeout, 
        s_time, solutions, 
        terminated, shortest_length
    )
    my_threads.append(th)
    th.start()

# 等待所有线程完成
for t in my_threads:
    t.join()

# 返回最短解法
if len(solutions) > 0:
    return min(solutions, key=len)`;

const router = useRouter();
const showBackToTop = ref(false);
const activeSection = ref("");
const activeFaq = ref("");

// 学习路径数据
const learningStages = ref([
  {
    icon: "📚",
    title: "阶段一：基础概念",
    duration: "1-2 天",
    path: "阅读顺序：enums.py → defs.py → cubie.py（前 100 行）",
    items: [
      "理解魔方的三种表示：Facelet、Cubie、Coordinate",
      "掌握角块/棱块方向定义（为什么是 3^7 和 2^11）",
      "学习基本移动的数学表示（置换群）",
    ],
  },
  {
    icon: "⚙️",
    title: "阶段二：核心算法",
    duration: "3-5 天",
    path: "阅读顺序：coord.py → moves.py → pruning.py → solver.py",
    items: [
      "理解坐标编码与状态映射",
      "掌握移动表的预计算原理",
      "学习剪枝表的生成与查询",
      "理解 IDA* 两阶段搜索流程",
    ],
  },
  {
    icon: "🚀",
    title: "阶段三：优化技术",
    duration: "2-3 天",
    path: "阅读顺序：symmetries.py（对称性处理）",
    items: [
      "理解魔方的 48 种对称操作",
      "学习对称性约减的原理",
      "掌握等价类（Equivalence Class）的概念",
    ],
  },
]);

// FAQ 数据
const faqs = ref([
  {
    id: "1",
    title: "为什么剪枝表只存储 mod 3 的距离？",
    content:
      "为了节省存储空间。每个状态只需 2 bit（存储 0/1/2），通过 distance 数组可以还原真实距离。这样相比 1 字节存储节省约 4 倍空间。",
  },
  {
    id: "2",
    title: "为什么使用 6 个线程而不是更多？",
    content:
      "3 个方向（0°、120°、240°）× 正逆各 1 次 = 6 个线程。更多线程收益递减，且受 Python GIL 限制。",
  },
  {
    id: "3",
    title: "如何理解「对称性约减」？",
    content:
      "魔方有 48 种对称操作（旋转、镜像）。对称状态下，解法步数相同。将等价状态归为一类，状态数从约 4.3×10^19 降至可管理的规模。",
  },
  {
    id: "4",
    title: "位压缩技术如何节省存储空间？",
    content:
      "使用 uint32 数组，每个元素存储 16 个状态（每个 2 bit）。通过位操作（右移、与运算）实现 O(1) 查询，节省约 75% 空间。",
  },
]);

// 章节配置
const sections = ref([
  { id: "background", title: "算法背景" },
  { id: "file-structure", title: "文件结构" },
  { id: "core-files", title: "核心文件" },
  { id: "learning-path", title: "学习路径" },
  { id: "code-analysis", title: "代码解析" },
  { id: "performance", title: "性能分析" },
  { id: "practice", title: "实践建议" },
  { id: "faq", title: "常见问题" },
  { id: "resources", title: "参考资源" },
]);

// 返回 About 页面
const goBackToAbout = () => {
  router.push({ path: "/about", state: { scrollTarget: "tech-docs" } });
};

// 滚动到指定章节
const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId);
  if (element) {
    const offset = 100;
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - offset;

    window.scrollTo({
      top: offsetPosition,
      behavior: "smooth",
    });
  }
};

// 返回顶部
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
};

// 监听滚动
const handleScroll = () => {
  showBackToTop.value = window.scrollY > 300;

  // 更新当前章节
  const sectionIds = sections.value.map((s) => s.id);
  for (let i = sectionIds.length - 1; i >= 0; i--) {
    const element = document.getElementById(sectionIds[i]);
    if (element && element.offsetTop <= window.scrollY + 150) {
      activeSection.value = sectionIds[i];
      break;
    }
  }
};

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
}

.page-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 24px;
}

/* 动画 */
.before-enter {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.enter {
  opacity: 1;
  transform: translateY(0);
}

/* 面包屑导航 */
.tech-doc-header {
  padding-top: 30px;
  margin-bottom: 20px;
}

.minimal-back-btn {
  background: none;
  border: none;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  margin-bottom: 16px;
  transition: color 0.3s;
}

.minimal-back-btn:hover {
  color: #3b82f6;
}

.breadcrumb-nav {
  margin-bottom: 20px;
}

.breadcrumb-links {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.breadcrumb-link {
  display: inline-block;
  padding: 6px 14px;
  background: #f1f5f9;
  color: #64748b;
  font-size: 13px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
}

.breadcrumb-link:hover {
  background: #e2e8f0;
  color: #334155;
}

.breadcrumb-link.active {
  background: #3b82f6;
  color: white;
}

/* Hero Section */
.hero-section {
  position: relative;
  padding: 60px 0;
  margin-bottom: 60px;
  border-radius: 24px;
  overflow: hidden;
}

.glow-bg {
  position: absolute;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
}

.glow-top-right {
  top: -100px;
  right: -100px;
  background: #3b82f6;
}

.glow-bottom-left {
  bottom: -100px;
  left: -100px;
  background: #8b5cf6;
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
}

.badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  border-radius: 100px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 24px;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background: #3b82f6;
  border-radius: 50%;
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
  margin-bottom: 20px;
  color: #0f172a;
  text-align: center;
}

.gradient-text {
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #64748b;
  max-width: 700px;
  margin: 0 auto 32px;
  line-height: 1.6;
  text-align: center;
}

.stats-pills {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
}

.stat-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: white;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
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

/* Section */
.section-block {
  margin-bottom: 80px;
}

.section-heading {
  font-size: 2rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 32px;
  text-align: left;
}

.subsection-heading {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 28px 0 16px;
  text-align: left;
}

/* 内容卡片 */
.content-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  text-align: left;
}

.paragraph {
  color: #475569;
  line-height: 1.7;
  margin-bottom: 16px;
  text-align: left;
}

.paragraph strong {
  color: #1e293b;
}

.paragraph.highlight {
  color: #1e293b;
  font-weight: 500;
}

/* 列表 */
.feature-list {
  list-style: none;
  padding: 0;
  margin: 0 0 20px;
}

.feature-list li {
  position: relative;
  padding-left: 20px;
  margin-bottom: 10px;
  color: #475569;
  line-height: 1.6;
}

.feature-list li::before {
  content: "→";
  position: absolute;
  left: 0;
  color: #3b82f6;
  font-weight: 600;
}

.checklist {
  list-style: none;
  padding: 0;
  margin: 0;
}

.checklist li {
  position: relative;
  padding-left: 24px;
  margin-bottom: 10px;
  color: #475569;
}

.checklist li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #10b981;
  font-weight: 700;
}

/* 代码块文本 */
.code-block-text {
  background: #f8fafc;
  border-left: 3px solid #3b82f6;
  padding: 16px 20px;
  font-family: "JetBrains Mono", monospace;
  font-size: 14px;
  color: #334155;
  line-height: 1.8;
  white-space: pre-wrap;
  margin: 16px 0;
  text-align: left;
}

/* 表格 */
.feature-table-wrapper {
  overflow-x: auto;
  margin: 20px 0;
}

.feature-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 15px;
}

.feature-table th {
  text-align: center;
  padding: 14px 16px;
  background: #f8fafc;
  color: #1e293b;
  font-weight: 600;
  border-bottom: 2px solid #e2e8f0;
}

.feature-table td {
  text-align: center;
  padding: 14px 16px;
  border-bottom: 1px solid #e2e8f0;
  color: #475569;
}

.feature-table tr:hover td {
  background: #f8fafc;
}

.feature-table code {
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: "JetBrains Mono", monospace;
  font-size: 13px;
  color: #334155;
}

/* 标签列表 */
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  display: inline-block;
  padding: 6px 12px;
  background: #f1f5f9;
  color: #64748b;
  font-size: 13px;
  border-radius: 6px;
}

/* 文件头部 */
.file-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.file-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.file-icon-text {
  color: white;
  font-size: 13px;
  font-weight: 700;
}

.file-title-group h3 {
  font-size: 1.4rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 4px;
}

.file-meta {
  color: #64748b;
  font-size: 14px;
}

/* 方法列表 */
.method-list {
  margin: 20px 0;
}

.method-list h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 12px;
}

.method-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.method-list li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
}

.method-list li:last-child {
  border-bottom: none;
}

.method-list code {
  background: #eff6ff;
  color: #3b82f6;
  padding: 2px 8px;
  border-radius: 4px;
  font-family: "JetBrains Mono", monospace;
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
}

.method-list span {
  color: #64748b;
  font-size: 14px;
}

/* 阶段标题 */
.phase-section h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 24px 0 12px;
  text-align: left;
}

/* 学习路径时间线 - Roadmap 风格 */
.roadmap-wrapper {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  padding-left: 40px;
}

/* 贯穿线 */
.roadmap-line {
  position: absolute;
  left: 19px;
  top: 20px;
  bottom: 20px;
  width: 2px;
  background: #e2e8f0;
  z-index: 0;
}

.roadmap-node {
  position: relative;
  margin-bottom: 40px;
}

.roadmap-node:last-child {
  margin-bottom: 0;
}

.node-marker {
  position: absolute;
  left: -40px;
  top: 24px;
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

/* 悬浮动效 */
.roadmap-node:hover .marker-circle {
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
.roadmap-node:hover .node-card {
  border-color: #3b82f6;
  transform: translateX(10px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
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
  opacity: 0.7;
  transition: opacity 0.3s;
}

.roadmap-node:hover .header-right {
  opacity: 1;
}

.card-body p {
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 16px;
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

.reading-path {
  background: #f8fafc;
  padding: 10px 14px;
  border-radius: 6px;
  font-family: "JetBrains Mono", monospace;
  font-size: 13px;
  color: #475569;
  margin-bottom: 16px;
}

/* 统计网格 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 16px;
  margin: 24px 0;
}

.stat-card {
  background: #f8fafc;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
}

.stat-card.highlight {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.stat-card.highlight .stat-value,
.stat-card.highlight .stat-label {
  color: white;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
}

/* 信息框 */
.info-box {
  border-radius: 12px;
  padding: 20px;
  margin: 24px 0;
}

.info-box.success {
  background: #f0fdf4;
  border-left: 4px solid #10b981;
}

.info-box h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 12px;
}

.info-box p {
  color: #475569;
  margin-bottom: 12px;
}

.info-box ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.info-box li {
  color: #475569;
  margin-bottom: 6px;
  padding-left: 16px;
  position: relative;
}

.info-box li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #10b981;
  font-weight: 700;
}

/* 实践网格 */
.practice-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.practice-item {
  background: #f8fafc;
  border-radius: 10px;
  padding: 20px;
  border-left: 3px solid #3b82f6;
}

.practice-item h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 8px;
}

.practice-item p {
  color: #64748b;
  font-size: 14px;
  margin: 0;
}

/* FAQ 手风琴样式 */
.faq-list-container {
  max-width: 800px;
  margin: 0 auto;
}

/* 深度重塑 Element Collapse */
.custom-modern-collapse {
  border: none !important;
}

/* 每一个折叠项 */
:deep(.el-collapse-item) {
  margin-bottom: 10px;
  border-radius: 16px;
  transition: all 0.3s ease;
  overflow: hidden;
  border-bottom: 1px solid #f1f5f9 !important;
}

/* 悬停效果 */
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
  color: #cbd5e1;
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
  color: #2563eb;
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

/* 资源网格 */
.resource-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.resource-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.2s;
}

.resource-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.resource-icon {
  font-size: 1.8rem;
  margin-bottom: 12px;
}

.resource-card h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 6px;
}

.resource-card p {
  color: #64748b;
  font-size: 13px;
  margin: 0;
}

/* 返回顶部按钮 */
.back-to-top-btn {
  position: fixed;
  bottom: 32px;
  right: 32px;
  width: 48px;
  height: 48px;
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
  transition: all 0.3s;
  z-index: 1000;
}

.back-to-top-btn.visible {
  opacity: 1;
  transform: translateY(0);
}

.back-to-top-btn:hover {
  background: #2563eb;
  transform: translateY(-2px);
}

/* 对比表格高亮行 */
.highlight-row {
  background: #eff6ff;
}

.highlight-row td {
  color: #1e40af;
}

/* 底部导航 */
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

.text-center {
  text-align: center;
}

/* 响应式 */
@media (max-width: 768px) {
  .page-container {
    padding: 0 16px;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .section-heading {
    font-size: 1.5rem;
  }

  .content-card {
    padding: 20px;
  }

  .breadcrumb-links {
    gap: 6px;
  }

  .breadcrumb-link {
    padding: 4px 10px;
    font-size: 12px;
  }

  .back-to-top-btn {
    bottom: 20px;
    right: 20px;
    width: 44px;
    height: 44px;
  }
}

/* ==================== 暗色模式 ==================== */
[data-theme="dark"] .tech-doc-page {
  background-color: #0f172a;
  color: #f1f5f9;
}

[data-theme="dark"] .hero-title,
[data-theme="dark"] .section-heading,
[data-theme="dark"] .subsection-heading,
[data-theme="dark"] .file-title-group h3,
[data-theme="dark"] .timeline-content h3,
[data-theme="dark"] .faq-question h4,
[data-theme="dark"] .resource-card h4 {
  color: #f1f5f9;
}

[data-theme="dark"] .content-card,
[data-theme="dark"] .timeline-content,
[data-theme="dark"] .stat-card,
[data-theme="dark"] .faq-item,
[data-theme="dark"] .resource-card {
  background: #1e293b;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

[data-theme="dark"] .paragraph,
[data-theme="dark"] .feature-list li,
[data-theme="dark"] .checklist li,
[data-theme="dark"] .method-list span,
[data-theme="dark"] .timeline-duration,
[data-theme="dark"] .stat-label,
[data-theme="dark"] .info-box p,
[data-theme="dark"] .info-box li,
[data-theme="dark"] .practice-item p,
[data-theme="dark"] .faq-answer,
[data-theme="dark"] .resource-card p {
  color: #94a3b8;
}

[data-theme="dark"] .code-block-text {
  background: #1e293b;
  color: #cbd5e1;
}

[data-theme="dark"] .feature-table th {
  background: #334155;
  color: #f1f5f9;
  border-bottom-color: #475569;
}

[data-theme="dark"] .feature-table td {
  border-bottom-color: #334155;
  color: #cbd5e1;
}

[data-theme="dark"] .feature-table tr:hover td {
  background: #334155;
}

[data-theme="dark"] .tag {
  background: #334155;
  color: #94a3b8;
}

[data-theme="dark"] .breadcrumb-link {
  background: #334155;
  color: #94a3b8;
}

[data-theme="dark"] .breadcrumb-link:hover {
  background: #475569;
  color: #cbd5e1;
}

[data-theme="dark"] .breadcrumb-link.active {
  background: #3b82f6;
  color: white;
}

[data-theme="dark"] .reading-path {
  background: #334155;
  color: #cbd5e1;
}

[data-theme="dark"] .practice-item,
[data-theme="dark"] .info-box.success {
  background: #334155;
}

[data-theme="dark"] .info-box.success li::before {
  color: #34d399;
}

[data-theme="dark"] .method-list code {
  background: #1e3a8a;
  color: #60a5fa;
}

[data-theme="dark"] .feature-table code {
  background: #334155;
  color: #cbd5e1;
}

[data-theme="dark"] .highlight-row {
  background: #1e3a8a;
}

[data-theme="dark"] .highlight-row td {
  color: #93c5fd;
}

[data-theme="dark"] .stat-card {
  background: #334155;
}

[data-theme="dark"] .stat-card .stat-value {
  color: #f1f5f9;
}

[data-theme="dark"] .minimal-back-btn {
  color: #94a3b8;
}

[data-theme="dark"] .minimal-back-btn:hover {
  color: #60a5fa;
}

[data-theme="dark"] .hero-subtitle {
  color: #94a3b8;
}

[data-theme="dark"] .file-meta {
  color: #64748b;
}

[data-theme="dark"] .phase-section h4 {
  color: #f1f5f9;
}

[data-theme="dark"] .pulse-dot {
  background: #60a5fa;
}

[data-theme="dark"] .badge-pill {
  background: rgba(96, 165, 250, 0.1);
  color: #60a5fa;
}

[data-theme="dark"] .stat-pill {
  background: #1e293b;
  color: #cbd5e1;
}

[data-theme="dark"] .dot-indicator.blue {
  background: #60a5fa;
}

[data-theme="dark"] .dot-indicator.green {
  background: #34d399;
}

[data-theme="dark"] .dot-indicator.purple {
  background: #a78bfa;
}

/* 学习路径时间线深色模式 */
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

[data-theme="dark"] .roadmap-node:hover .node-card {
  border-color: var(--dm-accent);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .step-title {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .header-right {
  color: var(--dm-accent);
}

[data-theme="dark"] .meta-tag {
  background: var(--dm-bg-hover);
  color: var(--dm-text-muted);
}

[data-theme="dark"] .meta-tag.highlight {
  background: rgba(59, 130, 246, 0.15);
  color: var(--dm-accent);
}

/* FAQ 深色模式 */
[data-theme="dark"] .faq-index {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .faq-question {
  color: var(--dm-text-primary);
}

html[data-theme="dark"] :deep(.el-collapse-item) {
  border-bottom-color: var(--dm-border) !important;
  transition: all 0.3s ease;
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

/* 底部导航深色模式 */
[data-theme="dark"] .nav-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
  box-shadow: var(--dm-shadow-md);
}

[data-theme="dark"] .nav-card:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
  border-color: var(--dm-accent);
}

[data-theme="dark"] .nav-card h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .nav-card p {
  color: var(--dm-text-muted);
}
</style>
