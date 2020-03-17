import getFlowDetail from '../apis/baseList'

export default {
  state: {
    focusedFlowDetail: null,
  },
  mutations: {
    setFocusedFlowDetail(state, focusedFlowDetail) {
      state.focusedFlowDetail = focusedFlowDetail
    },
  },
  actions: {
    loadFlowDetail({ commit }, flowId) {
      getFlowDetail(flowId)
        .then((response) => {
          commit('setFocusedFlowDetail', response.data.data)
        })
    },
  },
}
