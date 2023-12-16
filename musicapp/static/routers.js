// import {createRouter, createWebHistory} from 'vue-router';

import Index from './components/index.js' 
import Login from './components/login.js'
import Register from './components/register.js'
import Home from './components/home.js'

const routes = [
        {
            path: '/',
            component: Index,
            name: "Index"
        },
        {
            path: '/login',
            component: Login,
            name: "Login"
        },
        {
            path: '/register',
            component: Register,
            name: "Register"
        },
        {
            path: '/home',
            component: Home,
            name: "Home"
        }

    ];



const router = new VueRouter({
    // history: createWebHistory(),
    routes
});


export default router;