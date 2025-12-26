// 控制魔方转动
// 顺时针旋转一个面（3x3）
function rotateFaceCW(face) {
  return [
    face[6], face[3], face[0],
    face[7], face[4], face[1],
    face[8], face[5], face[2],
  ];
}

// 逆时针 = 顺时针转三次
function rotateFaceCCW(face) {
  return rotateFaceCW(rotateFaceCW(rotateFaceCW(face)));
}

// 180° = 顺时针转两次
function rotateFace180(face) {
  return rotateFaceCW(rotateFaceCW(face));
}

export function applyMove(cube, move) {
  switch (move) {
    case "U":
      cube.U = rotateFaceCW(cube.U);
      break;
    case "U'":
      cube.U = rotateFaceCCW(cube.U);
      break;
    case "U2":
      cube.U = rotateFace180(cube.U);
      break;
    default:
      console.warn("未实现的 move:", move);
  }
}