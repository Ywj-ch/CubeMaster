<template>
  <div class="customizer-page">
    <!-- 页面标题 -->
    <div class="page-header animate-entry">
      <h1>
        <span class="emoji">🎨</span
        ><span class="title-text">魔方外观自定义</span>
      </h1>
      <p class="subtitle">
        自定义魔方的材质、纹理和光照效果，打造属于你的独特魔方外观
      </p>
    </div>

    <!-- 错误提示 -->
    <el-alert
      v-if="error"
      :title="error"
      type="error"
      show-icon
      closable
      @close="error = null"
      class="error-alert"
    />

    <!-- 主内容区 -->
    <el-card class="customizer-main-card glass-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>魔方外观定制</span>
        </div>
      </template>

      <el-row :gutter="24" class="main-content unified-height">
        <!-- 左侧：预览区域 -->
        <el-col
          :xs="24"
          :sm="24"
          :md="10"
          :lg="10"
          :xl="10"
          class="animate-entry delay-1 preview-column"
        >
          <div class="preview-section">
            <div class="preview-container">
              <Cube3DView
                ref="cubeRef"
                :cube-state="demoCubeState"
                :customization="config"
                :enable-controls="true"
                :interactive="false"
                :auto-rotate="true"
                :auto-rotate-speed="autoRotateSpeed"
                class="cube-preview"
              />
            </div>

            <!-- 预览控制 -->
            <div class="preview-controls">
              <div class="control-row">
                <span class="control-label">旋转速度</span>
                <el-slider
                  v-model="autoRotateSpeed"
                  :min="0.5"
                  :max="5"
                  :step="0.1"
                  show-input
                  class="control-slider"
                />
                <el-button type="default" @click="resetView" class="reset-btn">
                  复位视角
                </el-button>
              </div>
            </div>

            <div class="preview-info">
              <div class="preview-info-group">
                <span class="info-icon">🎨</span>
                <div class="info-content">
                  <strong>材质设置</strong>
                  <span>{{ materialSummary }}</span>
                </div>
              </div>

              <div class="preview-info-group">
                <span class="info-icon">🖼️</span>
                <div class="info-content">
                  <strong>纹理系统</strong>
                  <span>{{ textureLabel }}</span>
                </div>
              </div>

              <div class="preview-info-group">
                <span class="info-icon">🔷</span>
                <div class="info-content">
                  <strong>几何体</strong>
                  <span>{{ geometrySummary }}</span>
                </div>
              </div>

              <div class="preview-info-group">
                <span class="info-icon">💡</span>
                <div class="info-content">
                  <strong>光照环境</strong>
                  <span>{{ lightingSummary }}</span>
                  <div
                    class="color-indicator"
                    :style="{ backgroundColor: lightingColorDisplay }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </el-col>

        <!-- 右侧：配置面板 -->
        <el-col
          :xs="24"
          :sm="24"
          :md="14"
          :lg="14"
          :xl="14"
          class="animate-entry delay-2 config-column"
        >
          <div class="config-section">
            <el-collapse v-model="activeNames" class="config-collapse">
              <el-collapse-item name="material" title="材质设置">
                <!-- 材质类型 -->
                <div class="config-section">
                  <h3>材质类型</h3>
                  <p class="section-description">
                    {{ currentMaterialType.description }}
                  </p>
                  <el-select
                    v-model="config.materialType"
                    placeholder="选择材质类型"
                    class="full-width"
                    @change="setMaterialType"
                  >
                    <el-option
                      v-for="material in materialTypes"
                      :key="material.value"
                      :label="material.label"
                      :value="material.value"
                    />
                  </el-select>
                </div>

                <!-- 材质参数 -->
                <div
                  class="config-section"
                  v-if="config.materialType !== 'basic'"
                >
                  <h3>材质参数</h3>

                  <!-- 通用参数：透明度 -->
                  <div class="param-row">
                    <span class="param-label">透明度</span>
                    <el-slider
                      v-model="config.materialParams.opacity"
                      :min="0"
                      :max="1"
                      :step="0.05"
                      show-input
                      @change="
                        setMaterialParam(
                          'opacity',
                          config.materialParams.opacity,
                        )
                      "
                      class="param-slider"
                    />
                  </div>

                  <!-- Lambert/Phong 参数：高光度 -->
                  <div
                    class="param-row"
                    v-if="
                      config.materialType === 'lambert' ||
                      config.materialType === 'phong'
                    "
                  >
                    <span class="param-label">高光度</span>
                    <el-slider
                      v-model="config.materialParams.shininess"
                      :min="0"
                      :max="100"
                      :step="1"
                      show-input
                      @change="
                        setMaterialParam(
                          'shininess',
                          config.materialParams.shininess,
                        )
                      "
                      class="param-slider"
                    />
                  </div>

                  <!-- Standard 参数：粗糙度/金属度 -->
                  <div
                    class="param-row"
                    v-if="config.materialType === 'standard'"
                  >
                    <span class="param-label">粗糙度</span>
                    <el-slider
                      v-model="config.materialParams.roughness"
                      :min="0"
                      :max="1"
                      :step="0.05"
                      show-input
                      @change="
                        setMaterialParam(
                          'roughness',
                          config.materialParams.roughness,
                        )
                      "
                      class="param-slider"
                    />
                  </div>
                  <div
                    class="param-row"
                    v-if="config.materialType === 'standard'"
                  >
                    <span class="param-label">金属度</span>
                    <el-slider
                      v-model="config.materialParams.metalness"
                      :min="0"
                      :max="1"
                      :step="0.05"
                      show-input
                      @change="
                        setMaterialParam(
                          'metalness',
                          config.materialParams.metalness,
                        )
                      "
                      class="param-slider"
                    />
                  </div>
                </div>
              </el-collapse-item>

              <!-- 纹理系统 -->
              <el-collapse-item name="texture" title="纹理系统">
                <div class="config-section">
                  <h3>纹理系统</h3>
                  <p class="section-description">
                    为魔方表面添加纹理图案，支持内置纹理或自定义上传
                  </p>

                  <!-- 纹理类型选择 -->
                  <div class="texture-type-selector">
                    <el-radio-group
                      v-model="config.texture.type"
                      @change="onTextureTypeChange"
                    >
                      <el-radio value="none">无纹理</el-radio>
                      <el-radio value="builtin">内置纹理</el-radio>
                      <el-radio value="custom">自定义纹理</el-radio>
                    </el-radio-group>
                  </div>

                  <!-- 内置纹理选择 -->
                  <div
                    class="texture-selector"
                    v-if="config.texture.type === 'builtin'"
                  >
                    <div class="texture-grid">
                      <div
                        v-for="texture in builtinTextures"
                        :key="texture.name"
                        :class="[
                          'texture-item',
                          {
                            active: config.texture.builtinName === texture.name,
                          },
                        ]"
                        @click="selectBuiltinTexture(texture.name)"
                      >
                        <div class="texture-preview">
                          <img :src="texture.preview" :alt="texture.label" />
                        </div>
                        <span class="texture-label">{{ texture.label }}</span>
                      </div>
                    </div>
                  </div>

                  <!-- 自定义纹理上传 -->
                  <div
                    class="texture-upload"
                    v-if="config.texture.type === 'custom'"
                  >
                    <el-upload
                      class="upload-demo"
                      drag
                      action=""
                      :auto-upload="false"
                      :on-change="handleTextureUpload"
                      :show-file-list="false"
                      accept="image/jpeg,image/png,image/webp"
                    >
                      <div class="upload-area">
                        <el-icon class="upload-icon"><Upload /></el-icon>
                        <div class="upload-text">
                          <p>点击或拖拽图片到此处上传</p>
                          <p class="upload-hint">
                            支持 JPG、PNG、WebP 格式，大小不超过 5MB
                          </p>
                        </div>
                      </div>
                    </el-upload>

                    <!-- 当前自定义纹理预览 -->
                    <div
                      class="custom-texture-preview"
                      v-if="config.texture.customData"
                    >
                      <h4>当前自定义纹理</h4>
                      <img
                        :src="config.texture.customData"
                        alt="自定义纹理"
                        class="custom-texture-image"
                      />
                      <el-button
                        type="danger"
                        size="small"
                        @click="clearTexture"
                        class="clear-texture-btn"
                      >
                        清除自定义纹理
                      </el-button>
                    </div>
                  </div>
                </div>
              </el-collapse-item>

              <!-- 几何体设置 -->
              <el-collapse-item name="geometry" title="几何体设置">
                <div class="config-section">
                  <h3>几何体设置</h3>
                  <p class="section-description">
                    调整魔方小方块的几何形状，支持标准方块或圆角方块
                  </p>

                  <!-- 几何体类型选择 -->
                  <div class="texture-type-selector">
                    <el-radio-group
                      v-model="config.geometry.type"
                      @change="(val) => setGeometryParam('type', val)"
                    >
                      <el-radio
                        v-for="geom in geometryTypes"
                        :key="geom.value"
                        :value="geom.value"
                      >
                        {{ geom.label }}
                        <el-tooltip
                          effect="dark"
                          :content="geom.description"
                          placement="top"
                        >
                          <el-icon class="info-icon"><InfoFilled /></el-icon>
                        </el-tooltip>
                      </el-radio>
                    </el-radio-group>
                  </div>

                  <!-- 圆角参数 (仅当类型为 'rounded' 时显示) -->
                  <div v-if="config.geometry.type === 'rounded'">
                    <!-- 圆角半径 -->
                    <div class="param-row">
                      <span class="param-label">圆角半径</span>
                      <el-slider
                        v-model="config.geometry.cornerRadius"
                        :min="0.01"
                        :max="0.5"
                        :step="0.01"
                        show-input
                        @change="
                          setGeometryParam(
                            'cornerRadius',
                            config.geometry.cornerRadius,
                          )
                        "
                        class="param-slider"
                      />
                    </div>

                    <!-- 细分段数 -->
                    <div class="param-row">
                      <span class="param-label">细分段数</span>
                      <el-slider
                        v-model="config.geometry.segments"
                        :min="1"
                        :max="8"
                        :step="1"
                        show-input
                        @change="
                          setGeometryParam('segments', config.geometry.segments)
                        "
                        class="param-slider"
                      />
                      <span class="param-hint"
                        >(值越高，圆角越平滑，性能影响越大)</span
                      >
                    </div>
                  </div>
                </div>
              </el-collapse-item>

              <!-- 光照环境 -->
              <el-collapse-item name="lighting" title="光照环境">
                <div class="config-section">
                  <h3>光照环境</h3>
                  <p class="section-description">
                    调整环境光和方向光的强度和颜色
                  </p>

                  <!-- 环境光强度 -->
                  <div class="param-row">
                    <span class="param-label">环境光强度</span>
                    <el-slider
                      v-model="config.lighting.ambientIntensity"
                      :min="0"
                      :max="1"
                      :step="0.05"
                      show-input
                      @change="
                        setLightingParam(
                          'ambientIntensity',
                          config.lighting.ambientIntensity,
                        )
                      "
                      class="param-slider"
                    />
                  </div>

                  <!-- 方向光强度 -->
                  <div class="param-row">
                    <span class="param-label">方向光强度</span>
                    <el-slider
                      v-model="config.lighting.directionalIntensity"
                      :min="0"
                      :max="1"
                      :step="0.05"
                      show-input
                      @change="
                        setLightingParam(
                          'directionalIntensity',
                          config.lighting.directionalIntensity,
                        )
                      "
                      class="param-slider"
                    />
                  </div>

                  <!-- 方向光颜色 -->
                  <div class="param-row">
                    <span class="param-label">方向光颜色</span>
                    <el-color-picker
                      v-model="config.lighting.directionalColor"
                      @change="
                        setLightingParam(
                          'directionalColor',
                          config.lighting.directionalColor,
                        )
                      "
                      class="color-picker"
                    />
                  </div>
                </div>
              </el-collapse-item>
            </el-collapse>

            <!-- 操作按钮 -->
            <div class="action-buttons">
              <el-button
                type="primary"
                @click="handleSave"
                :loading="isLoading"
                class="action-btn"
              >
                保存设置
              </el-button>
              <el-button
                @click="resetToDefault"
                :loading="isLoading"
                class="action-btn"
              >
                恢复默认
              </el-button>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 使用说明 -->
    <el-card class="instructions-card glass-card" shadow="never">
      <template #header>
        <h3>使用说明</h3>
      </template>
      <ul class="instructions-list">
        <li>所有设置自动保存到浏览器本地存储，下次访问时自动加载</li>
        <li>
          魔方的颜色映射（白、红、绿、黄、橙、蓝）保持不变，以确保求解算法的正确性
        </li>
        <li>
          纹理系统支持内置纹理和自定义上传，自定义纹理将转换为Base64存储在本地
        </li>
        <li>几何体设置允许选择标准方块或圆角方块，圆角半径和细分段数可调</li>
        <li>光照设置影响整个3D场景的视觉效果，可根据个人喜好调整</li>
        <li>不同材质类型提供不同的视觉效果，建议根据需求选择合适的材质</li>
      </ul>
    </el-card>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { ElMessage } from "element-plus";
