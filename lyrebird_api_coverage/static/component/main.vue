<template>
    <div>
        <banner @newbase="loadDetailData" @newcoverage="loadCoverageData" @poptarget="findTargetContext"></banner>
        <div class="row">
            <div class="col-md-3">
                <coverage :coveragedata ="coverageData" @newcoverage="loadCoverageData"></coverage>
                <info></info>
            </div>
            <div class="col-md-9">
                <api-list :detaildata ="showedAPIData"  @newbase="loadDetailData"></api-list>
            </div>
        </div>
    </div>
</template>

<script>
//websocket namespace /api_coverage
let apicoverageIO = io("/api_coverage");
let timer = null;

module.exports = {
  mounted: function() {
    this.loadCoverageData();
    this.loadDetailData();
    loadCoverageData = this.loadCoverageData;
    loadDetailData = this.loadDetailData;
    apicoverageIO.on("coverage message", function(msg) {
      loadCoverageData();
    });
    apicoverageIO.on("test_data message", function(msg) {
      console.log(msg);
      loadDetailData();
      if (!timer) {
        timer = setTimeout(() => {
          loadDetailData();
          clearTimeout(timer);
          timer = null;
        }, 1000);
      }
    });
  },
  data: function() {
    return {
      coverageData: {},
      detailData: [], //总体的数据
      showedAPIData: [], //搜索出的数据
      targetContext: null
    };
  },
  updated: function() {
    console.log("init");
  },
  methods: {
    loadCoverageData: function() {
      this.$http.get("/ui/plugin/api_coverage/getCoverage").then(
        response => {
          this.coverageData = response.data;
        },
        error => {
          console.log("load coverage data failed!", error);
        }
      );
    },
    loadDetailData: function() {
      this.$http.get("/ui/plugin/api_coverage/getTest").then(
        response => {
          this.detailData = response.data.test_data;
          // 总的数据赋值给show，搜索用的数据
          this.showedAPIData = this.detailData;
        },
        error => {
          console.log("load detail data failed!", error);
        }
      );
    },
    //搜索框
    findTargetContext: function(targetContext) {
      this.targetContext = targetContext;
      if (targetContext) {
        this.showedAPIData = [];
        for (const item of this.detailData) {
          if (JSON.stringify(item, null).search(this.targetContext) != -1) {
            this.showedAPIData.push(item);
          }
        }
      } else {
        this.showedAPIData = this.detailData;
      }
    }
  },
  components: {
    coverage: httpVueLoader("/ui/plugin/api_coverage/static/component/coverage.vue"),
    "api-list": httpVueLoader(
      "/ui/plugin/api_coverage/static/component/api-list.vue"
    ),
    banner: httpVueLoader("/ui/plugin/api_coverage/static/component/banner.vue"),
    info: httpVueLoader("/ui/plugin/api_coverage/static/component/info.vue")
  }
};
</script>

<style>
</style>
