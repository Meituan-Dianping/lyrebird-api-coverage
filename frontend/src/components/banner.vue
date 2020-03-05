<template>
  <Row>
    <i-col span="18" class="colLeft">
      <Button
        class="btn"
        :size="buttonSize"
        @click="openImportBaseIpt"
        icon="ios-create"
        type="primary"
        >Import Base</Button
      >
      <input
        ref="baseElem"
        id="importBaseIpt"
        type="file"
        class="upload-file"
        @change="importBase"
        style="display:none"
      />
      <Button
        class="btn"
        :size="buttonSize"
        @click="openResumeTestIpt"
        icon="md-cloud-upload"
        type="primary"
        >Resume Test</Button
      >
      <input
        ref="resumeElem"
        id="resumeTestIpt"
        type="file"
        class="upload-file"
        @change="resumeTest"
        style="display:none"
      />

      <Button
        class="btn"
        :size="buttonSize"
        icon="md-cloud-download"
        type="primary"
        @click="showSaveResultModal"
        >Save Result</Button
      >
      <Button
        class="btn"
        :size="buttonSize"
        icon="md-refresh-circle"
        type="primary"
        @click="clearTest"
        >Clear Test</Button
      >
      <Button
        class="btn"
        :size="buttonSize"
        icon="ios-construct"
        type="primary"
        @click="filterShow"
        >Filtering Rules</Button
      >
      <modal
        v-model="showFilterModal"
        title="Edit Filtering Rules"
        @on-ok="editFilterOk"
        style="width:1000px"
      >
        <form id="filtering-rules-form">
          <div class="form-group">
            <textarea
              name="filter_data"
              id="filtering-rules-modal-data"
              class="form-control"
              placeholder="filtering rules json"
              style="height: 350px;width:100%"
              v-model="filterRules"
            ></textarea>
          </div>
        </form>
      </modal>
    </i-col>
    <i-col span="6" class="colRight">
      <Input
        class="searchInput"
        v-model="targetContext"
        icon="md-search"
        @click.native="popTargetContext(targetContext)"
        @keyup.enter.native="popTargetContext(targetContext)"
        placeholder="Enter something..."
      />
    </i-col>
  </Row>
</template>

<script>
import * as api from "../apis";

