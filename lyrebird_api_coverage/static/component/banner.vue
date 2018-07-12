<template>
    <div class="box box-solid">
        <div class="box-body">
            <div class="row">
                <div class="col-lg-10">
                    <label class="btn btn-primary btn-file" style="backgroud-color:#1874CD;">
                      <Icon type="archive"></Icon> Import Base
                      <input id="load-file" type="file" name="import-base-file" @change="upload">
                    </label>
                    <label class="btn btn-primary btn-file" style="backgroud-color:#1874CD;">
                      <Icon type="refresh"></Icon> Resume Test
                      <input id="resume-file" type="file" name="import-test-file" @change="resumeTest">
                    </label>
                    <button class="btn btn-success" style="background-color:#20B2AA;" @click="showCreateResultModal=true">
                      <Icon type="folder"></Icon> Save Result
                    </button>
                    <modal v-model="showCreateResultModal" title="Save Result" @on-ok="createResultOk">
                        <label>Path: ~/.lyrebird/plugins/lyrebird_api_coverage/data</label>
                        <i-input placeholder="Type file name,eg:travel_9.5_test_result" v-model="newResultName">
                    </modal>
                    <button class="btn btn-warning" style="background-color:#EEAD0E;" @click="clearTest">
                      <Icon type="trash-b"></Icon> Clear Test
                    </button>
                    <button class="btn btn-primary" style="backgroud-color:#1874CD;" @click="filterShow">
                      <Icon type="paperclip"></Icon> Filtering Rules
                    </button>
                    <modal v-model="showFilterModal" title="Edit Filtering Rules" @on-ok="editFilterOk" style="width:1000px">
                      <form id="filtering-rules-form">
                        <div class="form-group">
                          <textarea name="filter_data" id="filtering-rules-modal-data" class="form-control" placeholder="filtering rules json" style="height: 350px;" v-model="filterRules"></textarea>
                        </div>
                      </form>
                    </modal>
                </div><!-- /.col-lg-10 -->
                <div class="col-lg-2">
                    <div class="input-group">
                        <input v-model="targetContext" type="text" class="form-control input-sm" placeholder="Search..." @keyup.enter="popTargetContext(targetContext)">
                        <span class="input-group-btn">
                            <button class="btn btn-primary btn-sm" type="button" @click="popTargetContext(targetContext)">
                              <Icon type="search"></Icon>
                            </button>
                        </span>
                    </div><!-- /input-group -->
                </div><!-- /.col-lg-2 -->
        </div><!-- /.box-body -->
    </div><!-- /.box -->
</template>

<script>
module.exports = {
  mounted: function() {
    this.$Notice.config({
      top: 75
    });
  },
  data: function() {
    return {
      targetContext: null,
      showCreateResultModal: false,
      showFilterModal: false,
      newResultName: "",
      filterRules: ""
    };
  },
  methods: {
    upload: function() {
      let file = document.getElementById("load-file");
      var filename = file.value;
      if (!filename || !filename.endsWith(".json")) {
        this.$Notice.open({ title: "只能上传.json后缀的文件 ：）" });
      } else {
        let upLoadFile = new FormData();
        upLoadFile.append("json-import", $("#load-file")[0].files[0]);
        this.$http
          .post("/ui/plugin/api_coverage/importBase", upLoadFile)
          .then(function(data) {
            console.log(data.data);
            if (data.data.code == 1000) {
              this.$Notice.open({ title: "Import base success!" });
              this.$emit("newbase");
              this.$emit("newcoverage");
            } else if (data.data.code == 3000) {
              this.$Notice.open({
                title: "import file failed!",
                desc: String(data.data.message)
              });
            } else {
              this.$Notice.open({ title: "Import base failed!" });
            }
          });
      }
      file.outerHTML = file.outerHTML;
    },
    clearTest: function() {
      this.$http.get("/ui/plugin/api_coverage/clearResult").then(function(data) {
        console.log(data.data);
        if (data.data.code == 1000) {
          this.$Notice.open({ title: "Clear test success!" });
          this.$emit("newbase");
          this.$emit("newcoverage");
        } else {
          this.$Notice.open({ title: "Clear test failed!" });
        }
      });
    },
    resumeTest: function() {
      let file = document.getElementById("resume-file");
      var filename = file.value;
      if (!filename || !filename.endsWith(".json")) {
        this.$Notice.open({ title: "只能上传.json后缀的文件 ：）" });
      } else {
        let upLoadFile = new FormData();
        upLoadFile.append("json-import", $("#resume-file")[0].files[0]);
        this.$http
          .post("/ui/plugin/api_coverage/resumeTest", upLoadFile)
          .then(function(data) {
            console.log(data.data);
            if (data.data.code == 1000) {
              this.$Notice.open({ title: "Resume test success!" });
              this.$emit("newbase");
              this.$emit("newcoverage");
            } else if (data.data.code == 3000) {
              this.$Notice.open({
                title: "Resume test failed!",
                desc: String(data.data.message)
              });
            } else {
              this.$Notice.open({ title: "Resume test failed!" });
            }
          });
      }
      file.outerHTML = file.outerHTML;
    },
    createResultOk: function() {
      let data = new FormData();
      data.append("result_name", this.newResultName);
      let name = this.newResultName;
      if (name) {
        this.$http.post("/ui/plugin/api_coverage/saveResult", data).then(response => {
          console.log("Create result success");
          this.$Notice.open({ title: "Create result success!" });
          this.newResultName = null;
        }),
          error => {
            this.$Notice.open({ title: "Create result error!" });
            this.newResultName = null;
          };
      } else {
        this.$Notice.open({ title: "Result name is null!" });
      }
    },
    filterShow: function() {
      this.showFilterModal = true;
      this.$http.get("/ui/plugin/api_coverage/getFilterConf").then(function(data) {
        if (data.data.code == 3000) {
          this.$Notice.open({ title: data.data.message });
        } else {
          $("#filtering-rules-modal-data").val(
            JSON.stringify(data.data, null, 4)
          );
          //$("#filtering-rules-modal").modal();
        }
      });
    },
    editFilterOk: function() {
      let data = new FormData($("#filtering-rules-form")[0]);
      this.$http
        .post("/ui/plugin/api_coverage/setFilterConf", data)
        .then(function(data) {
          if (data.data.code == 1000) {
            this.$Notice.open({ title: "Set filter success!" });
          } else if (data.data.code == 3000) {
            console.log(data);
            this.$Notice.open({
              title: "Set filter error!",
              desc: data.data.message
            });
          } else {
            this.$Notice.open({ title: "Set filter error!" });
          }
        });
    },
    popTargetContext: function(targetContext) {
      this.$emit("poptarget", targetContext);
    }
  }
};
</script>

<style>
</style>
