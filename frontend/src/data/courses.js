// src/data/courses.js
import { lblSteps } from "./lblData.js";

export const courseList = [
  {
    id: "basics",
    title: "入门：魔方基础知识",
    description: "认识魔方结构、及旋转符号定义。",
    steps: [], // 待开发：后续我们将在这里添加“结构篇”和“符号篇”
  },
  {
    id: "lbl",
    title: "基础：层先法 (LBL)",
    description: "适合零基础新手的入门教程",
    steps: lblSteps,
  },
  {
    id: "cfop",
    title: "进阶：CFOP 速拧 (开发中)",
    description: "迈向高手的必经之路",
    steps: [], // 暂时为空，未来填入 CFOP 数据
  },
];
