// cubeState.js
// 返回二维以及三维魔方状态

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
