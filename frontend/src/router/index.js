import { createRouter, createWebHistory } from "vue-router";
import MainLayout from "../layout/MainLayout.vue";

const routes = [
  {
    path: "/",
    component: MainLayout,
    children: [
      {
        path: "",
        name: "Home",
        component: () => import("../views/Home.vue"),
        meta: { title: "首页" },
      },
      {
        path: "cube",
        name: "CubeFree",
        component: () => import("../views/CubeFree.vue"),
        meta: { title: "自由练习" },
      },
      {
        path: "solver",
        name: "Solver",
        component: () => import("../views/Solver.vue"),
        meta: { title: "求解器" },
      },
      {
        path: "cfop",
        name: "CfopIntro",
        component: () => import("../views/CfopIntro.vue"),
        meta: { title: "CFOP 简介" },
      },
      {
        path: "cfop/lib/:step",
        name: "CfopLibrary",
        component: () => import("../views/CfopAlgorithmLibrary.vue"),
        meta: { title: "CFOP 算法库" },
      },
      {
        path: "learning",
        redirect: "/learning/basics",
      },
      {
        path: "learning/:courseId",
        name: "Learning",
        component: () => import("../views/Learning.vue"),
        meta: { title: "学习中心" },
        beforeEnter: (to, from, next) => {
          const validIds = ["basics", "lbl", "advanced"];
          if (validIds.includes(to.params.courseId)) {
            next();
          } else {
            next("/learning/basics");
          }
        },
      },
      {
        path: "about",
        name: "About",
        component: () => import("../views/About.vue"),
        meta: { title: "关于" },
      },
      {
        path: "tech/yolo",
        name: "TechYolo",
        component: () => import("../views/TechYolo.vue"),
        meta: { title: "YOLO 技术" },
      },
      {
        path: "tech/kociemba",
        name: "TechKociemba",
        component: () => import("../views/TechKociemba.vue"),
        meta: { title: "Kociemba 算法" },
      },
      {
        path: "tech/threejs",
        name: "TechThreejs",
        component: () => import("../views/TechThreejs.vue"),
        meta: { title: "Three.js 渲染" },
      },
      {
        path: "tech/architecture",
        name: "TechArchitecture",
        component: () => import("../views/TechArchitecture.vue"),
        meta: { title: "系统架构" },
      },
      {
        path: "customizer",
        name: "Customizer",
        component: () => import("../views/Customizer.vue"),
        meta: { title: "外观定制" },
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 如果有历史位置（点后退键），恢复位置
    if (savedPosition) {
      return savedPosition;
    }
    // 否则默认跳转回顶部
    return { top: 0 };
  },
});

export default router;
