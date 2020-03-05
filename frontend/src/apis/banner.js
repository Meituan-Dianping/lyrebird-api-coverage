import axios from 'axios'

const PREFIX = '/plugins/api_coverage/api'

// importBase
export const uploadBase = upLoadFile => {
    let url = PREFIX + '/importBase'
    return axios({
        url,
        method: 'POST',
        data: upLoadFile
    })
}

//resumeTest
export const resumeTest = upLoadFile => {
    let url = PREFIX + '/resumeTest'
    return axios({
        url,
        method: 'POST',
        data: upLoadFile
    })
}

//saveResult
export const saveResult = resultName => {
    let url = PREFIX + '/saveResult'
    return axios({
        url,
        method: 'POST',
        data: resultName
    })
}

// clearTest
export const clearTest = () => {
    let url = PREFIX + '/clearResult'
    return axios({
        url,
        method: 'GET',
    })
}

//getFilterConf
export const getFilterConf = () => {
    let url = PREFIX + '/getFilterConf'
    return axios({
        url,
        method: 'GET',
    })
}

//setFilterConf
export const setFilterConf = filterFile => {
    let url = PREFIX + '/setFilterConf'
    return axios({
        url,
        method: 'POST',
        data: filterFile
    })
}
