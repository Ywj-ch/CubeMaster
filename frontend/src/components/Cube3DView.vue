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
import { RoundedBoxGeometry } from "three/examples/jsm/geometries/RoundedBoxGeometry";
import { TextureLoader } from "three";
import { getTextureUrl } from "../utils/cubeCustomization";
import { COLOR_MAP } from "../constants/colors";

// 纹理加载器与缓存
const textureLoader = new TextureLoader();
const textureCache = new Map();
// 正在加载的纹理URL集合，防止重复加载和跟踪加载状态
const loadingTextures = new Set();

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
  customization: { type: Object, default: null },
});

/** @description 定义自定义事件，用于通知父组件发生了交互旋转 */
const emit = defineEmits(["move"]);

/** @constant {Number} DRAG_THRESHOLD 触发旋转的最小拖拽像素距离 */
const DRAG_THRESHOLD = 35;
/** @constant {Number} CUBIE_SIZE 单个小方块的几何尺寸 */
const CUBIE_SIZE = 0.95;

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
let ambientLight, directionalLight;
let isAnimating = false;
let isMouseDown = false;
let startCubie = null;
let startNormal = null;
const mouse = new THREE.Vector2();
const startMousePos = new THREE.Vector2();
const raycaster = new THREE.Raycaster();

// 调试模式：显示线框
const debugWireframe = ref(false);
// 配置更新防抖计时器
const configUpdateTimer = ref(null);

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

  ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
  scene.add(ambientLight);

  directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
  directionalLight.position.set(10, 20, 10);
  scene.add(directionalLight);

  // 初始应用自定义光照配置
  updateLighting();

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

/**
 * @description 更新光照设置基于自定义配置
 */
