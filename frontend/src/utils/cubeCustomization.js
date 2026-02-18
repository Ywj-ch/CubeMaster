// cubeCustomization.js
// 魔方外观自定义配置管理

/**
 * 默认配置结构
 * 注意：保持标准颜色映射不变 (白、红、绿、黄、橙、蓝)，仅修改材质/纹理/光影
 */
export const defaultConfig = {
  // 材质类型
  materialType: "lambert", // 'basic'|'lambert'|'phong'|'standard'|'toon'

  // 材质参数 (不同类型材质对应不同参数)
  materialParams: {
    // Lambert/Phong 材质
    shininess: 30, // 高光强度 (0-100)
    // Standard 材质
    roughness: 0.5, // 粗糙度 (0-1)
    metalness: 0, // 金属度 (0-1)
    // 通用
    opacity: 1.0, // 透明度 (0-1)
  },

  // 纹理系统
  texture: {
    type: "none", // 'none'|'builtin'|'custom'
    builtinName: "wood", // 内置纹理名称
    customData: null, // base64 字符串 (用户上传)
  },

  // 光照环境
  lighting: {
    ambientIntensity: 0.4, // 环境光强度 (0-1)
    directionalColor: "#ffffff", // 方向光颜色
    directionalIntensity: 0.8, // 方向光强度 (0-1)
  },

  // 几何体设置
  geometry: {
    type: "standard", // 'standard'|'rounded'
    cornerRadius: 0.1, // 圆角半径 (0-0.5)
    segments: 2, // 圆角细分段数 (1-8)
  },
};

/**
 * 内置纹理列表
 */
export const builtinTextures = [
  { name: "wood", label: "木纹", preview: "/textures/wood.jpg" },
  { name: "metal", label: "金属", preview: "/textures/metal.jpg" },
  { name: "plastic", label: "塑料", preview: "/textures/plastic.jpg" },
  { name: "marble", label: "大理石", preview: "/textures/marble.jpg" },
  { name: "checker", label: "棋盘格", preview: "/textures/checker.jpg" },
];

/**
 * 材质类型选项
 */
export const materialTypes = [
  { value: "basic", label: "基础材质", description: "无光照，纯色显示" },
  { value: "lambert", label: "朗伯材质", description: "漫反射，适合塑料质感" },
  { value: "phong", label: "冯氏材质", description: "高光反射，适合光泽表面" },
  {
    value: "standard",
    label: "标准材质",
    description: "PBR物理渲染，支持金属/粗糙度",
  },
  { value: "toon", label: "卡通材质", description: "卡通风格，色块分明" },
];

/**
 * 几何体类型选项
 */
export const geometryTypes = [
  {
    value: "standard",
    label: "标准方块",
    description: "直角方块，经典魔方外观",
  },
  {
    value: "rounded",
    label: "圆角方块",
    description: "圆润边缘，柔和卡通风格",
  },
];

/**
 * 加载配置
 * @returns {Object} 配置对象
 */
export function loadConfig() {
  try {
    const saved = localStorage.getItem("cubeMaster_customization_v1");
    if (saved) {
      const parsed = JSON.parse(saved);
      // 合并默认配置，确保新增字段存在
      return {
        ...defaultConfig,
        ...parsed,
        materialParams: {
          ...defaultConfig.materialParams,
          ...(parsed.materialParams || {}),
        },
        texture: {
          ...defaultConfig.texture,
          ...(parsed.texture || {}),
        },
        lighting: {
          ...defaultConfig.lighting,
          ...(parsed.lighting || {}),
        },
        geometry: {
          ...defaultConfig.geometry,
          ...(parsed.geometry || {}),
        },
      };
    }
  } catch (error) {
    console.error("加载外观配置失败:", error);
  }
  return { ...defaultConfig }; // 返回深拷贝
}

/**
 * 保存配置
 * @param {Object} config 配置对象
 */
export function saveConfig(config) {
  try {
    localStorage.setItem("cubeMaster_customization_v1", JSON.stringify(config));
  } catch (error) {
    console.error("保存外观配置失败:", error);
    // 如果存储失败（如超出配额），尝试清理旧数据
    if (error.name === "QuotaExceededError") {
      console.warn("localStorage 配额超出，尝试清理旧配置");
      localStorage.removeItem("cubeMaster_customization_v1");
    }
  }
}

/**
 * 重置为默认配置
 * @returns {Object} 默认配置
 */
export function resetConfig() {
  const config = { ...defaultConfig };
  saveConfig(config);
  return config;
}

/**
 * 获取纹理URL
 * @param {Object} textureConfig 纹理配置
 * @returns {string|null} 纹理URL或base64数据
 */
export function getTextureUrl(textureConfig) {
  if (!textureConfig || textureConfig.type === "none") {
    return null;
  }

  if (textureConfig.type === "builtin") {
    return `/textures/${textureConfig.builtinName}.jpg`;
  }

  if (textureConfig.type === "custom" && textureConfig.customData) {
    return textureConfig.customData; // base64字符串
  }

  return null;
}

/**
 * 验证配置有效性
 * @param {Object} config 配置对象
 * @returns {boolean} 是否有效
 */
export function validateConfig(config) {
  if (!config) return false;

  // 检查材质类型
  if (!materialTypes.some((m) => m.value === config.materialType)) {
    return false;
  }

  // 检查材质参数范围
  const params = config.materialParams;
  if (params.shininess < 0 || params.shininess > 100) return false;
  if (params.roughness < 0 || params.roughness > 1) return false;
  if (params.metalness < 0 || params.metalness > 1) return false;
  if (params.opacity < 0 || params.opacity > 1) return false;

  // 检查光照参数
  const lighting = config.lighting;
  if (lighting.ambientIntensity < 0 || lighting.ambientIntensity > 1)
    return false;
  if (lighting.directionalIntensity < 0 || lighting.directionalIntensity > 1)
    return false;

  // 检查几何体参数
  const geometry = config.geometry;
  if (!geometry) return false;
  if (!["standard", "rounded"].includes(geometry.type)) return false;
  if (geometry.cornerRadius < 0 || geometry.cornerRadius > 0.5) return false;
  if (geometry.segments < 1 || geometry.segments > 8) return false;

  return true;
}
