import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import Ping from '../components/Ping.vue';
import HDB from '../components/HDB.vue';
/*eslint linebreak-style: ["error", "windows"]*/
Vue.use(VueRouter);

const routes = [
/*  
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
*/
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
  },
  {
      path: '/ping',
      name: 'Ping',
      component: Ping,
  },
  {
      path: '/',
      name: 'HDB',
      component: HDB,
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
