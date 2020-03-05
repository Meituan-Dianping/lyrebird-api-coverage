import * as api from "../apis";

export default {
  state: {
    focusedFlowDetail: null
  },
  mutations: {
    setFocusedFlowDetail(state, flowDetail) {
      state.focusedFlowDetail = flowDetail;
    }
  },
  actions: {
    loadFlowDetail({ commit }, flowId) {
      api
        .getFlowDetail(flowId)
        .then(response => {
          commit("setFocusedFlowDetail", response.data.data);
        })
        .catch(error => {
          bus.$emit(
            "msg.error",
            "Load flow " + flowId + " error: " + error.data.message
          );
        });
    }
  }
};
