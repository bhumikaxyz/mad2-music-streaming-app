
import router from './routers.js';
import Navbar from './components/navbar.js';

// Navigation gaurd
// PROBLEM HERE!!! isAuthenticated not getting updated 
// const isAuthenticated = localStorage.getItem('auth-token') ? true : false

// router.beforeEach((to, from, next) => {
//     if (to.name !== 'Login' && !isAuthenticated) next({ name: 'Login' })
//     else next()
//   })



const app = new Vue({
    el: "#app",
    template: `
        <div>
        <Navbar></Navbar>
        <router-view></router-view>
        </div>`,
    router
});

