/**
 * @fileoverview API 请求模块
 *
 * 提供与后端通信的接口封装，包括魔方求解、状态保存、识别和会话管理功能。
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
 * 创建新的用户会话
 *
 * 后端会为该会话创建独立的文件存储目录，实现多用户并发隔离。
 *
 * @returns {Promise<import('axios').AxiosResponse>} 包含 session_id 的响应
 */
export function createSession() {
  return axios.post(`${BASE_URL}/api/session`);
}

/**
 * 销毁指定会话，删除其所有文件
 *
 * @param {string} sessionId - 要销毁的会话 ID
 * @returns {Promise<import('axios').AxiosResponse>} 销毁结果
 */
export function closeSession(sessionId) {
  return axios.delete(`${BASE_URL}/api/session/${sessionId}`);
}

/**
 * 获取魔方解法
 *
 * @param {string} [sessionId] - 会话 ID，用于文件隔离
 * @returns {Promise<import('axios').AxiosResponse>} 求解结果
 */
export function solveCube(sessionId) {
  const payload = {};
  if (sessionId) {
    payload.session_id = sessionId;
  }
  return axios.post(`${BASE_URL}/api/solve`, payload);
}

/**
 * 保存魔方状态到服务器
 *
 * @param {Object} facesData - 六面颜色数据
 * @param {string} [sessionId] - 会话 ID，用于文件隔离
 * @returns {Promise<import('axios').AxiosResponse>} 保存结果
 */
export function saveCubeState(facesData, sessionId) {
  const payload = { ...facesData };
  if (sessionId) {
    payload.session_id = sessionId;
  }
  return axios.post(`${BASE_URL}/api/save_state`, payload);
}

/**
 * 识别魔方状态
 *
 * @param {Object} payload - 包含 images 字段的请求体
 * @param {Object} [payload.images] - 面名到 base64 图片的映射
 * @param {string} [sessionId] - 会话 ID，用于文件隔离
 * @returns {Promise<import('axios').AxiosResponse>} 识别结果
 */
export function recognizeCube(payload, sessionId) {
  const data = { ...payload };
  if (sessionId) {
    data.session_id = sessionId;
  }
  return axios.post(`${BASE_URL}/api/recognize`, data, {
    timeout: 300000,
  });
}
