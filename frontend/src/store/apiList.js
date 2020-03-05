import getFlowDetail from '../apis/apiList'

export default {
  state: {
    focusedFlowDetail: null,
  },
  mutations: {
    setFocusedFlowDetail(state, flowDetail) {
      state.focusedFlowDetail = flowDetail
    },
  },
  actions: {
    loadFlowDetail({ commit }, flowId) {
      getFlowDetail(flowId)
        .then((response) => {
          commit('setFocusedFlowDetail', response.data.data)
        })
        .catch((error) => {
          bus.$emit(
            'msg.error',
            `Load flow ${flowId} error: ${error.data.message}`,
          )
        })
    },
  },
}
