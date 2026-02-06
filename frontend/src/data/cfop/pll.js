/**
 * CFOP - PLL (Permutation of Last Layer) 完整算法库
 * 共 21 个公式
 *
 * 技术说明:
 * - algorithm: 展示给用户的标准速拧公式 (可能包含 M, x, y)
 * - demoAlgorithm: 供 3D 引擎使用的纯面转动公式 (无 M, x, y)
 * - setup: demoAlgorithm 的逆序，用于生成初始状态
 */

export const pllAlgorithms = [
  // ================= 1. 仅棱块交换 (Edges Only) =================
  {
    id: "pll-ua",
    name: "Ua Perm",
    category: "edges",
    tags: ["逆时针", "常用"],
    recognition: "一侧完全还原，其余三边棱块需要【逆时针】轮换。背面有大灯。",
    difficulty: 1,
    algorithm: "R U' R U R U R U' R' U' R2",
    // 纯 RU 公式，直接使用
    setup: "R2 U R U R' U' R' U' R' U R'",
  },
  {
    id: "pll-ub",
    name: "Ub Perm",
    category: "edges",
    tags: ["顺时针", "常用"],
    recognition: "一侧完全还原，其余三边棱块需要【顺时针】轮换。前面有大灯。",
    difficulty: 1,
    algorithm: "R2 U R U R' U' R' U' R' U R'",
    setup: "R U' R U R U R U' R' U' R2",
  },
  {
    id: "pll-h",
    name: "H Perm",
    category: "edges",
    tags: ["M层", "对称"],
    recognition: "没有一面是还原的。前后棱块互换，左右棱块互换 (十字对换)。",
    difficulty: 1,
    algorithm: "M2 U M2 U2 M2 U M2",
    // 3D 引擎不支持 M，使用等价的 RU 公式演示
    demoAlgorithm: "R2 U2 R U2 R2 U2 R2 U2 R U2 R2",
    setup: "R2 U2 R' U2 R2 U2 R2 U2 R' U2 R2",
  },
  {
    id: "pll-z",
    name: "Z Perm",
    category: "edges",
    tags: ["M层", "相邻"],
    recognition: "相邻棱块互换 (两组)。没有大灯，角块位置正确。",
    difficulty: 2,
    algorithm: "M' U M2 U M2 U M' U2 M2",
    // 使用 RU 版本的 Z-Perm 进行演示
    demoAlgorithm: "R' U' R U' R U R U' R' U R U R2 U' R'",
    setup: "R U R2 U' R' U' R U R' U' R' U R' U R",
  },

  // ================= 2. 仅角块交换 (Corners Only) =================
  {
    id: "pll-aa",
    name: "Aa Perm",
    category: "corners",
    tags: ["大灯左置", "顺时针"],
    recognition: "有一组大灯（左侧），其他三角顺时针轮换。棱块已归位。",
    difficulty: 2,
    algorithm: "x R' U R' D2 R U' R' D2 R2",
    // 去除 x 旋转，改写为从底面操作的逻辑 (或等价公式)
    // 这里使用标准 A-perm 的无旋转版本 (Headlights Back)
    demoAlgorithm: "R' F R' B2 R F' R' B2 R2",
    setup: "R2 B2 R F R' B2 R F' R",
  },
  {
    id: "pll-ab",
    name: "Ab Perm",
    category: "corners",
    tags: ["大灯右置", "逆时针"],
    recognition: "有一组大灯（右侧），其他三角逆时针轮换。棱块已归位。",
    difficulty: 2,
    algorithm: "x R2 D2 R U R' D2 R U' R",
    // Aa 的镜像
    demoAlgorithm: "R B' R F2 R' B R F2 R2",
    setup: "R2 F2 R' B' R F2 R' B R'",
  },
  {
    id: "pll-e",
    name: "E Perm",
    category: "corners",
    tags: ["无大灯", "难"],
    recognition: "没有大灯。对角角块互换。侧面颜色看起来像'X'。",
    difficulty: 3,
    algorithm: "x' R U' R' D R U R' D' R U R' D R U' R' D'",
    demoAlgorithm: "R F' R' B R F R' B' R F R' B R F' R' B'",
    setup: "B R F R' B' R F' R' B R F' R' B' R F R'",
  },

  // ================= 3. 相邻交换 (Adjacent Swap) =================
  {
    id: "pll-t",
    name: "T Perm",
    category: "adjacent",
    tags: ["最常用", "T字"],
    recognition:
      "左侧有大灯，大灯侧的棱块与大灯颜色相反（形成 T 字）。角块相邻互换。",
    difficulty: 2,
    algorithm: "R U R' U' R' F R2 U' R' U' R U R' F'",
    setup: "F R U' R' U R U R2 F' R U R U' R'",
  },
  {
    id: "pll-ja",
    name: "Ja Perm",
    category: "adjacent",
    tags: ["左侧条", "L型"],
    recognition: "左侧有一条已还原的块（Bar）。左侧有大灯。相邻角块互换。",
    difficulty: 2,
    algorithm: "R' U L' U2 R U' R' U2 R L",
    // 包含 L，引擎支持 L，直接用
    setup: "L' R' U2 R U R' U2 L U' R",
  },
  {
    id: "pll-jb",
    name: "Jb Perm",
    category: "adjacent",
    tags: ["右侧条", "最顺手"],
    recognition: "右侧有一条已还原的块（Bar）。右侧有大灯。Ja 的镜像。",
    difficulty: 2,
    algorithm: "R U R' F' R U R' U' R' F R2 U' R'",
    setup: "R U R2 F' R U R U' R' F R U' R'",
  },
  {
    id: "pll-ra",
    name: "Ra Perm",
    category: "adjacent",
    tags: ["左后条", "复杂"],
    recognition: "左后方有已还原块。左侧有大灯。仅交换相邻角块和特定棱块。",
    difficulty: 3,
    algorithm: "R U R' F' R U2 R' U2 R' F R U R U2 R'",
    setup: "R U2 R' U' R' F' R U2 R U2 R' F R U' R'",
  },
  {
    id: "pll-rb",
    name: "Rb Perm",
    category: "adjacent",
    tags: ["右后条", "复杂"],
    recognition: "右后方有已还原块。右侧有大灯。Ra 的镜像。",
    difficulty: 3,
    algorithm: "R' U2 R U2 R' F R U R' U' R' F' R2",
    setup: "R2 F R U R U' R' F' R U2 R' U2 R",
  },
  {
    id: "pll-f",
    name: "F Perm",
    category: "adjacent",
    tags: ["长公式", "T-setup"],
    recognition:
      "左侧有大灯。有一条 3x1 的还原块（看起来像 T Perm 但位置不同）。",
    difficulty: 3,
    algorithm: "R' U' F' R U R' U' R' F R2 U' R' U' R U R' U R",
    setup: "R' U' R U' R' U R U R2 F' R U R U' R' F U R",
  },
  {
    id: "pll-ga",
    name: "Ga Perm",
    category: "adjacent",
    tags: ["G类", "左前灯"],
    recognition: "左前侧有大灯。右后侧有 2x1 块。G 类通常比较难识别。",
    difficulty: 3,
    algorithm: "R2 U R' U R' U' R U' R2 D U' R' U R D'",
    // D 和 U' 组合，引擎支持 D，直接用
    setup: "D R' U' R U D' R2 U R' U R U' R U' R2",
  },
  {
    id: "pll-gb",
    name: "Gb Perm",
    category: "adjacent",
    tags: ["G类", "右前灯"],
    recognition: "右前侧有大灯。左后侧有 2x1 块。",
    difficulty: 3,
    algorithm: "R' U' R U D' R2 U R' U R U' R U' R2 D",
    setup: "D' R2 U R' U R' U' R U' R2 D U' R' U R",
  },
  {
    id: "pll-gc",
    name: "Gc Perm",
    category: "adjacent",
    tags: ["G类", "左后灯"],
    recognition: "左后侧有大灯。右前侧有 2x1 块。",
    difficulty: 3,
    algorithm: "R2 U' R U' R U R' U R2 D' U R U' R' D",
    setup: "D' R U R' U' D R2 U' R U' R' U R' U R2",
  },
  {
    id: "pll-gd",
    name: "Gd Perm",
    category: "adjacent",
    tags: ["G类", "右后灯"],
    recognition: "右后侧有大灯。左前侧有 2x1 块。",
    difficulty: 3,
    algorithm: "R U R' U' D R2 U' R U' R' U R' U R2 D'",
    setup: "D R2 U' R U' R U R' U R2 D' U R U' R'",
  },

  // ================= 4. 对角交换 (Diagonal Swap) =================
  {
    id: "pll-y",
    name: "Y Perm",
    category: "diagonal",
    tags: ["无大灯", "对角"],
    recognition: "没有大灯。对角角块互换。看起来像 V Perm 但棱块位置不同。",
    difficulty: 3,
    algorithm: "F R U' R' U' R U R' F' R U R' U' R' F R F'",
    setup: "F R' F' R U R U' R' F R U' R' U R U R' F'",
  },
  {
    id: "pll-v",
    name: "V Perm",
    category: "diagonal",
    tags: ["一组灯", "V型"],
    recognition: "只有一组大灯。对角角块互换。角块和棱块形成 V 字。",
    difficulty: 3,
    algorithm: "R' U R' U' y R' F' R2 U' R' U R' F R F",
    demoAlgorithm: "R' U R' U' B' R' B2 U' B' U B' R B R",
    setup: "R' B' R' B U' B U B2 R B U R U' R",
  },
  {
    id: "pll-na",
    name: "Na Perm",
    category: "diagonal",
    tags: ["无大灯", "Setup+J"],
    recognition: "没有大灯。所有块都错位。Setup 后接 Jb Perm。",
    difficulty: 3,
    algorithm: "R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R'",
    demoAlgorithm: "R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R'",
    setup: "R U R' U2 R U R2 F' R U R U' R' F R U' R' U' R U' R'",
  },
  {
    id: "pll-nb",
    name: "Nb Perm",
    category: "diagonal",
    tags: ["无大灯", "Setup+J"],
    recognition: "没有大灯。Na 的镜像。Setup 后接 Ja Perm。",
    difficulty: 3,
    algorithm: "R' U R U' R' F' U' F R U R' F R' F' R U' R",
    setup: "R' U R' F R F' R U' R' F' U F R U R' U' R",
  },
];

export const pllCategories = [
  { label: "所有", value: "all" },
  { label: "棱块交换", value: "edges" },
  { label: "角块交换", value: "corners" },
  { label: "相邻交换", value: "adjacent" },
  { label: "对角交换", value: "diagonal" },
];
