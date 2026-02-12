<template>
  <div
    ref="container"
    class="cube-3d-container"
    :class="{ 'can-control': props.enableControls }"
  ></div>
</template>

<script setup>
/**
 * @file Cube3DView.vue
 * @description 基于 Three.js 实现的高保真 3D 魔方渲染引擎。
 * 支持多种数据结构适配、原子化旋转动画、矩阵烘焙、浮点误差归一化以及基于射线检测的交互逻辑。
 */
import {
  ref,
  onMounted,
  onUnmounted,
  watch,
  nextTick,
  computed,
  watchEffect,
} from "vue";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

// =========================================================
// 1. 配置与常量
// =========================================================

/**
 * @description 组件 Props 定义
 * @property {Object|Array} cubeState 魔方状态，支持 [U,R,F,D,L,B] 简单数组或复杂对象
 * @property {Boolean} interactive 是否允许用户手动旋转魔方层
 * @property {Boolean} enableControls 是否开启轨道控制器（旋转/缩放视角）
 * @property {Boolean} autoRotate 是否开启自动巡航旋转
 * @property {Number} autoRotateSpeed 自动旋转速度
 * @property {Array} cameraPosition 相机在世界坐标系中的初始位置
 * @property {Boolean} enableZoom 是否允许缩放
 * @property {Number} moveDuration 单次转动动画的持续时间（ms）
 */
const props = defineProps({
  cubeState: { type: [Object, Array], required: true },
  interactive: { type: Boolean, default: true },
  enableControls: { type: Boolean, default: true },
  autoRotate: { type: Boolean, default: false },
  autoRotateSpeed: { type: Number, default: 4.0 },
  cameraPosition: { type: Array, default: () => [6, 6, 6] },
  enableZoom: { type: Boolean, default: true },
  moveDuration: { type: Number, default: 300 },
});

/** @description 定义自定义事件，用于通知父组件发生了交互旋转 */
const emit = defineEmits(["move"]);

/** @constant {Number} DRAG_THRESHOLD 触发旋转的最小拖拽像素距离 */
const DRAG_THRESHOLD = 35;
/** @constant {Number} CUBIE_SIZE 单个小方块的几何尺寸 */
const CUBIE_SIZE = 0.95;

/**
 * @constant {Object} COLOR_MAP 颜色名称到 Hex 值的映射表
 * 包含内部暗色（internal）和未激活色（black）
 */
const COLOR_MAP = {
  white: "#FFFFFF",
  yellow: "#FFD500",
  red: "#C41E3A",
  orange: "#FF5800",
  blue: "#0051BA",
  green: "#009E60",
  internal: "#222222",
  black: "#000000",
};

// =========================================================
// 2. 核心：数据适配层 (Adapter)
// =========================================================

/**
 * @description 生成标准 3x3 离散点阵坐标系
 * @returns {Object} 包含 centers, edges, corners 的空间位置列表
 */
const generateBaseCubies = () => {
  const cubies = { centers: [], edges: [], corners: [] };
  for (let x = -1; x <= 1; x++) {
    for (let y = -1; y <= 1; y++) {
      for (let z = -1; z <= 1; z++) {
        const nonZero = Math.abs(x) + Math.abs(y) + Math.abs(z);
        const cubie = { pos: [x, y, z] };
        if (nonZero === 1) cubies.centers.push(cubie);
        else if (nonZero === 2) cubies.edges.push(cubie);
        else if (nonZero === 3) cubies.corners.push(cubie);
      }
    }
  }
  return cubies;
};

/** @description 静态基础点阵参考 */
const BASE_CUBIES = generateBaseCubies();

/**
 * @description 归一化计算属性
 * 将多格式输入转换为统一的渲染层数据模型，实现教学模式与自由模式的兼容
 */
const normalizedState = computed(() => {
  if (Array.isArray(props.cubeState)) {
    return {
      cubies: BASE_CUBIES,
      faces: {
        U: props.cubeState[0],
        R: props.cubeState[1],
        F: props.cubeState[2],
        D: props.cubeState[3],
        L: props.cubeState[4],
        B: props.cubeState[5],
      },
    };
  }
  return props.cubeState;
});

