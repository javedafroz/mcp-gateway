// Simplified auth service for development - replace with actual Keycloak integration

const keycloakConfig = {
  url: process.env.REACT_APP_KEYCLOAK_URL || 'http://localhost:1010',
  realm: process.env.REACT_APP_KEYCLOAK_REALM || 'mcp-gateway',
  clientId: process.env.REACT_APP_KEYCLOAK_CLIENT_ID || 'mcp-gateway-frontend',
};

// Mock authentication for development
let mockAuthenticated = true;
let mockToken = 'mock-jwt-token';
let mockUser = {
  id: 'user-123',
  username: 'demo-user',
  email: 'demo@example.com',
  firstName: 'Demo',
  lastName: 'User',
  roles: ['user'],
};

export const initKeycloak = async (): Promise<boolean> => {
  try {
    // Simulate initialization delay
    await new Promise(resolve => setTimeout(resolve, 500));
    console.log('Mock Keycloak initialized');
    return mockAuthenticated;
  } catch (error) {
    console.error('Failed to initialize Keycloak:', error);
    return false;
  }
};

export const login = () => {
  console.log('Mock login');
  mockAuthenticated = true;
};

export const logout = () => {
  console.log('Mock logout');
  mockAuthenticated = false;
  mockToken = '';
};

export const getToken = (): string | undefined => {
  return mockAuthenticated ? mockToken : undefined;
};

export const isAuthenticated = (): boolean => {
  return mockAuthenticated;
};

export const getUserInfo = () => {
  return mockAuthenticated ? mockUser : null;
};

export const updateToken = async (): Promise<boolean> => {
  try {
    console.log('Mock token refresh');
    return true;
  } catch (error) {
    console.error('Failed to refresh token:', error);
    return false;
  }
};

export default {
  init: initKeycloak,
  login,
  logout,
  authenticated: mockAuthenticated,
  token: mockToken,
};
