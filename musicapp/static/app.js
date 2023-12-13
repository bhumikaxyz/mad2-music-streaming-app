import { createApp } from 'vue'; 

import router from './routers.js';

new Vue({
    el: '#app',
    template: `<div>Hello from vue app.
    <router-view/>
    </div>`,
    router
})

// app.use(router)

// app.mount('#app')