// 控制魔方转动
import { COLOR_NAMES, COLOR_INDEX } from "../constants/colors";

/**
 * @fileoverview 魔方旋转逻辑模块
 *
 * 提供魔方状态管理和旋转操作，支持对象格式和数字数组格式的状态表示。
 * 对象格式: { faces: { U:[], D:[], F:[], B:[], L:[], R:[] } }
 * 数字数组格式: [[9个颜色], [9个颜色], ...] 共6面
 *
 * @module utils/cubeMoves
 */

/**
 * 复原状态的魔方（对象格式）
 * @constant {Object}
 */
export const SOLVED_STATE = {
  faces: {
    U: Array(9).fill("white"),
    D: Array(9).fill("yellow"),
    F: Array(9).fill("red"),
    B: Array(9).fill("orange"),
    L: Array(9).fill("blue"),
    R: Array(9).fill("green"),
  },
};

/**
 * 复原状态的魔方（数字数组格式）
 * 索引顺序: 0=U(白), 1=D(黄), 2=F(红), 3=B(橙), 4=L(蓝), 5=R(绿)
 * @constant {number[][]}
 */
export const SOLVED_STATE_NUMERIC = [
  Array(9).fill(0),
  Array(9).fill(1),
  Array(9).fill(2),
  Array(9).fill(3),
  Array(9).fill(4),
  Array(9).fill(5),
];

/**
 * 深拷贝魔方状态（对象格式）
 * @param {Object} cube - 魔方状态对象
 * @returns {Object} 深拷贝的状态
 */
export function cloneState(cube) {
  return {
    faces: {
      U: [...cube.faces.U],
      D: [...cube.faces.D],
      F: [...cube.faces.F],
      B: [...cube.faces.B],
      L: [...cube.faces.L],
      R: [...cube.faces.R],
    },
  };
}

/**
 * 深拷贝魔方状态（数字数组格式）
 * @param {number[][]} state - 数字数组状态
 * @returns {number[][]} 深拷贝的状态
 */
export function cloneStateNumeric(state) {
  return state.map((face) => [...face]);
}

/**
 * 将数字数组状态转换为对象状态
 * @param {number[][]} numericState - 6x9 数字数组
 * @returns {Object} 对象格式的魔方状态
 */
export function numericToObject(numericState) {
  const faceOrder = ["U", "D", "F", "B", "L", "R"];
  const faces = {};

  faceOrder.forEach((face, idx) => {
    faces[face] = numericState[idx].map((colorIdx) => COLOR_NAMES[colorIdx]);
  });

  return { faces };
}

/**
 * 将对象状态转换为数字数组状态
 * @param {Object} objectState - 对象格式的魔方状态
 * @returns {number[][]} 6x9 数字数组
 */
export function objectToNumeric(objectState) {
  const faceOrder = ["U", "D", "F", "B", "L", "R"];

  return faceOrder.map((face) =>
    objectState.faces[face].map((color) => COLOR_INDEX[color] ?? 0),
  );
}

/**
 * 将对象状态转换为 Cube3DView 需要的颜色数组格式
 * @param {Object} cube - 对象格式的魔方状态
 * @returns {string[][]} 颜色字符串数组 [[U的9色], [R的9色], [F的9色], [D的9色], [L的9色], [B的9色]]
 */
export function stateToColors(cube) {
  return [
    cube.faces.U,
    cube.faces.R,
    cube.faces.F,
    cube.faces.D,
    cube.faces.L,
    cube.faces.B,
  ];
}

/**
 * 将数字数组状态转换为颜色字符串数组
 * @param {number[][]} state - 数字数组状态
 * @returns {string[][]} 颜色字符串数组
 */
export function numericToColors(state) {
  return state.map((face) => face.map((colorIdx) => COLOR_NAMES[colorIdx]));
}

/**
 * 顺时针旋转一个面（3x3）
 * @param {Array} face - 面的9个元素数组
 * @returns {Array} 旋转后的面
 */
function rotateFaceCW(face) {
  return [
    face[6],
    face[3],
    face[0],
    face[7],
    face[4],
    face[1],
    face[8],
    face[5],
    face[2],
  ];
}

// F 面旋转
function moveF(cube) {
  cube.faces.F = rotateFaceCW(cube.faces.F);
  const temp = cube.faces.U.slice(6, 9);
  cube.faces.U[6] = cube.faces.L[8];
  cube.faces.U[7] = cube.faces.L[5];
  cube.faces.U[8] = cube.faces.L[2];
  cube.faces.L[2] = cube.faces.D[0];
  cube.faces.L[5] = cube.faces.D[1];
  cube.faces.L[8] = cube.faces.D[2];
  cube.faces.D[0] = cube.faces.R[6];
  cube.faces.D[1] = cube.faces.R[3];
  cube.faces.D[2] = cube.faces.R[0];
  cube.faces.R[0] = temp[0];
  cube.faces.R[3] = temp[1];
  cube.faces.R[6] = temp[2];
}

