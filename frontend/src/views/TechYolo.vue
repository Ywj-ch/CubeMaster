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
            YOLO 目标检测<br />
            <span class="gradient-text">从论文精读到工程实践</span>
          </h1>

          <p class="hero-subtitle">
            深入理解 YOLOv1 算法原理，结合 CubeMaster 魔方识别项目展示完整实现
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
              <span>训练数据：200张标注图像</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Research Background & Motivation -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">研究背景与动机</h2>
        <div class="research-background-card">
          <div class="background-content">
            <h3>
              <span class="background-icon">🔄</span> 传统目标检测方法的瓶颈
            </h3>
            <p>
              <strong>两阶段检测器（如 R-CNN 系列 / DPM）</strong>：
              需要先提取候选区域（Region
              Proposals），再进行分类，最后进行非极大值抑制（NMS）和边界框微调。
            </p>
            <p>
              <strong>主要缺点</strong
              >：流程复杂（多阶段），各个组件需要单独训练，导致<strong>检测速度慢</strong>，难以满足实时应用需求。
            </p>

            <h3><span class="background-icon">🚀</span> YOLO 的革命性突破</h3>
            <p>
              <strong>核心思想</strong
              >：去除繁琐的候选框提取步骤，直接将整张图输入一个单独的卷积神经网络（CNN），实现<strong>统一的、实时的</strong>目标检测框架。
            </p>
            <p>
              <strong>论文标题</strong>：<em
                >You Only Look Once: Unified, Real-Time Object Detection</em
              >
              (CVPR 2016)
            </p>
            <p>
              <strong>一句话总结</strong
              >：“你只需要看一次”——将目标检测任务从传统的“分类问题”巧妙地转换为一个<strong>单一的端到端回归问题</strong>，直接从完整图像中一次性预测出边界框的位置和类别概率。
            </p>
          </div>
        </div>
      </section>

      <!-- YOLOv1 Core Principles -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">YOLOv1 核心原理</h2>
        <div class="core-principles-card">
          <div class="principles-grid">
            <div class="principle-item">
              <div class="principle-icon">🔲</div>
              <h3>网格划分 (Grid Cell)</h3>
              <p>
                将输入图像（448 × 448）划分为 <strong>S × S</strong>（默认
                S=7）的网格。 如果一个物体的<strong>中心点</strong>落入某个 Grid
                Cell 内，该 Grid Cell 就负责检测该物体。
              </p>
            </div>
            <div class="principle-item">
              <div class="principle-icon">📊</div>
              <h3>预测张量 (Output Tensor)</h3>
              <p>
                每个 Grid Cell 预测 <strong>B</strong> 个边界框（默认
                B=2）及其置信度，外加 <strong>C</strong> 个类别概率（VOC
                数据集中 C=20）。 输出维度：<strong>S × S × (B × 5 + C)</strong>
              </p>
            </div>
            <div class="principle-item">
              <div class="principle-icon">🎯</div>
              <h3>置信度定义</h3>
              <p>
                置信度 =
                <strong>Pr(Object) × IOU<sub>pred</sub><sup>truth</sup></strong>
                <br />即：物体存在概率 × 预测框与真实框的交并比。
              </p>
            </div>
            <div class="principle-item">
              <div class="principle-icon">📈</div>
              <h3>分类得分计算</h3>
              <p>测试阶段最终得分：</p>
              <div class="formula-inline">
                <code
                  >Pr(Class<sub>i</sub>|Object) × Pr(Object) × IOU<sub>pred</sub
                  ><sup>truth</sup></code
                >
                <span class="formula-eq">=</span>
                <code
                  >Pr(Class<sub>i</sub>) × IOU<sub>pred</sub
                  ><sup>truth</sup></code
                >
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Network Architecture -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">网络架构</h2>
        <div class="architecture-card">
          <div class="architecture-image-full">
            <img
              src="/images/yolov1-architecture.png"
              alt="YOLOv1 网络结构图"
              class="architecture-image"
              @click="openImagePreview('/images/yolov1-architecture.png')"
              style="cursor: pointer"
            />
            <div class="image-caption">图3: YOLOv1 网络结构 (CVPR 2016)</div>
          </div>
          <div class="architecture-details-grid">
            <div class="architecture-detail-item">
              <h3><span class="detail-icon">🧠</span> 架构特点</h3>
              <ul>
                <li><strong>灵感来源</strong>：基于 GoogLeNet 修改</li>
                <li><strong>层数构成</strong>：24 层卷积 + 2 层全连接</li>
                <li><strong>激活函数</strong>：Leaky ReLU（α=0.1）</li>
                <li><strong>Fast YOLO</strong>：9 层卷积，155 FPS</li>
              </ul>
            </div>
            <div class="architecture-detail-item">
              <h3><span class="detail-icon">⚙️</span> 输出层设计</h3>
              <p>PASCAL VOC 数据集（S=7, B=2, C=20）最终输出：</p>
              <p class="output-tensor"><strong>7 × 7 × 30</strong> 张量</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Loss Function -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">损失函数详解</h2>
        <div class="loss-function-card">
          <div class="loss-function-content">
            <h3><span class="formula-icon">📐</span> 损失函数组成</h3>
            <p>
              YOLOv1 将检测视为回归问题，采用<strong>均方差误差</strong>。
              引入权重参数平衡不同误差：
              <strong>λ<sub>coord</sub>=5</strong>（坐标权重）、
              <strong>λ<sub>noobj</sub>=0.5</strong>（背景抑制）。
            </p>

            <div class="formula-total-box">
              <h4>完整损失函数</h4>
              <div class="formula-total">
                <div class="formula-line">
                  <span class="formula-var">Loss</span>
                  <span class="formula-eq">=</span>
                  <span class="formula-expr"
                    >λ<sub>coord</sub> × Σ[(x - x̂)² + (y - ŷ)²]</span
                  >
                </div>
                <div class="formula-line indent">
                  <span class="formula-plus">+</span>
                  <span class="formula-expr"
                    >λ<sub>coord</sub> × Σ[(√w - √ŵ)² + (√h - √ĥ)²]</span
                  >
                </div>
                <div class="formula-line indent">
                  <span class="formula-plus">+</span>
                  <span class="formula-expr">Σ(C - Ĉ)²</span>
                </div>
                <div class="formula-line indent">
                  <span class="formula-plus">+</span>
                  <span class="formula-expr"
                    >λ<sub>noobj</sub> × Σ(C - Ĉ)²</span
                  >
                </div>
                <div class="formula-line indent">
                  <span class="formula-plus">+</span>
                  <span class="formula-expr">ΣΣ(p(c) - p̂(c))²</span>
                </div>
              </div>
            </div>

            <div class="formula-details">
              <h4>各部分详解</h4>
              <div class="formula-parts">
                <div class="formula-part">
                  <span class="part-num">1</span>
                  <div class="part-content">
                    <span class="part-label">中心点坐标误差</span>
                    <code class="part-formula"
                      >λ_coord × Σ[(x - x̂)² + (y - ŷ)²]</code
                    >
                  </div>
                </div>
                <div class="formula-part">
                  <span class="part-num">2</span>
                  <div class="part-content">
                    <span class="part-label">边界框宽高误差</span>
                    <code class="part-formula"
                      >λ_coord × Σ[(√w - √ŵ)² + (√h - √ĥ)²]</code
                    >
                  </div>
                </div>
                <div class="formula-part">
                  <span class="part-num">3</span>
                  <div class="part-content">
                    <span class="part-label">含物体置信度误差</span>
                    <code class="part-formula">Σ(C - Ĉ)²</code>
                  </div>
                </div>
                <div class="formula-part">
                  <span class="part-num">4</span>
                  <div class="part-content">
                    <span class="part-label">无物体置信度误差</span>
                    <code class="part-formula">λ_noobj × Σ(C - Ĉ)²</code>
                  </div>
                </div>
                <div class="formula-part">
                  <span class="part-num">5</span>
                  <div class="part-content">
                    <span class="part-label">类别预测误差</span>
                    <code class="part-formula">ΣΣ(p(c) - p̂(c))²</code>
                  </div>
                </div>
              </div>
            </div>

            <div class="formula-notes">
              <h4>💡 关键设计解析</h4>
              <ul>
                <li>
                  <strong>宽高开根号</strong
                  >：对小框误差惩罚更大，避免对小物体不公平
                </li>
                <li>
                  <strong>λ_noobj = 0.5</strong
                  >：抑制大量背景产生的压倒性梯度，防止模型发散
                </li>
                <li>
                  <strong>指示函数 𝕀^obj</strong
                  >：表示预测框是否对真实物体"负责"（IOU最大）
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- Advantages & Limitations -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">YOLOv1 优缺点分析</h2>
        <div class="advantages-limitations-card">
          <div class="advantages-section">
            <h3><span class="advantage-icon">✅</span> 优势</h3>
            <div class="advantage-grid">
              <div class="advantage-item">
                <h4>速度极快 (Extremely Fast)</h4>
                <p>
                  基础版 45 FPS，Fast 版本 155 FPS，非常适合实时视频流检测。
                </p>
              </div>
              <div class="advantage-item">
                <h4>全局感受野 (Global Reasoning)</h4>
                <p>
                  与基于局部区域的方法不同，YOLO
                  每次观测完整图像，包含丰富上下文信息，背景误检率不到 Fast
                  R-CNN 的一半。
                </p>
              </div>
              <div class="advantage-item">
                <h4>泛化能力强 (Generalizable)</h4>
                <p>
                  学到了物体的通用特征，当从自然图像迁移到艺术品等其他领域时，表现远超
                  DPM 和 R-CNN。
                </p>
              </div>
            </div>
          </div>

          <div class="limitations-section">
            <h3><span class="limitation-icon">❌</span> 局限性</h3>
            <div class="limitation-grid">
              <div class="limitation-item">
                <h4>强空间限制</h4>
                <p>
                  每个 Grid Cell 只能预测 2 个框且只能属于 1
                  个类别，难以检测密集小物体（鸟群、人群）。
                </p>
              </div>
              <div class="limitation-item">
                <h4>不寻常比例物体</h4>
                <p>对训练集未见过的异常长宽比物体，定位效果差。</p>
              </div>
              <div class="limitation-item">
                <h4>定位误差大</h4>
                <p>
                  这是 YOLOv1 的主要错误来源，虽然 Loss
                  中加入了开根号处理，但依然无法完美解决大框与小框误差权重分配问题。
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Evolution Path -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">从 YOLOv1 到 YOLOv8 演进</h2>
        <div class="evolution-timeline-wrapper">
          <!-- 贯穿线 -->
          <div class="evolution-line"></div>

          <div class="evolution-timeline">
            <div class="evolution-node">
              <div class="evolution-marker">
                <div class="evolution-circle">1</div>
              </div>
              <div class="evolution-content">
                <div class="evolution-card-item">
                  <div class="evolution-header">
                    <span class="evolution-year">2016</span>
                    <h3>YOLOv1：开创单阶段检测</h3>
                  </div>
                  <div class="evolution-body">
                    <p>
                      摒弃 Region
                      Proposal，直接利用全图信息回归，思想上的巨大飞跃。
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div class="evolution-node">
              <div class="evolution-marker">
                <div class="evolution-circle">2</div>
              </div>
              <div class="evolution-content">
                <div class="evolution-card-item">
                  <div class="evolution-header">
                    <span class="evolution-year">2017</span>
                    <h3>YOLOv2 (YOLO9000)</h3>
                  </div>
                  <div class="evolution-body">
                    <p>
                      引入 Anchor Boxes、多尺度训练、Darknet-19
                      骨干网络，显著提升精度。
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div class="evolution-node">
              <div class="evolution-marker">
                <div class="evolution-circle">3</div>
              </div>
              <div class="evolution-content">
                <div class="evolution-card-item">
                  <div class="evolution-header">
                    <span class="evolution-year">2018</span>
                    <h3>YOLOv3</h3>
                  </div>
                  <div class="evolution-body">
                    <p>
                      多尺度特征金字塔（FPN）、更深的
                      Darknet-53、更好的小目标检测。
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div class="evolution-node">
              <div class="evolution-marker">
                <div class="evolution-circle">4</div>
              </div>
              <div class="evolution-content">
                <div class="evolution-card-item">
                  <div class="evolution-header">
                    <span class="evolution-year">2020</span>
                    <h3>YOLOv4/v5/v6/v7/v8</h3>
                  </div>
                  <div class="evolution-body">
                    <p>
                      持续优化：Bag of Freebies、Anchor-Free
                      设计、模型轻量化、实时性能提升。
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="evolution-summary-box">
            <h3>
              <span class="summary-icon">🔮</span> CubeMaster 中的 YOLOv8 应用
            </h3>
            <p>
              项目选用 <strong>YOLOv8n (Nano)</strong> 版本，平衡了精度与速度，
              针对魔方色块小目标检测进行了专门优化，并结合 HSV
              颜色空间分析提升颜色识别鲁棒性。
            </p>
          </div>
        </div>
      </section>

      <!-- Workflow Diagram -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">CubeMaster 检测工作流程</h2>
        <div class="workflow-horizontal">
          <div class="workflow-step-h">
            <div class="step-icon">📷</div>
            <div class="step-info">
              <span class="step-num">01</span>
              <h4>图像采集</h4>
              <p>拍摄魔方六面</p>
            </div>
          </div>
          <div class="workflow-arrow">→</div>
          <div class="workflow-step-h">
            <div class="step-icon">🔧</div>
            <div class="step-info">
              <span class="step-num">02</span>
              <h4>预处理</h4>
              <p>640×640 + 归一化</p>
            </div>
          </div>
          <div class="workflow-arrow">→</div>
          <div class="workflow-step-h">
            <div class="step-icon">🤖</div>
            <div class="step-info">
              <span class="step-num">03</span>
              <h4>YOLOv8推理</h4>
              <p>9色块检测</p>
            </div>
          </div>
          <div class="workflow-arrow">→</div>
          <div class="workflow-step-h">
            <div class="step-icon">📊</div>
            <div class="step-info">
              <span class="step-num">04</span>
              <h4>空间排序</h4>
              <p>3×3矩阵映射</p>
            </div>
          </div>
          <div class="workflow-arrow">→</div>
          <div class="workflow-step-h">
            <div class="step-icon">✅</div>
            <div class="step-info">
              <span class="step-num">05</span>
              <h4>状态验证</h4>
              <p>可解性检查</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Training Details -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">CubeMaster 模型训练</h2>
        <div class="training-details">
          <div class="detail-card">
            <h3><span class="detail-icon">📊</span> 数据集构成</h3>
            <ul>
              <li>
                <strong>200 张标注图像</strong>：涵盖不同光照、角度、背景条件
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
        <h2 class="section-heading">CubeMaster 后端集成</h2>
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
            <h4>关键设计决策</h4>
            <ul>
              <li><strong>批处理优化</strong>：六个面图像一次性送入模型</li>
              <li><strong>缓存机制</strong>：模型加载后常驻内存</li>
              <li><strong>错误恢复</strong>：检测失败时自动HSV回退</li>
              <li><strong>异步支持</strong>：FastAPI异步端点高并发响应</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Challenges & Solutions -->
      <section class="section-block" v-animate>
        <h2 class="section-heading">CubeMaster 挑战与解决方案</h2>
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

    <!-- 图片预览模态框 -->
    <div v-if="showImageModal" class="image-modal" @click="closeImagePreview">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closeImagePreview">×</button>
        <img :src="currentImageSrc" alt="预览图片" class="modal-image" />
        <div class="image-caption-modal">YOLOv1 网络结构 (CVPR 2016)</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useRouter } from "vue-router";
