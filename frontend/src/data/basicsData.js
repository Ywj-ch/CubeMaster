// src/data/basicsData.js

export const basicsSteps = [
  {
    id: "step-1",
    title: "第一章：核心概念",
    description: "在开始拧动魔方之前，理解它的物理结构至关重要。",
    cases: [
      {
        id: "concept-1",
        type: "graphic", // 标记为图文模式
        title: "中心块是固定的",
        image: "/images/basics/core-concept-center-pieces.png",
        description: "",
        points: [
          "六个中心块（白色、黄色、红色、橙色、蓝色、绿色）永远不会改变相对位置。",
          "它们定义了该面最终应该是什么颜色（例如：白色中心块所在的面最终就是白色面）。",
          "在整个解法过程中，我们将把它们作为坐标参考点。",
        ],
      },
      {
        id: "concept-2",
        type: "graphic",
        title: "逐层解决，而不是逐面",
        image: "/images/basics/core-concept-layer-by-layer.png",
        points: [
          "常见错误：试图一次拼好一个颜色的面（如拼完红色面再去拼蓝色面）。",
          "正确方法：像盖楼一样，一层一层地完成（底座 -> 中间层 -> 顶层）。",
          "每一层的还原都必须建立在前一层不被破坏的基础上。",
        ],
      },
      {
        id: "concept-3",
        type: "graphic",
        title: "三种块类型",
        image: "/images/basics/core-concept-piece-types.png",
        points: [
          "中心块 (Center)：6 个，每个 1 种颜色，位置固定不动。",
          "棱块 (Edge)：12 个，每个 2 种颜色，位于两个中心块之间。",
          "角块 (Corner)：8 个，每个 3 种颜色，位于角落。",
        ],
      },
    ],
  },
  {
    id: "step-2",
    title: "第二章：阅读魔方记法",
    description: "这是魔方的‘乐谱’。学会它，你就能读懂世界上所有的魔方公式。",
    cases: [
      {
        id: "notation-1",
        type: "notation-grid", // 标记为特殊的符号网格模式
        title: "基础字母含义",
        description: "每个字母代表旋转一个层。想象你就面对着那个面。",
        image: "/images/basics/notation-guide-full-diagram.png", // 参考图里那个立体的图
        notationItems: [
          { key: "F", name: "Front", desc: "前面 (面向你的面)" },
          { key: "B", name: "Back", desc: "后面 (背向你的面)" },
          { key: "U", name: "Up", desc: "顶面 (上面的面)" },
          { key: "D", name: "Down", desc: "底面 (下面的面)" },
          { key: "L", name: "Left", desc: "左面 (左手的面)" },
          { key: "R", name: "Right", desc: "右面 (右手的面)" },
        ],
      },
      {
        id: "notation-2",
        type: "notation-grid",
        title: "旋转方向符号",
        description: "字母后面跟着的小尾巴决定了转动的方向和幅度。",
        notationItems: [
          { key: "R", name: "顺时针", desc: "顺时针转动 90° (Clockwise)" },
          {
            key: "R'",
            name: "逆时针",
            desc: "逆时针转动 90° (Counter-clockwise)",
          },
          { key: "R2", name: "180度", desc: "转动 180° (半圈，方向无所谓)" },
        ],
      },
    ],
  },
];
