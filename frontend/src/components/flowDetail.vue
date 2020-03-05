<template>
  <div v-if="flowDetail">
    <Row type="flex" justify="center" align="middle">

      <i-col span="23" class="small-tab">
        <Tabs :value="currentTab" :animated="false" size="small" @on-click="switchTab">
          <TabPane label="Request" name="req"></TabPane>
          <TabPane label="RequestBody" name="req-body"></TabPane>
          <TabPane label="Response" name="resp"></TabPane>
          <TabPane label="ResponseBody" name="resp-body"></TabPane>
        </Tabs>
      </i-col>
    </Row>
    <code-editor
      v-if="flowDetail"
      :language="codeType"
      :content="codeContents"
      class="flow-detail">
    </code-editor>
  </div>
</template>

<script>
import CodeEditor from '@/components/CodeEditor.vue'

export default {
  name: 'flowDetail',
  components: {
    CodeEditor,
  },
  data() {
    return {
      codeType: 'json',
      currentTab: 'req',
    }
  },
  computed: {
    flowDetail() {
      return this.$store.state.apiList.focusedFlowDetail
    },
    codeContents() {
      let codeContent = ''
      if (this.currentTab === 'req') {
        codeContent = JSON.stringify(this.flowDetail.request, null, 4)
        this.codeType = 'json'
      } else if (this.currentTab === 'req-body') {
        if (this.flowDetail.request.data) {
          codeContent = JSON.stringify(this.flowDetail.request.data, null, 4)
          this.codeType = 'json'
        } else {
          codeContent = ''
          this.codeType = 'text'
        }
      } else if (this.currentTab === 'resp') {
        const respInfo = {
          code: this.flowDetail.response.code,
          headers: this.flowDetail.response.headers,
        }
        codeContent = JSON.stringify(respInfo, null, 4)
        this.codeType = 'json'
      } else if (this.currentTab === 'resp-body') {
        if (this.flowDetail.response.data === null) {
          codeContent = ''
          this.codeType = 'text'
          return
        }
        if (this.flowDetail.response.headers.hasOwnProperty('Content-Type')) {
          const contentType = this.flowDetail.response.headers['Content-Type']
          if (contentType.includes('html')) {
            codeContent = this.parseHtmlData(this.flowDetail.response.data)
          } else if (contentType.includes('xml')) {
            codeContent = this.parseXmlData(this.flowDetail.response.data)
          } else if (contentType.includes('json')) {
            codeContent = this.parseJsonData(this.flowDetail.response.data)
          } else {
            codeContent = this.parseTextData(this.flowDetail.response.data)
          }
        } else {
          codeContent = this.parseTextData(this.flowDetail.response.data)
        }
      }
      return codeContent
    },
  },
  methods: {
    switchTab(name) {
      this.currentTab = name
    },
    parseJsonData(data) {
      this.codeType = 'json'
      return JSON.stringify(data, null, 4)
    },
    parseHtmlData() {
      this.codeType = 'html'
      return this.flowDetail.response.data
    },
    parseXmlData() {
      this.codeType = 'xml'
      return this.flowDetail.response.data
    },
    parseTextData() {
      this.codeType = 'text'
      return this.flowDetail.response.data
    },
  },
}
</script>

<style lang="css">
.small-tab > .ivu-tabs > .ivu-tabs-bar {
  margin-bottom: 0;
}
.flow-detail {
  height: 50vh;
}
</style>
