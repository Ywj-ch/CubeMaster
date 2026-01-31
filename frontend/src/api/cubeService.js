// 接口请求模块
import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

// 获取魔方解法
export function solveCube() {
  return axios.post(`${BASE_URL}/api/solve`);
}

// 保存魔方状态
export function saveCubeState(facesData) {
  return axios.post(`${BASE_URL}/api/save_state`, facesData);
}

// 识别魔方状态
export function recognizeCube(payload) {
  return axios.post(`${BASE_URL}/api/recognize`, payload, {
    timeout: 300000,
  });
}
