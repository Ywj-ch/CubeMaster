// 定义魔方状态
export function createCubeFromJson(cubeJson = null) {
  const flatten = (face) => face.flat();

  if (!cubeJson) {
    return {
      U: Array(9).fill("white"),
      D: Array(9).fill("yellow"),
      L: Array(9).fill("orange"),
      R: Array(9).fill("red"),
      F: Array(9).fill("green"),
      B: Array(9).fill("blue"),
    };
  }

  return {
    U: flatten(cubeJson.U),
    D: flatten(cubeJson.D),
    L: flatten(cubeJson.L),
    R: flatten(cubeJson.R),
    F: flatten(cubeJson.F),
    B: flatten(cubeJson.B),
  };
}
