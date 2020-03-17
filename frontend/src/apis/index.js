import axios from 'axios'

export * from '@/apis/buttonBar'
export * from '@/apis/baseInfo'
export * from '@/apis/baseList'

const PREFIX = '/plugins/api_coverage/api'

// getTest
export const getTest = () => {
  const url = `${PREFIX}/getTest`
  return axios({
    url,
    method: 'GET',
  })
}

// getCoverage
export const getCoverage = () => {
  const url = `${PREFIX}/getCoverage`
  return axios({
    url,
    method: 'GET',
  })
}
