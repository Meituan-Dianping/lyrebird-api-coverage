<template>
  <div id="tab" class="box box-solid">
    <div class="box-body" style="height:80vh; overflow:auto">
      <i-table height="1000" stripe :columns="columns" :data="showedAPIData" ></i-table>
      <Modal
        v-model="isApiDetailModalShow"
        title="Custom width"
        width="1300">
        <FlowDetail></FlowDetail>
    </Modal>
    </div>
  </div>
</template>


<script>
import FlowDetail from '@/components/flowDetail.vue'

export default {
  components: {
    FlowDetail,
  },

  computed: {
    showedAPIData() {
      return this.$store.state.showedAPIData
    },
  },
  methods: {
    viewDetail(id) {
      this.isApiDetailModalShow = true
      console.log(id)
      this.$store.dispatch('loadFlowDetail', id)
    },
  },
  data() {
    return {
      msg: 1,
      columns: [
        {
          title: 'Priority',
          key: 'priority',
          sortable: true,
          width: 110,
        },
        {
          title: 'API',
          key: 'url',
          sortable: true,
          width: 380,
        },
        {
          title: 'Description',
          key: 'desc',
          sortable: true,
          width: 200,
        },
        {
          title: 'Count',
          key: 'count',
          sortable: true,
        },
        {
          title: 'Status',
          key: 'status',
          render: (h, params) => {
            if (params.row.status === 0) {
              return h('p', { style: { color: 'orange' } }, 'NotTest')
            } if (params.row.status === 1) {
              return h('p', { style: { color: 'green' } }, 'Tested')
            } if (params.row.status === 2) {
              return h('p', 'NewAPI')
            }
          },
          sortable: true,
          filters: [
            {
              label: 'Tested',
              value: 1,
            },
            {
              label: 'NotTest',
              value: 0,
            },
            {
              label: 'NewAPI',
              value: 2,
            },
          ],
          filterMultiple: false,
          filterMethod(value, row) {
            if (value === 1) {
              return row.status === 1
            } if (value === 2) {
              return row.status === 2
            } if (value === 0) {
              return row.status === 0
            }
          },
        },
        {
          title: 'Detail',
          key: 'id',
          render: (h, params) => {
            if (params.row.id) {
              return h(
                'i-button',
                {
                  props: { size: 'small' },
                  on: {
                    click: () => {
                      this.viewDetail(params.row.id)
                    },
                  },
                },
                'Detail',
              )
            }
            return h(
              'i-button',
              { props: { size: 'small', type: 'dashed', disabled: true } },
              'NotTest',
            )
          },
        },
      ],
      table_data: [],
      api_id: '',
      isApiDetailModalShow: false,
    }
  },

}
</script>

<style  scoped>
#tab {
  background-color: pink;
  width: 100%;
  height: 100%;
  margin-top: 30px;
}
</style>
