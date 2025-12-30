/** API服务 */
import axios from 'axios';
import { ChatRequest, ChatResponse } from '../types';

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

/**
 * 聊天接口
 */
export const chat = async (request: ChatRequest): Promise<ChatResponse> => {
  const response = await api.post<ChatResponse>('/chat/', request);
  return response.data;
};

/**
 * 健康检查
 */
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
