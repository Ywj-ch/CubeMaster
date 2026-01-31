<template>
  <div
    ref="container"
    class="cube-3d-container"
    :class="{ 'can-control': props.enableControls }"
  ></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from "vue";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

// =========================================================
// 1. 配置与常量
// =========================================================
const props = defineProps({
  // 支持两种格式：
  // 1. 复杂对象 { faces: {...}, cubies: {...} } (兼容旧代码)
  // 2. 简单数组 [U[], R[], F[], D[], L[], B[]] (教学模块用)
  cubeState: { type: [Object, Array], required: true },

  interactive: { type: Boolean, default: true },
  enableControls: { type: Boolean, default: true },
  autoRotate: { type: Boolean, default: false },
  autoRotateSpeed: { type: Number, default: 4.0 },
  cameraPosition: { type: Array, default: () => [6, 6, 6] },
  enableZoom: { type: Boolean, default: true },
  moveDuration: { type: Number, default: 300 },
});

const emit = defineEmits(["move"]);

const DRAG_THRESHOLD = 35;
const CUBIE_SIZE = 0.95;

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

// 生成默认的魔方块空间坐标 (x, y, z from -1 to 1)
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

const BASE_CUBIES = generateBaseCubies();

// 归一化状态：无论传入 Array 还是 Object，都转为统一格式供渲染使用
const normalizedState = computed(() => {
  // 情况 A: 传入的是简单数组 (来自 cubeLogic.js / TutorialCube)
  // 索引映射: 0:U, 1:R, 2:F, 3:D, 4:L, 5:B
  if (Array.isArray(props.cubeState)) {
    return {
      cubies: BASE_CUBIES, // 使用自动生成的坐标
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
  // 情况 B: 传入的是复杂对象 (来自 Solver / Free 模式)
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

  // 应用 Props 配置
  controls.enabled = props.enableControls;
  controls.autoRotate = props.autoRotate;
  controls.autoRotateSpeed = props.autoRotateSpeed;
  controls.enableZoom = props.enableZoom;

  cubeGroup = new THREE.Group();
  scene.add(cubeGroup);
}

function animate() {
  requestAnimationFrame(animate);
  if (controls) controls.update();
  if (renderer && scene && camera) renderer.render(scene, camera);
}

function onResize() {
  if (!container.value || !camera || !renderer) return;
  const w = container.value.clientWidth;
  const h = container.value.clientHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
}

// =========================================================
// 4. 渲染逻辑 (使用 normalizedState)
// =========================================================
function getFaceColor(face, x, y, z, faces) {
  let row, col;
  // 这里的映射逻辑必须与 cubeLogic.js 的扁平化逻辑一致
  switch (face) {
    case "U":
      row = z + 1;
      col = x + 1;
      break;
    case "D":
      row = 0 - z + 1;
      col = x + 1;
      break; // 注意 D 面的坐标映射
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
  // 容错处理：如果 faces 数据没准备好，返回黑色
  if (!faces || !faces[face]) return "black";
  return faces[face][row * 3 + col];
}

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

function renderCubies() {
  if (isAnimating || !cubeGroup) return;

  // 清空旧模型
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
    // 绑定数据以便交互检测
    mesh.userData = { isCubie: true };
    cubeGroup.add(mesh);
  });
}

// =========================================================
// 5. 动画引擎 (支持 Promise)
// =========================================================
function playMove(move) {
  return new Promise((resolve) => {
    if (isAnimating) {
      resolve(); // 如果正在动画，直接跳过
      return;
    }
    isAnimating = true;

    let axis, layerValue, angle;
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

    const targets = cubeGroup.children.filter(
      (m) => Math.round(m.position[axis]) === layerValue,
    );
    const rotateGroup = new THREE.Group();
    scene.add(rotateGroup);
    targets.forEach((m) => {
      cubeGroup.remove(m);
      rotateGroup.add(m);
    });

    const start = performance.now();
    function step(now) {
      const t = Math.min((now - start) / props.moveDuration, 1);
      rotateGroup.rotation[axis] = angle * t;

      if (t < 1) {
        requestAnimationFrame(step);
      } else {
        // 动画结束
        rotateGroup.updateMatrixWorld();
        while (rotateGroup.children.length) {
          const m = rotateGroup.children[0];
          m.applyMatrix4(rotateGroup.matrix);
          ["x", "y", "z"].forEach(
            (coord) => (m.position[coord] = Math.round(m.position[coord])),
          );
          rotateGroup.remove(m);
          cubeGroup.add(m);
        }
        scene.remove(rotateGroup);
        isAnimating = false;
        resolve(); // 关键：动画完成，解除 Promise
      }
    }
    requestAnimationFrame(step);
  });
}

// =========================================================
// 6. 交互处理
// =========================================================
function onMouseDown(event) {
  if (isAnimating || !props.interactive) return; // 交互锁

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

function onMouseUp() {
  isMouseDown = false;
  startCubie = null;
  startNormal = null;
  if (controls) controls.enabled = props.enableControls;
}

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

function handleCubeRotation(dragDir) {
  const normal = startNormal;
  let possibleAxes = [];

  // 根据法向确定可能的滑动轴
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
  renderCubies(); // 使用新的渲染逻辑
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

// 监听归一化后的状态变化
watch(
  normalizedState,
  () => {
    if (!isAnimating) renderCubies();
  },
  { deep: true },
);

// 监听配置变化
watch(
  () => props.enableControls,
  (val) => {
    if (controls) controls.enabled = val;
  },
);
watch(
  () => props.autoRotate,
  (val) => {
    if (controls) controls.autoRotate = val;
  },
);
watch(
  () => props.autoRotateSpeed,
  (val) => {
    if (controls) controls.autoRotateSpeed = val;
  },
);
watch(
  () => props.enableZoom,
  (val) => {
    if (controls) controls.enableZoom = val;
  },
);

// 暴露方法
defineExpose({
  playMove,
  triggerMove: playMove, // 别名，兼容 TutorialCube
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
