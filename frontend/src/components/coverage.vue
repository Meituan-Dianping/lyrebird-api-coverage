<template>
  <div id="coverage" class="box box-solid">
    <Card>
      <table>
        <thead>
          <tr>
            <td v-for="item in headerShowedInList" :key="item">
              <b>{{ item }}</b>
            </td>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td width="80" style="vertical-align:middle;">Total</td>
            <td width="80" style="vertical-align:middle;">
              {{ coverageData.test_len + "/" + coverageData.len }}
            </td>
            <td width="160">
              <Progress
                :percent="coverageData.total"
                status="active"
                :stroke-color="['#108ee9', '#87d068']"
              />
            </td>
          </tr>
          <tr v-for="item in coverageData.priorities" :key="item.label">
            <td style="vertical-align:middle;">{{ "P" + item.label }}</td>
            <td style="vertical-align:middle;">
              {{ item.test_len + "/" + item.len }}
            </td>
            <Progress
              :percent="item.value"
              status="active"
              :stroke-color="['#108ee9', '#87d068']"
            />
          </tr>
        </tbody>
      </table>
    </Card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      headerShowedInList: ['Priority', 'Number', 'Coverage'],
    }
  },
  computed: {
    coverageData() {
      return this.$store.state.coverageData
    },
  },
  methods: {
    setCoverageClass(value) {
      if (value >= 90) {
        return 'badge bg-green'
      } if (value >= 60 && value < 90) {
        return 'badge bg-light-blue'
      } if (value >= 30 && value < 60) {
        return 'badge bg-yellow'
      }
      return 'badge bg-red'
    },
    setProgressClass(data) {
      if (data >= 90) {
        return 'progress-bar progress-bar-success'
      } if (data >= 60 && data < 90) {
        return 'progress-bar progress-bar-primary'
      } if (data >= 30 && data < 60) {
        return 'progress-bar progress-bar-warning'
      }
      return 'progress-bar progress-bar-danger'
    },
    setProgressStyle(data) {
      return `${data}%`
    },
  },
}
</script>

<style scoped>
#coverage {
  width: 300px;
  height: 150px;
  margin: 30px 30px 0 30px;
}
</style>
