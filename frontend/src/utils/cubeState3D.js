// cubeState3D.js

const COLOR_TO_FACE = {
  white: "U",
  red: "R",
  green: "F",
  yellow: "D",
  orange: "L",
  blue: "B",
};

const CORNER_DEFS = {
  URF: ["U", "R", "F"],
  UFL: ["U", "F", "L"],
  ULB: ["U", "L", "B"],
  UBR: ["U", "B", "R"],
  DFR: ["D", "F", "R"],
  DLF: ["D", "L", "F"],
  DBL: ["D", "B", "L"],
  DRB: ["D", "R", "B"],
};

const EDGE_DEFS = {
  UR: ["U", "R"],
  UF: ["U", "F"],
  UL: ["U", "L"],
  UB: ["U", "B"],
  FR: ["F", "R"],
  FL: ["F", "L"],
  BL: ["B", "L"],
  BR: ["B", "R"],
  DR: ["D", "R"],
  DF: ["D", "F"],
  DL: ["D", "L"],
  DB: ["D", "B"],
};

export function create3DCubeFromJson(cubeJson = null) {
  // 复原态
  if (!cubeJson) {
    return {
      corners: Object.keys(CORNER_DEFS).map(id => ({ id, slot: id, ori: 0 })),
      edges: Object.keys(EDGE_DEFS).map(id => ({ id, slot: id, ori: 0 })),
      centers: ["U","D","L","R","F","B"].map(id => ({ id, slot: id })),
      orientation: { up: "U", front: "F" },
    };
  }

  const faces = {
    U: cubeJson.U.flat(),
    D: cubeJson.D.flat(),
    L: cubeJson.L.flat(),
    R: cubeJson.R.flat(),
    F: cubeJson.F.flat(),
    B: cubeJson.B.flat(),
  };

  // ===== 角块 =====
  const cornerIndices = {
    URF: ["U2", "R0", "F2"],
    UFL: ["U0", "F0", "L2"],
    ULB: ["U6", "L0", "B2"],
    UBR: ["U8", "B0", "R2"],
    DFR: ["D2", "F8", "R6"],
    DLF: ["D0", "L8", "F6"],
    DBL: ["D6", "B8", "L6"],
    DRB: ["D8", "R8", "B6"],
  };

  const corners = Object.entries(cornerIndices).map(([slot, stickers]) => {
    const facesSeen = stickers.map(s => {
      const face = s[0];
      const idx = Number(s.slice(1));
      return COLOR_TO_FACE[faces[face][idx]];
    });

    const id = Object.keys(CORNER_DEFS).find(cid =>
      CORNER_DEFS[cid].every(f => facesSeen.includes(f))
    );

    const upDown = CORNER_DEFS[id].find(f => f === "U" || f === "D");
    const pos = facesSeen.indexOf(upDown);
    const faceAt = stickers[pos][0];

    const ori =
      faceAt === "U" || faceAt === "D" ? 0 :
      faceAt === "R" || faceAt === "L" ? 1 : 2;

    return { id, slot, ori };
  });

  // ===== 边块 =====
  const edgeIndices = {
    UR: ["U5","R1"],
    UF: ["U1","F1"],
    UL: ["U3","L1"],
    UB: ["U7","B1"],
    FR: ["F5","R3"],
    FL: ["F3","L5"],
    BL: ["B3","L3"],
    BR: ["B5","R5"],
    DR: ["D5","R7"],
    DF: ["D1","F7"],
    DL: ["D3","L7"],
    DB: ["D7","B7"],
  };

  const edges = Object.entries(edgeIndices).map(([slot, stickers]) => {
    const facesSeen = stickers.map(s => {
      const face = s[0];
      const idx = Number(s.slice(1));
      return COLOR_TO_FACE[faces[face][idx]];
    });

    const id = Object.keys(EDGE_DEFS).find(eid =>
      EDGE_DEFS[eid].every(f => facesSeen.includes(f))
    );

    const main = EDGE_DEFS[id].find(f => f === "U" || f === "D") ||
                 EDGE_DEFS[id].find(f => f === "F" || f === "B");

    const pos = facesSeen.indexOf(main);
    const faceAt = stickers[pos][0];

    const ori =
      faceAt === main ? 0 : 1;

    return { id, slot, ori };
  });

  const centers = ["U","D","L","R","F","B"].map(id => ({ id, slot: id }));

  return {
    corners,
    edges,
    centers,
    orientation: { up: "U", front: "F" },
  };
}