import { ArrowLeft, ArrowUp } from "@element-plus/icons-vue";

const router = useRouter();
const showBackToTop = ref(false);
const showImageModal = ref(false);
const currentImageSrc = ref("");

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

// 图片预览功能
const openImagePreview = (src) => {
  currentImageSrc.value = src;
  showImageModal.value = true;
  document.body.style.overflow = "hidden";
};

const closeImagePreview = () => {
  showImageModal.value = false;
  document.body.style.overflow = "";
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

/* 横向工作流程 */
.workflow-horizontal {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
  background: #ffffff;
  border-radius: 24px;
  padding: 30px 20px;
  border: 1px solid #e2e8f0;
}

.workflow-step-h {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  background: #f8fafc;
  border-radius: 12px;
  padding: 16px 12px;
  min-width: 100px;
  transition: all 0.3s ease;
}

.workflow-step-h:hover {
  background: #eff6ff;
  transform: translateY(-2px);
}

.step-icon {
  font-size: 1.8rem;
  margin-bottom: 8px;
}

.step-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.step-num {
  font-size: 0.7rem;
  font-weight: 700;
  color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
  padding: 2px 8px;
  border-radius: 4px;
  margin-bottom: 4px;
}

.step-info h4 {
  font-size: 0.9rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 2px 0;
}

.step-info p {
  font-size: 0.75rem;
  color: #64748b;
  margin: 0;
}

.workflow-arrow {
  color: #3b82f6;
  font-size: 1.5rem;
  font-weight: 300;
}

@media (max-width: 992px) {
  .workflow-horizontal {
    gap: 8px;
    padding: 20px 16px;
  }

  .workflow-step-h {
    min-width: 80px;
    padding: 12px 8px;
  }

  .step-icon {
    font-size: 1.5rem;
  }

  .workflow-arrow {
    font-size: 1.2rem;
  }
}

@media (max-width: 768px) {
  .workflow-horizontal {
    flex-direction: column;
    gap: 4px;
  }

  .workflow-step-h {
    flex-direction: row;
    width: 100%;
    min-width: unset;
    padding: 12px 16px;
    text-align: left;
  }

  .step-icon {
    margin-bottom: 0;
    margin-right: 12px;
  }

  .step-info {
    align-items: flex-start;
  }

  .workflow-arrow {
    transform: rotate(90deg);
    font-size: 1rem;
  }
}

/* 训练详情 */
.training-details {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  text-align: left;
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
  display: flex;
  flex-direction: column;
  gap: 30px;
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
  text-align: left;
}

.code-snippet code {
  font-family: "JetBrains Mono", monospace;
  font-size: 14px;
  color: #e2e8f0;
  line-height: 1.6;
  text-align: left;
  display: block;
}

.integration-note {
  background: #f8fafc;
  border-radius: 12px;
  padding: 24px;
  border-left: 4px solid #10b981;
}

.integration-note h4 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #1e293b;
}