import { Upload, InfoFilled } from "@element-plus/icons-vue";
import Cube3DView from "../components/Cube3DView.vue";
import { createCubeFromJson } from "../utils/cubeState.js";
import { useCubeCustomization } from "../composables/useCubeCustomization.js";

// 初始化自定义配置
const {
  config,
  isLoading,
  error,
  builtinTextures,
  materialTypes,
  geometryTypes,
  currentMaterialType,
  saveCurrentConfig,
  resetToDefault,
  uploadCustomTexture,
  selectBuiltinTexture,
  clearTexture,
  setMaterialType,
  setMaterialParam,
  setLightingParam,
  setGeometryParam,
} = useCubeCustomization();

// 演示用的魔方状态（已还原状态）
const demoCubeState = createCubeFromJson();

// 3D预览控件
const cubeRef = ref(null);
const autoRotateSpeed = ref(2.0);

// 手风琴当前展开的面板
const activeNames = ref(["material", "texture", "geometry", "lighting"]);

// 复位视角
const resetView = () => {
  if (cubeRef.value) {
    cubeRef.value.resetView();
  }
};

// 计算纹理标签
const textureLabel = computed(() => {
  const tex = config.value.texture;
  if (tex.type === "none") return "无纹理";
  if (tex.type === "builtin") {
    const texture = builtinTextures.find((t) => t.name === tex.builtinName);
    return texture ? texture.label : "未知纹理";
  }
  if (tex.type === "custom") return "自定义纹理";
  return "未知";
});