function updateLighting() {
  if (!ambientLight || !directionalLight) return;

  const config = props.customization;
  if (!config || !config.lighting) return;

  const lighting = config.lighting;

  // 更新环境光
  ambientLight.intensity = lighting.ambientIntensity || 0.4;

  // 更新方向光
  directionalLight.intensity = lighting.directionalIntensity || 0.8;
  directionalLight.color = new THREE.Color(
    lighting.directionalColor || "#ffffff",
  );
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
 * @description 加载纹理
 * @param {Object} config 自定义配置
 * @returns {THREE.Texture|null} 纹理对象
 */
function loadTexture(config) {
  if (!config || !config.texture || config.texture.type === "none") {
    return null;
  }
  const textureUrl = getTextureUrl(config.texture);
  if (!textureUrl) return null;

  const cacheKey = textureUrl;
  if (textureCache.has(cacheKey)) {
    return textureCache.get(cacheKey);
  }

  loadingTextures.add(cacheKey);
  const texture = textureLoader.load(
    textureUrl,
    (tex) => {
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(1, 1);
      tex.needsUpdate = true;
      // 加载成功，从加载中集合移除
      loadingTextures.delete(cacheKey);
    },
    undefined,
    (error) => {
      // 从加载中集合移除
      loadingTextures.delete(cacheKey);

      // 检查是否为可忽略的错误类型
      let shouldIgnore = false;

      if (!error) {
        // 错误对象为null/undefined
        shouldIgnore = true;
      } else if (!error.target) {
        // 目标为null（可能已清理或组件已卸载）
        shouldIgnore = true;
      } else if (error.target.naturalWidth && error.target.naturalWidth > 0) {
        // 图片实际上加载成功了（naturalWidth > 0），但可能触发了某些事件
        shouldIgnore = true;
      } else if (error.type === "abort") {
        // 加载被中止
        shouldIgnore = true;
      } else if (
        error.message &&
        (error.message.includes("cancel") || error.message.includes("load"))
      ) {
        // 取消相关错误或一般加载错误
        shouldIgnore = true;
      } else if (typeof error === "string" && error.includes("cancel")) {
        // 字符串类型的取消错误
        shouldIgnore = true;
      }

      if (!shouldIgnore) {
        console.error("纹理加载失败:", error);
        // 真正的失败，从缓存中移除
        textureCache.delete(cacheKey);
      }
      // 对于可忽略的错误，保留缓存条目（纹理可能实际上已加载成功）
    },
  );
  textureCache.set(cacheKey, texture);
  return texture;
}

/**
 * @description 根据自定义配置创建面材质
 * @param {string} color 颜色名称
 * @param {Object} config 自定义配置
 * @returns {THREE.Material} Three.js材质
 */
function createFaceMaterial(color, config) {
  if (!config) {
    // 默认材质
    return new THREE.MeshLambertMaterial({
      color: color ? COLOR_MAP[color] : COLOR_MAP.internal,
    });
  }

  const baseColor = color ? COLOR_MAP[color] : COLOR_MAP.internal;
  const params = config.materialParams || {};
  const texture = loadTexture(config);

  // 基础材质选项
  const baseOptions = {
    color: baseColor,
    opacity: params.opacity || 1.0,
    transparent: params.opacity < 1.0,
  };

  // 如果存在纹理，添加map属性
  if (texture) {
    baseOptions.map = texture;
  }

  // 根据材质类型创建不同的材质
  switch (config.materialType) {
    case "basic":
      return new THREE.MeshBasicMaterial(baseOptions);

    case "lambert":
      return new THREE.MeshLambertMaterial(baseOptions);

    case "phong":
      return new THREE.MeshPhongMaterial({
        ...baseOptions,
        shininess: params.shininess || 30,
      });

    case "standard":
      return new THREE.MeshStandardMaterial({
        ...baseOptions,
        roughness: params.roughness || 0.5,
        metalness: params.metalness || 0,
      });

    case "toon":
      return new THREE.MeshToonMaterial(baseOptions);

    default:
      return new THREE.MeshLambertMaterial(baseOptions);
  }
}

/**
 * @description 根据自定义配置创建几何体
 * @param {Object} config 自定义配置
 * @returns {THREE.BufferGeometry} Three.js几何体
 */
function createGeometry(config) {
  // 检查Three.js环境

  if (!config || !config.geometry || config.geometry.type !== "rounded") {
    // 标准方块几何体

    return new THREE.BoxGeometry(CUBIE_SIZE, CUBIE_SIZE, CUBIE_SIZE);
  }

  // 圆角方块几何体

  // 圆角半径计算：使用配置参数
  const cornerRadius = config.geometry.cornerRadius || 0.1;
  let segments = config.geometry.segments || 4;
  let radius = cornerRadius * CUBIE_SIZE;

  // 验证半径有效性
  if (isNaN(radius) || radius <= 0) {
    console.error("❌ 无效的半径值:", radius);
    return new THREE.BoxGeometry(CUBIE_SIZE, CUBIE_SIZE, CUBIE_SIZE);
  }
  const maxRadius = CUBIE_SIZE * 0.5;
  if (radius > maxRadius) {
    console.warn("⚠️ 半径超过最大限制，已截断:", radius, ">", maxRadius);
    radius = maxRadius;
  }

  try {
    // 检查 RoundedBoxGeometry 是否可用
    if (typeof RoundedBoxGeometry === "undefined") {
      console.error("RoundedBoxGeometry 未定义，请检查导入");
      return new THREE.BoxGeometry(CUBIE_SIZE, CUBIE_SIZE, CUBIE_SIZE);
    }

    // 测试RoundedBoxGeometry基本功能

    let RoundedBoxGeometryConstructor = RoundedBoxGeometry;

    // 检查是否可以通过THREE访问
    if (THREE.RoundedBoxGeometry && !RoundedBoxGeometry) {
      RoundedBoxGeometryConstructor = THREE.RoundedBoxGeometry;
    }

    try {
      const testGeometry = new RoundedBoxGeometryConstructor(1, 1, 1, 0.3, 8);
    } catch (testError) {
      console.error("🧪 测试失败:", testError.message);
      // 尝试参数顺序交换

      try {
        const testGeometry2 = new RoundedBoxGeometryConstructor(
          1,
          1,
          1,
          8,
          0.3,
        );

        // 如果这个成功，更新参数顺序
        segments = Math.max(segments, 1); // 确保有效
        radius = Math.min(radius, CUBIE_SIZE * 0.49); // 留有余地
      } catch (testError2) {
        console.error("🔄 参数顺序也失败:", testError2.message);
      }
    }

    // 确定参数顺序 - 基于测试结果
    let useSegmentsFirst = false;

    // 测试两种参数顺序

    try {
      // 测试顺序1: width, height, depth, radius, segments
      const test1 = new RoundedBoxGeometryConstructor(1, 1, 1, 0.3, 8);
      const vertices1 = test1.attributes.position?.count || 0;

      // 测试顺序2: width, height, depth, segments, radius
      const test2 = new RoundedBoxGeometryConstructor(1, 1, 1, 8, 0.3);
      const vertices2 = test2.attributes.position?.count || 0;

      // 选择顶点数较多的顺序（应该是真正的圆角几何体）
      if (vertices2 > vertices1 && vertices2 > 36) {
        useSegmentsFirst = true;
      } else if (vertices1 > 36) {
      } else {
      }
    } catch (orderError) {
      console.error("🔄 参数顺序测试失败:", orderError.message);
    }

    // 创建圆角方块几何体
    let geometry;
    if (useSegmentsFirst) {
      geometry = new RoundedBoxGeometryConstructor(
        CUBIE_SIZE,
        CUBIE_SIZE,
        CUBIE_SIZE,
        segments,
        radius,
      );
    } else {
      geometry = new RoundedBoxGeometryConstructor(
        CUBIE_SIZE,
        CUBIE_SIZE,
        CUBIE_SIZE,
        radius,
        segments,
      );
    }

    // 最终验证
    const finalVertexCount = geometry.attributes.position?.count;
    if (finalVertexCount && finalVertexCount <= 36) {
      console.error("❌ 最终几何体仍是标准方块！顶点数:", finalVertexCount);

      return new THREE.BoxGeometry(CUBIE_SIZE, CUBIE_SIZE, CUBIE_SIZE);
    }

    return geometry;
  } catch (error) {
    console.error("创建圆角几何体失败:", error);
    // 回退到标准方块
    return new THREE.BoxGeometry(CUBIE_SIZE, CUBIE_SIZE, CUBIE_SIZE);
  }
}

/**
 * @description 核心渲染函数：根据逻辑状态构建/刷新 3D 网格模型
 * 包含内存清理机制（旧模型销毁）与基于自定义配置的多材质构建
 */
function renderCubies() {
  if (isAnimating || !cubeGroup) {
    return;
  }

  const beforeCount = cubeGroup.children.length;

  while (cubeGroup.children.length) cubeGroup.remove(cubeGroup.children[0]);

  const state = normalizedState.value;
  const allCubies = [
    ...state.cubies.corners,
    ...state.cubies.edges,
    ...state.cubies.centers,
  ];

  let successCount = 0;
  let errorCount = 0;

  allCubies.forEach((c, index) => {
    try {
      const faceColors = getCubieFaceColors(c, state.faces);
      const geometry = createGeometry(props.customization);
      const materials = faceColors.map((color) =>
        createFaceMaterial(color, props.customization),
      );
      const mesh = new THREE.Mesh(geometry, materials);
      mesh.position.set(...c.pos);
      mesh.userData = { isCubie: true };
      cubeGroup.add(mesh);

      if (index === 0) {
      }
      successCount++;
    } catch (error) {
      errorCount++;
      console.error(`创建第 ${index} 个网格时出错:`, error);
      console.error("错误详情:", error.message, error.stack);

      // 尝试使用默认几何体作为后备
      try {
        const faceColors = getCubieFaceColors(c, state.faces);
        const fallbackGeometry = new THREE.BoxGeometry(
          CUBIE_SIZE,
          CUBIE_SIZE,
          CUBIE_SIZE,
        );
        const materials = faceColors.map((color) =>
          createFaceMaterial(color, props.customization),
        );
        const mesh = new THREE.Mesh(fallbackGeometry, materials);
        mesh.position.set(...c.pos);
        mesh.userData = { isCubie: true };
        cubeGroup.add(mesh);
        successCount++;
      } catch (fallbackError) {
        console.error(`后备几何体也失败:`, fallbackError);
      }
    }
  });

  // 强制更新矩阵
  cubeGroup.updateMatrixWorld(true);

  // 标记所有对象需要更新矩阵
  scene.traverse((obj) => {
    obj.matrixWorldNeedsUpdate = true;
  });

  // 手动触发一次渲染
  if (renderer && scene && camera) {
    renderer.render(scene, camera);
  }
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
  // 清理加载状态，防止组件卸载后错误回调触发
  loadingTextures.clear();
  // 清理配置更新计时器
  if (configUpdateTimer.value) {
    clearTimeout(configUpdateTimer.value);
    configUpdateTimer.value = null;
  }
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

/** @description 监听自定义配置变化，更新材质和光照（带防抖避免频繁纹理重载） */
watch(
  () => props.customization,
  (newConfig, oldConfig) => {
    updateLighting();
    if (!isAnimating) {
      // 清除之前的计时器
      if (configUpdateTimer.value) {
        clearTimeout(configUpdateTimer.value);
        configUpdateTimer.value = null;
      }
      // 设置防抖计时器，150ms后执行渲染
      configUpdateTimer.value = setTimeout(() => {
        configUpdateTimer.value = null;
        renderCubies();
      }, 150);
    } else {
    }
  },
  { deep: true },
);

// 专门监听几何体配置变化，确保圆角参数立即生效
watch(
  () => props.customization?.geometry,
  (newGeometry, oldGeometry) => {
    if (!isAnimating) {
      renderCubies();
    } else {
    }
  },
  { deep: true },
);

// 专门监听 autoRotateSpeed 变化，确保 Three.js 控件更新
watch(
  () => props.autoRotateSpeed,
  (newSpeed) => {
    if (controls) {
      controls.autoRotateSpeed = newSpeed;
    }
  },
);

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

/* ============================================
   暗色模式覆盖
   ============================================ */

/* 3D容器在暗色模式下可以添加微妙的背景 */
[data-theme="dark"] .cube-3d-container {
  /* 3D渲染器背景由组件内部控制 */
}
</style>