.integration-note ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.integration-note li {
  margin-bottom: 10px;
  color: #475569;
  line-height: 1.6;
  padding-left: 20px;
  position: relative;
}

.integration-note li:before {
  content: "→";
  color: #10b981;
  position: absolute;
  left: 0;
}

.integration-note li strong {
  color: #1e293b;
}

.code-snippet {
  background: #0f172a;
  border-radius: 16px;
  overflow: hidden;
  text-align: left;
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

/* 挑战网格 - 固定2列布局 */
.challenges-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  text-align: left;
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

/* ==================== 新增 Section 样式 ==================== */

/* 研究背景卡片 */
.research-background-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.background-content h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 10px;
}

.background-icon {
  font-size: 1.8rem;
}

.background-content p {
  color: #475569;
  line-height: 1.8;
  margin-bottom: 16px;
}

.background-content p strong {
  color: #1e293b;
}

/* 核心原理卡片 */
.core-principles-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.principles-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
}

@media (max-width: 768px) {
  .principles-grid {
    grid-template-columns: 1fr;
  }
}

.principle-item {
  text-align: left;
  padding: 24px;
  background: #f8fafc;
  border-radius: 16px;
  border-left: 4px solid #3b82f6;
}

.principle-icon {
  font-size: 2rem;
  margin-bottom: 12px;
}

