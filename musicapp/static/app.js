//import { createApp } from 'vue'; 

import router from './routers.js';
import Navbar from './components/navbar.js';

// const app = createApp({
   
//     template: `<div>
//     <Navbar></Navbar>
//     <router-view> </router-view>
//     </div>`

// })

// app.use(router);

// app.mount('#app');

const app = new Vue({
    el: "#app",
    template: `
    <div>
    <Navbar></Navbar>
    <router-view> </router-view>
    </div>`,
    router,
    data: {
        message: "Hello World !!"
    },
    methods: {

    }
});