// =========================================================
// 3. Three.js 初始化
// =========================================================
const container = ref(null);
let scene, camera, renderer, cubeGroup, controls;
let isAnimating = false;
let isMouseDown = false;
let startCubie = null;
let startNormal = null;
const mouse = new THREE.Vector2();
const startMousePos = new THREE.Vector2();
const raycaster = new THREE.Raycaster();

/**
 * @description 初始化 Three.js 渲染环境
 * 包含透视相机、WebGL 渲染器、环境光/平行光、轨道控制器以及场景组配置
 */
function initThree() {
  const width = container.value.clientWidth;
  const height = container.value.clientHeight;

  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
  camera.position.set(...props.cameraPosition);
  camera.lookAt(0, 0, 0);

  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(window.devicePixelRatio);
  container.value.appendChild(renderer.domElement);

  scene.add(new THREE.AmbientLight(0xffffff, 0.6));
  const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
  dirLight.position.set(10, 20, 10);
  scene.add(dirLight);

  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.enablePan = false;
  controls.minDistance = 3;
  controls.maxDistance = 15;

  controls.enabled = props.enableControls;
  controls.autoRotate = props.autoRotate;
  controls.autoRotateSpeed = props.autoRotateSpeed;
  controls.enableZoom = props.enableZoom;

  cubeGroup = new THREE.Group();
  scene.add(cubeGroup);
}

/** @description 场景主渲染循环，维持 60fps 刷新并更新控制器状态 */
function animate() {
  requestAnimationFrame(animate);
  if (controls) controls.update();
  if (renderer && scene && camera) renderer.render(scene, camera);
}

/** @description 窗口或容器尺寸变更时的视口自适应逻辑 */
function onResize() {
  if (!container.value || !camera || !renderer) return;
  const w = container.value.clientWidth;
  const h = container.value.clientHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
}

// =========================================================
// 4. 颜色渲染逻辑
// =========================================================

/**
 * @description 坐标映射算法：根据 Cubie 的三维位置计算在 2D 逻辑矩阵中的索引
 * @param {String} face 面标识符 (U,D,F,B,R,L)
 * @param x
 * @param y
 * @param z
 * @param {Object} faces 2D 颜色矩阵集合
 * @returns {String} 该面对应的颜色名称
 */
function getFaceColor(face, x, y, z, faces) {
  let row, col;
  switch (face) {
    case "U":
      row = z + 1;
      col = x + 1;
      break;
    case "D":
      row = 1 - z;
      col = x + 1;
      break;
    case "F":
      row = 1 - y;
      col = x + 1;
      break;
    case "B":
      row = 1 - y;
      col = 1 - x;
      break;
    case "R":
      row = 1 - y;
      col = 1 - z;
      break;
    case "L":
      row = 1 - y;
      col = z + 1;
      break;
  }
  if (!faces || !faces[face]) return "black";
  return faces[face][row * 3 + col];
}

/**
 * @description 计算单个 Cubie 六个面的颜色分布
 * @param {Object} cubie 包含位置信息的块对象
 * @param {Object} faces 2D 状态引用
 * @returns {Array<String|null>} 长度为6的颜色序列 [R,L,U,D,F,B]
 */
function getCubieFaceColors(cubie, faces) {
  const res = Array(6).fill(null);
  const [x, y, z] = cubie.pos;
  if (x === 1) res[0] = getFaceColor("R", x, y, z, faces);
  if (x === -1) res[1] = getFaceColor("L", x, y, z, faces);
  if (y === 1) res[2] = getFaceColor("U", x, y, z, faces);
  if (y === -1) res[3] = getFaceColor("D", x, y, z, faces);
  if (z === 1) res[4] = getFaceColor("F", x, y, z, faces);
  if (z === -1) res[5] = getFaceColor("B", x, y, z, faces);
  return res;
}

/**
 * @description 核心渲染函数：根据逻辑状态构建/刷新 3D 网格模型
 * 包含内存清理机制（旧模型销毁）与基于 MeshLambertMaterial 的多材质构建
 */
