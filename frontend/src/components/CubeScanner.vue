<template>
  <transition name="fade">
    <div v-if="visible" class="scanner-overlay-backdrop">
      <div class="scanner-card">
        <div class="scanner-header">
          <h2 class="header-title">扫描魔方状态</h2>
          <button @click="close" class="close-icon-btn">
            <el-icon size="20"><Close /></el-icon>
          </button>
        </div>

        <div class="camera-section">
          <div class="camera-wrapper">
            <video
              ref="videoRef"
              autoplay
              playsinline
              class="video-feed"
            ></video>

            <div class="instruction-overlay">
              <h3 class="step-title">
                步骤 {{ currentFaceIndex + 1 }}/6: 扫描{{
                  scanSteps[currentFace].title
                }}
              </h3>
              <p class="step-guide">
                <el-icon><Aim /></el-icon>
                {{ scanSteps[currentFace].guide }}
              </p>
            </div>

            <div class="scan-window">
              <div class="grid-line v-1"></div>
              <div class="grid-line v-2"></div>
              <div class="grid-line h-1"></div>
              <div class="grid-line h-2"></div>
              <div class="corner tl"></div>
              <div class="corner tr"></div>
              <div class="corner bl"></div>
              <div class="corner br"></div>
            </div>
          </div>
        </div>

        <div class="scanner-footer">
          <div class="preview-strip">
            <div
              v-for="(face, index) in scanOrder"
              :key="face"
              class="preview-slot"
              :class="{
                active: index === currentFaceIndex,
                completed: scannedImages[face],
              }"
            >
              <img
                v-if="scannedImages[face]"
                :src="scannedImages[face]"
                class="slot-img"
              />
              <span v-else class="slot-label">{{ face }}面</span>
            </div>
          </div>

          <div class="action-area">
            <el-button
              class="reset-btn"
              link
              @click="resetScanner"
              :disabled="currentFaceIndex === 0"
            >
              重拍
            </el-button>

            <button
              class="shutter-button"
              @click="capture"
              :disabled="isProcessing"
            >
              <div
                class="inner-circle"
                :class="{ 'is-loading': isProcessing }"
              ></div>
            </button>

            <div class="placeholder-spacer"></div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch, nextTick, computed, onUnmounted } from "vue";
import { Close, Aim } from "@element-plus/icons-vue";
import { ElMessage, ElLoading } from "element-plus";
import { recognizeCube } from "../api/cubeService.js";

const props = defineProps({ visible: Boolean });
const emit = defineEmits(["close", "scanned"]);

const videoRef = ref(null);
const isProcessing = ref(false);
let activeStream = null;

// 扫描顺序 F L R B U D
const scanOrder = ["F", "L", "B", "R", "U", "D"];
const currentFaceIndex = ref(0);
const currentFace = computed(() => scanOrder[currentFaceIndex.value] || "F");

// 详细的引导步骤定义
const scanSteps = {
  F: { title: "前面 (Front)", guide: "绿色中心对准镜头，白色中心向上" },
  L: { title: "左面 (Left)", guide: "橙色中心对准镜头，白色中心向上" },
  B: { title: "后面 (Back)", guide: "蓝色中心对准镜头，白色中心向上" },
  R: { title: "右面 (Right)", guide: "红色中心对准镜头，白色中心向上" },
  U: { title: "顶面 (Up)", guide: "白色中心对准镜头，蓝色中心向上" },
  D: { title: "底面 (Down)", guide: "黄色中心对准镜头，绿色中心向上" },
};

// 存储 6 个面的图片
const scannedImages = ref({});

// --- 摄像头控制 ---
const startCamera = async () => {
  // 先关闭可能存在的旧流，防止重复开启
  stopCamera();

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: "environment",
        width: { ideal: 1280 },
        height: { ideal: 720 },
      },
    });

    // 将流保存到我们定义的变量中
    activeStream = stream;

    // 再赋值给 video 标签进行预览
    if (videoRef.value) {
      videoRef.value.srcObject = stream;
    }
  } catch (err) {
    console.error("摄像头启动失败:", err);
    ElMessage.error("无法访问摄像头权限");
    emit("close");
  }
};

const stopCamera = () => {
  // 修改关闭逻辑：直接操作 activeStream，不再依赖 videoRef
  if (activeStream) {
    const tracks = activeStream.getTracks();
    tracks.forEach((track) => {
      track.stop(); // 这才是真正关闭硬件指令
    });
    activeStream = null; // 清空变量
  }

  // 顺便清理一下 videoRef (如果 DOM 还在的话)
  if (videoRef.value) {
    videoRef.value.srcObject = null;
  }
};

