<template>
  <div ref="container" class="cube-3d-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from "vue";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

// =========================================================
// 1. 配置与常量
// =========================================================
const props = defineProps({
  cubeState: { type: Object, required: true }
});
const emit = defineEmits(['move']);

const DRAG_THRESHOLD = 35; // 拖拽触发阈值（像素）
const ANIMATION_DURATION = 300; // 旋转动画时长（毫秒）
const CUBIE_SIZE = 0.95; // 小块尺寸

const COLOR_MAP = {
  white: "#FFFFFF",
  yellow: "#FFD500",
  red: "#C41E3A",
  orange: "#FF5800",
  blue: "#0051BA",
  green: "#009E60",
  internal: "#222222"
};

// =========================================================
// 2. 响应式引用与全局变量
// =========================================================
const container = ref(null);

// Three.js 核心对象
let scene, camera, renderer, cubeGroup, controls;

// 交互状态
let isAnimating = false;
let isMouseDown = false;
let startCubie = null;
let startNormal = null;
const mouse = new THREE.Vector2();
const startMousePos = new THREE.Vector2();
const raycaster = new THREE.Raycaster();

// =========================================================
// 3. Three.js 初始化与生命周期
// =========================================================

/** 初始化环境 */
function initThree() {
  const width = container.value.clientWidth;
  const height = container.value.clientHeight;

  scene = new THREE.Scene();

  // 相机设置
  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
  camera.position.set(6, 6, 6);
  camera.lookAt(0, 0, 0);

  // 渲染器设置
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(window.devicePixelRatio);
  container.value.appendChild(renderer.domElement);

  // 光照
  scene.add(new THREE.AmbientLight(0xffffff, 0.6));
  const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
  dirLight.position.set(10, 20, 10);
  scene.add(dirLight);

  // 控制器
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.enablePan = false;
  controls.minDistance = 3;
  controls.maxDistance = 15;

  // 魔方容器
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
// 4. 魔方构建逻辑 (数据 -> 3D 视图)
// =========================================================

/** 获取单个面的颜色索引 */
function getFaceColor(face, x, y, z, faces) {
  let row, col;
  switch (face) {
    case "U": row = z + 1; col = x + 1; break;
    case "D": row = 0 - z + 1; col = x + 1; break;
    case "F": row = 1 - y; col = x + 1; break;
    case "B": row = 1 - y; col = 1 - x; break;
    case "R": row = 1 - y; col = 1 - z; break;
    case "L": row = 1 - y; col = z + 1; break;
  }
  return faces[face][row * 3 + col];
}

/** 计算小块六个面的颜色数组 [R, L, U, D, F, B] */
function getCubieFaceColors(cubie, faces) {
  const res = Array(6).fill(null);
  const [x, y, z] = cubie.pos;
  if (x === 1)  res[0] = getFaceColor("R", x, y, z, faces);
  if (x === -1) res[1] = getFaceColor("L", x, y, z, faces);
  if (y === 1)  res[2] = getFaceColor("U", x, y, z, faces);
  if (y === -1) res[3] = getFaceColor("D", x, y, z, faces);
  if (z === 1)  res[4] = getFaceColor("F", x, y, z, faces);
  if (z === -1) res[5] = getFaceColor("B", x, y, z, faces);
  return res;
}

/** 渲染所有小块 */
function renderCubies(cubies) {
  if (isAnimating) return;
  while (cubeGroup.children.length) cubeGroup.remove(cubeGroup.children[0]);

  const allCubies = [...cubies.corners, ...cubies.edges, ...cubies.centers];
  allCubies.forEach(c => {
    const faceColors = getCubieFaceColors(c, props.cubeState.faces);
    const geometry = new THREE.BoxGeometry(CUBIE_SIZE, CUBIE_SIZE, CUBIE_SIZE);
    const materials = faceColors.map(color =>
      new THREE.MeshLambertMaterial({ color: color ? COLOR_MAP[color] : COLOR_MAP.internal })
    );
    const mesh = new THREE.Mesh(geometry, materials);
    mesh.position.set(...c.pos);
    cubeGroup.add(mesh);
  });
}

// =========================================================
// 5. 动画引擎
// =========================================================

/** 播放单步骤旋转动画 */
function playMove(move) {
  if (isAnimating) return;
  isAnimating = true;

  let axis, layerValue, angle;
  // 指令解析
  const moveMap = {
    "R":  { axis: 'x', lv: 1,  a: -Math.PI/2 }, "R'": { axis: 'x', lv: 1,  a: Math.PI/2 },
    "L":  { axis: 'x', lv: -1, a: Math.PI/2 },  "L'": { axis: 'x', lv: -1, a: -Math.PI/2 },
    "U":  { axis: 'y', lv: 1,  a: -Math.PI/2 }, "U'": { axis: 'y', lv: 1,  a: Math.PI/2 },
    "D":  { axis: 'y', lv: -1, a: Math.PI/2 },  "D'": { axis: 'y', lv: -1, a: -Math.PI/2 },
    "F":  { axis: 'z', lv: 1,  a: -Math.PI/2 }, "F'": { axis: 'z', lv: 1,  a: Math.PI/2 },
    "B":  { axis: 'z', lv: -1, a: Math.PI/2 },  "B'": { axis: 'z', lv: -1, a: -Math.PI/2 },
    "R2": { axis: 'x', lv: 1,  a: -Math.PI },    "L2": { axis: 'x', lv: -1, a: Math.PI },
    "U2": { axis: 'y', lv: 1,  a: -Math.PI },    "D2": { axis: 'y', lv: -1, a: Math.PI },
    "F2": { axis: 'z', lv: 1,  a: -Math.PI },    "B2": { axis: 'z', lv: -1, a: Math.PI }
  };

  const config = moveMap[move];
  if (!config) { isAnimating = false; return; }
  ({ axis, lv: layerValue, a: angle } = config);

  const targets = cubeGroup.children.filter(m => Math.round(m.position[axis]) === layerValue);
  const rotateGroup = new THREE.Group();
  scene.add(rotateGroup);
  targets.forEach(m => { cubeGroup.remove(m); rotateGroup.add(m); });

  const start = performance.now();
  function step(now) {
    const t = Math.min((now - start) / ANIMATION_DURATION, 1);
    rotateGroup.rotation[axis] = angle * t;
    if (t < 1) {
      requestAnimationFrame(step);
    } else {
      rotateGroup.updateMatrixWorld();
      while (rotateGroup.children.length) {
        const m = rotateGroup.children[0];
        m.applyMatrix4(rotateGroup.matrix);
        ["x", "y", "z"].forEach(coord => m.position[coord] = Math.round(m.position[coord]));
        rotateGroup.remove(m);
        cubeGroup.add(m);
      }
      scene.remove(rotateGroup);
      isAnimating = false;
    }
  }
  requestAnimationFrame(step);
}

// =========================================================
// 6. 交互处理逻辑
// =========================================================

function onMouseDown(event) {
  if (isAnimating) return;
  const rect = container.value.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(cubeGroup.children);

  if (intersects.length > 0) {
    const intersect = intersects[0];
    startCubie = intersect.object;
    // 转换法向量到世界坐标并规范化
    startNormal = intersect.face.normal.clone().applyQuaternion(startCubie.quaternion);
    ["x", "y", "z"].forEach(a => startNormal[a] = Math.round(startNormal[a]));

    startMousePos.set(event.clientX, event.clientY);
    isMouseDown = true;
    controls.enabled = false;
  }
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

function onMouseUp() {
  isMouseDown = false;
  startCubie = null;
  startNormal = null;
  controls.enabled = true;
}

/** 处理拖拽触发的旋转 */
function handleCubeRotation(dragDir) {
  const normal = startNormal;
  let possibleAxes = [];

  // 根据法向确定可能的滑动轴
  if (Math.abs(normal.x) > 0.5) possibleAxes = [new THREE.Vector3(0, 1, 0), new THREE.Vector3(0, 0, 1)];
  else if (Math.abs(normal.y) > 0.5) possibleAxes = [new THREE.Vector3(1, 0, 0), new THREE.Vector3(0, 0, 1)];
  else possibleAxes = [new THREE.Vector3(1, 0, 0), new THREE.Vector3(0, 1, 0)];

  let bestDragAxis = null, maxDot = -1, moveSign = 1;

  possibleAxes.forEach(axis => {
    const p1 = startCubie.position.clone().project(camera);
    const p2 = startCubie.position.clone().add(axis).project(camera);
    const screenVector = new THREE.Vector2(p2.x - p1.x, p2.y - p1.y).normalize();
    const dot = dragDir.dot(screenVector);
    if (Math.abs(dot) > maxDot) {
      maxDot = Math.abs(dot);
      bestDragAxis = axis;
      moveSign = dot > 0 ? 1 : -1;
    }
  });

  if (bestDragAxis && maxDot > 0.5) {
    const move = getMoveCommand(bestDragAxis, moveSign, startCubie.position, normal);
    if (move) {
      emit('move', move);
      playMove(move);
    }
  }
}

// =========================================================
// 7. 核心映射算法 (UI 拖拽 -> 魔方指令)
// =========================================================

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
// 8. 生命周期与监听
// =========================================================

onMounted(async () => {
  await nextTick();
  initThree();
  renderCubies(props.cubeState.cubies);
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

watch(() => props.cubeState.cubies, (newC) => {
  if (!isAnimating) renderCubies(newC);
}, { deep: true });

defineExpose({ playMove, resetView: () => controls?.reset(), renderCubies });
</script>

<style scoped>
.cube-3d-container {
  width: 100%;
  height: 100%;
  cursor: grab;
  user-select: none; /* 防止拖拽时选中文字 */
}
.cube-3d-container:active {
  cursor: grabbing;
}
</style>