.principle-item h3 {
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: #1e293b;
}

.principle-item p {
  color: #64748b;
  line-height: 1.6;
  font-size: 0.95rem;
}

.principle-item p strong {
  color: #1e293b;
}

/* 网络架构卡片 - 新布局 */
.architecture-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.architecture-image-full {
  text-align: center;
  margin-bottom: 30px;
}

.architecture-image {
  max-width: 100%;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  cursor: pointer;
}

.architecture-image:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
}

.image-caption {
  margin-top: 12px;
  font-size: 14px;
  color: #64748b;
  font-style: italic;
}

.architecture-details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

@media (max-width: 768px) {
  .architecture-details-grid {
    grid-template-columns: 1fr;
  }
}

.architecture-detail-item {
  background: #f8fafc;
  border-radius: 16px;
  padding: 24px;
  border-left: 4px solid #3b82f6;
}

.architecture-detail-item h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 10px;
}

.detail-icon {
  font-size: 1.5rem;
}

.architecture-detail-item ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.architecture-detail-item li {
  margin-bottom: 10px;
  color: #64748b;
  line-height: 1.5;
  font-size: 0.95rem;
}

.architecture-detail-item li strong {
  color: #1e293b;
}

.architecture-detail-item p {
  color: #475569;
  line-height: 1.6;
  margin-bottom: 8px;
}

