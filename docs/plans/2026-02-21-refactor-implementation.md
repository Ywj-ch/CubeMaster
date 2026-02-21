# CubeMaster 全面重构实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在不改变任何已完成功能和逻辑的前提下，优化项目整体结构，包括清理冗余、合并逻辑、拆分组件、完善注释、统一风格。

**Architecture:** 渐进式重构，分5个阶段进行，每个阶段独立验证，出现问题可快速回滚。

**Tech Stack:** Vue 3, Vite, Element Plus, Three.js (前端); FastAPI, YOLOv8, pytest (后端)

---

## 阶段1：清理冗余

### Task 1.1: 确认并删除顶层 twophase 目录

**Files:**
- Delete: `twophase/` (顶层目录)

**Step 1: 验证后端不依赖顶层 twophase**

运行命令检查后端是否导入顶层 twophase：
```bash
cd E:/PyCharmProjects/CubeMaster
grep -r "import twophase" backend/ || echo "No import found in backend/"
grep -r "from twophase" backend/ || echo "No from import found in backend/"
```

预期：后端使用的是虚拟环境中的 twophase 包，不依赖顶层目录

**Step 2: 删除顶层 twophase 目录**

```bash
rm -rf E:/PyCharmProjects/CubeMaster/twophase
```

**Step 3: 验证后端仍可正常启动**

```bash
cd E:/PyCharmProjects/CubeMaster/backend
python -c "from twophase import solver; print('twophase OK')"
```

预期：输出 "twophase OK"

**Step 4: Commit**

```bash
git add -A
git commit -m "chore: 删除冗余的顶层 twophase 目录"
```

---

### Task 1.2: 归档工具脚本

**Files:**
- Create: `scripts/` 目录
- Move: `merge_code.py` → `scripts/merge_code.py`

**Step 1: 创建 scripts 目录并移动文件**

```bash
mkdir -p E:/PyCharmProjects/CubeMaster/scripts
mv E:/PyCharmProjects/CubeMaster/merge_code.py E:/PyCharmProjects/CubeMaster/scripts/
```

**Step 2: 验证移动成功**

```bash
ls E:/PyCharmProjects/CubeMaster/scripts/
```

预期：显示 `merge_code.py`

**Step 3: Commit**

```bash
git add -A
git commit -m "chore: 归档工具脚本到 scripts 目录"
```

---

### Task 1.3: 创建统一颜色常量文件

**Files:**
- Create: `frontend/src/constants/colors.js`
- Modify: `frontend/src/components/Face2DView.vue`
- Modify: `frontend/src/components/Cube3DView.vue`

**Step 1: 创建 colors.js**

```javascript
// frontend/src/constants/colors.js

/**
 * 魔方颜色常量
 * 包含颜色名称到十六进制值的映射
 */
export const COLOR_MAP = {
  white: '#FFFFFF',
  yellow: '#FFFF00',
  red: '#FF0000',
  orange: '#FFA500',
  blue: '#0000FF',
  green: '#00FF00',
  gray: '#808080'
}

/**
 * 颜色名称数组（按面顺序：U, D, F, B, L, R）
 */
export const COLOR_NAMES = ['white', 'yellow', 'red', 'orange', 'blue', 'green']

/**
 * 获取颜色的十六进制值
 * @param {string} colorName - 颜色名称
 * @returns {string} 十六进制颜色值
 */
export function getHexColor(colorName) {
  return COLOR_MAP[colorName] || COLOR_MAP.gray
}
```

**Step 2: 更新 Face2DView.vue**

找到文件中的 `colorMap` 定义，替换为：
```javascript
import { COLOR_MAP, getHexColor } from '@/constants/colors'

// 删除本地的 colorMap 定义
// 将使用 colorMap 的地方改为使用 COLOR_MAP 或 getHexColor
```

**Step 3: 更新 Cube3DView.vue**

找到文件中的 `COLOR_MAP` 定义，替换为：
```javascript
import { COLOR_MAP, COLOR_NAMES } from '@/constants/colors'

// 删除本地的 COLOR_MAP 定义
```

**Step 4: 验证前端正常**

```bash
cd E:/PyCharmProjects/CubeMaster/frontend
npm run dev
```

手动测试：打开浏览器检查 2D 面视图和 3D 渲染颜色是否正常

**Step 5: Commit**

```bash
git add -A
git commit -m "refactor: 提取颜色常量到统一文件"
```

---

## 阶段2：逻辑合并

### Task 2.1: 在 cubeMoves.js 添加适配函数

**Files:**
- Modify: `frontend/src/utils/cubeMoves.js`

**Step 1: 读取当前 cubeMoves.js 内容**

先读取文件了解当前结构。

**Step 2: 添加数字数组适配函数**

在文件末尾添加以下函数：

