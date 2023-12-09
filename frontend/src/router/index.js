import { createRouter, createWebHistory } from 'vue-router'
import PingVue from '@/components/Ping.vue'

import SearchComponent from "@/components/SearchComponent.vue"

const routes = [
    {
        path: '/',
        name: 'Search',
        component: SearchComponent
      },
      {
        path: '/ping',
        name: 'ping',
        component: PingVue
      },

]


const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
  })
  
  
  export default router