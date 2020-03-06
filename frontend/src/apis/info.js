import axios from 'axios'

const PREFIX = '/plugins/api_coverage/api'

// getBaseInfo
const getBaseInfo = () => {
  const url = `${PREFIX}/baseInfo`
  return axios({
    url,
    method: 'GET',
  })
}
export default getBaseInfo
