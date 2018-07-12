Vue.config.devtools = true;

iview.lang('en-US');

new Vue({
    el: '#app',
    data: {
    },
    components: {
      'apicoverage': httpVueLoader('/ui/plugin/api_coverage/static/component/main.vue')
    }
})