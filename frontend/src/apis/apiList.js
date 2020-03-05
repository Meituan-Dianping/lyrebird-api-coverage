import axios from 'axios'

const PREFIX = '/plugins/api_coverage/api'

// getFlowDetail
const getFlowDetail = (flowId) => axios({
  url: `/api/flow/${flowId}`,
})

export default getFlowDetail
