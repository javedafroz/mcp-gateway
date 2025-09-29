import { useState, useEffect, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService } from '../services/api';
import type { ServicesResponse, ServiceConfig, ApiError } from '../types';

export const useServices = () => {
  const queryClient = useQueryClient();

  const {
    data: services,
    isLoading,
    error,
    refetch,
  } = useQuery<ServicesResponse, ApiError>({
    queryKey: ['services'],
    queryFn: () => apiService.getServices(),
    refetchInterval: 30000, // Refetch every 30 seconds
    staleTime: 10000, // Consider data stale after 10 seconds
  });

  const registerMutation = useMutation({
    mutationFn: (config: ServiceConfig) => apiService.registerService(config),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['services'] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (serviceName: string) => apiService.deleteService(serviceName),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['services'] });
    },
  });

  const registerService = useCallback(
    async (config: ServiceConfig) => {
      try {
        await registerMutation.mutateAsync(config);
        return { success: true };
      } catch (error) {
        return { 
          success: false, 
          error: error instanceof Error ? error.message : 'Failed to register service' 
        };
      }
    },
    [registerMutation]
  );

  const deleteService = useCallback(
    async (serviceName: string) => {
      try {
        await deleteMutation.mutateAsync(serviceName);
        return { success: true };
      } catch (error) {
        return { 
          success: false, 
          error: error instanceof Error ? error.message : 'Failed to delete service' 
        };
      }
    },
    [deleteMutation]
  );

  return {
    services: services || { active_servers: [], details: {} },
    isLoading: isLoading || registerMutation.isPending || deleteMutation.isPending,
    error,
    registerService,
    deleteService,
    refetch,
    isRegistering: registerMutation.isPending,
    isDeleting: deleteMutation.isPending,
  };
};

export default useServices;
