<template>
  <div ref="container" class="cube-3d-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick} from "vue";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import * as THREE from "three";

// ========================
// 组件 Props
// ========================
const props = defineProps({
  cubeState: { type: Object, required: true }
});

const container = ref(null);

// ========================
// Three.js 渲染变量
// ========================
let scene;
let camera;
let renderer;
let cubeGroup;
let controls;
let isAnimating = false;

// ========================
// 颜色映射配置
// ========================
const colorMap = {
  white: "#FFFFFF",
  yellow: "#FFD500",
  red: "#C41E3A",
  orange: "#FF5800",
  blue: "#0051BA",
  green: "#009E60"
};

// ========================
// 初始化 Three.js 环境
// ========================
function initThree() {
  scene = new THREE.Scene();

  const width = container.value.clientWidth;
  const height = container.value.clientHeight;

  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
  camera.position.set(6, 6, 6);
  camera.lookAt(0, 0, 0);

  renderer = new THREE.WebGLRenderer({ antialias: true , alpha: true});
  renderer.setSize(width, height);
  renderer.setPixelRatio(window.devicePixelRatio);
  container.value.appendChild(renderer.domElement);

  // 添加光源
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
  scene.add(ambientLight);
  const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
  dirLight.position.set(10, 20, 10);
  scene.add(dirLight);

  // 初始化轨道控制器 (鼠标交互的核心)
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true; // 开启阻尼滑动
  controls.dampingFactor = 0.05;
  controls.enablePan = false;    // 禁止右键平移
  controls.minDistance = 3;
  controls.maxDistance = 15;

  // 创建魔方组
  cubeGroup = new THREE.Group();
  scene.add(cubeGroup);
}

// ========================
// 获取 Cubie 六个面的颜色
// ========================
// 函数说明：
//   根据 cubie 的 3D 坐标 (x, y, z) 计算其六个面对应的颜色
//   解决 2D 面索引与 3D 坐标系方向不一致的问题
//
// 返回顺序：[R, L, U, D, F, B]
// 关键点：
//   - U/D 面需要反向处理 z 坐标
//   - F/B 面需要处理 x/y 坐标方向差异
//   - L/R 面需要处理 z/y 坐标方向差异
// ========================
function getCubieFaceColors(cubie, faces) {
  const res = [null, null, null, null, null, null];
  const [x, y, z] = cubie.pos;

  if (x === 1)  res[0] = getFaceColor("R", x, y, z, faces);
  if (x === -1) res[1] = getFaceColor("L", x, y, z, faces);
  if (y === 1)  res[2] = getFaceColor("U", x, y, z, faces);
  if (y === -1) res[3] = getFaceColor("D", x, y, z, faces);
  if (z === 1)  res[4] = getFaceColor("F", x, y, z, faces);
  if (z === -1) res[5] = getFaceColor("B", x, y, z, faces);

  return res;
}

// ========================
// 获取单个面的颜色
// ========================
function getFaceColor(face, x, y, z, faces) {
  let row, col;

  switch (face) {
    case "U":
      row = z + 1;      // z=-1->0, 0->1, 1->2
      col = x + 1;      // x=-1->0, 0->1, 1->2
      break;
    case "D":
      row = 0 - z + 1;  // z=-1->2, 0->1, 1->0
      col = x + 1;      // x=-1->0, 0->1, 1->2
      break;
    case "F":
      row = 1 - y;      // y=1->0, 0->1, -1->2
      col = x + 1;      // x=-1->0, 0->1, 1->2
      break;
    case "B":
      row = 1 - y;      // y=1->0, 0->1, -1->2
      col = 1 - x;      // x=-1->2, 0->1, 1->0
      break;
    case "R":
      row = 1 - y;      // y=1->0, 0->1, -1->2
      col = 1 - z;      // z=-1->2, 0->1, 1->0
      break;
    case "L":
      row = 1 - y;      // y=1->0, 0->1, -1->2
      col = z + 1;      // z=-1->0, 0->1, 1->2
      break;
  }

  return faces[face][row * 3 + col];
}

// ========================
// 创建单个 Cubie 的 Mesh
// ========================
function createCubieMesh(size, faceColors) {
  const geometry = new THREE.BoxGeometry(size, size, size);

  const materials = faceColors.map(c =>
    new THREE.MeshLambertMaterial({
      color: c ? colorMap[c] : 0x222222
    })
  );

  return new THREE.Mesh(geometry, materials);
}

// ========================
// 渲染所有 Cubies
// ========================
function renderCubies(cubies) {
  if (isAnimating) return;

  // 清空现有的 Cubies
  while (cubeGroup.children.length) {
    cubeGroup.remove(cubeGroup.children[0]);
  }

  const size = 0.95;

  // 渲染角块、棱块和中心块
  [...cubies.corners, ...cubies.edges, ...cubies.centers].forEach(c => {
    const colors = getCubieFaceColors(c, props.cubeState.faces);
    const mesh = createCubieMesh(size, colors);
    mesh.position.set(...c.pos);
    cubeGroup.add(mesh);
  });
}

