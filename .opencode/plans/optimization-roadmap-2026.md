# CubeMaster 项目优化路线图 (2026)

> **文档版本**: v1.0  
> **创建日期**: 2026-02-26  
> **优先级排序**: 高 → 中 → 低  

---

## 📊 优化概览

| 优先级 | 优化方向 | 预计工时 | 收益评估 | 风险等级 |
|:------:|---------|---------|---------|---------|
| 🔴 高 | 测试框架搭建 | 4-6 小时 | ⭐⭐⭐⭐⭐ | 低 |
| 🟡 中 | CI/CD 配置 | 3-5 小时 | ⭐⭐⭐⭐ | 中 |
| 🟡 中 | 性能优化 | 4-8 小时 | ⭐⭐⭐⭐ | 低 |

---

## 1️⃣ 测试框架搭建 (高优先级)

### 1.1 现状分析

**前端测试空白**:
```json
// package.json 当前状态
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "format": "prettier --write .",
    "lint": "eslint . --ext .vue,.js,.ts"
    // ❌ 缺少 "test" 脚本
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^6.0.1",
    "prettier": "3.8.1",
    "vite": "^7.2.4"
    // ❌ 缺少 vitest、@vue/test-utils 等测试依赖
  }
}
```

**后端测试不足**:
```text
backend/tests/
├── conftest.py          # 仅路径配置
└── test_app.py          # 5 个基础 API 测试
    ├── test_root_endpoint()
    ├── test_health_check()
    ├── test_solve_endpoint()
    ├── test_recognize_endpoint_invalid()
    └── test_performance_middleware()
```

**缺失覆盖**:
- ❌ 业务逻辑测试 (`cube_service.py`)
- ❌ 图像处理测试 (`cube_image_detection.py`)
- ❌ 算法集成测试 (`twophase/`)
- ❌ 前端组件测试 (所有 Vue 组件)
- ❌ 工具函数测试 (`utils/`)

---

### 1.2 实施方案

#### 阶段 1: 前端测试框架 (2-3 小时)

**Step 1.1: 安装测试依赖**
```bash
cd frontend
npm install -D vitest @vue/test-utils @testing-library/vue jsdom happy-dom
```

**Step 1.2: 配置 Vite 测试选项**
```javascript
// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,           // 启用全局测试 API
    environment: 'jsdom',    // 浏览器环境模拟
    setupFiles: './src/test/setup.js',  // 测试配置文件
    include: ['**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}'],
    coverage: {
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'src/test/']
    }
  }
})
```

**Step 1.3: 添加 npm 脚本**
```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui"
  }
}
```

**Step 1.4: 创建测试示例**
```javascript
// src/utils/__tests__/cubeMoves.test.js
import { describe, it, expect } from 'vitest'
import { applyMove } from '../cubeMoves'

describe('cubeMoves', () => {
  it('should apply R move correctly', () => {
    const state = createTestCube()
    applyMove(state, 'R')
    expect(state.faces.R).toEqual(expectedState)
  })
})
```

---

#### 阶段 2: 后端测试增强 (2-3 小时)

**Step 2.1: 安装测试工具**
```bash
cd backend
pip install pytest-cov pytest-asyncio httpx
```

**Step 2.2: 增加业务逻辑测试**
```python
# tests/test_cube_service.py
import pytest
from unittest.mock import Mock, patch
from cube_service import recognize_cube, save_cube_state, solve_cube

class TestCubeService:
    @patch('cube_service.get_detector')
    def test_recognize_cube_success(self, mock_detector):
        """测试魔方识别功能"""
        mock_detector.detect_all_faces.return_value = ['R']*9 + ['U']*9 + ...
        result = recognize_cube(test_images)
        assert len(result) == 54
        assert mock_detector.called
    
    @patch('cube_service.solve_cube_pipeline')
    def test_solve_cube(self, mock_solve):
        """测试求解功能"""
        mock_solve.return_value = {'readable_solution': 'R U R\' U\'', 'moves': ['R', 'U', ...]}
        result = solve_cube()
        assert 'readable_solution' in result
```

