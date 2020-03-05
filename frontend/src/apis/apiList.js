import axios from 'axios'

// getFlowDetail
const getFlowDetail = (flowId) => axios({
  url: `/api/flow/${flowId}`,
})

export default getFlowDetail