function renderCubies() {
  if (isAnimating || !cubeGroup) return;

  while (cubeGroup.children.length) cubeGroup.remove(cubeGroup.children[0]);

  const state = normalizedState.value;
  const allCubies = [
    ...state.cubies.corners,
    ...state.cubies.edges,
    ...state.cubies.centers,
  ];

  allCubies.forEach((c) => {
    const faceColors = getCubieFaceColors(c, state.faces);
    const geometry = new THREE.BoxGeometry(CUBIE_SIZE, CUBIE_SIZE, CUBIE_SIZE);
    const materials = faceColors.map(
      (color) =>
        new THREE.MeshLambertMaterial({
          color: color ? COLOR_MAP[color] : COLOR_MAP.internal,
        }),
    );
    const mesh = new THREE.Mesh(geometry, materials);
    mesh.position.set(...c.pos);
    mesh.userData = { isCubie: true };
    cubeGroup.add(mesh);
  });
}

// =========================================================
// 5. 动画引擎逻辑
// =========================================================

/**
 * @description 原子化执行魔方转动指令，核心涉及 Pivot Grouping 技术与矩阵烘焙
 * @param {String} move 记法指令 (如 "R", "U'", "F2")
 * @returns {Promise} 异步 Promise，解决时意味着动画完成及坐标归一化结束
 */
function playMove(move) {
  return new Promise((resolve) => {
    if (isAnimating) {
      resolve();
      return;
    }
    isAnimating = true;

    let axis, layerValue, angle;
    // 指令到旋转参数的物理映射表
    const moveMap = {
      R: { axis: "x", lv: 1, a: -Math.PI / 2 },
      "R'": { axis: "x", lv: 1, a: Math.PI / 2 },
      L: { axis: "x", lv: -1, a: Math.PI / 2 },
      "L'": { axis: "x", lv: -1, a: -Math.PI / 2 },
      U: { axis: "y", lv: 1, a: -Math.PI / 2 },
      "U'": { axis: "y", lv: 1, a: Math.PI / 2 },
      D: { axis: "y", lv: -1, a: Math.PI / 2 },
      "D'": { axis: "y", lv: -1, a: -Math.PI / 2 },
      F: { axis: "z", lv: 1, a: -Math.PI / 2 },
      "F'": { axis: "z", lv: 1, a: Math.PI / 2 },
      B: { axis: "z", lv: -1, a: Math.PI / 2 },
      "B'": { axis: "z", lv: -1, a: -Math.PI / 2 },
      R2: { axis: "x", lv: 1, a: -Math.PI },
      L2: { axis: "x", lv: -1, a: Math.PI },
      U2: { axis: "y", lv: 1, a: -Math.PI },
      D2: { axis: "y", lv: -1, a: Math.PI },
      F2: { axis: "z", lv: 1, a: -Math.PI },
      B2: { axis: "z", lv: -1, a: Math.PI },
    };

    const config = moveMap[move];
    if (!config) {
      isAnimating = false;
      resolve();
      return;
    }
    ({ axis, lv: layerValue, a: angle } = config);

    // 筛选当前参与旋转的 9 个 Cubie
    const targets = cubeGroup.children.filter(
      (m) => Math.round(m.position[axis]) === layerValue,
    );

    // 建立临时枢轴组实现绕魔方中心旋转
    const rotateGroup = new THREE.Group();
    scene.add(rotateGroup);
    targets.forEach((m) => {
      cubeGroup.remove(m);
      rotateGroup.add(m);
    });

    const start = performance.now();

    /**
     * @description 动画函数
     * @param {DOMHighResTimeStamp} now
     */
    function step(now) {
      const t = Math.min((now - start) / props.moveDuration, 1);
      rotateGroup.rotation[axis] = angle * t;

      if (t < 1) {
        requestAnimationFrame(step);
      } else {
        rotateGroup.updateMatrixWorld();
        while (rotateGroup.children.length) {
          const m = rotateGroup.children[0];

          // 矩阵烘焙：将枢轴组的旋转量永久写入子方块的 position 数值
          m.applyMatrix4(rotateGroup.matrix);

          // 精度归一化处理：消除浮点误差，强制吸附至整数点阵
          ["x", "y", "z"].forEach(
            (coord) => (m.position[coord] = Math.round(m.position[coord])),
          );

          rotateGroup.remove(m);
          cubeGroup.add(m);
        }
        scene.remove(rotateGroup);
        isAnimating = false;
        resolve();
      }
    }
    requestAnimationFrame(step);
  });
}

