<template>
  <div id="tab" class="box box-solid">
    <div class="box-body" style="max-height:calc(100vh - 100px) overflow:auto">
      <i-table stripe :columns="columns" :data="showedAPIData">
        <template #product="{ row, index }">
          <template v-if="row.products.length > 0">
            <template v-for="item in row.products">
              <Tag v-if="item.status == 1" color="green">{{
                item.label.split("-")[0]
              }}</Tag>
            </template>
          </template>
        </template>
      </i-table>
      <Modal v-model="isApiDetailModalShow" title="Flow Detail" width="1300">
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
          // width: 110,
        },
        {
          title: 'API',
          key: 'url',
          sortable: true,
          // width: 380,
        },
        {
          title: 'Description',
          key: 'desc',
          sortable: true,
          // width: 200,
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
            }
            if (params.row.status === 1) {
              return h('p', { style: { color: 'green' } }, 'Tested')
            }
            if (params.row.status === 2) {
              return h('p', 'NewAPI')
            }
            return h('p', null)
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
            }
            if (value === 2) {
              return row.status === 2
            }
            if (value === 0) {
              return row.status === 0
            }
            return row.status === null
          },
        },
        {
          title: 'Coverage-Product',
          key: 'product',
          slot: 'product',
          sortable: true,
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
                'Detail'
              )
            }
            return h(
              'i-button',
              { props: { size: 'small', type: 'dashed', disabled: true } },
              'Detail'
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
  width: 100%;
  height: 100%;
  margin-top: 30px;
}
</style>
