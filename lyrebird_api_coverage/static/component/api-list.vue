<template>
    <div class="box box-solid">
        <div class="box-body" style="height:80vh; overflow:auto">
          <i-table height="1000" stripe :columns="columns" :data="detaildata"></i-table>
          <modal v-model="showAPIDetailModal" title="Data Detail" @on-cancel="showAPIDetailModal=false" width=820>
             <div class="nav-tabs-custom">
                        <ul class="nav nav-tabs">
                            <li class="active"><a href="#tab_req" data-toggle="tab">Request</a></li>
                            <li><a href="#tab_req_data" data-toggle="tab">RequestData</a></li>
                            <li><a href="#tab_resp" data-toggle="tab">Response</a></li> 
                            <li><a href="#tab_resp_data" data-toggle="tab">ResponseData</a></li>
                        </ul>
                        <div class="tab-content">
                             <div class="tab-pane active pre-scrollable" id="tab_req">
                                <div name="req" id="data-modal-req" class="form-control" placeholder=""
                                    style="height: 400px; border:0px"></div>
                             </div><!-- /.tab-pane -->
                             <div class="tab-pane pre-scrollable" id="tab_req_data">
                                <div name="req_data" id="data-modal-req-data" class="form-control" placeholder=""
                                    style="height: 400px; border:0px"></div>
                             </div><!-- /.tab-pane -->
                             <div class="tab-pane pre-scrollable" id="tab_resp">
                                <div name="resp" id="data-modal-resp" class="form-control" placeholder=""
                                     style="height: 400px; border:0px"></div>
                             </div><!-- /.tab-pane -->
                             <div class="tab-pane pre-scrollable" id="tab_resp_data">
                                <div name="resp_data" id="data-modal-resp-data" class="form-control" placeholder=""
                                     style="height: 400px; border:0px"></div>
                             </div><!-- /.tab-pane -->
                        </div><!-- /.tab-content -->
                    </div><!-- nav-tabs-custom -->
            <div slot="footer">
              <i-button type="primary" size="small" @click="showAPIDetailModal=false">OK</i-button>
            </div>
          </modal>
        </div>
    </div>
</template>

<script>
module.exports = {
  props: ["detaildata"],
  mounted: function() {},
  // watch: {
  //   detaildata(val) {
  //     this.table_data = this.detaildata;
  //   }
  // },
  data: function() {
    return {
      columns: [
        {
          title: "Priority",
          key: "priority",
          sortable: true,
          width: 100
        },
        {
          title: "API",
          key: "url",
          sortable: true,
          width: 380
        },
        {
          title: "Description",
          key: "desc",
          sortable: true,
          width: 200
        },
        {
          title: "Count",
          key: "count",
          sortable: true
        },
        {
          title: "Status",
          key: "status",
          render: (h, params) => {
            if (params.row.status === 0) {
              return h("p", { style: { color: "orange" } }, "NotTest");
            } else if (params.row.status === 1) {
              return h("p", { style: { color: "green" } }, "Tested");
            } else if (params.row.status === 2) {
              return h("p", "NewAPI");
            }
          },
          sortable: true,
          filters: [
            {
              label: "Tested",
              value: 1
            },
            {
              label: "NotTest",
              value: 0
            },
            {
              label: "NewAPI",
              value: 2
            }
          ],
          filterMultiple: false,
          filterMethod(value, row) {
            if (value === 1) {
              return row.status === 1;
            } else if (value === 2) {
              return row.status === 2;
            } else if (value === 0) {
              return row.status === 0;
            }
          }
        },
        {
          title: "Detail",
          key: "id",
          render: (h, params) => {
            if (params.row.id) {
              return h(
                "i-button",
                {
                  props: { size: "small" },
                  on: {
                    click: () => {
                      this.viewDetail(params.row.id);
                    }
                  }
                },
                "Detail"
              );
            } else {
              return h(
                "i-button",
                { props: { size: "small", type: "dashed", disabled: true } },
                "NotTest"
              );
            }
          }
        }
      ],
      table_data: [],
      api_id: "",
      showAPIDetailModal: false
    };
  },
  methods: {
    viewDetail: function(id) {
      console.log(id);
      this.api_id = id;
      this.showAPIDetailModal = true;
      this.$http.get("/api/flow/" + id).then(function(data) {
        console.log(data.data);
        var req = {
          url: data.data.request.url,
          method: data.data.request.method,
          headers: data.data.request.headers
        };
        var resp = {
          code: data.data.response.code,
          headers: data.data.response.headers
        };
        $("#data-detail-source").html("Data source : " + resp.headers.lyrebird);
        $("#data-modal-req").JSONView(JSON.stringify(req, null, 4));
        $("#data-modal-req-data").JSONView(
          JSON.stringify(data.data.request.data, null, 4)
        );
        $("#data-modal-resp").JSONView(JSON.stringify(resp, null, 4));
        $("#data-modal-resp-data").JSONView(
          JSON.stringify(data.data.response.data, null, 4)
        );
      });
    }
  }
};
</script>

<style>
</style>
