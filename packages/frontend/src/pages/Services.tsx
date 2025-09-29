import React, { useState } from 'react';
import { PlusIcon, ServerIcon } from '@heroicons/react/24/outline';
import { useServices } from '../hooks/useServices';
import ServiceCard from '../components/ServiceCard';
import ServiceRegistrationForm from '../components/ServiceRegistrationForm';
import Modal from '../components/Modal';
import LoadingSpinner from '../components/LoadingSpinner';

const Services: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { services, isLoading, error, deleteService, refetch } = useServices();

  const handleDeleteService = async (serviceName: string) => {
    const result = await deleteService(serviceName);
    if (!result.success) {
      alert(`Failed to delete service: ${result.error}`);
    }
  };

  const handleServiceRegistered = () => {
    setIsModalOpen(false);
    refetch();
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-4xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Failed to load services
          </h2>
          <p className="text-gray-600 mb-4">
            {error.message || 'An unexpected error occurred'}
          </p>
          <button
            onClick={() => refetch()}
            className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Services</h1>
              <p className="mt-2 text-gray-600">
                Manage your registered OpenAPI services and their MCP integrations
              </p>
            </div>
            <button
              onClick={() => setIsModalOpen(true)}
              className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <PlusIcon className="h-5 w-5 mr-2" />
              Register Service
            </button>
          </div>
        </div>

        {/* Services Grid */}
        {isLoading ? (
          <div className="flex justify-center items-center py-12">
            <LoadingSpinner size="lg" />
          </div>
        ) : services.active_servers.length === 0 ? (
          <div className="text-center py-12">
            <ServerIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No services registered</h3>
            <p className="mt-1 text-sm text-gray-500">
              Get started by registering your first OpenAPI service.
            </p>
            <div className="mt-6">
              <button
                onClick={() => setIsModalOpen(true)}
                className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
              >
                <PlusIcon className="h-5 w-5 mr-2" />
                Register Your First Service
              </button>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {services.active_servers.map((serviceName) => {
              const service = services.details[serviceName];
              return service ? (
                <ServiceCard
                  key={serviceName}
                  service={{ ...service, name: serviceName }}
                  onDelete={handleDeleteService}
                />
              ) : null;
            })}
          </div>
        )}

        {/* Statistics */}
        {services.active_servers.length > 0 && (
          <div className="mt-8 bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Statistics</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-primary-600">
                  {services.active_servers.length}
                </div>
                <div className="text-sm text-gray-500">Active Services</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {Object.values(services.details).reduce(
                    (total, service) => total + service.tools_count,
                    0
                  )}
                </div>
                <div className="text-sm text-gray-500">Total Tools</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {Object.values(services.details).reduce(
                    (total, service) => 
                      total + Object.keys(service.config.openapi_spec.paths || {}).length,
                    0
                  )}
                </div>
                <div className="text-sm text-gray-500">API Endpoints</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Registration Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Register New Service"
      >
        <ServiceRegistrationForm
          onSuccess={handleServiceRegistered}
          onCancel={() => setIsModalOpen(false)}
        />
      </Modal>
    </div>
  );
};

export default Services;