```javascript
/**
 * 将数字数组状态转换为对象状态
 * 数字顺序: 0=white(U), 1=yellow(D), 2=red(F), 3=orange(B), 4=blue(L), 5=green(R)
 * @param {number[][]} numericState - 6x9 数字数组
 * @returns {Object} 对象格式的魔方状态
 */
export function numericToObject(numericState) {
  const colorNames = ['white', 'yellow', 'red', 'orange', 'blue', 'green']
  const faces = {}
  const faceOrder = ['U', 'D', 'F', 'B', 'L', 'R']
  
  faceOrder.forEach((face, idx) => {
    faces[face] = numericState[idx].map(colorIdx => colorNames[colorIdx])
  })
  
  return { faces }
}

/**
 * 将对象状态转换为数字数组状态
 * @param {Object} objectState - 对象格式的魔方状态
 * @returns {number[][]} 6x9 数字数组
 */
export function objectToNumeric(objectState) {
  const colorToNum = {
    white: 0, yellow: 1, red: 2,
    orange: 3, blue: 4, green: 5
  }
  const faceOrder = ['U', 'D', 'F', 'B', 'L', 'R']
  
  return faceOrder.map(face => 
    objectState.faces[face].map(color => colorToNum[color] || 0)
  )
}
```

**Step 3: 验证**

```bash
cd E:/PyCharmProjects/CubeMaster/frontend
npm run dev
```

**Step 4: Commit**

```bash
git add -A
git commit -m "feat(cubeMoves): 添加数字数组和对象格式的转换函数"
```

---

### Task 2.2: 更新 TutorialCube.vue 使用新 API

**Files:**
- Modify: `frontend/src/components/TutorialCube.vue`

**Step 1: 读取 TutorialCube.vue 和 cubeLogic.js**

了解 TutorialCube 如何使用 cubeLogic

**Step 2: 更新导入和使用方式**

将 `import * as cubeLogic from '@/utils/cubeLogic'` 改为使用 cubeMoves 的新函数。

**Step 3: 验证学习模块功能**

手动测试：
1. 打开学习页面
2. 测试层先法教程的每一步旋转
3. 确保 3D 渲染正常

**Step 4: Commit**

```bash
git add -A
git commit -m "refactor(TutorialCube): 迁移到 cubeMoves API"
```

---

### Task 2.3: 删除 cubeLogic.js

**Files:**
- Delete: `frontend/src/utils/cubeLogic.js`

**Step 1: 确认没有其他文件依赖 cubeLogic.js**

```bash
cd E:/PyCharmProjects/CubeMaster/frontend
grep -r "cubeLogic" src/ --include="*.vue" --include="*.js"
```

预期：只有 TutorialCube.vue 的旧引用（已在上一步更新）

**Step 2: 删除文件**

```bash
rm E:/PyCharmProjects/CubeMaster/frontend/src/utils/cubeLogic.js
```

**Step 3: 验证前端正常**

```bash
npm run dev
```

**Step 4: Commit**

```bash
git add -A
git commit -m "refactor: 删除冗余的 cubeLogic.js"
```

---

## 阶段3：组件拆分

### Task 3.1: 分析 Solver.vue 结构

**Files:**
- Read: `frontend/src/views/Solver.vue`

**Step 1: 读取并分析组件结构**

识别可拆分的 UI 块：
- 扫描面板区域
- 控制按钮区域
- 解法展示区域

**Step 2: 规划子组件**

创建拆分计划，确定每个子组件的职责和接口。

---

### Task 3.2: 创建 ScanPanel 组件

**Files:**
- Create: `frontend/src/components/solver/ScanPanel.vue`

**Step 1: 从 Solver.vue 提取扫描相关代码**

包括：
- 摄像头视图
- 图片上传
- 扫描进度显示

**Step 2: 定义 props 和 emits**

```javascript
const props = defineProps({
  // 扫描状态、当前面等
})

const emit = defineEmits(['scan', 'upload', 'reset'])
```

**Step 3: 在 Solver.vue 中使用新组件**

**Step 4: 验证扫描功能**

手动测试上传图片和摄像头扫描功能

**Step 5: Commit**

```bash
git add -A
git commit -m "refactor(Solver): 提取 ScanPanel 子组件"
```

---

### Task 3.3: 创建 SolutionDisplay 组件

**Files:**
- Create: `frontend/src/components/solver/SolutionDisplay.vue`

**Step 1: 从 Solver.vue 提取解法展示代码**

包括：
- 步骤列表
- 当前步骤高亮
- 动画控制

**Step 2: 定义 props 和 emits**

**Step 3: 在 Solver.vue 中使用新组件**

**Step 4: 验证解法展示功能**

**Step 5: Commit**

```bash
git add -A
git commit -m "refactor(Solver): 提取 SolutionDisplay 子组件"
```

---

### Task 3.4: 创建 SolverControls 组件

**Files:**
- Create: `frontend/src/components/solver/SolverControls.vue`

**Step 1: 从 Solver.vue 提取控制按钮代码**

**Step 2: 定义 props 和 emits**

**Step 3: 在 Solver.vue 中使用新组件**

**Step 4: 验证控制功能**

**Step 5: Commit**

```bash
git add -A
git commit -m "refactor(Solver): 提取 SolverControls 子组件"
```

---

### Task 3.5: 分析 CubeFree.vue 结构

**Files:**
- Read: `frontend/src/views/CubeFree.vue`

**Step 1: 读取并分析组件结构**

识别可拆分的 UI 块。

