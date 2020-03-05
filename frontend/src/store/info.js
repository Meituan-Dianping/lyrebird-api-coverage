import * as api from "../apis";

export default {
    state: {
        business: '',
        versionCode: '',
        versionName: ''
    },
    mutations: {
        setBusiness (state, business) {
            state.business = business;
        },
        setVersionCode (state, versionCode) {
            state.versionCode = versionCode;
        },
        setVersionName (state, versionName) {
            state.versionName = versionName;
        },
        
    },
    actions: {
        loadBaseInfo (context) {
            api
                .getBaseInfo()
                .then(response => {
                    if (response.data.code === 1000) {
                        context.commit("setBusiness", response.data.business);
                        context.commit("setVersionCode", response.data.version_code);
                        context.commit("setVersionName", response.data.version_name);
                    } else {
                        console.error("loadBandwidth failed", error);
                    }
                })
                .catch(error => {
                    console.error("loadBandwidth failed", error);
                });
        }
    }
};
