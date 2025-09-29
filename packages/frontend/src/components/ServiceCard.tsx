import React, { useState } from 'react';
import { TrashIcon, CogIcon, CheckCircleIcon } from '@heroicons/react/24/outline';
import type { ServiceCardProps } from '../types';
import LoadingSpinner from './LoadingSpinner';

const ServiceCard: React.FC<ServiceCardProps> = ({ service, onDelete }) => {
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete the service "${service.name}"?`)) {
      setIsDeleting(true);
      try {
        await onDelete(service.name);
      } finally {
        setIsDeleting(false);
      }
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <h3 className="text-lg font-semibold text-gray-900">{service.name}</h3>
            <CheckCircleIcon className="h-5 w-5 text-green-500" />
          </div>
          
          <div className="space-y-2 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <CogIcon className="h-4 w-4" />
              <span>{service.tools_count} tools available</span>
            </div>
            
            <div>
              <span className="font-medium">Base URL:</span>{' '}
              <span className="text-primary-600">{service.config.base_url}</span>
            </div>
            
            <div>
              <span className="font-medium">API Version:</span>{' '}
              {service.config.openapi_spec.info.version}
            </div>
            
            {service.config.openapi_spec.info.description && (
              <div>
                <span className="font-medium">Description:</span>{' '}
                {service.config.openapi_spec.info.description}
              </div>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2 ml-4">
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
            Active
          </span>
          
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-md transition-colors disabled:opacity-50"
            title="Delete service"
          >
            {isDeleting ? (
              <LoadingSpinner size="sm" />
            ) : (
              <TrashIcon className="h-5 w-5" />
            )}
          </button>
        </div>
      </div>

      {/* API Endpoints Preview */}
      <div className="mt-4 pt-4 border-t border-gray-100">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Available Endpoints</h4>
        <div className="space-y-1">
          {Object.entries(service.config.openapi_spec.paths || {})
            .slice(0, 3)
            .map(([path, methods]) => (
              <div key={path} className="text-xs text-gray-500">
                <span className="font-mono bg-gray-100 px-2 py-1 rounded">
                  {Object.keys(methods as object).join(', ').toUpperCase()}
                </span>{' '}
                <span>{path}</span>
              </div>
            ))}
          {Object.keys(service.config.openapi_spec.paths || {}).length > 3 && (
            <div className="text-xs text-gray-400">
              +{Object.keys(service.config.openapi_spec.paths || {}).length - 3} more endpoints
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ServiceCard;