.output-tensor {
  background: #f1f5f9;
  padding: 8px 16px;
  border-radius: 8px;
  margin-top: 8px;
}

.output-tensor strong {
  font-size: 1.1rem;
  font-family: "JetBrains Mono", monospace;
}

/* 损失函数卡片 */
.loss-function-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.loss-function-content h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 10px;
}

.formula-icon {
  font-size: 1.8rem;
}

.loss-function-content > p {
  color: #475569;
  line-height: 1.8;
  margin-bottom: 24px;
}

.loss-function-content > p strong {
  color: #1e293b;
}

.formula-total-box {
  background: #f8fafc;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  border: 2px solid #3b82f6;
}

.formula-total-box h4 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #1e293b;
}

.formula-total {
  font-family: "JetBrains Mono", monospace;
  background: #ffffff;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.formula-line {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
  font-size: 0.95rem;
}

.formula-line.indent {
  padding-left: 48px;
}

.formula-line:last-child {
  margin-bottom: 0;
}

.formula-var {
  font-weight: 700;
  color: #1e293b;
  min-width: 50px;
}

.formula-eq {
  color: #94a3b8;
  font-weight: 600;
}

.formula-plus {
  color: #3b82f6;
  font-weight: 700;
  min-width: 20px;
}

.formula-expr {
  color: #475569;
}