// --- 拍摄逻辑 ---
const capture = () => {
  if (!videoRef.value || isProcessing.value) return;

  const video = videoRef.value;
  // 创建临时 canvas
  const canvas = document.createElement("canvas");
  canvas.width = 640;
  canvas.height = 640;
  const ctx = canvas.getContext("2d");

  // 计算截取区域：截取视频中心的正方形区域
  // 我们希望截取的内容与视觉上的九宫格框尽可能一致
  const videoW = video.videoWidth;
  const videoH = video.videoHeight;
  const cropSize = Math.min(videoW, videoH) * 0.75; // 截取视频最短边的 75%，与 CSS 中的 scan-window 比例对应
  const sx = (videoW - cropSize) / 2;
  const sy = (videoH - cropSize) / 2;

  ctx.drawImage(video, sx, sy, cropSize, cropSize, 0, 0, 640, 640);
  const base64 = canvas.toDataURL("image/jpeg", 0.85);

  // 保存当前面图片
  scannedImages.value[currentFace.value] = base64;

  // 进度控制
  if (currentFaceIndex.value < 5) {
    currentFaceIndex.value++;
  } else {
    finishScanning();
  }
};

const finishScanning = async () => {
  if (isProcessing.value) return;
  isProcessing.value = true;

  // 使用 Element Plus 的全屏 Loading，给用户一种正在“深度计算”的视觉感
  const loading = ElLoading.service({
    lock: true,
    text: "正在上传并识别魔方颜色...",
    background: "rgba(255, 255, 255, 0.7)",
  });

  try {
    // 1. 构造请求体，与后端 Body(payload) 对应
    const payload = {
      images: scannedImages.value, // { 'F': 'base64...', 'L': '...', ... }
    };

    // 2. 发送请求给 FastAPI 后端
    const response = await recognizeCube(payload);

    if (response.data.success) {
      ElMessage.success("识别成功！");

      // 3. 将后端返回的识别结果 (3x3矩阵数据) 发给父组件
      // 这样 SolverView 就可以打开“颜色纠错面板”了
      emit("scanned", response.data.data);

      // 4. 识别成功才自动关闭扫描器
      close();
    } else {
      // 后端返回识别不全 (比如只识别了 4/6)
      throw new Error(response.data.error || "识别失败，请检查魔方放置位置");
    }
  } catch (error) {
    console.error("Recognition Error:", error);

    // 如果失败了，不要关闭扫描器，让用户有机会重拍
    ElMessage({
      message: error.message || "网络连接失败，请检查后端服务是否开启",
      type: "error",
      duration: 5000,
    });

    // 可以在这里提供一个“重置”当前进度的选项
    // 或者保持当前已经拍好的图片，让用户手动点“重拍”
  } finally {
    loading.close();
    isProcessing.value = false;
  }
};

const resetScanner = () => {
  currentFaceIndex.value = 0;
  scannedImages.value = {};
};

const close = () => {
  stopCamera();
  resetScanner();
  emit("close");
};

watch(
  () => props.visible,
  (newVal) => {
    if (newVal) {
      nextTick(() => {
        startCamera();
      });
    } else {
      // 界面关闭时，立即停止
      stopCamera();
    }
  },
  { immediate: true },
);

// 安全兜底：组件卸载时（例如路由跳转）强制关闭
onUnmounted(() => {
  stopCamera();
});
</script>

<style scoped>
/* 背景遮罩：毛玻璃效果 */
.scanner-overlay-backdrop {
  position: fixed;
  inset: 0;
  z-index: 2000;
  background: rgba(255, 255, 255, 0.6); /* 调亮背景 */
  backdrop-filter: blur(20px) saturate(120%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px; /* 给四周留白 */
}

/* 核心白卡片容器 */
.scanner-card {
  width: 100%;
  max-width: 500px; /* 限制最大宽度，类似于手机屏幕或 iPad 弹窗 */
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Header */
.scanner-header {
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #f0f0f0;
}

.header-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1d1d1f;
}

.close-icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: #86868b;
  transition: color 0.2s;
}
.close-icon-btn:hover {
  color: #1d1d1f;
}

/* Camera Section */
.camera-section {
  position: relative;
  width: 100%;
  /* 设置一个合理的固定高度或比例，防止视频过大 */
  height: 0;
  padding-bottom: 100%; /* 1:1 正方形区域，适合扫描 */
  background: #000;
  overflow: hidden;
}

