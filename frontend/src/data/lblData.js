// src/data/lblData.js
export const lblSteps = [
  {
    id: "step-1",
    title: "第一步：底层黄色十字",
    shortDesc: "打好地基",
    description: "选择黄色作为底层（D面），构建黄色十字，并确保每个黄色棱块的侧面颜色与中心块对齐。这是后续所有步骤的基础。",
    cases: [
      {
        id: "case-1-1",
        title: "黄色棱块在顶层",
        description: "黄色棱块位于顶层（U面），且其侧面颜色已对准对应中心块。",
        setup: "F' F'",
        algorithm: "F2",
        tips: "若棱块在顶层且已对齐，只需将其所在面旋转180度到底层即可。"
      },
      {
        id: "case-1-2",
        title: "黄色棱块在中层",
        description: "黄色棱块在中层，此时需要观察底层情况。",
        setup: "R D R",
        algorithm: "D' R D",
        tips: "转动中层将棱块送到底层时，注意不要打乱已归位的白色十字。若棱块方向错误，可先将其转至顶层再接case1。"
      },
      {
        id: "case-1-3",
        title: "白色棱块在底层但错位",
        description: "白色棱块已在底层，但侧面颜色未与中心块对齐。",
        setup: "R D R D' R'",
        algorithm: "R2 U F2", // 调整错位棱块
        tips: "先将该棱块移出底层，调整顶层方向使其侧面颜色对准中心，再将其放回底层正确位置。"
      }
    ]
  },
  {
    id: "step-2",
    title: "第二步：完成第一层（底层角块）",
    shortDesc: "填平第一层",
    description: "将四个带有黄色的角块放入底层的四个角位。完成后，底层完全为黄色，且每个角块的侧面颜色与中心块颜色一致。",
    cases: [
      {
        id: "case-2-1",
        title: "角块在顶层，黄色朝前",
        description: "黄色角块位于顶层，且黄色面朝前，并且左侧面或者是右边侧面与该侧面中心颜色相同，",
        setup: "U' F2 U2 F2 R2 D R2 U R2 U B R B' R' D2 F2 D R U R'",
        algorithm: "U R U' R'",
        tips: "对于在左侧的情况也是类似的，把操作对称一下就行了。"
      },
      {
        id: "case-2-2",
        title: "角块在顶层，黄色朝侧面",
        description: "黄色角块位于顶层，但黄色面朝左侧或右侧。",
        setup: "R2 F' R2 U2 R2 F2 R2 U2 R' F2 U2 F U' R U",
        algorithm: "U' U' R' U R",
        tips: "转动顶层使得黄色角块的相邻侧面与中心色对其，然后再接case1"
      },
      {
        id: "case-2-3",
        title: "角块在底层但错位",
        description: "白色角块已在底层，但位置错误或朝向错误。",
        setup: "B D2 F R2 B2 U2 R2 U2 F' U2 R F' D2 F' L B2 U' L U' B'",
        algorithm: "R U R' U'",
        tips: "先通过公式将错位角块移到顶层，再按情况一或二处理。"
      }
    ]
  },
  {
    id: "step-3",
    title: "第三步：还原第二层（中层棱块）",
    shortDesc: "加固第二层",
    description: "还原中间层的四个棱块（这些棱块不带白色）。从顶层寻找不含白色的棱块，将其插入中层的正确位置。",
    cases: [
      {
        id: "case-3-1",
        title: "往右侧入位",
        description: "棱块在顶层，其侧面颜色与前面中心块对齐，目标空位在右侧。",
        setup: "L2 D R2 U' F2 D B2 D' R2 U' F' U' F' R' D U' B R2 D2 F2",
        algorithm: "U R U' R' U' F' U F",
        tips: "口诀：‘远切回回，接孩子放学’。先将棱块远离目标位置，再做公式。"
      },
      {
        id: "case-3-2",
        title: "往左侧入位",
        description: "棱块在顶层，其侧面颜色与前面中心块对齐，目标空位在左侧。",
        setup: "U2 B2 D' R2 D' R2 D2 B2 L' D U2 R' D2 L2 B' L D L' F'",
        algorithm: "U' L' U L U F U' F'",
        tips: "镜像公式：往左远离，左手操作。"
      },
      {
        id: "case-3-3",
        title: "棱块在中层但错位",
        description: "棱块已在中层，但位置错误或朝向错误。",
        setup: "D2 U2 F2 R2 U2 R2 F2 L2 B F' U' B' D R F2 U R2 D L2",
        algorithm: "U R U' R' U' F' U F U' U' U R U' R' U' F' U F",
        tips: "右侧错位就用case1，左侧错位用case2， 转出来之后再看情况接case1或case2处理。"
      }
    ]
  },
  {
    id: "step-4",
    title: "第四步：顶层白色十字",
    shortDesc: "顶层十字",
    description: "在顶层（白色面）形成一个白色十字，不考虑角块的颜色。通过一个公式处理两种情况（拐角、直线）。",
    cases: [
      {
        id: "case-4-1",
        title: "小拐角（两个相邻棱块白色朝上）",
        description: "顶层有两个相邻的白色棱块朝上，形成L形。",
        setup: "F R U R' U' F'",
        algorithm: "F R U R' U' F'",
        tips: "这里只用记住这一个公式，做一次公式即可形成一字。"
      },
      {
        id: "case-4-2",
        title: "直线（两个相对棱块白色朝上）",
        description: "顶层有两个相对的白色棱块朝上，形成一条直线。让直线水平。",
        setup: "F R U R' U' F' F R U R' U' F'",
        algorithm: "F R U R' U' F'",
        tips: "直线横放，做一次公式即可完成十字（如果发现还没出现十字就多做几次）。"
      }
    ]
  },
  {
    id: "step-5",
    title: "第五步：顶层全白",
    description: "使用小鱼公式调整顶层角块方向，使整个顶面变为白色。此时角块位置可能还不正确。",
    cases: [
      {
        id: "case-5-1",
        title: "右手小鱼（鱼头在左下，缺白色在右）",
        description: "顶层像一条小鱼，鱼头朝左下方，缺少白色的角块在鱼头右侧。",
        setup: "B2 D F2 R2 B2 U2 L2 U' L2 U' F' U B' R2 U B U F' U2 R U R' U R U2 R' U",
        algorithm: "R U R' U R U2 R'",
        tips: "公式后可能得到另一条小鱼或直接全白。记住这个最顺手的公式。"
      },
      {
        id: "case-5-2",
        title: "左手小鱼（鱼头在右下，缺白色在左）",
        description: "镜像情况：鱼头朝右下方，缺少白色的角块在鱼头左侧。",
        setup: "U' F2 D' L2 D L2 U' L2 U L2 F' U F' U F U2 F'",
        algorithm: "L' U' L U' L' U2 L",
        tips: "左手公式，与右手小鱼对称。"
      },
      {
        id: "case-5-3",
        title: "双鱼头或十字",
        description: "其他情况（如十字、双鱼头等），可通过转换为小鱼处理。",
        setup: "B2 D F2 R2 B2 U2 L2 U' L2 U' F' U B' R2 U B U F' U2",
        algorithm: "R U R' U R U2 R'",
        tips: "先按‘二后四左’摆好方向，做一次右手小鱼，通常会变成标准小鱼，再做对应小鱼公式即可。"
      }
    ]
  },
  {
    id: "step-6",
    title: "第六步：顶层角块归位",
    description: "调整顶层四个角块的位置（不翻转朝向），使每个角块的三种颜色与对应的三个中心块颜色匹配。",
    cases: [
      {
        id: "case-6-1",
        title: "有‘眼睛’（两角同色）",
        description: "已经找到一对颜色相同的角块，将其放在右侧。",
        setup: "B R2 F' L2 B2 L2 U2 B L2 F' D' F2 D' F2 L2 U' F2",
        algorithm: "R R D R' R' D' F F R' R' U' R R U F' F'",
        tips: "这个公式较长，但非常有用。做一次后，四个角块位置应全部正确（这里运气较好直接还原了）。建议做这个公式的时候将魔方的右侧朝上这样会顺手一些。"
      },
      {
        id: "case-6-2",
        title: "无‘眼睛’（四角均不同色）",
        description: "四个角块颜色均不相同，没有形成‘眼睛’。",
        setup: "R U R' U' R' F R2 U' R' U' R U R' F' R R D R' R' D' F F R' R' U' R R U F' F'",
        algorithm: "R R D R' R' D' F F R' R' U' R R U F' F'",
        tips: "此时再做一次case1，就会出现‘眼睛’（这里蓝色面出现了‘眼睛’），然后我们将蓝色面其放在右侧再做一次公式即可。"
      }
    ]
  },
  {
    id: "step-7",
    title: "第七步：顶层棱块归位（完成还原）",
    shortDesc: "调整棱块，大功告成！",
    description: "最后一步！调整顶层四个棱块的位置，完成整个魔方的还原。将已经完成的一面放在后面（B面）。",
    cases: [
      {
        id: "case-7-1",
        title: "顺时针三棱换",
        description: "有三个棱块需要顺时针方向轮换。将已完成的一面朝后。",
        setup: "R U' R U R U R U' R' U' R2",
        algorithm: "R U R' U R U U R' F' U' F U' F' U' U' F",
        tips: "先做右手小鱼公式然后将魔方顺时针转动90°后再做一次左手小鱼公式。"
      },
      {
        id: "case-7-2",
        title: "逆时针三棱换",
        description: "有三个棱块需要逆时针方向轮换。将已完成的一面朝后。",
        setup: "R2 U R U R' U' R' U' R' U R'",
        algorithm: "L' U' L U' L' U' U' L F U F' U F U U F'",
        tips: "先做左手小鱼公式然后将魔方逆时针转动90°后再做一次右手小鱼公式。"
      },
      {
        id: "case-7-3",
        title: "棱块对换",
        description: "四个棱块两两相对",
        setup: "L2 B2 F2 R2 D L2 B2 F2 R2 U'",
        algorithm: "R U R' U R U U R' F' U' F U' F' U' U' F",
        tips: "任意选择上面的两个公式之一执行一次，然后就会转化为上述两种情况之一。"
      }
    ]
  }
];