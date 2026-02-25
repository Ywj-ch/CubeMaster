/**
 * @fileoverview API 请求模块
 *
 * 提供与后端通信的接口封装，包括魔方求解、状态保存和识别功能。
 * API 基础地址通过环境变量配置。
 *
 * @module api/cubeService
 */

import axios from "axios";

/**
 * API 基础地址
 * - 开发环境: http://127.0.0.1:8000 (.env.development)
 * - 生产环境: /api (.env.production，通过代理或同源访问)
 */
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

/**
 * 获取魔方解法
 *
 * @returns {Promise<import('axios').AxiosResponse>} 求解结果
 */
export function solveCube() {
  return axios.post(`${BASE_URL}/api/solve`);
}

/**
 * 保存魔方状态到服务器
 *
 * @param {Object} facesData - 六面颜色数据
 * @returns {Promise<import('axios').AxiosResponse>} 保存结果
 */
export function saveCubeState(facesData) {
  return axios.post(`${BASE_URL}/api/save_state`, facesData);
}

/**
 * 识别魔方状态
 *
 * @param {Object} payload - 包含 images 字段的请求体
 * @param {Object} [payload.images] - 面名到 base64 图片的映射
 * @returns {Promise<import('axios').AxiosResponse>} 识别结果
 */
export function recognizeCube(payload) {
  return axios.post(`${BASE_URL}/api/recognize`, payload, {
    timeout: 300000,
  });
}
