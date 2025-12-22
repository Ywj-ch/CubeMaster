import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

export function pingBackend() {
  return axios.get(`${BASE_URL}/api/ping`);
}

export function solveCube() {
  return axios.post(`${BASE_URL}/api/solve`);
}