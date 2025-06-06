import { createRouter, createWebHistory } from 'vue-router';
import CourseResultT from "../components/CourseResultT.vue";

const routes = [
    {
        path: '/',
        redirect: '/5/CourseResultT'
    },
    {
        path: '/:userId/CourseResultT',
        name: 'CourseResultT',
        component: CourseResultT
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