**Step 2.3: 增加图像处理测试**
```python
# tests/test_image_detection.py
import pytest
import numpy as np
from cube_image_detection import CubeDetector

class TestCubeDetector:
    def test_color_detection(self):
        """测试颜色识别准确性"""
        detector = CubeDetector()
        test_image = create_test_image('red')
        color = detector.detect_color(test_image)
        assert color == 'R'
```

**Step 2.4: 更新 pytest 配置**
```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --cov=. --cov-report=html --cov-report=term
```

---

### 1.3 预期收益

| 指标 | 当前 | 目标 | 提升 |
|-----|------|------|------|
| 测试覆盖率 (前端) | 0% | 60%+ | +60% |
| 测试覆盖率 (后端) | ~15% | 80%+ | +65% |
| 回归测试时间 | 手动 | 自动 5 分钟 | -90% |
| Bug 检出率 | 依赖人工 | 自动化 | +50% |

---

### 1.4 验收标准

- [ ] 前端测试覆盖率报告生成成功
- [ ] 后端 `pytest --cov` 显示覆盖率 > 80%
- [ ] 所有测试在 CI 中自动运行
- [ ] 新增功能必须附带测试用例

---

## 2️⃣ CI/CD 配置 (中优先级)

### 2.1 现状分析

**缺失内容**:
- ❌ 无 GitHub Actions 工作流
- ❌ 无自动化代码检查
- ❌ 无自动化测试触发
- ❌ 无自动构建验证
- ❌ 无自动化部署流程

**手动流程风险**:
```text
开发者提交 → 人工 review → 手动测试 → 手动构建 → 手动部署
   ↓           ↓           ↓          ↓          ↓
 易遗漏      主观判断     耗时        易出错      不可追溯
```

---

### 2.2 实施方案

#### 阶段 1: 基础 CI 流水线 (2 小时)

**Step 1.1: 创建 GitHub Actions 工作流**
```yaml
# .github/workflows/ci.yml
name: CubeMaster CI

on:
  push:
    branches: [master, develop]
  pull_request:
    branches: [master]

jobs:
  frontend-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
      - run: cd frontend && npm ci
      - run: cd frontend && npm run lint
      - run: cd frontend && npm run format -- --check

  frontend-test:
    runs-on: ubuntu-latest
    needs: frontend-lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: cd frontend && npm ci
      - run: cd frontend && npm run test:coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./frontend/coverage/coverage-final.json

  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install -r backend/requirements.txt
      - run: pip install pytest pytest-cov pytest-asyncio
      - run: cd backend && pytest --cov=. --cov-report=xml

  frontend-build:
    runs-on: ubuntu-latest
    needs: [frontend-test, backend-test]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: cd frontend && npm ci
      - run: cd frontend && npm run build
      - name: Upload dist
        uses: actions/upload-artifact@v4
        with:
          name: frontend-dist
          path: frontend/dist/
          retention-days: 7
```

---

#### 阶段 2: 代码质量检查 (1 小时)

**Step 2.1: 添加 CodeQL 安全扫描**
```yaml
# .github/workflows/codeql.yml
name: "CodeQL"

on:
  push:
    branches: [master]
  pull_request:
    branches: [master]
  schedule:
    - cron: '0 2 * * 1'  # 每周一凌晨 2 点

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    strategy:
      fail-fast: false
      matrix:
        language: ['javascript-typescript', 'python']

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v3
      with:
        languages: ${{ matrix.language }}

    - name: Autobuild
      uses: github/codeql-action/autobuild@v3

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v3
```

**Step 2.2: 添加依赖安全检查**
```yaml
# .github/workflows/dependency-review.yml
name: 'Dependency Review'

on:
  pull_request:

permissions:
  contents: read

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - name: 'Checkout Repository'
        uses: actions/checkout@v4
      - name: 'Dependency Review'
        uses: actions/dependency-review-action@v3
```

---

#### 阶段 3: 自动化部署 (可选，1-2 小时)

**Step 3.1: 生产环境部署流程**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'  # 仅当推送版本标签时触发

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Build Frontend
        run: |
          cd frontend
          npm ci
          npm run build
      
      - name: Deploy to Server
        uses: easingthemes/ssh-deploy@v4
        with:
          SSH_PRIVATE_KEY: ${{ secrets.SERVER_SSH_KEY }}
          ARGS: "-rltgoDzvO --delete"
          SOURCE: "frontend/dist/"
          REMOTE_HOST: ${{ secrets.SERVER_HOST }}
          REMOTE_USER: ${{ secrets.SERVER_USER }}
          TARGET: "/var/www/cubemaster"
          EXCLUDE: "/dist/, /node_modules/"
