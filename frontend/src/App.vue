<template>
    <div id='app'>
        <banner @newbase="loadDetailData" @poptarget="findTargetContext" ></banner>
        <Divider style="margin:0" />
        <Row>
          <i-col span="6">
            <coverage />
            <info />
          </i-col>
          <i-col span="18" >
            <api-list ></api-list>
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
    this.loadDetailData()
    const { loadDetailData } = this
    this.$io.on('apiCoverageBaseData', this.loadDetailData)
    this.$io.on('apiCoverageCoverData', this.loadCoverageData)
  },


  methods: {
    loadDetailData() {
      this.$store.dispatch('loadDetailData')
      this.$store.dispatch('loadBaseInfo')
      this.$store.dispatch('loadCoverageData')
    },
    loadCoverageData() {
      this.$store.dispatch('loadCoverageData')
    },
    // 搜索框
    findTargetContext(targetContext) {
      this.$store.dispatch('setTargetContext', targetContext)
      console.log(this.$store.state.targetContext)

      var ShowedAPIData = []
      console.log(ShowedAPIData)
      const { detailData } = this.$store.state
      console.log(detailData)
      var { targetContext } = this.$store.state
      if (targetContext) {
        var ShowedAPIData = []
        for (const item of detailData) {
          if (JSON.stringify(item, null).search(targetContext) != -1) {
            ShowedAPIData.push(item)
          }
        }
      } else {
        ShowedAPIData = detailData
      }
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
  min-width: 1500px;
}

</style>
