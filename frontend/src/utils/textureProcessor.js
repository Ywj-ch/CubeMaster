/**
 * @fileoverview 纹理图片处理工具模块
 * 
 * 提供用户上传纹理图片的处理功能，包括：
 * - 图片压缩和尺寸调整
 * - Base64 编码转换
 * - 文件格式和大小验证
 * 
 * @module utils/textureProcessor
 */

/**
 * 压缩图片文件
 * @param {File} file 图片文件
 * @param {number} maxSize 最大边长（像素）
 * @param {number} quality JPEG质量 (0-1)
 * @returns {Promise<Blob>} 压缩后的Blob
 */
export function compressImage(file, maxSize = 512, quality = 0.8) {
  return new Promise((resolve, reject) => {
    // 检查文件类型
    if (!file.type.match(/^image\/(jpeg|png|jpg|webp)$/)) {
      reject(new Error("仅支持 JPEG、PNG、WebP 格式的图片"));
      return;
    }

    // 检查文件大小 (限制为5MB)
    if (file.size > 5 * 1024 * 1024) {
      reject(new Error("图片大小不能超过 5MB"));
      return;
    }

    const img = new Image();
    const reader = new FileReader();

    reader.onload = (e) => {
      img.src = e.target.result;
    };

    img.onload = () => {
      // 计算缩放比例
      let width = img.width;
      let height = img.height;

      if (width > maxSize || height > maxSize) {
        if (width > height) {
          height = Math.round((height * maxSize) / width);
          width = maxSize;
        } else {
          width = Math.round((width * maxSize) / height);
          height = maxSize;
        }
      }

      // 创建Canvas进行压缩
      const canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;

      const ctx = canvas.getContext("2d");

      // 设置背景为白色（避免透明区域变黑）
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(0, 0, width, height);

      // 绘制图像
      ctx.drawImage(img, 0, 0, width, height);

      // 转换为Blob
      canvas.toBlob(
        (blob) => {
          if (blob) {
            resolve(blob);
          } else {
            reject(new Error("图片压缩失败"));
          }
        },
        "image/jpeg",
        quality,
      );
    };

    img.onerror = () => {
      reject(new Error("图片加载失败，请检查文件格式"));
    };

    reader.onerror = () => {
      reject(new Error("文件读取失败"));
    };

    reader.readAsDataURL(file);
  });
}

/**
 * 将图片文件转换为base64字符串
 * @param {File} file 图片文件
 * @returns {Promise<string>} base64数据URL
 */
export async function imageToBase64(file) {
  try {
    // 先压缩图片
    const blob = await compressImage(file);

    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result);
      reader.onerror = () => reject(new Error("base64转换失败"));
      reader.readAsDataURL(blob);
    });
  } catch (error) {
    throw error; // 传递compressImage的错误
  }
}

/**
 * 估算base64字符串的大小（KB）
 * @param {string} base64 base64字符串
 * @returns {number} 大小（KB）
 */
export function estimateBase64Size(base64) {
  if (!base64) return 0;

  // base64大小估算公式：原始大小 ≈ base64长度 * 3/4
  const length = base64.length;
  const sizeInBytes = (length * 3) / 4;
  return Math.round(sizeInBytes / 1024); // 转换为KB
}

/**
 * 检查base64字符串是否超出限制
 * @param {string} base64 base64字符串
 * @param {number} maxKB 最大KB数（默认500KB）
 * @returns {boolean} 是否超出限制
 */
export function isBase64OverLimit(base64, maxKB = 500) {
  const sizeKB = estimateBase64Size(base64);
  return sizeKB > maxKB;
}

/**
 * 创建内置纹理预览图（占位符）
 * 实际项目中，预览图应预先生成并存储在public目录
 * @param {string} textureName 纹理名称
 * @returns {string} 预览图URL
 */
export function getBuiltinPreviewUrl(textureName) {
  return `/textures/${textureName}.jpg`;
}

/**
 * 验证图片文件
 * @param {File} file 图片文件
 * @returns {string|null} 错误信息，null表示验证通过
 */
export function validateImageFile(file) {
  // 检查文件类型
  const validTypes = ["image/jpeg", "image/png", "image/jpg", "image/webp"];
  if (!validTypes.includes(file.type)) {
    return "仅支持 JPEG、PNG、WebP 格式的图片";
  }

  // 检查文件大小（5MB限制）
  const maxSize = 5 * 1024 * 1024; // 5MB
  if (file.size > maxSize) {
    return "图片大小不能超过 5MB";
  }

  // 检查文件名（防止特殊字符）
  if (/[<>:"/\\|?*]/.test(file.name)) {
    return "文件名包含非法字符";
  }

  return null; // 验证通过
}
