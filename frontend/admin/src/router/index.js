import { createRouter, createWebHashHistory } from 'vue-router';
import SelectionTime from '../components/SelectionTime.vue';
import HelpSelect from '../components/HelpSelect.vue';

const routes = [
    {
        path: '/',
        redirect: 'SelectionTime'
    },
    {
        path: '/SelectionTime',
        name: 'SelectionTime',
        component: SelectionTime
    },
    {
        path: '/HelpSelect',
        name: 'HelpSelect',
        component: HelpSelect
    }
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

export default router;