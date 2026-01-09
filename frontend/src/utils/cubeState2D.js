// cubeState2D.js
// 返回二维魔方状态

export function create2DCubeFromJson(cubeJson = null) {
  const flatten = (face) => face.flat();
  // 处理数据为空的情况
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
    };
  }
  // 根据 json 返回 2D 魔方状态
  return {
    faces: {
      U: flatten(cubeJson.U),
      D: flatten(cubeJson.D),
      L: flatten(cubeJson.L),
      R: flatten(cubeJson.R),
      F: flatten(cubeJson.F),
      B: flatten(cubeJson.B),
    },
  };
}
