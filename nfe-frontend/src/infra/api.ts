import axios from 'axios';
import { getUserFromLocalStorage } from './getToken';

export const api = axios.create({
  baseURL: 'https://sistema-erp-ffk6w.ondigitalocean.app/api/v1/',
});

//REQUEST
api.interceptors.request.use(
  (config) => {
    const getLocal = getUserFromLocalStorage();
    if (getLocal?.access) {
      config.headers.Authorization = `Bearer ${getLocal.access}`;
    }
    return config;
  },
  (error) => {
    localStorage.clear();
    return Promise.reject(error);
  },
);

api.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    const getStatusError = error.response.status;
    if (getStatusError === 401) {
      localStorage.clear();
    }
    return Promise.reject(error);
  },
);