// 计算材质设置摘要
const materialSummary = computed(() => {
  const matType = config.value.materialType;
  const params = config.value.materialParams || {};
  let summary = currentMaterialType.value.label;

  // 添加透明度信息（如果透明度小于1.0）
  if (params.opacity < 1.0) {
    summary += ` · 透明度${(params.opacity * 100).toFixed(0)}%`;
  }

  // 根据材质类型添加特定参数
  if (matType === "lambert" || matType === "phong") {
    if (params.shininess !== undefined) {
      summary += ` · 高光度${params.shininess}`;
    }
  } else if (matType === "standard") {
    if (params.roughness !== undefined) {
      summary += ` · 粗糙度${params.roughness.toFixed(2)}`;
    }
    if (params.metalness !== undefined) {
      summary += ` · 金属度${params.metalness.toFixed(2)}`;
    }
  }

  return summary;
});

// 计算几何体设置摘要
const geometrySummary = computed(() => {
  const geom = config.value.geometry || {};
  if (geom.type === "rounded") {
    return `圆角方块(半径:${geom.cornerRadius.toFixed(2)}, 细分:${geom.segments})`;
  }
  return "标准方块";
});

// 计算光照设置摘要
const lightingSummary = computed(() => {
  const lighting = config.value.lighting || {};
  const ambient = lighting.ambientIntensity?.toFixed(2) || "0.00";
  const directional = lighting.directionalIntensity?.toFixed(2) || "0.00";
  const color = lighting.directionalColor || "#ffffff";

  return `环境${ambient} · 方向${directional}`;
});