// ========================
// 渲染循环
// ========================
function animate() {
  requestAnimationFrame(animate);
  // 将控制器绑定到相机上，此时魔方的坐标系是没有变的，改变的只是相机的位置
  if (controls) controls.update();
  renderer.render(scene, camera);
}

// ========================
// 播放旋转动画
// ========================
// 说明：执行指定的魔方转动操作，包括 3D 动画和数据同步

function playMove(move) {
  if (isAnimating) return;
  isAnimating = true;

  let axis = null;      // 旋转轴：'x', 'y', 'z'
  let layerValue = 0;   // 旋转层的位置：-1, 0, 1
  let angle = 0;        // 旋转角度

  // 解析转动指令
  switch (move) {
    case "R":   axis = "x"; layerValue = 1;  angle = -Math.PI / 2; break;
    case "R'":  axis = "x"; layerValue = 1;  angle = Math.PI / 2;  break;
    case "L":   axis = "x"; layerValue = -1; angle = Math.PI / 2;  break;
    case "L'":  axis = "x"; layerValue = -1; angle = -Math.PI / 2; break;
    case "U":   axis = "y"; layerValue = 1;  angle = -Math.PI / 2; break;
    case "U'":  axis = "y"; layerValue = 1;  angle = Math.PI / 2;  break;
    case "D":   axis = "y"; layerValue = -1; angle = Math.PI / 2;  break;
    case "D'":  axis = "y"; layerValue = -1; angle = -Math.PI / 2; break;
    case "F":   axis = "z"; layerValue = 1;  angle = -Math.PI / 2; break;
    case "F'":  axis = "z"; layerValue = 1;  angle = Math.PI / 2;  break;
    case "B":   axis = "z"; layerValue = -1; angle = Math.PI / 2;  break;
    case "B'":  axis = "z"; layerValue = -1; angle = -Math.PI / 2; break;
    case "R2":  axis = "x"; layerValue = 1;  angle = -Math.PI;     break;
    case "L2":  axis = "x"; layerValue = -1; angle = Math.PI;      break;
    case "U2":  axis = "y"; layerValue = 1;  angle = -Math.PI;     break;
    case "D2":  axis = "y"; layerValue = -1; angle = Math.PI;      break;
    case "F2":  axis = "z"; layerValue = 1;  angle = -Math.PI;     break;
    case "B2":  axis = "z"; layerValue = -1; angle = Math.PI;      break;
    default:
      console.warn("未识别的 move:", move);
      isAnimating = false;
      return;
  }

  // 选中需要旋转的 Cubie Meshes
  const targets = cubeGroup.children.filter(mesh => {
    const pos = mesh.position;
    return Math.round(pos[axis]) === layerValue;
  });

  // 创建临时旋转组
  const rotateGroup = new THREE.Group();
  scene.add(rotateGroup);
  targets.forEach(m => {
    cubeGroup.remove(m);
    rotateGroup.add(m);
  });

  // 执行动画
  const duration = 300;
  const start = performance.now();

  function rotate(time) {
    const t = Math.min((time - start) / duration, 1);
    rotateGroup.rotation[axis] = angle * t;

    if (t < 1) {
      requestAnimationFrame(rotate);
    } else {
      // 动画结束，应用旋转到每个 Mesh
      rotateGroup.updateMatrixWorld();
      while (rotateGroup.children.length) {
        const m = rotateGroup.children[0];
        m.applyMatrix4(rotateGroup.matrix);
        m.position.x = Math.round(m.position.x);
        m.position.y = Math.round(m.position.y);
        m.position.z = Math.round(m.position.z);
        rotateGroup.remove(m);
        cubeGroup.add(m);
      }
      scene.remove(rotateGroup);
      isAnimating = false;
    }
  }

  requestAnimationFrame(rotate);
}

function resetView() {
  if (controls) controls.reset();
}
// ========================
// 暴露方法给父组件
// ========================
defineExpose({ playMove, resetView, renderCubies});

// ========================
// 组件生命周期
// ========================
onMounted(async () => {
  await nextTick();
  initThree();
  renderCubies(props.cubeState.cubies);
  animate();
  window.addEventListener("resize", onResize);
});

onUnmounted(() => {
  window.removeEventListener("resize", onResize);
  if(renderer) renderer.dispose();
});

function onResize() {
  if (!container.value || !camera || !renderer) return;
  const w = container.value.clientWidth;
  const h = container.value.clientHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
}
// ========================
// 监听数据变化
// ========================
watch(
  () => props.cubeState.cubies,
  (newC) => {
    if (!isAnimating) renderCubies(newC);
  },
  { deep: true }
);
</script>

<style scoped>
.cube-3d-container {
  width: 100%;
  height: 100%;
  cursor: grab;
}

.cube-3d-container:active {
  cursor: grabbing;
}
</style>