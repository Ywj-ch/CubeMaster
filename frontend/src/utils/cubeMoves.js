// 控制魔方转动
// 顺时针旋转一个面（3x3）
function rotateFaceCW(face) {
  return [
    face[6], face[3], face[0],
    face[7], face[4], face[1],
    face[8], face[5], face[2],
  ];
}

// F 面旋转
function moveF(cube) {
  cube.F = rotateFaceCW(cube.F);
  const temp = cube.U.slice(6, 9);
  cube.U[6] = cube.L[8]; cube.U[7] = cube.L[5]; cube.U[8] = cube.L[2];
  cube.L[2] = cube.D[0]; cube.L[5] = cube.D[1]; cube.L[8] = cube.D[2];
  cube.D[0] = cube.R[6]; cube.D[1] = cube.R[3]; cube.D[2] = cube.R[0];
  cube.R[0] = temp[0]; cube.R[3] = temp[1]; cube.R[6] = temp[2];
}

// B 面旋转
function moveB(cube) {
  cube.B = rotateFaceCW(cube.B);
  const temp = cube.U.slice(0, 3);
  cube.U[0] = cube.R[2]; cube.U[1] = cube.R[5]; cube.U[2] = cube.R[8];
  cube.R[2] = cube.D[8]; cube.R[5] = cube.D[7]; cube.R[8] = cube.D[6];
  cube.D[6] = cube.L[0]; cube.D[7] = cube.L[3]; cube.D[8] = cube.L[6];
  cube.L[0] = temp[2]; cube.L[3] = temp[1]; cube.L[6] = temp[0];
}

// U 面旋转
function moveU(cube) {
  cube.U = rotateFaceCW(cube.U);
  const temp = cube.F.slice(0, 3);
  cube.F[0] = cube.R[0]; cube.F[1] = cube.R[1]; cube.F[2] = cube.R[2];
  cube.R[0] = cube.B[0]; cube.R[1] = cube.B[1]; cube.R[2] = cube.B[2];
  cube.B[0] = cube.L[0]; cube.B[1] = cube.L[1]; cube.B[2] = cube.L[2];
  cube.L[0] = temp[0]; cube.L[1] = temp[1]; cube.L[2] = temp[2];
}

// D 面旋转
function moveD(cube) {
  cube.D = rotateFaceCW(cube.D);
  const temp = cube.F.slice(6, 9);
  cube.F[6] = cube.L[6]; cube.F[7] = cube.L[7]; cube.F[8] = cube.L[8];
  cube.L[6] = cube.B[6]; cube.L[7] = cube.B[7]; cube.L[8] = cube.B[8];
  cube.B[6] = cube.R[6]; cube.B[7] = cube.R[7]; cube.B[8] = cube.R[8];
  cube.R[6] = temp[0]; cube.R[7] = temp[1]; cube.R[8] = temp[2];
}

// L 面旋转
function moveL(cube) {
  cube.L = rotateFaceCW(cube.L);
  const temp = [cube.U[0], cube.U[3], cube.U[6]];
  cube.U[0] = cube.B[8]; cube.U[3] = cube.B[5]; cube.U[6] = cube.B[2];
  cube.B[2] = cube.D[6]; cube.B[5] = cube.D[3]; cube.B[8] = cube.D[0];
  cube.D[0] = cube.F[0]; cube.D[3] = cube.F[3]; cube.D[6] = cube.F[6];
  cube.F[0] = temp[0]; cube.F[3] = temp[1]; cube.F[6] = temp[2];
}

// R 面旋转
function moveR(cube) {
  cube.R = rotateFaceCW(cube.R);
  const temp = [cube.U[2], cube.U[5], cube.U[8]];
  cube.U[2] = cube.F[2]; cube.U[5] = cube.F[5]; cube.U[8] = cube.F[8];
  cube.F[2] = cube.D[2]; cube.F[5] = cube.D[5]; cube.F[8] = cube.D[8];
  cube.D[2] = cube.B[6]; cube.D[5] = cube.B[3]; cube.D[8] = cube.B[0];
  cube.B[0] = temp[2]; cube.B[3] = temp[1]; cube.B[6] = temp[0];
}


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

  const face = move[0];        // F / B / U ...
  const suffix = move.slice(1); // "", "2", "'"

  const fn = baseMoves[face];
  if (!fn) {
    console.warn("未实现的 move:", move);
    return;
  }

  if (suffix === "") {
    fn(cube);
  } else if (suffix === "2") {
    fn(cube);
    fn(cube);
  } else if (suffix === "'") {
    fn(cube);
    fn(cube);
    fn(cube);
  } else {
    console.warn("非法 move 格式:", move);
  }
}

export function invertMove(move) {
  if (!move || typeof move !== "string") return move;

  const suffix = move.slice(1);
  const face = move[0];

  if (suffix === "'") return face;       // X' → X
  if (suffix === "2") return move;       // X2 → X2
  return face + "'";                     // X → X'
}

