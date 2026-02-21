# CubeMaster 全面重构设计文档

> **创建时间:** 2026-02-21
> **状态:** 已批准
> **目标:** 在不改变任何已完成功能和逻辑的前提下，优化项目整体结构

---

## 一、重构目标

1. **删除冗余代码** - 清理未使用的文件和重复的逻辑
2. **合并重复逻辑** - 统一魔方旋转逻辑，消除 `cubeLogic.js` 和 `cubeMoves.js` 的重复
3. **拆分大型组件** - 将 `Solver.vue` 和 `CubeFree.vue` 拆分为更小的子组件
4. **统一代码风格** - 命名约定、注释风格、格式化
5. **完善文档注释** - 所有函数添加 JSDoc/docstrings

---

## 二、当前问题分析

### 2.1 冗余文件

| 文件/目录 | 问题描述 | 处理方式 |
|-----------|----------|----------|
| `twophase/` (顶层) | 与 `backend/twophase/` 重复，后端使用的是虚拟环境中的包 | 删除 |
| `merge_code.py` | 工具脚本，项目运行时不需要 | 移至 `scripts/` 归档 |

### 2.2 重复的魔方旋转逻辑

| 文件 | 数据结构 | 使用者 | 行数 |
|------|----------|--------|------|
| `utils/cubeLogic.js` | 数字数组 `[6][9]` | TutorialCube | 182 |
| `utils/cubeMoves.js` | 对象 `{faces: {U:[], D:[]...}}` | Solver, CubeFree | 169 |

**决策:** 保留 `cubeMoves.js`，为 `TutorialCube` 提供适配层，删除 `cubeLogic.js`

### 2.3 重复的常量定义

`COLOR_MAP` 在三处有不同定义：
- `Face2DView.vue` - `colorMap` (camelCase)
- `Cube3DView.vue` - `COLOR_MAP` (UPPER_CASE)
- `cubeLogic.js` - 数组格式

**决策:** 提取到 `frontend/src/constants/colors.js`

### 2.4 大型组件

| 组件 | 行数 | 需拆分的内容 |
|------|------|--------------|
| `Solver.vue` | 1377 | 扫描面板、控制按钮、结果显示 |
| `CubeFree.vue` | 1413 | 控制面板、快捷键提示、动画控制 |

### 2.5 注释风格不一致

- 部分文件有详细 JSDoc（如 `cubeCustomization.js`）
- 部分文件几乎无注释（如 `cubeMoves.js`）
- 后端部分函数无 docstrings

**决策:** 统一使用 JSDoc（前端）和 docstrings（后端）

---

## 三、重构方案

### 阶段1：清理冗余 (风险: 低)

**目标:** 删除未使用的文件，提取重复常量

**任务:**
1. 确认并删除顶层 `twophase/` 目录
2. 创建 `scripts/` 目录，移动 `merge_code.py`
3. 创建 `frontend/src/constants/colors.js`，统一 `COLOR_MAP`
4. 更新所有引用 `COLOR_MAP` 的文件

### 阶段2：逻辑合并 (风险: 中)

**目标:** 合并两套魔方旋转逻辑

**任务:**
1. 在 `cubeMoves.js` 添加数字数组适配函数
2. 更新 `TutorialCube.vue` 使用新 API
3. 验证 TutorialCube 功能正常
4. 删除 `cubeLogic.js`

### 阶段3：组件拆分 (风险: 中)

**目标:** 拆分大型 View 组件

**Solver.vue 拆分:**
- `ScanPanel.vue` - 扫描面板（摄像头、图片上传）
- `SolutionDisplay.vue` - 解法展示
- `SolverControls.vue` - 控制按钮组

**CubeFree.vue 拆分:**
- `FreeControlPanel.vue` - 控制面板
- `ShortcutsHint.vue` - 快捷键提示

### 阶段4：注释完善 (风险: 低)

**目标:** 为所有工具函数添加完整文档

**前端 (JSDoc):**
- `utils/*.js` - 所有导出函数
- `composables/*.js` - 所有导出函数和响应式变量
- `api/cubeService.js` - 所有 API 函数

**后端 (docstrings):**
- `app.py` - 所有路由处理函数
- `cube_service.py` - 所有服务函数
- `cube_image_detection.py` - 所有检测函数
- `convert_cube_state.py` - 所有转换函数
- `image_utils.py` - 所有工具函数

### 阶段5：风格统一 (风险: 低)

**目标:** 统一命名和格式化

**任务:**
1. 常量统一使用 `UPPER_SNAKE_CASE`
2. 变量统一使用 `camelCase`（前端）/ `snake_case`（后端）
3. 运行 `npm run format` 和 `black .`
4. 运行 `npm run lint` 和 `ruff check --fix`

---

## 四、验证策略

每个阶段完成后执行：

1. **前端:** `npm run dev` 启动开发服务器，手动测试各页面功能
2. **后端:** `python -m pytest tests/ -v` 运行测试
3. **构建:** `npm run build` 确保生产构建成功

---

## 五、回滚策略

- 每个阶段完成后创建一个 commit
- 如发现问题，可 `git revert` 回滚到上一个阶段
- 大改动前可创建分支保存当前状态

---

## 六、预计时间

| 阶段 | 预计时间 | 风险 |
|------|----------|------|
| 阶段1: 清理冗余 | 30分钟 | 低 |
| 阶段2: 逻辑合并 | 1小时 | 中 |
| 阶段3: 组件拆分 | 2小时 | 中 |
| 阶段4: 注释完善 | 1.5小时 | 低 |
| 阶段5: 风格统一 | 30分钟 | 低 |
| **总计** | **5.5小时** | - |

---

*文档创建时间: 2026-02-21*
*批准人: 用户*