.camera-wrapper {
  position: absolute;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.video-feed {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 确保填满容器 */
}

/* 悬浮引导提示框 */
.instruction-overlay {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 85%;
  background: rgba(0, 0, 0, 0.75); /* 深色半透明背景 */
  color: #fff;
  padding: 12px 16px;
  border-radius: 12px;
  text-align: center;
  z-index: 10;
  backdrop-filter: blur(8px);
}

.step-title {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
}

.step-guide {
  margin: 0;
  font-size: 13px;
  opacity: 0.9;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

/* 扫描参考框 (关键修改：调整大小比例) */
.scan-window {
  position: absolute;
  /* 让扫描框占视频区域的 75%，大大增加视觉占比 */
  width: 75%;
  height: 75%;
  border: 1px solid rgba(255, 255, 255, 0.3);
  /* 使用巨大的阴影来压暗周围区域，聚焦中心 */
  box-shadow: 0 0 0 1000px rgba(0, 0, 0, 0.5);
  z-index: 5;
}

/* 九宫格线与角标  */
.grid-line {
  position: absolute;
  background: rgba(255, 255, 255, 0.2);
}
.v-1 {
  left: 33.3%;
  top: 0;
  bottom: 0;
  width: 1px;
}
.v-2 {
  left: 66.6%;
  top: 0;
  bottom: 0;
  width: 1px;
}
.h-1 {
  top: 33.3%;
  left: 0;
  right: 0;
  height: 1px;
}
.h-2 {
  top: 66.6%;
  left: 0;
  right: 0;
  height: 1px;
}
.corner {
  position: absolute;
  width: 24px;
  height: 24px;
  border: 3px solid #0071e3; /* 加粗角标 */
}
.tl {
  top: -2px;
  left: -2px;
  border-right: none;
  border-bottom: none;
  border-radius: 8px 0 0 0;
}
.tr {
  top: -2px;
  right: -2px;
  border-left: none;
  border-bottom: none;
  border-radius: 0 8px 0 0;
}
.bl {
  bottom: -2px;
  left: -2px;
  border-right: none;
  border-top: none;
  border-radius: 0 0 0 8px;
}
.br {
  bottom: -2px;
  right: -2px;
  border-left: none;
  border-top: none;
  border-radius: 0 0 8px 0;
}

/* Footer Area */
.scanner-footer {
  padding: 20px 24px;
  background: #fff;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 底部预览条 */
.preview-strip {
  display: flex;
  justify-content: space-between;
  gap: 8px;
}

.preview-slot {
  flex: 1;
  aspect-ratio: 1; /* 正方形槽位 */
  background: #f5f5f7;
  border-radius: 8px;
  border: 2px solid transparent;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 12px;
  color: #a1a1a6;
  overflow: hidden;
  transition: all 0.3s;
}

.preview-slot.active {
  border-color: #0071e3; /* 当前正在拍的面高亮 */
  background: #fff;
}

.preview-slot.completed {
  border-color: #34c759; /* 已完成的面变绿 */
}

.slot-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 底部按钮操作区 */
.action-area {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.reset-btn,
.placeholder-spacer {
  width: 60px;
  text-align: center;
}

/* 拟物化快门按钮 */
.shutter-button {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  border: 4px solid #f5f5f7;
  padding: 0;
  background: #fff;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.1s;
}
.shutter-button:active {
  transform: scale(0.95);
}
.inner-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(145deg, #ffffff, #f0f0f0);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Dark Mode Styles */
[data-theme="dark"] .scanner-overlay-backdrop {
  background: rgba(15, 23, 42, 0.8);
}

[data-theme="dark"] .scanner-card {
  background: var(--dm-bg-card);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

[data-theme="dark"] .scanner-header {
  border-bottom: 1px solid var(--dm-border);
}

[data-theme="dark"] .header-title {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .close-icon-btn {
  color: var(--dm-text-muted);
}

[data-theme="dark"] .close-icon-btn:hover {
  color: var(--dm-text-primary);
}

[data-theme="dark"] .scanner-footer {
  background: var(--dm-bg-card);
}

[data-theme="dark"] .preview-slot {
  background: var(--dm-bg-page);
  color: var(--dm-text-muted);
}

[data-theme="dark"] .preview-slot.active {
  background: var(--dm-bg-card);
  border-color: var(--dm-accent);
}

[data-theme="dark"] .shutter-button {
  border-color: var(--dm-border);
  background: var(--dm-bg-card);
}

[data-theme="dark"] .inner-circle {
  background: linear-gradient(145deg, var(--dm-bg-card), var(--dm-bg-page));
  border: 1px solid var(--dm-border);
}
</style>
