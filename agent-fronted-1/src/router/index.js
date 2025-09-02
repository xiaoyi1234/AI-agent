import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import LoveAppChat from '../views/LoveAppChat.vue'
import ManusChat from '../views/ManusChat.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/love-app-chat',
    name: 'LoveAppChat',
    component: LoveAppChat
  },
  {
    path: '/manus-chat',
    name: 'ManusChat',
    component: ManusChat
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
