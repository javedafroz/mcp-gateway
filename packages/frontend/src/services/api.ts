import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { getToken, updateToken, login } from './keycloak';
import type {
  ServiceConfig,
  ServicesResponse,
  ChatMessage,
  ChatResponse,
  ApiResponse,
  ApiError,
} from '../types';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8090',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      async (config) => {
        const token = getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor to handle token refresh and errors
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const refreshed = await updateToken();
            if (refreshed) {
              const token = getToken();
              if (token) {
                originalRequest.headers.Authorization = `Bearer ${token}`;
                return this.client(originalRequest);
              }
            }
          } catch (refreshError) {
            console.error('Token refresh failed:', refreshError);
          }

          // If refresh fails, redirect to login
          login();
          return Promise.reject(error);
        }

        return Promise.reject(this.handleError(error));
      }
    );
  }

  private handleError(error: any): ApiError {
    if (error.response) {
      // Server responded with error status
      return {
        message: error.response.data?.detail || error.response.data?.message || 'Server error',
        status: error.response.status,
        details: error.response.data,
      };
    } else if (error.request) {
      // Request was made but no response received
      return {
        message: 'Network error - please check your connection',
        status: 0,
      };
    } else {
      // Something else happened
      return {
        message: error.message || 'An unexpected error occurred',
      };
    }
  }

  // Health check
  async healthCheck(): Promise<any> {
    const response = await this.client.get('/health');
    return response.data;
  }

  // Services API
  async getServices(): Promise<ServicesResponse> {
    const response: AxiosResponse<ServicesResponse> = await this.client.get('/services');
    return response.data;
  }

  async registerService(config: ServiceConfig): Promise<ApiResponse> {
    const response: AxiosResponse<ApiResponse> = await this.client.post('/register-service', config);
    return response.data;
  }

  async deleteService(serviceName: string): Promise<ApiResponse> {
    const response: AxiosResponse<ApiResponse> = await this.client.delete(`/delete-service/${serviceName}`);
    return response.data;
  }

  // Chat API
  async sendChatMessage(message: ChatMessage): Promise<ChatResponse> {
    const response: AxiosResponse<ChatResponse> = await this.client.post('/chat', message);
    return response.data;
  }

  // File upload helper
  async uploadOpenAPIFile(file: File): Promise<any> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const content = e.target?.result as string;
          const parsed = JSON.parse(content);
          resolve(parsed);
        } catch (error) {
          reject(new Error('Invalid JSON file'));
        }
      };
      reader.onerror = () => reject(new Error('Failed to read file'));
      reader.readAsText(file);
    });
  }

  // Validate OpenAPI spec
  validateOpenAPISpec(spec: any): boolean {
    return (
      spec &&
      typeof spec === 'object' &&
      spec.openapi &&
      spec.info &&
      spec.info.title &&
      spec.info.version &&
      spec.paths &&
      typeof spec.paths === 'object'
    );
  }
}

export const apiService = new ApiService();
export default apiService;
