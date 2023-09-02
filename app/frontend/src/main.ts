import 'core-js/stable';
import 'regenerator-runtime/runtime';
// Import Component hooks before component definitions
import './component-hooks';
import Vue from 'vue';
import './plugins/vee-validate';
import App from './App.vue';
import vuetify from '@/plugins/vuetify';
import router from './router';
import store from '@/store';
import './registerServiceWorker';
import 'vuetify/dist/vuetify.min.css';


Vue.config.productionTip = false;

new Vue({
  vuetify,
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