// =========================================================
// 6. 交互处理 (Raycasting & Vector Logic)
// =========================================================

/** @description 处理鼠标点击按下，记录起始位置并执行射线检测以锁定目标 Cubie */
function onMouseDown(event) {
  if (isAnimating || !props.interactive) return;

  const rect = container.value.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(cubeGroup.children);

  if (intersects.length > 0) {
    const intersect = intersects[0];
    startCubie = intersect.object;
    startNormal = intersect.face.normal
      .clone()
      .applyQuaternion(startCubie.quaternion);
    ["x", "y", "z"].forEach(
      (a) => (startNormal[a] = Math.round(startNormal[a])),
    );

    startMousePos.set(event.clientX, event.clientY);
    isMouseDown = true;
    if (controls) controls.enabled = false;
  }
}

/** @description 释放鼠标，恢复轨道控制器 */
function onMouseUp() {
  isMouseDown = false;
  startCubie = null;
  startNormal = null;
  if (controls) controls.enabled = props.enableControls;
}

/** @description 监听鼠标移动，判断是否超过拖拽阈值并触发魔方层转动 */
function onMouseMove(event) {
  if (!isMouseDown || isAnimating || !startCubie) return;
  const deltaX = event.clientX - startMousePos.x;
  const deltaY = event.clientY - startMousePos.y;
  if (Math.sqrt(deltaX ** 2 + deltaY ** 2) > DRAG_THRESHOLD) {
    isMouseDown = false;
    const dragDirection = new THREE.Vector2(deltaX, -deltaY).normalize();
    handleCubeRotation(dragDirection);
  }
}

/**
 * @description 处理用户拖拽行为：通过屏幕投影向量与轴向向量的点击点对比，识别用户的转动意图
 * @param {THREE.Vector2} dragDir 归一化的屏幕拖拽方向向量
 */
function handleCubeRotation(dragDir) {
  const normal = startNormal;
  let possibleAxes = [];

  // 根据法向确定可能的滑动轴（切向量）
  if (Math.abs(normal.x) > 0.5)
    possibleAxes = [new THREE.Vector3(0, 1, 0), new THREE.Vector3(0, 0, 1)];
  else if (Math.abs(normal.y) > 0.5)
    possibleAxes = [new THREE.Vector3(1, 0, 0), new THREE.Vector3(0, 0, 1)];
  else possibleAxes = [new THREE.Vector3(1, 0, 0), new THREE.Vector3(0, 1, 0)];

  let bestDragAxis = null,
    maxDot = -1,
    moveSign = 1;

  possibleAxes.forEach((axis) => {
    const p1 = startCubie.position.clone().project(camera);
    const p2 = startCubie.position.clone().add(axis).project(camera);
    const screenVector = new THREE.Vector2(
      p2.x - p1.x,
      p2.y - p1.y,
    ).normalize();
    const dot = dragDir.dot(screenVector);
    if (Math.abs(dot) > maxDot) {
      maxDot = Math.abs(dot);
      bestDragAxis = axis;
      moveSign = dot > 0 ? 1 : -1;
    }
  });

  if (bestDragAxis && maxDot > 0.5) {
    const move = getMoveCommand(
      bestDragAxis,
      moveSign,
      startCubie.position,
      normal,
    );
    if (move) {
      emit("move", move);
    }
  }
}

