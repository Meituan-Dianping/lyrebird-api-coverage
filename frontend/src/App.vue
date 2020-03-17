<template>
    <div id='app'>
        <button-bar @newbase="loadBasicDatas" @poptarget="findTargetContext" ></button-bar>
        <Divider style="margin:0" />
        <Row>
          <i-col span="6">
            <coverage-stats />
            <base-info />
          </i-col>
          <i-col span="18" >
            <base-list />
          </i-col>
        </Row>
    </div>
</template>

<script>
import ButtonBar from './components/ButtonBar'
import CoverageStats from './components/CoverageStats'
import BaseInfo from './components/BaseInfo'
import BaseList from './components/BaseList'

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
    ButtonBar,
    CoverageStats,
    BaseInfo,
    BaseList,
  },
}
</script>

<style scoped>
#app {
  min-width: 1500px;
}
</style>
