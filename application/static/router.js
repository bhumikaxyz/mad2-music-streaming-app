// import {createRouter, createWebHistory} from 'vue-router';

import LandingPage from './components/landing_page.js' 
import NewLogin from './components/NewLogin.js'
import NewRegister from './components/NewRegister.js'
import NewHome from './components/NewHome.js'
import UploadSong from './components/UploadSong.js'


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
            path: '/userhome',
            component: NewHome,
            name: "NewHome"
        },
        {
            path: '/uploadsong',
            component: UploadSong,
            name: "Upload Song"
        }


    ];



const router = new VueRouter({
    // history: createWebHistory(),
    routes
});


export default router;