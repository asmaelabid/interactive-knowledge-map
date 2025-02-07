import './style.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Graph from './components/Graph.vue'
import { ToastPlugin } from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-bootstrap.css';

const routes = [
  { path: '/', component: Graph }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(ToastPlugin);
app.mount('#app')