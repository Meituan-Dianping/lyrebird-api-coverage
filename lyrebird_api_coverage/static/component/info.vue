<template>
  <Card>
    <p dis-hover slot="title">Info</p>
    <li v-for="(value, key) in info" :key="key">{{ key }}: {{ value }}</li>
  </Card>
</template>

<script>
module.exports = {
  props: [],
  mounted: function() {
    this.loadBaseInfo();
  },
  data: function() {
    return {
      info: ""
    };
  },
  methods: {
    loadBaseInfo: function() {
      this.$http.get("/ui/plugin/api_coverage/baseInfo").then(function(data) {
        console.log(data.data);
        this.info = data.data;
      });
    }
  }
};
</script>

<style>
</style>
