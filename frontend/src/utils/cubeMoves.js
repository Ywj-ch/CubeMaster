// 控制魔方转动
// 顺时针旋转一个面（3x3）
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
