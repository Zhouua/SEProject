import { createRouter, createWebHashHistory } from 'vue-router';
import CourseTableS from '../components/CourseTableS.vue';
import CurriculumPlan from '../components/CurriculumPlan.vue';
import CourseSelectS from "../components/CourseSelectS.vue";
import CourseInfoS from "../components/CourseInfoS.vue";
import CourseResultS from "../components/CourseResultS.vue";

const routes = [
    {
        path: '/',
        redirect: 'CourseResultS'
    },
    {
        path: '/CurriculumPlan',
        name: 'CurriculumPlan',
        component: CurriculumPlan
    },
    {
        path: '/CourseTableS/:userId',
        name: 'CourseTableS',
        component: CourseTableS
    },
    {
        path: '/CourseSelectS',
        name: 'CourseSelectS',
        component: CourseSelectS
    },
    {
        path: '/CourseInfoS',
        name: 'CourseInfoS',
        component: CourseInfoS
    },
    {
        path: '/CourseResultS/:userId',
        name: 'CourseResultS',
        component: CourseResultS
    },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

export default router;