// import {createRouter, createWebHistory} from 'vue-router';

import LandingPage from './components/landing_page.js' 
// import Login from './components/login.js'
import Register from './components/register.js'
import Home from './components/home.js'
// import login_iitm from './components/login_iitm.js'
import NewLogin from './components/NewLogin.js'
import NewRegister from './components/NewRegister.js'
// import Logout from './components/Logout.js'

const routes = [
        {
            path: '/',
            component: LandingPage,
            name: "Landing Page"
        },
        {
            path: '/login',
            component: NewLogin,
            name: "NewLogin"
        },
        {
            path: '/register',
            component: NewRegister,
            name: "NewRegister"
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