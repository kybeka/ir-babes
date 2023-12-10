import { createRouter, createWebHistory } from 'vue-router'

import SearchComponent from "@/components/SearchComponent.vue"

const routes = [
    {
        path: '/search',
        name: 'Search',
        component: SearchComponent
      },
]


const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
  })
  
  
  export default router