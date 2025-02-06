import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Graph from './components/Graph.vue'
import HelloWorld from './components/HelloWorld.vue'
import './style.css'

const routes = [
  { path: '/', component: HelloWorld },
  { path: '/graph', component: Graph }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')