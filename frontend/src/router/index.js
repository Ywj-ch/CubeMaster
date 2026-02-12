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
      },
      {
        path: "cube",
        name: "CubeFree",
        component: () => import("../views/CubeFree.vue"),
      },
      {
        path: "solver",
        name: "Solver",
        component: () => import("../views/Solver.vue"),
      },
      {
        path: "cfop",
        name: "CfopIntro",
        component: () => import("../views/CfopIntro.vue"),
      },
      {
        path: "cfop/lib/:step",
        name: "CfopLibrary",
        component: () => import("../views/CfopAlgorithmLibrary.vue"),
      },
      {
        path: "learning",
        redirect: "/learning/basics",
      },
      {
        path: "learning/:courseId",
        name: "Learning",
        component: () => import("../views/Learning.vue"),
        beforeEnter: (to, from, next) => {
          console.log("检查路由参数:", to.params.courseId);
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