.formula-details {
  margin-bottom: 24px;
}

.formula-details h4 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #1e293b;
}

.formula-parts {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.formula-part {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #f8fafc;
  padding: 12px 16px;
  border-radius: 12px;
  border-left: 3px solid #8b5cf6;
}

.part-num {
  background: #8b5cf6;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
  flex-shrink: 0;
}

.part-content {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.part-label {
  font-size: 0.9rem;
  color: #475569;
  font-weight: 600;
  min-width: 120px;
}

.part-formula {
  font-family: "JetBrains Mono", monospace;
  font-size: 0.85rem;
  color: #3b82f6;
  background: #eff6ff;
  padding: 4px 12px;
  border-radius: 6px;
}

.formula-notes {
  background: #f8fafc;
  border-radius: 16px;
  padding: 24px;
  border-left: 4px solid #10b981;
}

.formula-notes h4 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 10px;
}

.formula-notes ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.formula-notes li {
  margin-bottom: 12px;
  color: #475569;
  line-height: 1.7;
  padding-left: 24px;
  position: relative;
}

.formula-notes li:before {
  content: "•";
  color: #10b981;
  font-weight: bold;
  position: absolute;
  left: 8px;
}

.formula-notes li strong {
  color: #1e293b;
}

.formula-notes li:before {
  content: "•";
  color: #10b981;
  font-weight: bold;
  position: absolute;
  left: 8px;
}

.formula-notes li strong {
  color: #1e293b;
}

/* 核心原理 - 内联公式样式 */
.formula-inline {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.formula-inline code {
  font-family: "JetBrains Mono", monospace;
  font-size: 0.85rem;
  color: #3b82f6;
  background: #eff6ff;
  padding: 4px 10px;
  border-radius: 6px;
}

.formula-eq {
  color: #64748b;
  font-weight: 600;
}

/* 优缺点卡片 */
.advantages-limitations-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.advantages-section,
.limitations-section {
  margin-bottom: 40px;
}

.advantages-section:last-child,
.limitations-section:last-child {
  margin-bottom: 0;
}

.advantages-section h3,
.limitations-section h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 24px;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 10px;
}

.advantage-icon,
.limitation-icon {
  font-size: 1.8rem;
}

.advantage-grid,
.limitation-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

@media (max-width: 992px) {
  .advantage-grid,
  .limitation-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .advantage-grid,
  .limitation-grid {
    grid-template-columns: 1fr;
  }
}

.advantage-item,
.limitation-item {
  background: #f8fafc;
  border-radius: 16px;
  padding: 24px;
  border-left: 4px solid #10b981;
}

.limitation-item {
  border-left-color: #ef4444;
}

.advantage-item h4,
.limitation-item h4 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #1e293b;
}

