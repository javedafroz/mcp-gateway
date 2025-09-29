import React from 'react';
import { ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline';
import ChatInterface from '../components/ChatInterface';
import { useServices } from '../hooks/useServices';

const Chat: React.FC = () => {
  const { services } = useServices();

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center">
            <ChatBubbleLeftRightIcon className="h-8 w-8 text-primary-600 mr-3" />
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Chat Interface</h1>
              <p className="mt-2 text-gray-600">
                Interact with your registered services using natural language
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Chat Interface */}
          <div className="lg:col-span-3">
            <div className="h-[600px]">
              <ChatInterface />
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Available Services
              </h3>
              
              {services.active_servers.length === 0 ? (
                <div className="text-center py-4">
                  <div className="text-gray-400 text-2xl mb-2">🔧</div>
                  <p className="text-sm text-gray-500">
                    No services registered yet. Register a service to start chatting!
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  {services.active_servers.map((serviceName) => {
                    const service = services.details[serviceName];
                    return service ? (
                      <div
                        key={serviceName}
                        className="p-3 bg-gray-50 rounded-md border"
                      >
                        <div className="flex items-center justify-between">
                          <h4 className="font-medium text-gray-900 text-sm">
                            {serviceName}
                          </h4>
                          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                            Active
                          </span>
                        </div>
                        <p className="text-xs text-gray-500 mt-1">
                          {service.tools_count} tools available
                        </p>
                      </div>
                    ) : null;
                  })}
                </div>
              )}

              {/* Usage Tips */}
              <div className="mt-6 pt-6 border-t border-gray-200">
                <h4 className="text-sm font-medium text-gray-900 mb-3">
                  💡 Usage Tips
                </h4>
                <ul className="text-xs text-gray-600 space-y-2">
                  <li>• Ask about available services and their capabilities</li>
                  <li>• Request specific data from your APIs</li>
                  <li>• Use natural language - no need for technical syntax</li>
                  <li>• The AI will automatically use the right tools</li>
                </ul>
              </div>

              {/* Example Queries */}
              <div className="mt-4">
                <h4 className="text-sm font-medium text-gray-900 mb-3">
                  📝 Example Queries
                </h4>
                <div className="space-y-2 text-xs">
                  <div className="p-2 bg-blue-50 rounded border-l-2 border-blue-200">
                    "List all employees in the engineering department"
                  </div>
                  <div className="p-2 bg-blue-50 rounded border-l-2 border-blue-200">
                    "What services are currently registered?"
                  </div>
                  <div className="p-2 bg-blue-50 rounded border-l-2 border-blue-200">
                    "Show me the API endpoints for the user service"
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