```

---

### 2.3 预期收益

| 指标 | 当前 | 目标 | 提升 |
|-----|------|------|------|
| 代码审查效率 | 手动 | 自动 | +70% |
| Bug 流入生产 | 高频 | 阻断式 | -80% |
| 部署时间 | 30 分钟 | 5 分钟 | -83% |
| 问题定位时间 | 数小时 | 数分钟 | -90% |

---

### 2.4 验收标准

- [ ] 每次 Push 自动触发 CI 检查
- [ ] PR 必须通过所有测试才能合并
- [ ] 构建产物自动上传为 Artifact
- [ ] 覆盖率报告可在线查看
- [ ] 安全扫描结果无高危漏洞

---

## 3️⃣ 性能优化 (中优先级)

### 3.1 现状分析

**当前 Vite 配置**:
```javascript
// vite.config.js - 过于简单
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  // ❌ 缺少构建优化配置
});
```

**构建产物分析** (预估):
```text
frontend/dist/assets/
├── index-abc123.js       ~800 KB  (未分割，包含所有依赖)
├── index-def456.css      ~200 KB
└── ...
```

**性能瓶颈**:
- ❌ 无代码分割 → 首屏加载缓慢
- ❌ 无 Tree Shaking 优化 → 包体积过大
- ❌ 无资源预加载 → 关键路径延迟
- ❌ 无 CDN 配置 → 静态资源加载慢

---

### 3.2 实施方案

#### 阶段 1: 代码分割优化 (2 小时)

**Step 1.1: 配置手动分包策略**
```javascript
// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { visualizer } from 'rollup-plugin-visualizer'

export default defineConfig({
  plugins: [
    vue(),
    visualizer({ open: true, gzipSize: true, brotliSize: true })
  ],
  build: {
    target: 'esnext',
    minify: 'esbuild',
    cssCodeSplit: true,
    rollupOptions: {
      output: {
        manualChunks: {
          // Vue 核心库
          'vue-vendor': ['vue', 'vue-router'],
          // UI 组件库
          'element-plus': ['element-plus'],
          'element-icons': ['@element-plus/icons-vue'],
          // 3D 引擎
          'three-vendor': ['three'],
          // 工具库
          'utils': ['axios', 'canvas-confetti', 'katex']
        },
        // 分包命名规则
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: 'assets/[ext]/[name]-[hash].[ext]'
      }
    }
  }
})
```

**Step 1.2: 路由懒加载**
```javascript
// src/router/index.js
const routes = [
  {
    path: '/',
    component: () => import('../layout/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('../views/Home.vue')
      },
      {
        path: 'solver',
        name: 'Solver',
        component: () => import('../views/Solver.vue')
      },
      {
        path: 'learning',
        name: 'Learning',
        component: () => import('../views/Learning.vue')
      },
      // ... 其他路由
    ]
  }
]
```

---

#### 阶段 2: Tree Shaking 优化 (1 小时)

**Step 2.1: 优化 Element Plus 导入**
```javascript
// 当前 (全量导入) - ❌
import ElementPlus from 'element-plus'
app.use(ElementPlus)

// 优化后 (按需导入) - ✅
// vite.config.js
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
  plugins: [
    vue(),
    Components({
      resolvers: [
        ElementPlusResolver({
          importStyle: 'sass'  // 按需加载样式
        })
      ]
    })
  ]
})
```

**Step 2.2: 安装必要依赖**
```bash
npm install -D unplugin-vue-components sass
```

---

#### 阶段 3: 资源优化 (1-2 小时)

**Step 3.1: 图片资源优化**
```javascript
// vite.config.js
export default defineConfig({
  build: {
    assetsInlineLimit: 4096,  // 小于 4KB 的图片内联为 base64
    assetsDir: 'assets',
  },
  server: {
    fs: {
      strict: true  // 限制访问上级目录
    }
  }
})
```

**Step 3.2: 预加载关键资源**
```html
<!-- index.html -->
<head>
  <link rel="modulepreload" href="/src/main.js" />
  <link rel="preload" href="/src/style.css" as="style" />
  <link rel="prefetch" href="/src/views/Home.vue" />
