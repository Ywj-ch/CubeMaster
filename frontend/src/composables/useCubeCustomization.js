// useCubeCustomization.js
// 魔方外观自定义组合式函数

import { ref, computed, watch } from "vue";
import {
  loadConfig,
  saveConfig,
  resetConfig,
  validateConfig,
  getTextureUrl,
  builtinTextures,
  materialTypes,
  geometryTypes,
  defaultConfig,
} from "../utils/cubeCustomization.js";
import { imageToBase64, validateImageFile } from "../utils/textureProcessor.js";

/**
 * 魔方外观自定义组合式函数
 * @returns {Object} 响应式状态和方法
 */
export function useCubeCustomization() {
  // 当前配置（响应式）
  const config = ref(loadConfig());

  // 加载状态
  const isLoading = ref(false);
  const error = ref(null);

  /**
   * 更新配置（部分更新）
   * @param {Object} updates 部分配置更新
   */
  function updateConfig(updates) {
    if (!updates || typeof updates !== "object") return;

    // 深度合并更新
    const updateDeep = (target, source) => {
      for (const key in source) {
        if (
          source[key] &&
          typeof source[key] === "object" &&
          !Array.isArray(source[key])
        ) {
          if (!target[key] || typeof target[key] !== "object") {
            target[key] = {};
          }
          updateDeep(target[key], source[key]);
        } else {
          target[key] = source[key];
        }
      }
    };

    updateDeep(config.value, updates);
  }

  /**
   * 保存当前配置到localStorage
   */
  function saveCurrentConfig() {
    try {
      if (validateConfig(config.value)) {
        saveConfig(config.value);
        error.value = null;
      } else {
        error.value = "配置无效，保存失败";
      }
    } catch (err) {
      error.value = `保存失败: ${err.message}`;
      console.error("保存配置失败:", err);
    }
  }

  /**
   * 重置为默认配置
   */
  function resetToDefault() {
    config.value = resetConfig();
    error.value = null;
  }

  /**
   * 上传自定义纹理图片
   * @param {File} file 图片文件
   * @returns {Promise<void>}
   */
  async function uploadCustomTexture(file) {
    isLoading.value = true;
    error.value = null;

    try {
      // 验证文件
      const validationError = validateImageFile(file);
      if (validationError) {
        throw new Error(validationError);
      }

      // 转换为base64
      const base64Data = await imageToBase64(file);

      // 更新配置
      updateConfig({
        texture: {
          type: "custom",
          builtinName: "",
          customData: base64Data,
        },
      });

      // 自动保存
      saveCurrentConfig();
    } catch (err) {
      error.value = `纹理上传失败: ${err.message}`;
      console.error("纹理上传失败:", err);
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * 选择内置纹理
   * @param {string} textureName 纹理名称
   */
  function selectBuiltinTexture(textureName) {
    const texture = builtinTextures.find((t) => t.name === textureName);
    if (!texture) {
      error.value = `纹理 "${textureName}" 不存在`;
      return;
    }

    updateConfig({
      texture: {
        type: "builtin",
        builtinName: textureName,
        customData: null,
      },
    });
    saveCurrentConfig();
  }

  /**
   * 清除纹理（使用纯色）
   */
  function clearTexture() {
    updateConfig({
      texture: {
        type: "none",
        builtinName: "",
        customData: null,
      },
    });
    saveCurrentConfig();
  }

  /**
   * 更新材质类型
   * @param {string} materialType 材质类型
   */
  function setMaterialType(materialType) {
    const material = materialTypes.find((m) => m.value === materialType);
    if (!material) {
      error.value = `材质类型 "${materialType}" 不存在`;
      return;
    }

    updateConfig({ materialType });
    saveCurrentConfig();
  }

  /**
   * 更新材质参数
   * @param {string} paramName 参数名
   * @param {number} value 值
   */
  function setMaterialParam(paramName, value) {
    updateConfig({
      materialParams: {
        [paramName]: value,
      },
    });
    saveCurrentConfig();
  }

  /**
   * 更新光照参数
   * @param {string} paramName 参数名
   * @param {number|string} value 值
   */
  function setLightingParam(paramName, value) {
    updateConfig({
      lighting: {
        [paramName]: value,
      },
    });
    saveCurrentConfig();
  }

  /**
   * 更新几何体参数
   * @param {string} paramName 参数名
   * @param {number|string} value 值
   */
  function setGeometryParam(paramName, value) {
    updateConfig({
      geometry: {
        [paramName]: value,
      },
    });
    saveCurrentConfig();
  }

  // 计算属性：当前纹理URL（用于Three.js）
  const textureUrl = computed(() => getTextureUrl(config.value.texture));

  // 计算属性：当前材质类型选项
  const currentMaterialType = computed(
    () =>
      materialTypes.find((m) => m.value === config.value.materialType) ||
      materialTypes[1],
  );

  // 计算属性：当前纹理选项
  const currentTexture = computed(() => {
    const tex = config.value.texture;
    if (tex.type === "builtin") {
      return (
        builtinTextures.find((t) => t.name === tex.builtinName) ||
        builtinTextures[0]
      );
    }
    return null;
  });

  // 自动保存监听（防抖）
  let saveTimeout = null;
  watch(
    config,
    () => {
      if (saveTimeout) clearTimeout(saveTimeout);
      saveTimeout = setTimeout(() => {
        saveCurrentConfig();
      }, 1000); // 1秒防抖
    },
    { deep: true },
  );

  // 初始化时验证配置
  if (!validateConfig(config.value)) {
    console.warn("加载的配置无效，重置为默认配置");
    config.value = { ...defaultConfig };
    saveConfig(config.value);
  }

  return {
    // 状态
    config,
    isLoading,
    error,

    // 配置数据
    builtinTextures,
    materialTypes,
    geometryTypes,

    // 计算属性
    textureUrl,
    currentMaterialType,
    currentTexture,
    // 方法
    saveCurrentConfig,
    resetToDefault,
    uploadCustomTexture,
    selectBuiltinTexture,
    clearTexture,
    setMaterialType,
    setMaterialParam,
    setLightingParam,
    setGeometryParam,
  };
}
