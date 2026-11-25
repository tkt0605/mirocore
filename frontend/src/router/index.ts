import { createRouter, createWebHistory } from 'vue-router';
import Index from '../views/Index.vue';
import Output from '../views/Output.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            name: 'index',
            component: Index
        },
        {
            path: "/output",
            name: 'output',
            component: Output
        }
    ]
})

export default router