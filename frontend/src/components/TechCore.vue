<template>
  <div class="lab-container">
    <div ref="stage" class="webgl-stage"></div>

    <div class="control-panel">
      <h2 class="title">Three.js 基础实验室</h2>

      <section class="module">
        <h3>📍 空间辅助 (Helpers)</h3>
        <div class="toggle-group">
          <label
            ><input type="checkbox" v-model="showAxes" @change="toggleAxes" />
            坐标轴 (RGB = XYZ)</label
          >
          <label
            ><input type="checkbox" v-model="showGrid" @change="toggleGrid" />
            水平网格 (XZ平面)</label
          >
        </div>
        <p class="tip">红色: X轴 | 绿色: Y轴 | 蓝色: Z轴</p>
      </section>

      <section class="module">
        <h3>📐 几何变换 (Transform)</h3>
        <div class="btn-grid">
          <button @click="resetTransform">重置变换</button>
          <button @click="isRotating = !isRotating">
            {{ isRotating ? "停止动画" : "开启旋转" }}
          </button>
        </div>
        <div class="slider-item">
          <span>Y轴高度:</span>
          <input
            type="range"
            min="0"
            max="5"
            step="0.1"
            v-model="cubeY"
            @input="updatePosition"
          />
        </div>
      </section>

      <section class="module">
        <h3>💡 灯光实验 (Lighting)</h3>
        <button @click="toggleLight">
          {{ lightEnabled ? "关闭主光源" : "开启主光源" }}
        </button>
        <p class="tip">关闭后物体变黑，证明 MeshStandardMaterial 依赖光照。</p>
      </section>

      <section class="module">
        <h3>🧱 材质模式 (Material)</h3>
        <button @click="toggleWireframe">
          {{ isWireframe ? "关闭线框模式" : "开启线框模式" }}
        </button>
        <p class="tip">
          线框模式显示物体的几何结构，有助于理解顶点和边的分布。
        </p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

// 响应式状态控制
const stage = ref(null);
const showAxes = ref(true);
const showGrid = ref(true);
const isRotating = ref(false);
const lightEnabled = ref(true);
const cubeY = ref(1);
const isWireframe = ref(false);

// Three.js 核心对象
let scene,
  camera,
  renderer,
  controls,
  cube,
  axesHelper,
  gridHelper,
  mainLight,
  animationId;

const initLab = () => {
  const w = stage.value.clientWidth;
  const h = stage.value.clientHeight;

  // --- [知识点: Scene] 容器 ---
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0xeeeeee);

  // --- [知识点: Camera] 透视相机 ---
  // 50度角，靠近物体，方便观察细节
  camera = new THREE.PerspectiveCamera(50, w / h, 0.1, 1000);
  camera.position.set(5, 5, 5);

  // --- [知识点: Renderer] 渲染器 ---
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(w, h);
  stage.value.appendChild(renderer.domElement);

  // --- [知识点: Controls] 交互 ---
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;

  // --- [知识点: Helpers] 坐标线和网格辅助工具 ---
  axesHelper = new THREE.AxesHelper(5); // 参数 5 表示轴的长度
  scene.add(axesHelper);

  gridHelper = new THREE.GridHelper(10, 10); // 10x10的网格
  scene.add(gridHelper);

  // --- [知识点: Mesh] 物体 = 几何体 + 材质 ---
  const geometry = new THREE.BoxGeometry(2, 2, 2);
  const material = new THREE.MeshStandardMaterial({
    color: 0x3498db,
    roughness: 0.3,
  });
  cube = new THREE.Mesh(geometry, material);
  cube.position.y = 1; // 初始高度，使其位于网格上方
  scene.add(cube);

  // --- [知识点: Light] 光源 ---
  const ambient = new THREE.AmbientLight(0xffffff, 0.5);
  scene.add(ambient);

  mainLight = new THREE.DirectionalLight(0xffffff, 1);
  mainLight.position.set(5, 10, 5);
  scene.add(mainLight);

  render();
};

// 动画循环
const render = () => {
  animationId = requestAnimationFrame(render);
  if (isRotating.value) {
    cube.rotation.y += 0.005;
  }
  controls.update();
  renderer.render(scene, camera);
};

// --- 实验交互方法 ---

const toggleAxes = () => {
  axesHelper.visible = showAxes.value;
};
const toggleGrid = () => {
  gridHelper.visible = showGrid.value;
};

const updatePosition = () => {
  cube.position.y = parseFloat(cubeY.value);
};

const toggleLight = () => {
  lightEnabled.value = !lightEnabled.value;
  mainLight.intensity = lightEnabled.value ? 1 : 0;
};

const toggleWireframe = () => {
  isWireframe.value = !isWireframe.value;
  // 修改物体材质的属性
  cube.material.wireframe = isWireframe.value;
};

const resetTransform = () => {
  cube.rotation.set(0, 0, 0);
  cube.scale.set(1, 1, 1);
  cubeY.value = 1;
  cube.position.y = 1;
  isRotating.value = false;
};

// 窗口自适应
const handleResize = () => {
  if (!stage.value) return;
  camera.aspect = stage.value.clientWidth / stage.value.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(stage.value.clientWidth, stage.value.clientHeight);
};

onMounted(() => {
  initLab();
  window.addEventListener("resize", handleResize);
});

onUnmounted(() => {
  cancelAnimationFrame(animationId);
  renderer.dispose();
  window.removeEventListener("resize", handleResize);
});
</script>

<style scoped>
.lab-container {
  display: flex;
  width: 100%;
  height: 60vh;
  background: #fff;
  border: 2px solid #ddd;
  font-family: sans-serif;
}

.webgl-stage {
  flex: 1;
  background: #ccc;
}

.control-panel {
  width: 300px;
  background: #f9f9f9;
  padding: 20px;
  border-left: 2px solid #ddd;
  overflow-y: auto;
  color: #333;
}

.title {
  margin-top: 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #3498db;
  font-size: 1.2rem;
}

.module {
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.module h3 {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 10px;
}

.toggle-group label {
  display: block;
  margin: 8px 0;
  font-size: 0.85rem;
  cursor: pointer;
}

.btn-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 15px;
}

button {
  padding: 8px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

button:hover {
  background: #2980b9;
}

.slider-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.85rem;
}

input[type="range"] {
  flex: 1;
}

.tip {
  font-size: 0.75rem;
  color: #999;
  margin-top: 8px;
  line-height: 1.4;
}

/* Dark Mode Styles */
[data-theme="dark"] .lab-container {
  background: var(--dm-bg-card);
  border: 2px solid var(--dm-border);
}

[data-theme="dark"] .control-panel {
  background: var(--dm-bg-page);
  border-left: 2px solid var(--dm-border);
  color: var(--dm-text-body);
}

[data-theme="dark"] .title {
  border-bottom: 2px solid var(--dm-accent);
  color: var(--dm-text-primary);
}

[data-theme="dark"] .module {
  border-bottom: 1px solid var(--dm-border);
}

[data-theme="dark"] .module h3 {
  color: var(--dm-text-secondary);
}

[data-theme="dark"] .toggle-group label {
  color: var(--dm-text-body);
}

[data-theme="dark"] button {
  background: var(--dm-accent);
  color: var(--dm-text-primary);
}

[data-theme="dark"] button:hover {
  background: var(--dm-accent-hover);
}

[data-theme="dark"] .slider-item {
  color: var(--dm-text-body);
}

[data-theme="dark"] .tip {
  color: var(--dm-text-muted);
}
</style>
