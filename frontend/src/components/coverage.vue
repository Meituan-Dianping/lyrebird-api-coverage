<template>
  <div id="coverage" class="box box-solid">
    <div class="box-body" style="height:auto; overflow:auto">
      <table  class="table table-hover">
        <thead>
          <!-- <tr v-for="item in data.headers"> -->
          <tr>
            <td v-for="item in headerShowedInList" :key="item"  >
              <b>{{item}}</b>
            </td>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td width="80"  style="vertical-align:middle;">Total</td>
            <td width="80" style="vertical-align:middle;">{{coveragedata.test_len + "/" + coveragedata.len}}</td>
            <!-- <td >
              <span :class="[setCoverageClass(coveragedata.total)]">{{coveragedata.total+ "%"}}</span>
            </td> -->
            <td width="160">
              <!-- <div class="progress progress-xs progress-striped active">
                <div
                  :class="[setProgressClass(coveragedata.total)]"
                  :style="{width:setProgressStyle(coveragedata.total)}"
                ></div>
              </div> -->
                <Progress :percent="coveragedata.total" status="active" :stroke-color="['#108ee9', '#87d068']" />
            </td>
          </tr>
          <tr v-for="item in coveragedata.priorities" :key="item.label">
            <td style="vertical-align:middle;">{{"P" + item.label}}</td>
            <td style="vertical-align:middle;">{{item.test_len + "/" + item.len}}</td>
            <!-- <td>
              <span :class="[setCoverageClass(item.value)]">{{item.value+ "%"}}</span>
            </td> -->
            <td>
              <!-- <div class="progress progress-xs progress-striped active">
                <div
                  :class="[setProgressClass(item.value)]"
                  :style="{width:setProgressStyle(item.value)}"
                ></div>
              </div> -->
             <Progress :percent="item.value" status="active" :stroke-color="['#108ee9', '#87d068']" />

            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      headerShowedInList: ["Priority", "Number", "Coverage"]
    }
  },
  computed: {
    coveragedata () {
        return this.$store.state.coverageData
    },
  },
  methods: {
    setCoverageClass: function(value) {
      if (value >= 90) {
        return "badge bg-green";
      } else if (value >= 60 && value < 90) {
        return "badge bg-light-blue";
      } else if (value >= 30 && value < 60) {
        return "badge bg-yellow";
      } else {
        return "badge bg-red";
      }
    },
    setProgressClass: function(data) {
      if (data >= 90) {
        return "progress-bar progress-bar-success";
      } else if (data >= 60 && data < 90) {
        return "progress-bar progress-bar-primary";
      } else if (data >= 30 && data < 60) {
        return "progress-bar progress-bar-warning";
      } else {
        return "progress-bar progress-bar-danger";
      }
    },
    setProgressStyle: function(data) {
      return data + "%";
    }
  }
}
</script>

<style  scoped>
#coverage {
  /* background-color: red; */
  width: 300px !important;
  height: 150px !important;
  margin: 30px 30px 0 30px;
}
</style>