</head>
```

**Step 3.3: Gzip/Brotli 压缩**
```bash
# 安装压缩插件
npm install -D vite-plugin-compression
```

```javascript
// vite.config.js
import viteCompression from 'vite-plugin-compression'

export default defineConfig({
  plugins: [
    vue(),
    viteCompression({ algorithm: 'gzip' }),
    viteCompression({ algorithm: 'brotliCompress' })
  ]
})
```

---

#### 阶段 4: CDN 加速 (可选，1 小时)

**Step 4.1: 配置外部 CDN**
```javascript
// vite.config.js
export default defineConfig({
  build: {
    rollupOptions: {
      external: ['vue', 'vue-router', 'three', 'element-plus'],
      output: {
        globals: {
          vue: 'Vue',
          'vue-router': 'VueRouter',
          three: 'THREE',
          'element-plus': 'ElementPlus'
        }
      }
    }
  }
})
```

```html
<!-- index.html -->
<head>
  <script src="https://cdn.jsdelivr.net/npm/vue@3/dist/vue.global.prod.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/vue-router@4/dist/vue-router.global.prod.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.182.0/build/three.min.js"></script>
</head>
```

---

### 3.3 预期收益

| 指标 | 当前 | 目标 | 提升 |
|-----|------|------|------|
| 首屏加载时间 | ~3s | <1.5s | -50% |
| 初始包体积 | ~1MB | ~400KB | -60% |
| Lighthouse 性能分 | ~70 | ~90+ | +28% |
| 缓存命中率 | ~50% | ~90% | +80% |

---

### 3.4 验收标准

- [ ] 构建产物通过 `rollup-plugin-visualizer` 可视化分析
- [ ] Lighthouse 性能评分 > 90
- [ ] 首屏加载时间 < 1.5s
- [ ] 所有 Chunk 体积 < 200KB
- [ ] CDN 资源加载正常 (如启用)

---

## 📋 执行计划表

### 第 1 周：测试框架搭建
| 任务 | 负责人 | 状态 | 截止日期 |
|-----|--------|------|---------|
| 前端 Vitest 配置 | 待定 | ⏳ Pending | 2026-03-05 |
| 后端 pytest 扩展 | 待定 | ⏳ Pending | 2026-03-05 |
| 核心模块测试编写 | 待定 | ⏳ Pending | 2026-03-07 |

### 第 2 周：CI/CD 配置
| 任务 | 负责人 | 状态 | 截止日期 |
|-----|--------|------|---------|
| GitHub Actions 基础配置 | 待定 | ⏳ Pending | 2026-03-12 |
| CodeQL 安全扫描 | 待定 | ⏳ Pending | 2026-03-12 |
| 自动化部署流程 | 待定 | ⏳ Pending | 2026-03-14 |

### 第 3 周：性能优化
| 任务 | 负责人 | 状态 | 截止日期 |
|-----|--------|------|---------|
| 代码分割配置 | 待定 | ⏳ Pending | 2026-03-19 |
| Tree Shaking 优化 | 待定 | ⏳ Pending | 2026-03-19 |
| CDN 加速配置 | 待定 | ⏳ Pending | 2026-03-21 |
| 性能基准测试 | 待定 | ⏳ Pending | 2026-03-21 |

---

## 📎 附录

### A. 相关资源
- [Vitest 官方文档](https://vitest.dev/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Vite 性能优化指南](https://vitejs.dev/guide/performance.html)

### B. 工具清单
| 工具 | 用途 | 安装命令 |
|-----|------|---------|
| vitest | 前端测试 | `npm i -D vitest` |
| pytest-cov | 后端覆盖率 | `pip install pytest-cov` |
| rollup-plugin-visualizer | 打包分析 | `npm i -D rollup-plugin-visualizer` |
| vite-plugin-compression | 资源压缩 | `npm i -D vite-plugin-compression` |

### C. 变更日志
| 版本 | 日期 | 修改内容 | 作者 |
|-----|------|---------|------|
| v1.0 | 2026-02-26 | 初始版本 | AI Assistant |

---

> **备注**: 本计划书为动态文档，将根据实际执行情况适时更新。
