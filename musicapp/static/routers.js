import {createRouter, createWebHistory} from 'vue-router';

import Index from './components/index.js' 
import Login from './components/login.js'
import Register from './components/register.js'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: Index
        },
        {
            path: '/login',
            component: Login
        },
        {
            path: '/register',
            component: Register
        }

    ]
});


export default router;