---

### Task 3.6: 创建 FreeControlPanel 组件

**Files:**
- Create: `frontend/src/components/cubefree/FreeControlPanel.vue`

**Step 1: 从 CubeFree.vue 提取控制面板代码**

**Step 2: 定义 props 和 emits**

**Step 3: 在 CubeFree.vue 中使用新组件**

**Step 4: 验证控制功能**

**Step 5: Commit**

```bash
git add -A
git commit -m "refactor(CubeFree): 提取 FreeControlPanel 子组件"
```

---

### Task 3.7: 创建 ShortcutsHint 组件

**Files:**
- Create: `frontend/src/components/cubefree/ShortcutsHint.vue`

**Step 1: 从 CubeFree.vue 提取快捷键提示代码**

**Step 2: 定义 props**

**Step 3: 在 CubeFree.vue 中使用新组件**

**Step 4: 验证快捷键提示显示**

**Step 5: Commit**

```bash
git add -A
git commit -m "refactor(CubeFree): 提取 ShortcutsHint 子组件"
```

---

## 阶段4：注释完善

### Task 4.1: 为前端 utils 添加 JSDoc

**Files:**
- Modify: `frontend/src/utils/cubeMoves.js`
- Modify: `frontend/src/utils/cubeState.js`
- Modify: `frontend/src/utils/cubeCustomization.js`
- Modify: `frontend/src/utils/textureProcessor.js`

**Step 1: 为每个文件的所有导出函数添加 JSDoc**

格式：
```javascript
/**
 * 函数简短描述
 * 
 * @param {Type} paramName - 参数描述
 * @returns {Type} 返回值描述
 * @throws {ErrorType} 异常描述（如有）
 * @example
 * // 使用示例
 * functionName(arg)
 */
```

**Step 2: Commit**

```bash
git add -A
git commit -m "docs(frontend): 为 utils 文件添加 JSDoc 注释"
```

---

### Task 4.2: 为前端 composables 添加 JSDoc

**Files:**
- Modify: `frontend/src/composables/useTheme.js`
- Modify: `frontend/src/composables/useLoading.js`
- Modify: `frontend/src/composables/useCubeCustomization.js`

**Step 1: 为每个 composable 添加完整文档**

**Step 2: Commit**

```bash
git add -A
git commit -m "docs(frontend): 为 composables 添加 JSDoc 注释"
```

---

### Task 4.3: 为后端添加 docstrings

**Files:**
- Modify: `backend/app.py`
- Modify: `backend/cube_service.py`
- Modify: `backend/cube_image_detection.py`
- Modify: `backend/convert_cube_state.py`
- Modify: `backend/image_utils.py`

**Step 1: 为每个 Python 函数添加 docstring**

格式：
```python
def function_name(param: Type) -> ReturnType:
    """函数简短描述。
    
    Args:
        param: 参数描述。
        
    Returns:
        返回值描述。
        
    Raises:
        ExceptionType: 异常描述。
        
    Example:
        >>> function_name(arg)
        expected_result
    """
```

**Step 2: Commit**

```bash
git add -A
git commit -m "docs(backend): 为所有模块添加 docstrings"
```

---

## 阶段5：风格统一

### Task 5.1: 运行代码格式化

**Step 1: 格式化前端代码**

```bash
cd E:/PyCharmProjects/CubeMaster/frontend
npm run format
```

**Step 2: 格式化后端代码**

```bash
cd E:/PyCharmProjects/CubeMaster/backend
black .
```

**Step 3: Commit**

```bash
git add -A
git commit -m "style: 运行代码格式化"
```

---

### Task 5.2: 运行代码检查

**Step 1: 前端 lint**

```bash
cd E:/PyCharmProjects/CubeMaster/frontend
npm run lint
```

如有错误，修复后继续。

**Step 2: 后端 lint**

```bash
cd E:/PyCharmProjects/CubeMaster/backend
ruff check --fix
```

**Step 3: 后端类型检查**

```bash
cd E:/PyCharmProjects/CubeMaster/backend
mypy .
```

**Step 4: Commit**

```bash
git add -A
git commit -m "fix: 修复 lint 检查发现的问题"
```

---

### Task 5.3: 运行测试验证

**Step 1: 运行后端测试**

```bash
cd E:/PyCharmProjects/CubeMaster/backend
python -m pytest tests/ -v
```

预期：所有测试通过

**Step 2: 构建前端生产版本**

```bash
cd E:/PyCharmProjects/CubeMaster/frontend
npm run build
```

预期：构建成功

**Step 3: 最终 Commit**

```bash
git add -A
git commit -m "chore: 完成全面重构，验证所有功能正常"
```

---

## 验证清单

- [ ] 前端开发服务器正常启动
- [ ] 首页正常显示
- [ ] 学习模块（层先法教程）正常
- [ ] 自由模式正常旋转
- [ ] 求解器扫描和求解正常
- [ ] 外观定制功能正常
- [ ] 暗色模式切换正常
- [ ] 后端 API 正常响应
- [ ] 后端测试全部通过
- [ ] 前端生产构建成功

---

*计划创建时间: 2026-02-21*