export default {
  data() {
    return {
      buttonSize: "default",
      newResultName: "",
      showFilterModal: false,
      filterRules: "",
      targetContext: null
    };
  },
  methods: {
    // import base
    openImportBaseIpt() {
      this.$refs.baseElem.dispatchEvent(new MouseEvent("click"));
    },
    importBase(e) {
      const file = document.getElementById("importBaseIpt");
      const filename = file.value;
      if (!filename || !filename.endsWith(".json")) {
        this.$Notice.open({ title: "只能上传.json后缀的文件 ：）" });
      } else {
        const upLoadFile = new FormData();

        upLoadFile.append("json-import", e.target.files[0]);
        api
          .uploadBase(upLoadFile)
          .then(response => {
            if (response.data.code === 1000) {
              this.$Notice.open({ title: "Import base success!" });
              this.$emit("newbase");
            } else {
              this.$Notice.open({
                title: "import file failed!",
                desc: String(response.data.message)
              });
            }
          })
          .catch(() => {
            this.$Notice.open({ title: "Import base failed!" });
          });
      }
    },

    // resume Test
    openResumeTestIpt() {
      this.$refs.resumeElem.dispatchEvent(new MouseEvent("click"));
    },
    resumeTest(e) {
      const file = document.getElementById("resumeTestIpt");
      const filename = file.value;
      if (!filename || !filename.endsWith(".json")) {
        this.$Notice.open({ title: "只能上传.json后缀的文件 ：）" });
      } else {
        const upLoadFile = new FormData();
        upLoadFile.append("json-import", e.target.files[0]);
        api.resumeTest(upLoadFile).then(response => {
          if (response.data.code === 1000) {
            this.$Notice.open({ title: "resume Test success!" });
            this.$emit("newbase");
          } else {
            this.$Notice.open({
              title: response.data.message
            });
          }
        });
      }
    },

    // save result
    showSaveResultModal() {
      this.$Modal.confirm({
        render: h =>
          h("div", [
            h(
              "div",
              {
                style:
                  "margin-bottom:20px;vertical-align: middle;font-size: 16px;color: #17233d;font-weight: 700;"
              },
              "Save Result"
            ),
            h(
              "div",
              {
                style:
                  "margin-bottom:20px;vertical-align: middle;color: #17233d;font-weight: 200;"
              },
              [
                h(
                  "span",
                  "Path: ~/.lyrebird/plugins/lyrebird_api_coverage/data"
                ),
                h("Icon", {
                  props: {
                    type: "md-copy"
                  },
                  style: {
                    fontSize: "18px",
                    color: "gary",
                    marginLeft: "5px"
                  },
                  on: {
                    click: e => {
                      // 获取需要复制的文字
                      const copyStr = e.target.offsetParent.innerText.split(
                        ":"
                      )[1];
                      // 创建input标签存放需要复制的文字
                      const oInput = document.createElement("input");
                      // 把文字放进input中，供复制
                      oInput.value = copyStr;
                      document.body.appendChild(oInput);
                      // 选中创建的input
                      oInput.select();
                      // 执行复制方法， 该方法返回bool类型的结果，告诉我们是否复制成功
                      const copyResult = document.execCommand("copy");
                      // 操作中完成后 从Dom中删除创建的input
                      document.body.removeChild(oInput);
                      // 根据返回的复制结果 给用户不同的提示
                      if (copyResult) {
                        this.$Message.info(
                          "The saved path has been copied to the clipboard"
                        );
                      } else {
                        this.$Message.error("copy failed");
                      }
                    }
                  }
                })
              ]
            ),
            h("Input", {
              props: {
                value: this.value,
                autofocus: true,
                placeholder: "Type file name,eg:travel_9.5_test_result"
              },
              on: {
                input: val => {
                  this.newResultName = val;
                }
              }
            })
          ]),
        onOk: () => {
          const data = new FormData();
          data.append("result_name", this.newResultName);
          const name = this.newResultName;
          if (name) {
            api.saveResult(data).then(() => {
              if (response.data.code === 1000) {
                this.$Notice.open({ title: "Create result success!" });
                this.newResultName = null;
              } else {
                this.$Notice.open({ title: "Create result failed!" });
                this.newResultName = null;
              }
            });
          } else {
            this.$Notice.open({ title: "Result name is null!" });
          }
        }
      });
    },

    // clear test
    clearTest() {
      api.clearTest().then(response => {
        if (response.data.code === 1000) {
          this.$Notice.open({ title: "Clear test success!" });
          this.$emit("newbase");
          this.$emit("newcoverage");
        } else {
          this.$Notice.open({ title: "Clear test failed!" });
        }
      });
    },

    // filter
    filterShow() {
      this.showFilterModal = true;
      api.getFilterConf().then(data => {
        if (data.data.code === 3000) {
          this.$Notice.open({ title: data.data.message });
        } else {
          document.getElementById(
            "filtering-rules-modal-data"
          ).value = JSON.stringify(data.data, null, 4);
        }
      });
    },
    editFilterOk() {
      const data = new FormData(
        document.getElementById("filtering-rules-form")
      );
      api.setFilterConf(data).then(data => {
        if (data.data.code === 1000) {
          this.$Notice.open({ title: "Set filter success!" });
        } else if (data.data.code === 3000) {
          this.$Notice.open({
            title: "Set filter error!",
            desc: data.data.message
          });
        } else {
          this.$Notice.open({ title: "Set filter error!" });
        }
      });
    },

    // search
    popTargetContext(targetContext) {
      this.$emit("poptarget", targetContext);
    },
  }
};
</script>

<style scoped>
.colLeft {
  min-width: 750px;
}
.colLeft .btn {
  margin: 10px 5px 10px 5px;
}
.colRight .searchInput {
  margin: 10px 5px 10px 5px;
  width: 300px;
  min-width: 350px;
}
</style>
