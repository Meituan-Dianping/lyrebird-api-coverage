<template>
  <div id="coverage" class="box box-solid">
    <Card>
      <p dis-hover slot="title">Coverage</p>
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
}
</script>

<style scoped>
#coverage {
  width: 80%;
  height: 200px;
  margin: 30px 30px 0 30px;
}
</style>