/**
 * @description 空间逻辑映射：将拖拽轴与法线组合转化为 Singmaster 指令
 * @param {THREE.Vector3} dragAxis 拖拽的主物理轴
 * @param {Number} sign 拖拽正负向
 * @param {THREE.Vector3} pos 目标方块坐标
 * @param {THREE.Vector3} normal 被点击面的法向
 * @returns {String|null} 指令字符串
 */
function getMoveCommand(dragAxis, sign, pos, normal) {
  const [x, y, z] = [Math.round(pos.x), Math.round(pos.y), Math.round(pos.z)];

  // Case 1: 前面 F (Z=1) 或 后面 B (Z=-1)
  if (Math.abs(normal.z) > 0.5) {
    const isFront = normal.z > 0;
    if (Math.abs(dragAxis.x) > 0.5) {
      const s = isFront ? sign : -sign;
      if (y === 1) return s > 0 ? "U'" : "U";
      if (y === -1) return s > 0 ? "D" : "D'";
    } else {
      const s = isFront ? sign : -sign;
      if (x === 1) return s > 0 ? "R" : "R'";
      if (x === -1) return s > 0 ? "L'" : "L";
    }
  }
  // Case 2: 顶面 U (Y=1) 或 底面 D (Y=-1)
  else if (Math.abs(normal.y) > 0.5) {
    const isTop = normal.y > 0;
    if (Math.abs(dragAxis.x) > 0.5) {
      const s = isTop ? sign : -sign;
      if (z === 1) return s > 0 ? "F" : "F'";
      if (z === -1) return s > 0 ? "B'" : "B";
    } else {
      const s = isTop ? -sign : sign;
      if (x === 1) return s > 0 ? "R" : "R'";
      if (x === -1) return s > 0 ? "L'" : "L";
    }
  }
  // Case 3: 右面 R (X=1) 或 左面 L (X=-1)
  else if (Math.abs(normal.x) > 0.5) {
    const isRight = normal.x > 0;
    if (Math.abs(dragAxis.y) > 0.5) {
      const s = isRight ? sign : -sign;
      if (z === 1) return s > 0 ? "F'" : "F";
      if (z === -1) return s > 0 ? "B" : "B'";
    } else {
      const s = isRight ? sign : -sign;
      if (y === 1) return s > 0 ? "U" : "U'";
      if (y === -1) return s > 0 ? "D'" : "D";
    }
  }
  return null;
}

// =========================================================
// 7. 生命周期与监听
// =========================================================
onMounted(async () => {
  await nextTick();
  initThree();
  renderCubies();
  animate();
  container.value.addEventListener("mousedown", onMouseDown);
  container.value.addEventListener("mousemove", onMouseMove);
  window.addEventListener("mouseup", onMouseUp);
  window.addEventListener("resize", onResize);
});

onUnmounted(() => {
  window.removeEventListener("resize", onResize);
  window.removeEventListener("mouseup", onMouseUp);
  if (container.value) {
    container.value.removeEventListener("mousedown", onMouseDown);
    container.value.removeEventListener("mousemove", onMouseMove);
  }
  if (renderer) renderer.dispose();
});

/** @description 核心数据监听：外部状态变更时触发重绘，但由于带有动画锁，不会打断旋转中的块 */
watch(
  normalizedState,
  () => {
    if (!isAnimating) renderCubies();
  },
  { deep: true },
);

/** @description 配置监听：使用 watchEffect 同步 Vue Prop 到 Three.js 命令式对象 */
watchEffect(() => {
  if (!controls) return;
  controls.enabled = props.enableControls;
  controls.autoRotate = props.autoRotate;
  controls.autoRotateSpeed = props.autoRotateSpeed;
  controls.enableZoom = props.enableZoom;
});

// =========================================================
// 8. 方法暴露
// =========================================================
defineExpose({
  playMove,
  triggerMove: playMove,
  resetView: () => controls?.reset(),
  renderCubies,
});
</script>

<style scoped>
.cube-3d-container {
  width: 100%;
  height: 100%;
  cursor: default;
  user-select: none;
}
.cube-3d-container.can-control {
  cursor: grab;
}
.cube-3d-container.can-control:active {
  cursor: grabbing;
}
</style>
