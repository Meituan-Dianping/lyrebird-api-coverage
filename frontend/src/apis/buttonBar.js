import axios from 'axios'

const PREFIX = '/plugins/api_coverage/api'

// importBase
export const uploadBase = (upLoadFile) => {
  const url = `${PREFIX}/importBase`
  return axios({
    url,
    method: 'POST',
    data: upLoadFile,
  })
}

// resumeTest
export const resumeTest = (upLoadFile) => {
  const url = `${PREFIX}/resumeTest`
  return axios({
    url,
    method: 'POST',
    data: upLoadFile,
  })
}

// saveResult
export const saveResult = (resultName) => {
  const url = `${PREFIX}/saveResult`
  return axios({
    url,
    method: 'POST',
    data: resultName,
  })
}

// clearTest
export const clearTest = () => {
  const url = `${PREFIX}/clearResult`
  return axios({
    url,
    method: 'GET',
  })
}

// getFilterConf
export const getFilterConf = () => {
  const url = `${PREFIX}/getFilterConf`
  return axios({
    url,
    method: 'GET',
  })
}

// setFilterConf
export const setFilterConf = (filterFile) => {
  const url = `${PREFIX}/setFilterConf`
  return axios({
    url,
    method: 'POST',
    data: filterFile,
  })
}
