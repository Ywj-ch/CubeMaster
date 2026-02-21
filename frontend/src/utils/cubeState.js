/**
 * @fileoverview 魔方状态管理模块
 * 
 * 提供魔方状态的创建和管理功能，支持从 JSON 数据生成 2D/3D 渲染所需的状态对象。
 * 
 * @module utils/cubeState
 */

/**
 * 面颜色数据结构
 * @typedef {Object} CubeFaces
 * @property {string[]} U - 顶面 (白色)
 * @property {string[]} D - 底面 (黄色)
 * @property {string[]} L - 左面 (橙色)
 * @property {string[]} R - 右面 (红色)
 * @property {string[]} F - 前面 (绿色)
 * @property {string[]} B - 后面 (蓝色)
 */

/**
 * 小方块数据结构
 * @typedef {Object} Cubie
 * @property {string} id - 小方块标识 (如 "URF", "DLF")
 * @property {number[]} pos - 三维坐标 [x, y, z]
 */

/**
 * 小方块集合
 * @typedef {Object} Cubies
 * @property {Cubie[]} corners - 角块 (8个)
 * @property {Cubie[]} edges - 棱块 (12个)
 * @property {Cubie[]} centers - 中心块 (6个)
 */

/**
 * 魔方状态对象
 * @typedef {Object} CubeState
 * @property {CubeFaces} faces - 六面颜色数据
 * @property {Cubies} cubies - 小方块几何信息
 */

/**
 * 从 JSON 数据创建魔方状态对象
 * 
 * @param {Object|null} [cubeJson=null] - 可选的 JSON 数据，包含六面颜色数组
 * @param {string[]|string[][]} [cubeJson.U] - 顶面颜色
 * @param {string[]|string[][]} [cubeJson.D] - 底面颜色
 * @param {string[]|string[][]} [cubeJson.L] - 左面颜色
 * @param {string[]|string[][]} [cubeJson.R] - 右面颜色
 * @param {string[]|string[][]} [cubeJson.F] - 前面颜色
 * @param {string[]|string[][]} [cubeJson.B] - 后面颜色
 * @returns {CubeState} 魔方状态对象，包含 faces 和 cubies
 * 
 * @example
 * // 创建复原状态的魔方
 * const solvedCube = createCubeFromJson();
 * 
 * @example
 * // 从 JSON 数据创建
 * const cube = createCubeFromJson({
 *   U: ['white', 'white', ...],
 *   D: ['yellow', 'yellow', ...],
 *   ...
 * });
 */
export function createCubeFromJson(cubeJson = null) {
  const flatten = (face) => face.flat();

  if (!cubeJson) {
    return {
      faces: {
        U: Array(9).fill("white"),
        D: Array(9).fill("yellow"),
        L: Array(9).fill("orange"),
        R: Array(9).fill("red"),
        F: Array(9).fill("green"),
        B: Array(9).fill("blue"),
      },
      cubies: createCubieGeometry(),
    };
  }

  return {
    faces: {
      U: flatten(cubeJson.U),
      D: flatten(cubeJson.D),
      L: flatten(cubeJson.L),
      R: flatten(cubeJson.R),
      F: flatten(cubeJson.F),
      B: flatten(cubeJson.B),
    },
    cubies: createCubieGeometry(),
  };
}

/**
 * 创建小方块几何信息
 * 
 * 生成魔方所有小块的位置信息，用于 3D 渲染。
 * - 角块：3面可见，8个
 * - 棱块：2面可见，12个
 * - 中心块：1面可见，6个
 * 
 * @returns {Cubies} 小方块集合
 * @private
 */
function createCubieGeometry() {
  return {
    corners: [
      { id: "URF", pos: [1, 1, 1] },
      { id: "UFL", pos: [-1, 1, 1] },
      { id: "ULB", pos: [-1, 1, -1] },
      { id: "UBR", pos: [1, 1, -1] },

      { id: "DFR", pos: [1, -1, 1] },
      { id: "DLF", pos: [-1, -1, 1] },
      { id: "DBL", pos: [-1, -1, -1] },
      { id: "DRB", pos: [1, -1, -1] },
    ],
    edges: [
      { id: "UR", pos: [1, 1, 0] },
      { id: "UF", pos: [0, 1, 1] },
      { id: "UL", pos: [-1, 1, 0] },
      { id: "UB", pos: [0, 1, -1] },

      { id: "FR", pos: [1, 0, 1] },
      { id: "FL", pos: [-1, 0, 1] },
      { id: "BL", pos: [-1, 0, -1] },
      { id: "BR", pos: [1, 0, -1] },

      { id: "DR", pos: [1, -1, 0] },
      { id: "DF", pos: [0, -1, 1] },
      { id: "DL", pos: [-1, -1, 0] },
      { id: "DB", pos: [0, -1, -1] },
    ],
    centers: [
      { id: "U", pos: [0, 1, 0] },
      { id: "D", pos: [0, -1, 0] },
      { id: "F", pos: [0, 0, 1] },
      { id: "B", pos: [0, 0, -1] },
      { id: "R", pos: [1, 0, 0] },
      { id: "L", pos: [-1, 0, 0] },
    ],
  };
}
