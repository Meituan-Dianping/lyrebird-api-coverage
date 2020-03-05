<template>
  <Card id="info">
    <p dis-hover slot="title">Info</p>
    <li> business : {{business}} </li>
    <li> versionCode : {{versionCode}} </li>
    <li> versionName : {{versionName}} </li>
  </Card>
</template>

<script>
export default {
  created() {

  },
  computed: {
    business() {
      return this.$store.state.info.business
    },
    versionCode() {
      return this.$store.state.info.versionCode
    },
    versionName() {
      return this.$store.state.info.versionName
    },
  },

}
</script>

<style  scoped>
#info {
        width: 300px !important;
  height: 150px !important;
  margin: 30px 30px 0 30px;
    }
</style>
