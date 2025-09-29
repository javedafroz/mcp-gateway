import React from 'react';
import { Link } from 'react-router-dom';
import { 
  ServerIcon, 
  ChatBubbleLeftRightIcon, 
  PlusIcon,
  ChartBarIcon,
  CogIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { useServices } from '../hooks/useServices';
import LoadingSpinner from '../components/LoadingSpinner';

const Dashboard: React.FC = () => {
  const { services, isLoading } = useServices();

  const stats = {
    totalServices: services.active_servers.length,
    totalTools: Object.values(services.details).reduce(
      (total, service) => total + service.tools_count,
      0
    ),
    totalEndpoints: Object.values(services.details).reduce(
      (total, service) => 
        total + Object.keys(service.config.openapi_spec.paths || {}).length,
      0
    ),
  };

  const quickActions = [
    {
      title: 'Register Service',
      description: 'Add a new OpenAPI service to the gateway',
      icon: PlusIcon,
      href: '/services',
      color: 'bg-blue-500',
    },
    {
      title: 'Start Chatting',
      description: 'Interact with your services using AI',
      icon: ChatBubbleLeftRightIcon,
      href: '/chat',
      color: 'bg-green-500',
    },
    {
      title: 'Manage Services',
      description: 'View and configure your registered services',
      icon: ServerIcon,
      href: '/services',
      color: 'bg-purple-500',
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-2 text-gray-600">
            Welcome to MCP Gateway - Your OpenAPI to MCP bridge
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ServerIcon className="h-8 w-8 text-blue-600" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">
                  {isLoading ? <LoadingSpinner size="sm" /> : stats.totalServices}
                </div>
                <div className="text-sm text-gray-500">Active Services</div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CogIcon className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">
                  {isLoading ? <LoadingSpinner size="sm" /> : stats.totalTools}
                </div>
                <div className="text-sm text-gray-500">Available Tools</div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ChartBarIcon className="h-8 w-8 text-purple-600" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">
                  {isLoading ? <LoadingSpinner size="sm" /> : stats.totalEndpoints}
                </div>
                <div className="text-sm text-gray-500">API Endpoints</div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Quick Actions</h2>
            </div>
            <div className="p-6 space-y-4">
              {quickActions.map((action) => (
                <Link
                  key={action.title}
                  to={action.href}
                  className="flex items-center p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                >
                  <div className={`flex-shrink-0 p-2 rounded-md ${action.color}`}>
                    <action.icon className="h-6 w-6 text-white" />
                  </div>
                  <div className="ml-4">
                    <div className="text-sm font-medium text-gray-900">
                      {action.title}
                    </div>
                    <div className="text-sm text-gray-500">
                      {action.description}
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>

          {/* Recent Services */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Recent Services</h2>
            </div>
            <div className="p-6">
              {isLoading ? (
                <div className="flex justify-center py-4">
                  <LoadingSpinner size="md" />
                </div>
              ) : services.active_servers.length === 0 ? (
                <div className="text-center py-8">
                  <ServerIcon className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">
                    No services registered
                  </h3>
                  <p className="mt-1 text-sm text-gray-500">
                    Get started by registering your first service.
                  </p>
                  <div className="mt-6">
                    <Link
                      to="/services"
                      className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
                    >
                      <PlusIcon className="h-4 w-4 mr-2" />
                      Register Service
                    </Link>
                  </div>
                </div>
              ) : (
                <div className="space-y-3">
                  {services.active_servers.slice(0, 5).map((serviceName) => {
                    const service = services.details[serviceName];
                    return service ? (
                      <div
                        key={serviceName}
                        className="flex items-center justify-between p-3 bg-gray-50 rounded-md"
                      >
                        <div className="flex items-center">
                          <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                          <div>
                            <div className="text-sm font-medium text-gray-900">
                              {service.name}
                            </div>
                            <div className="text-xs text-gray-500">
                              {service.tools_count} tools • {service.config.openapi_spec.info.version}
                            </div>
                          </div>
                        </div>
                        <div className="text-xs text-gray-400">
                          Active
                        </div>
                      </div>
                    ) : null;
                  })}
                  {services.active_servers.length > 5 && (
                    <div className="text-center pt-2">
                      <Link
                        to="/services"
                        className="text-sm text-primary-600 hover:text-primary-700"
                      >
                        View all {services.active_servers.length} services →
                      </Link>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Getting Started */}
        {services.active_servers.length === 0 && (
          <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <div className="text-2xl">🚀</div>
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-blue-900">
                  Getting Started with MCP Gateway
                </h3>
                <div className="mt-2 text-sm text-blue-700">
                  <ol className="list-decimal list-inside space-y-1">
                    <li>Register your first OpenAPI service</li>
                    <li>The gateway will automatically create MCP tools</li>
                    <li>Start chatting with your APIs using natural language</li>
                  </ol>
                </div>
                <div className="mt-4">
                  <Link
                    to="/services"
                    className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                  >
                    Get Started
                  </Link>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