.advantage-item p,
.limitation-item p {
  color: #64748b;
  line-height: 1.6;
}

/* 演进卡片 */
.evolution-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 40px;
  border: 1px solid #e2e8f0;
  text-align: left;
}

/* 演进时间线 - About风格 */
.evolution-timeline-wrapper {
  position: relative;
  max-width: 900px;
  margin: 0 auto;
  padding-left: 60px;
}

.evolution-line {
  position: absolute;
  left: 19px;
  top: 20px;
  bottom: 80px;
  width: 2px;
  background: #e2e8f0;
  z-index: 0;
}

.evolution-timeline {
  display: flex;
  flex-direction: column;
  gap: 30px;
  margin-bottom: 40px;
}

.evolution-node {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.evolution-marker {
  position: absolute;
  left: -60px;
  top: 0;
  width: 40px;
  display: flex;
  justify-content: center;
  z-index: 1;
}

.evolution-circle {
  width: 40px;
  height: 40px;
  background: #fff;
  border: 2px solid #e2e8f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 16px;
  color: #94a3b8;
  transition: all 0.3s;
}

.evolution-content {
  flex: 1;
}

.evolution-card-item {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 20px 24px;
  transition: all 0.3s;
}

.evolution-card-item:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.evolution-card-item:hover .evolution-circle {
  border-color: #3b82f6;
  color: #3b82f6;
  transform: scale(1.1);
}

.evolution-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.evolution-year {
  background: #3b82f6;
  color: white;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 700;
}

.evolution-header h3 {
  font-size: 1.15rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.evolution-body p {
  color: #475569;
  line-height: 1.6;
  font-size: 0.95rem;
  margin: 0;
}

.evolution-summary-box {
  background: #f8fafc;
  border-radius: 16px;
  padding: 24px;
  border-left: 4px solid #8b5cf6;
}

.evolution-summary-box h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 10px;
}

.summary-icon {
  font-size: 1.5rem;
}

.evolution-summary-box p {
  color: #475569;
  line-height: 1.7;
  margin: 0;
}

.evolution-summary-box p strong {
  color: #1e293b;
}

/* 图片预览模态框样式（复用 TechArchitecture.vue） */
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

@media (max-width: 768px) {
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

[data-theme="dark"] .integration-note {
  background: var(--dm-bg-hover);
  border-left-color: #10b981;
}

[data-theme="dark"] .integration-note h4 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .integration-note li {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .integration-note li:before {
  color: #10b981;
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

/* ==================== 新增 Section 深色模式样式 ==================== */

[data-theme="dark"] .research-background-card,
[data-theme="dark"] .core-principles-card,
[data-theme="dark"] .architecture-card,
[data-theme="dark"] .loss-function-card,
[data-theme="dark"] .advantages-limitations-card,
[data-theme="dark"] .evolution-card {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .background-content h3,
[data-theme="dark"] .architecture-details h3,
[data-theme="dark"] .loss-function-content h3,
[data-theme="dark"] .advantages-section h3,
[data-theme="dark"] .limitations-section h3,
[data-theme="dark"] .evolution-summary h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .background-content p,
[data-theme="dark"] .loss-function-content p,
[data-theme="dark"] .evolution-summary p {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .background-content p strong,
[data-theme="dark"] .loss-function-content p strong,
[data-theme="dark"] .evolution-summary p strong {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .principle-item,
[data-theme="dark"] .advantage-item,
[data-theme="dark"] .limitation-item,
[data-theme="dark"] .formula-display,
[data-theme="dark"] .formula-notes,
[data-theme="dark"] .architecture-detail-item {
  background: var(--dm-bg-hover);
}

[data-theme="dark"] .principle-item h3,
[data-theme="dark"] .advantage-item h4,
[data-theme="dark"] .limitation-item h4,
[data-theme="dark"] .formula-display h4,
[data-theme="dark"] .formula-notes h4,
[data-theme="dark"] .architecture-detail-item h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .principle-item p,
[data-theme="dark"] .advantage-item p,
[data-theme="dark"] .limitation-item p,
[data-theme="dark"] .formula-notes li {
  color: var(--dm-text-secondary);
}

/* 演进时间线深色模式 */
[data-theme="dark"] .evolution-line {
  background: var(--dm-border);
}

[data-theme="dark"] .evolution-circle {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
  color: var(--dm-text-muted);
}

[data-theme="dark"] .evolution-card-item {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .evolution-card-item:hover {
  border-color: var(--dm-accent);
}

[data-theme="dark"] .evolution-card-item:hover .evolution-circle {
  border-color: var(--dm-accent);
  color: var(--dm-accent);
}

[data-theme="dark"] .evolution-year {
  background: var(--dm-accent);
}

[data-theme="dark"] .evolution-header h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .evolution-body p {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .evolution-summary-box {
  background: var(--dm-bg-hover);
  border-left-color: #8b5cf6;
}

[data-theme="dark"] .evolution-summary-box h3 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .evolution-summary-box p {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .evolution-summary-box p strong {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .principle-item p strong {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .architecture-detail-item li,
[data-theme="dark"] .architecture-detail-item p,
[data-theme="dark"] .formula-notes li strong {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .architecture-detail-item li strong {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .formula-part {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .part-label {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .part-formula {
  background: var(--dm-bg-hover);
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .formula-legend {
  border-top-color: var(--dm-border);
}

[data-theme="dark"] .formula-legend span {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .image-caption {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .architecture-image {
  border-color: var(--dm-border);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .workflow-horizontal {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .workflow-step-h {
  background: var(--dm-bg-hover);
}

[data-theme="dark"] .workflow-step-h:hover {
  background: rgba(59, 130, 246, 0.1);
}

[data-theme="dark"] .step-num {
  background: rgba(59, 130, 246, 0.2);
}

[data-theme="dark"] .step-info h4 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .step-info p {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .workflow-arrow {
  color: var(--dm-accent);
}

[data-theme="dark"] .formula-total-box {
  background: var(--dm-bg-hover);
  border-color: var(--dm-accent);
}

[data-theme="dark"] .formula-total-box h4 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .formula-total {
  background: var(--dm-bg-card);
  border-color: var(--dm-border);
}

[data-theme="dark"] .formula-var {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .formula-expr {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .formula-details h4 {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .formula-part {
  background: var(--dm-bg-hover);
  border-left-color: #8b5cf6;
}

[data-theme="dark"] .part-label {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .part-formula {
  background: rgba(59, 130, 246, 0.1);
  color: #60a5fa;
}

[data-theme="dark"] .formula-inline code {
  background: rgba(59, 130, 246, 0.1);
  color: #60a5fa;
}

[data-theme="dark"] .output-tensor {
  background: var(--dm-bg-hover);
}

[data-theme="dark"] .output-tensor strong {
  color: var(--dm-text-primary);
}
</style>
