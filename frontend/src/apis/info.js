import axios from 'axios'

const PREFIX = '/plugins/api_coverage/api'

// getBaseInfo
export const getBaseInfo = () => {
    let url = PREFIX + '/baseInfo'
    return axios({
        url,
        method: 'GET',
    })
}
