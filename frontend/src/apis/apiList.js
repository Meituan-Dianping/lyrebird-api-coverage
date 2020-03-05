import axios from "axios";

const PREFIX = "/plugins/api_coverage/api";

// getFlowDetail
export const getFlowDetail = flowId => {
  return axios({
    url: "/api/flow/" + flowId
  });
};
