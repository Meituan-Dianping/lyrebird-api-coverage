import Vue from 'vue'
import ViewUI from 'view-design'
import io from "socket.io-client"
import App from './App.vue'
import store from './store'
import 'view-design/dist/styles/iview.css'

Vue.config.productionTip = false
Vue.use(ViewUI)
Vue.prototype.$io = io()
new Vue({
  store,
  render: (h) => h(App),
}).$mount('#app')
