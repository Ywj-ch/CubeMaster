// 定义魔方状态
export function createInitialCube() {
  return {
    U: ["U1","U2","U3","U4","U5","U6","U7","U8","U9"],
    D: Array(9).fill("D"),
    L: Array(9).fill("L"),
    R: Array(9).fill("R"),
    F: Array(9).fill("F"),
    B: Array(9).fill("B"),
  };
}