// 获取光照颜色显示
const lightingColorDisplay = computed(() => {
  const color = config.value.lighting?.directionalColor || "#ffffff";
  return color;
});

// 纹理类型变化处理
const onTextureTypeChange = (type) => {
  if (type === "builtin" && !config.value.texture.builtinName) {
    // 如果没有选择内置纹理，默认选择第一个
    selectBuiltinTexture(builtinTextures[0].name);
  } else if (type === "none") {
    clearTexture();
  }
};

// 处理纹理上传
const handleTextureUpload = (file) => {
  uploadCustomTexture(file.raw)
    .then(() => {
      ElMessage.success("纹理上传成功");
    })
    .catch((err) => {
      // 错误已由 composable 设置到 error 变量
      console.error("纹理上传失败:", err);
    });
};

// 处理保存设置
const handleSave = () => {
  saveCurrentConfig();
  // 延迟检查错误状态，确保错误消息已更新
  setTimeout(() => {
    if (!error.value) {
      ElMessage.success({
        message: "设置保存成功！",
        type: "success",
        duration: 2000,
        showClose: true,
      });
    }
  }, 50);
};
</script>

<style scoped>
.customizer-page {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.error-alert {
  margin-bottom: 20px;
}

.main-content {
  margin-bottom: 30px;
  overflow-x: hidden;
}
.main-content .el-row {
  align-items: stretch;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-description {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 15px;
}

.full-width {
  width: 100%;
}

.info-icon {
  margin-left: 5px;
  color: #999;
  cursor: help;
  vertical-align: middle;
}

.param-hint {
  margin-left: 10px;
  font-size: 0.85rem;
  color: #888;
  font-style: italic;
}

.color-picker {
  margin-left: 15px;
}

.texture-type-selector {
  margin-bottom: 20px;
}

.texture-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.texture-item {
  cursor: pointer;
  text-align: center;
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.texture-item:hover {
  border-color: #409eff;
}

.texture-item.active {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.texture-preview {
  width: 80px;
  height: 80px;
  margin: 0 auto 8px;
  overflow: hidden;
  border-radius: 4px;
  background: #f5f5f5;
}

.texture-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.texture-label {
  font-size: 0.85rem;
  color: #333;
}

.texture-upload {
  margin-top: 15px;
}

.upload-area {
  padding: 40px 20px;
  text-align: center;
}

.upload-icon {
  font-size: 48px;
  color: #c0c4cc;
  margin-bottom: 15px;
}

.upload-text p {
  margin: 5px 0;
  color: #666;
}

.upload-hint {
  font-size: 0.85rem;
  color: #999;
}

.custom-texture-preview {
  margin-top: 20px;
  text-align: center;
}

.custom-texture-image {
  max-width: 200px;
  max-height: 200px;
  border-radius: 8px;
  margin: 10px 0;
  border: 1px solid #ddd;
}

.clear-texture-btn {
  margin-top: 10px;
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin-top: 30px;
}

.action-btn {
  min-width: 100px;
}

.instructions-card {
  margin-top: 30px;
}

.instructions-list {
  padding-left: 20px;
  color: #555;
}

.instructions-list li {
  margin-bottom: 8px;
  line-height: 1.5;
}

/* 玻璃态卡片样式 */
.glass-card {
  position: relative;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 24px;
  box-shadow:
    0 20px 50px -12px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.5) inset;
}

/* 动画入场效果 */
.animate-entry {
  opacity: 0;
  will-change: transform, opacity;
  animation: fadeInUp 0.8s cubic-bezier(0.33, 1, 0.68, 1) forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
    filter: blur(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
    filter: blur(0);
  }
}

/* 延迟动画 */
.delay-1 {
  animation-delay: 0.2s;
}
.delay-2 {
  animation-delay: 0.4s;
}
.delay-3 {
  animation-delay: 0.6s;
}

/* 现代化配置区域 */
.config-section {
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.config-section:last-child {
  border-bottom: none;
}

.config-section h3 {
  font-size: 1.1rem;
  margin-bottom: 12px;
  color: #0f172a;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
}

.config-section h3::before {
  content: "";
  display: block;
  width: 4px;
  height: 16px;
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  border-radius: 2px;
}

.section-description {
  font-size: 0.9rem;
  color: #64748b;
  margin-bottom: 20px;
  line-height: 1.5;
}

/* 现代化参数行 */
.param-row {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.param-row:hover {
  background: rgba(255, 255, 255, 0.7);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.param-label {
  width: 120px;
  font-size: 0.95rem;
  color: #475569;
  font-weight: 600;
}

.param-slider {
  flex: 1;
  margin-left: 20px;
}

/* 现代化纹理选择器 */
.texture-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
  gap: 16px;
  margin-top: 20px;
}

.texture-item {
  cursor: pointer;
  text-align: center;
  padding: 16px 12px;
  border: 2px solid rgba(226, 232, 240, 0.8);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.6);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.texture-item:hover {
  border-color: #2563eb;
  background: rgba(37, 99, 235, 0.05);
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(37, 99, 235, 0.15);
}

.texture-item.active {
  border-color: #2563eb;
  background: rgba(37, 99, 235, 0.1);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
}

.texture-item.active::after {
  content: "✓";
  position: absolute;
  top: 8px;
  right: 8px;
  width: 20px;
  height: 20px;
  background: #2563eb;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

.texture-preview {
  width: 80px;
  height: 80px;
  margin: 0 auto 12px;
  overflow: hidden;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(226, 232, 240, 0.8);
  padding: 4px;
}

.texture-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.texture-label {
  font-size: 0.85rem;
  color: #334155;
  font-weight: 600;
  display: block;
}

/* 现代化上传区域 */
.upload-area {
  padding: 40px 20px;
  text-align: center;
  background: rgba(255, 255, 255, 0.5);
  border: 2px dashed #cbd5e1;
  border-radius: 20px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.upload-area:hover {
  background: rgba(255, 255, 255, 0.8);
  border-color: #2563eb;
  transform: translateY(-2px);
}

.upload-icon {
  font-size: 48px;
  color: #94a3b8;
  margin-bottom: 16px;
  transition: all 0.3s ease;
}

.upload-area:hover .upload-icon {
  color: #2563eb;
  transform: scale(1.1);
}

.upload-text p {
  margin: 8px 0;
  color: #475569;
}

.upload-hint {
  font-size: 0.85rem;
  color: #94a3b8;
}

/* 现代化操作按钮 */
.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid rgba(255, 255, 255, 0.3);
}

.action-btn {
  min-width: 140px;
  height: 48px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.action-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

/* 现代化预览区域 */
.preview-container {
  width: 100%;
  max-width: 100%;
  height: 450px; /* 固定高度确保3D画布有空间 */
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-sizing: border-box;
}

.cube-preview {
  width: 100%;
  height: 100%;
  max-width: 100%;
  display: block;
}

.preview-controls {
  margin-top: 20px;
  padding: 18px;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.6);
}

.control-row {
  display: flex;
  align-items: center;
  gap: 20px;
}

.control-label {
  font-size: 0.95rem;
  color: #475569;
  font-weight: 500;
  min-width: 80px;
}

.control-slider {
  flex: 1;
}

.reset-btn {
  min-width: 100px;
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.reset-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.preview-info {
  margin-top: 24px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 16px;
  font-size: 0.95rem;
  color: #475569;
  border: 1px solid rgba(255, 255, 255, 0.6);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.preview-info-group {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.preview-info-group:hover {
  background: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.info-icon {
  font-size: 1.2rem;
  min-width: 24px;
  text-align: center;
  margin-top: 2px;
}

.info-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-content strong {
  font-size: 0.9rem;
  color: #1e293b;
  font-weight: 600;
}

.info-content span {
  font-size: 0.85rem;
  color: #64748b;
  line-height: 1.4;
}

.color-indicator {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  display: inline-block;
  margin-left: 8px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  vertical-align: middle;
}

/* 现代化页面标题 */
.page-header h1 {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  font-size: 3rem;
  margin-bottom: 16px;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.page-header h1 .emoji {
  font-size: 3rem;
  line-height: 1;
}

.page-header h1 .title-text {
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 1.2rem;
  color: #64748b;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

/* 手风琴样式 */
.config-collapse {
  border: none;
  background: transparent;
}

.config-collapse .el-collapse-item {
  margin-bottom: 16px;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  overflow: hidden;
}

.config-collapse .el-collapse-item__header {
  padding: 20px 24px;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  background: rgba(255, 255, 255, 0.6);
  border-bottom: 1px solid rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.config-collapse .el-collapse-item__header:hover {
  background: rgba(255, 255, 255, 0.8);
}

.config-collapse .el-collapse-item__wrap {
  background: transparent;
  border: none;
  overflow: visible;
}

.config-collapse .el-collapse-item__content {
  padding: 24px;
  padding-top: 0;
  overflow: visible !important;
  max-height: none !important;
}

.config-collapse .config-section {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

/* 统一高度布局 */
.customizer-main-card {
  position: relative;
}

.customizer-main-card .main-content {
  /* 使用自动高度而不是固定高度，避免内部滚动条 */
  height: auto;
  min-height: 600px;
  /* 移除flex布局，让el-row控制水平布局 */
}

.unified-height .el-col {
  /* 使用flex而不是固定高度 */
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0; /* 允许内容收缩 */
}

.preview-column,
.config-column {
  /* 高度由flexbox控制 */
  border-radius: 12px;
}

.preview-column {
  background: rgba(240, 249, 255, 0.3); /* 浅蓝色背景 */
  padding: 20px;
  border: 1px solid rgba(37, 99, 235, 0.1);
}

.config-column {
  background: rgba(255, 250, 240, 0.3); /* 浅黄色背景 */
  padding: 20px;
  border: 1px solid rgba(245, 158, 11, 0.1);
  position: relative;
}

/* 在配置列左侧添加分隔线 */
.config-column::before {
  content: "";
  position: absolute;
  left: -12px; /* 负一半的gutter值 */
  top: 20px;
  bottom: 20px;
  width: 1px;
  background: linear-gradient(
    to bottom,
    transparent,
    rgba(0, 0, 0, 0.1),
    transparent
  );
}

.preview-section {
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 20px;
  min-height: 0; /* 允许内容收缩 */
}

.config-section {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0; /* 允许内容收缩 */
}

.config-section > .el-collapse {
  flex: 1;
  /* 始终显示滚动条，内容可滚动 */
  overflow-y: auto;
  max-height: none;
  /* 为滚动条预留空间 */
  padding-right: 6px;
}

/* 自定义滚动条样式 */
.config-section > .el-collapse::-webkit-scrollbar {
  width: 6px;
}

.config-section > .el-collapse::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 3px;
}

.config-section > .el-collapse::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.config-section > .el-collapse::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .param-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .param-label {
    width: 100%;
  }

  .param-slider {
    margin-left: 0;
    width: 100%;
  }

  .preview-controls {
    padding: 15px;
  }

  .preview-info {
    padding: 15px;
    gap: 12px;
  }

  .preview-info-group {
    padding: 10px;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .info-icon {
    font-size: 1rem;
    margin-top: 0;
  }

  .info-content {
    width: 100%;
  }

  .control-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .control-label {
    width: 100%;
    min-width: auto;
  }

  .control-slider {
    width: 100%;
    margin-left: 0;
  }

  .reset-btn {
    width: 100%;
    margin-top: 10px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
  }

  .texture-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  /* 小屏幕隐藏分隔线，调整列样式 */
  .preview-column,
  .config-column {
    padding: 15px;
    margin-bottom: 20px;
  }

  .config-column::before {
    display: none; /* 隐藏分隔线 */
  }

  .preview-container {
    height: 350px; /* 移动端减小高度 */
  }
}
</style>