// B 面旋转
function moveB(cube) {
  cube.faces.B = rotateFaceCW(cube.faces.B);
  const temp = cube.faces.U.slice(0, 3);
  cube.faces.U[0] = cube.faces.R[2];
  cube.faces.U[1] = cube.faces.R[5];
  cube.faces.U[2] = cube.faces.R[8];
  cube.faces.R[2] = cube.faces.D[8];
  cube.faces.R[5] = cube.faces.D[7];
  cube.faces.R[8] = cube.faces.D[6];
  cube.faces.D[6] = cube.faces.L[0];
  cube.faces.D[7] = cube.faces.L[3];
  cube.faces.D[8] = cube.faces.L[6];
  cube.faces.L[0] = temp[2];
  cube.faces.L[3] = temp[1];
  cube.faces.L[6] = temp[0];
}

// U 面旋转
function moveU(cube) {
  cube.faces.U = rotateFaceCW(cube.faces.U);
  const temp = cube.faces.F.slice(0, 3);
  cube.faces.F[0] = cube.faces.R[0];
  cube.faces.F[1] = cube.faces.R[1];
  cube.faces.F[2] = cube.faces.R[2];
  cube.faces.R[0] = cube.faces.B[0];
  cube.faces.R[1] = cube.faces.B[1];
  cube.faces.R[2] = cube.faces.B[2];
  cube.faces.B[0] = cube.faces.L[0];
  cube.faces.B[1] = cube.faces.L[1];
  cube.faces.B[2] = cube.faces.L[2];
  cube.faces.L[0] = temp[0];
  cube.faces.L[1] = temp[1];
  cube.faces.L[2] = temp[2];
}

// D 面旋转
function moveD(cube) {
  cube.faces.D = rotateFaceCW(cube.faces.D);
  const temp = cube.faces.F.slice(6, 9);
  cube.faces.F[6] = cube.faces.L[6];
  cube.faces.F[7] = cube.faces.L[7];
  cube.faces.F[8] = cube.faces.L[8];
  cube.faces.L[6] = cube.faces.B[6];
  cube.faces.L[7] = cube.faces.B[7];
  cube.faces.L[8] = cube.faces.B[8];
  cube.faces.B[6] = cube.faces.R[6];
  cube.faces.B[7] = cube.faces.R[7];
  cube.faces.B[8] = cube.faces.R[8];
  cube.faces.R[6] = temp[0];
  cube.faces.R[7] = temp[1];
  cube.faces.R[8] = temp[2];
}

// L 面旋转
function moveL(cube) {
  cube.faces.L = rotateFaceCW(cube.faces.L);
  const temp = [cube.faces.U[0], cube.faces.U[3], cube.faces.U[6]];
  cube.faces.U[0] = cube.faces.B[8];
  cube.faces.U[3] = cube.faces.B[5];
  cube.faces.U[6] = cube.faces.B[2];
  cube.faces.B[2] = cube.faces.D[6];
  cube.faces.B[5] = cube.faces.D[3];
  cube.faces.B[8] = cube.faces.D[0];
  cube.faces.D[0] = cube.faces.F[0];
  cube.faces.D[3] = cube.faces.F[3];
  cube.faces.D[6] = cube.faces.F[6];
  cube.faces.F[0] = temp[0];
  cube.faces.F[3] = temp[1];
  cube.faces.F[6] = temp[2];
}

// R 面旋转
function moveR(cube) {
  cube.faces.R = rotateFaceCW(cube.faces.R);
  const temp = [cube.faces.U[2], cube.faces.U[5], cube.faces.U[8]];
  cube.faces.U[2] = cube.faces.F[2];
  cube.faces.U[5] = cube.faces.F[5];
  cube.faces.U[8] = cube.faces.F[8];
  cube.faces.F[2] = cube.faces.D[2];
  cube.faces.F[5] = cube.faces.D[5];
  cube.faces.F[8] = cube.faces.D[8];
  cube.faces.D[2] = cube.faces.B[6];
  cube.faces.D[5] = cube.faces.B[3];
  cube.faces.D[8] = cube.faces.B[0];
  cube.faces.B[0] = temp[2];
  cube.faces.B[3] = temp[1];
  cube.faces.B[6] = temp[0];
}

// 应用 move
export function applyMove(cube, move) {
  if (!move || typeof move !== "string") {
    console.warn("非法 move:", move);
    return;
  }

  const baseMoves = {
    F: moveF,
    B: moveB,
    U: moveU,
    D: moveD,
    L: moveL,
    R: moveR,
  };

  const face = move[0];
  const suffix = move.slice(1);

  const fn = baseMoves[face];
  if (!fn) {
    console.warn("未实现的 move:", move);
    return;
  }

  if (suffix === "") fn(cube);
  else if (suffix === "2") {
    fn(cube);
    fn(cube);
  } else if (suffix === "'") {
    fn(cube);
    fn(cube);
    fn(cube);
  } else console.warn("非法 move 格式:", move);
}

// 反向 move
export function invertMove(move) {
  if (!move || typeof move !== "string") return move;
  const suffix = move.slice(1);
  const face = move[0];
  if (suffix === "'") return face;
  if (suffix === "2") return move;
  return face + "'";
}

/**
 * 对数字数组状态应用移动（兼容 cubeLogic 接口）
 * @param {number[][]} state - 数字数组状态
 * @param {string} move - 移动指令
 * @returns {number[][]} 新状态
 */
export function applyMoveNumeric(state, move) {
  const cube = numericToObject(state);
  applyMove(cube, move);
  return objectToNumeric(cube);
}
