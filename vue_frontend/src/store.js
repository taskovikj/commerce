import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    user: null,
    isAuthenticated: false,
    listings: [],
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
      state.isAuthenticated = !!user;
    },
    clearUser(state) {
      state.user = null;
      state.isAuthenticated = false;
    },
    setListings(state, listings) {
      state.listings = listings;
    }
  },
  actions: {
    loginUser({ commit }, credentials) {
      return axios.post('/api/login/', credentials)
        .then(response => {
          commit('setUser', response.data.user);
        });
    },
    fetchListings({ commit }) {
      return axios.get('/api/listings/')
        .then(response => {
          commit('setListings', response.data.listings);
        });
    }
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    getListings: state => state.listings,
  }
});
