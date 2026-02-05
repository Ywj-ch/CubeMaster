// src/data/courses.js
import { lblSteps } from "./lblData.js";
import { basicsSteps } from "./basicsData.js";
import { ollPllSteps } from "./ollPllData.js";

export const courseList = [
  {
    id: "basics",
    title: "入门：魔方基础知识",
    description: "认识魔方结构、及旋转符号定义。",
    steps: basicsSteps,
  },
  {
    id: "lbl",
    title: "基础：层先法 (LBL)",
    description: "适合零基础新手的入门教程",
    steps: lblSteps,
  },
  {
    id: "advanced",
    title: "进阶：2-Look OLL/PLL",
    description: "从入门到熟练的必经之路，仅需16个公式即可快速缩短还原时间。",
    steps: ollPllSteps,
  },
  {
    id: "cfop",
    title: "突破：CFOP 速拧",
    description: "迈向高手的必经之路",
  },
];
