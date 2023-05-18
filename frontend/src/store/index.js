import Vue from 'vue'
import Vuex from 'vuex'
import * as apis from '@/apis'
import info from '@/store/info'
import apiList from '@/store/apiList'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    detailData: [],
    coverageData: {},
    showedAPIData: [],
  },
  mutations: {
    setDetailData(state, detailData) {
      state.detailData = detailData
    },
    setCoverageData(state, coverageData) {
      state.coverageData = coverageData
    },
    setShowedAPIData(state, showedAPIData) {
      state.showedAPIData = showedAPIData
    },
  },
  actions: {
    loadDetailData(context) {
      apis
        .getTest()
        .then((response) => {
          context.commit('setDetailData', response.data.test_data)
          context.commit('setShowedAPIData', response.data.test_data)
        })
        .catch(() => {
          this.$Notice.open({ title: 'loadDetailData error!' })
        })
    },
    loadCoverageData(context) {
      apis
        .getCoverage()
        .then((response) => {
          context.commit('setCoverageData', response.data.coverage)
        })
        .catch(() => {
          this.$Notice.open({ title: 'loadCoverageData error!' })
        })
    },
    setShowedAPIData(context, showedAPIData) {
      context.commit('setShowedAPIData', showedAPIData)
    },
  },
  modules: {
    info,
    apiList,
  },
})
