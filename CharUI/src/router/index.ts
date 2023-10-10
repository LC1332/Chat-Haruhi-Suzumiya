import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: async () => await import("../views/FrameView.vue"),
      children: [
        {
          path: "",
          component: async () => await import("../views/HomeView.vue"),
        },
        {
          path: "chat",
          component: async () => await import("../views/ChatView.vue"),
        },
        {
          path: "about",
          component: async () => await import("../views/AboutView.vue"),
        },
      ],
    },
  ],
});

export default router;
