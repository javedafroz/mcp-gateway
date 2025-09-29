import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { initKeycloak, login, logout, isAuthenticated, getUserInfo, getToken } from '../services/keycloak';
import type { AuthContextType, User } from '../types';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const initAuth = async () => {
      try {
        setIsLoading(true);
        const authenticated = await initKeycloak();
        
        if (authenticated) {
          const userInfo = getUserInfo();
          const authToken = getToken();
          
          setUser(userInfo);
          setToken(authToken || null);
        }
      } catch (error) {
        console.error('Authentication initialization failed:', error);
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  const handleLogin = () => {
    login();
  };

  const handleLogout = () => {
    logout();
    setUser(null);
    setToken(null);
  };

  const contextValue: AuthContextType = {
    user,
    isAuthenticated: isAuthenticated(),
    isLoading,
    login: handleLogin,
    logout: handleLogout,
    token,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default useAuth;
