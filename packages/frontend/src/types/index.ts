// API Types
export interface OpenAPISpec {
  openapi: string;
  info: {
    title: string;
    description?: string;
    version: string;
  };
  paths: Record<string, any>;
  components?: Record<string, any>;
}

export interface ServiceConfig {
  name: string;
  openapi_spec: OpenAPISpec;
  base_url: string;
}

export interface Service {
  name: string;
  port: number;
  config: ServiceConfig;
  tools_count: number;
}

export interface ServicesResponse {
  active_servers: string[];
  details: Record<string, Service>;
}

export interface ChatMessage {
  message: string;
  session_id: string;
}

export interface ChatResponse {
  response: string;
  tools_used: string[];
  session_id: string;
}

export interface ApiResponse<T = any> {
  message?: string;
  data?: T;
  error?: string;
}

// UI Types
export interface User {
  id: string;
  username: string;
  email: string;
  firstName?: string;
  lastName?: string;
  roles: string[];
}

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: () => void;
  logout: () => void;
  token: string | null;
}

export interface ServiceFormData {
  name: string;
  base_url: string;
  openapi_spec: OpenAPISpec | null;
  upload_method: 'file' | 'text';
  openapi_text?: string;
}

export interface ChatContextType {
  messages: Array<{
    id: string;
    content: string;
    sender: 'user' | 'assistant';
    timestamp: Date;
    tools_used?: string[];
  }>;
  isLoading: boolean;
  sendMessage: (message: string) => Promise<void>;
  clearMessages: () => void;
}

// Component Props
export interface ServiceCardProps {
  service: Service;
  onDelete: (serviceName: string) => void;
}

export interface FileUploadProps {
  onFileSelect: (file: File) => void;
  accept?: string;
  maxSize?: number;
}

export interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

// Form Types
export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'url' | 'textarea' | 'file' | 'select';
  required?: boolean;
  placeholder?: string;
  options?: Array<{ value: string; label: string }>;
}

// Error Types
export interface ApiError {
  message: string;
  status?: number;
  details?: any;
}

export class AppError extends Error {
  constructor(
    message: string,
    public status?: number,
    public details?: any
  ) {
    super(message);
    this.name = 'AppError';
  }
}
