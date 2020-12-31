<template>
    <div id='app'>
        <banner @newbase="loadBasicDatas" @poptarget="findTargetContext" ></banner>
        <Divider style="margin:0" />
        <Row>
          <i-col span="6">
            <coverage />
            <info />
          </i-col>
          <i-col span="18" >
            <api-list />
          </i-col>
        </Row>
    </div>
</template>

<script>
import banner from './components/banner.vue'
import coverage from './components/coverage.vue'
import info from './components/info.vue'
import apiList from './components/apiList.vue'

export default {
  name: 'app',
  created() {
    // Get basic data when refresh page
    this.loadBasicDatas()
    // Get basic data when new proxy or mock by socketio
    this.$io.on('apiCoverageBaseData', this.loadBasicDatas)
  },
  methods: {
    // Load basic datas : coveragedData、 baseInfo、 coverageDetail、
    loadBasicDatas() {
      this.$store.dispatch('loadDetailData')
      this.$store.dispatch('loadBaseInfo')
      this.$store.dispatch('loadCoverageData')
    },
    // search input
    findTargetContext(targetContext) {
      // Create a list to save the display result data after the search
      let ShowedAPIData = []
      // get user imported base  (full data)
      const { detailData } = this.$store.state
      if (targetContext) {
        for (const item of detailData) {
          if (JSON.stringify(item, null).search(targetContext) !== -1) {
            ShowedAPIData.push(item)
          }
        }
      } else {
        ShowedAPIData = detailData
      }
      // Assemble the ShowedAPIData for page display
      this.$store.dispatch('setShowedAPIData', ShowedAPIData)
    },
  },
  components: {
    banner,
    coverage,
    info,
    apiList,
  },
}
</script>

<style scoped>
#app {
  min-width: 1390px;
}
</style>
