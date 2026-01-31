// src/utils/cubeLogic.js

// 定义魔方的面索引
// U:0, R:1, F:2, D:3, L:4, B:5
// 每个面有 9 个块，索引 0-8

// 初始复原状态 (6面 * 9块)
// U:白(0), R:红(1), F:绿(2), D:黄(3), L:橙(4), B:蓝(5)
// 注意：这里用数字代表颜色，渲染时再映射回颜色字符串
export const SOLVED_STATE = [
  Array(9).fill(0), // U
  Array(9).fill(1), // R
  Array(9).fill(2), // F
  Array(9).fill(3), // D
  Array(9).fill(4), // L
  Array(9).fill(5), // B
];

// 颜色映射表 (用于转换回 Cube3DView 需要的格式)
// 遵循 standard: U=White, R=Red, F=Green, D=Yellow, L=Orange, B=Blue
const COLOR_MAP = ["white", "red", "green", "yellow", "orange", "blue"];

/**
 * 深拷贝状态
 */
export function cloneState(state) {
  return state.map((face) => [...face]);
}

/**
 * 将数字状态转换为颜色字符串状态 (供 3DView 使用)
 */
export function stateToColors(state) {
  return state.map((face) => face.map((colorIndex) => COLOR_MAP[colorIndex]));
}

/**
 * 核心旋转逻辑
 * @param {Array} state 当前状态
 * @param {String} move 动作 (e.g., "R", "U'", "F2")
 */
export function applyMove(state, move) {
  const baseMove = move[0]; // R, L, U...
  const suffix = move.substring(1); // ', 2, or empty

  let times = 1;
  if (suffix === "'")
    times = 3; // 逆时针 = 顺时针转3次
  else if (suffix === "2") times = 2;

  const newState = cloneState(state);

  for (let i = 0; i < times; i++) {
    rotateOnce(newState, baseMove);
  }

  return newState;
}

// 旋转一次 (顺时针 90度)
function rotateOnce(s, face) {
  // 1. 旋转面本身的 9 个块 (顺时针 90度)
  const faceIdx = getFaceIndex(face);
  const oldFace = [...s[faceIdx]];
  // 0 1 2    6 3 0
  // 3 4 5 -> 7 4 1
  // 6 7 8    8 5 2
  s[faceIdx][0] = oldFace[6];
  s[faceIdx][1] = oldFace[3];
  s[faceIdx][2] = oldFace[0];
  s[faceIdx][3] = oldFace[7];
  s[faceIdx][4] = oldFace[4];
  s[faceIdx][5] = oldFace[1];
  s[faceIdx][6] = oldFace[8];
  s[faceIdx][7] = oldFace[5];
  s[faceIdx][8] = oldFace[2];

  // 2. 旋转侧边块 (核心修正点)
  let temp;
  switch (face) {
    case "U": // 涉及 F, R, B, L 的顶行 (0,1,2)
      temp = [s[2][0], s[2][1], s[2][2]]; // 暂存 F 顶行
      s[2][0] = s[1][0];
      s[2][1] = s[1][1];
      s[2][2] = s[1][2]; // F = R
      s[1][0] = s[5][0];
      s[1][1] = s[5][1];
      s[1][2] = s[5][2]; // R = B
      s[5][0] = s[4][0];
      s[5][1] = s[4][1];
      s[5][2] = s[4][2]; // B = L
      s[4][0] = temp[0];
      s[4][1] = temp[1];
      s[4][2] = temp[2]; // L = F
      break;

    case "D": // 涉及 F, R, B, L 的底行 (6,7,8)
      temp = [s[2][6], s[2][7], s[2][8]]; // 暂存 F 底行
      s[2][6] = s[4][6];
      s[2][7] = s[4][7];
      s[2][8] = s[4][8]; // F = L
      s[4][6] = s[5][6];
      s[4][7] = s[5][7];
      s[4][8] = s[5][8]; // L = B
      s[5][6] = s[1][6];
      s[5][7] = s[1][7];
      s[5][8] = s[1][8]; // B = R
      s[1][6] = temp[0];
      s[1][7] = temp[1];
      s[1][8] = temp[2]; // R = F
      break;

    case "L": // 涉及 U, F, D, B 的左列
      temp = [s[0][0], s[0][3], s[0][6]]; // U 左列
      s[0][0] = s[5][8];
      s[0][3] = s[5][5];
      s[0][6] = s[5][2]; // U = B倒序 (B面特殊)
      s[5][8] = s[3][0];
      s[5][5] = s[3][3];
      s[5][2] = s[3][6]; // B = D倒序
      s[3][0] = s[2][0];
      s[3][3] = s[2][3];
      s[3][6] = s[2][6]; // D = F
      s[2][0] = temp[0];
      s[2][3] = temp[1];
      s[2][6] = temp[2]; // F = U
      break;

    case "R": // 涉及 U, F, D, B 的右列
      temp = [s[0][2], s[0][5], s[0][8]]; // U 右列
      s[0][2] = s[2][2];
      s[0][5] = s[2][5];
      s[0][8] = s[2][8]; // U = F
      s[2][2] = s[3][2];
      s[2][5] = s[3][5];
      s[2][8] = s[3][8]; // F = D
      s[3][2] = s[5][6];
      s[3][5] = s[5][3];
      s[3][8] = s[5][0]; // D = B倒序
      s[5][6] = temp[0];
      s[5][3] = temp[1];
      s[5][0] = temp[2]; // B = U倒序
      break;

    case "F": // 涉及 U底行, R左列, D顶行, L右列
      temp = [s[0][6], s[0][7], s[0][8]]; // U 底行
      s[0][6] = s[4][8];
      s[0][7] = s[4][5];
      s[0][8] = s[4][2]; // U = L右列倒序
      s[4][8] = s[3][2];
      s[4][5] = s[3][1];
      s[4][2] = s[3][0]; // L = D顶行倒序
      s[3][0] = s[1][6];
      s[3][1] = s[1][3];
      s[3][2] = s[1][0]; // D = R左列倒序
      s[1][6] = temp[2];
      s[1][3] = temp[1];
      s[1][0] = temp[0]; // R = U底行倒序
      break;

    case "B": // 涉及 U顶行, L左列, D底行, R右列
      temp = [s[0][0], s[0][1], s[0][2]]; // U 顶行
      s[0][0] = s[1][2];
      s[0][1] = s[1][5];
      s[0][2] = s[1][8]; // U = R右列
      s[1][2] = s[3][8];
      s[1][5] = s[3][7];
      s[1][8] = s[3][6]; // R = D底行
      s[3][8] = s[4][6];
      s[3][7] = s[4][3];
      s[3][6] = s[4][0]; // D = L左列
      s[4][6] = temp[0];
      s[4][3] = temp[1];
      s[4][0] = temp[2]; // L = U顶行
      break;
  }
}

function getFaceIndex(faceChar) {
  const map = { U: 0, R: 1, F: 2, D: 3, L: 4, B: 5 };
  return map[faceChar];
}
