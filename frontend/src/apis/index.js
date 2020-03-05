import axios from 'axios'
export * from '@/apis/banner'
export * from '@/apis/info'
export * from '@/apis/apiList'

const PREFIX = '/plugins/api_coverage/api'

// getTest
export const getTest = () => {
    let url = PREFIX + '/getTest'
    return axios({
        url,
        method: 'GET',
    })
}

// getCoverage
export const getCoverage = () => {
    let url = PREFIX + '/getCoverage'
    return axios({
        url,
        method: 'GET',
    })
}
