import { createRouter, createWebHistory } from "vue-router";
import SignUp from "../components/SignUp.vue";
import Login from "../components/Login.vue";
import NotFound from "../components/NotFound.vue";
import Tasks from "../components/Tasks.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Login,
  },
  {
    path: "/tasks",
    name: "Tasks",
    component: Tasks,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/signup",
    name: "SignUp",
    component: SignUp,
  },
  { path: "/:pathMatch(.*)", component: NotFound },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
