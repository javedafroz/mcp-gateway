import React, { useState } from 'react';
import { PlusIcon, DocumentTextIcon, CloudArrowUpIcon } from '@heroicons/react/24/outline';
import FileUpload from './FileUpload';
import LoadingSpinner from './LoadingSpinner';
import { apiService } from '../services/api';
import type { ServiceFormData, OpenAPISpec } from '../types';

interface ServiceRegistrationFormProps {
  onSuccess: () => void;
  onCancel: () => void;
  isLoading?: boolean;
}

const ServiceRegistrationForm: React.FC<ServiceRegistrationFormProps> = ({
  onSuccess,
  onCancel,
  isLoading = false,
}) => {
  const [formData, setFormData] = useState<ServiceFormData>({
    name: '',
    base_url: '',
    openapi_spec: null,
    upload_method: 'file',
    openapi_text: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Service name is required';
    }

    if (!formData.base_url.trim()) {
      newErrors.base_url = 'Base URL is required';
    } else {
      try {
        new URL(formData.base_url);
      } catch {
        newErrors.base_url = 'Please enter a valid URL';
      }
    }

    if (!formData.openapi_spec) {
      if (formData.upload_method === 'file') {
        newErrors.openapi_spec = 'Please upload an OpenAPI specification file';
      } else {
        newErrors.openapi_text = 'Please provide OpenAPI specification text';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleFileSelect = async (file: File) => {
    try {
      const spec = await apiService.uploadOpenAPIFile(file);
      if (apiService.validateOpenAPISpec(spec)) {
        setFormData(prev => ({ ...prev, openapi_spec: spec }));
        setErrors(prev => ({ ...prev, openapi_spec: '' }));
      } else {
        setErrors(prev => ({ ...prev, openapi_spec: 'Invalid OpenAPI specification' }));
      }
    } catch (error) {
      setErrors(prev => ({ 
        ...prev, 
        openapi_spec: error instanceof Error ? error.message : 'Failed to parse file' 
      }));
    }
  };

  const handleTextChange = (text: string) => {
    setFormData(prev => ({ ...prev, openapi_text: text }));
    
    if (text.trim()) {
      try {
        const spec = JSON.parse(text);
        if (apiService.validateOpenAPISpec(spec)) {
          setFormData(prev => ({ ...prev, openapi_spec: spec }));
          setErrors(prev => ({ ...prev, openapi_text: '' }));
        } else {
          setErrors(prev => ({ ...prev, openapi_text: 'Invalid OpenAPI specification' }));
        }
      } catch {
        setErrors(prev => ({ ...prev, openapi_text: 'Invalid JSON format' }));
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setIsSubmitting(true);
    try {
      const config = {
        name: formData.name.trim(),
        base_url: formData.base_url.trim(),
        openapi_spec: formData.openapi_spec!,
      };

      const response = await apiService.registerService(config);
      
      if (response) {
        onSuccess();
      }
    } catch (error) {
      setErrors(prev => ({
        ...prev,
        submit: error instanceof Error ? error.message : 'Failed to register service',
      }));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Service Name */}
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
          Service Name
        </label>
        <input
          type="text"
          id="name"
          value={formData.name}
          onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
          placeholder="e.g., employee-service"
        />
        {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name}</p>}
      </div>

      {/* Base URL */}
      <div>
        <label htmlFor="base_url" className="block text-sm font-medium text-gray-700 mb-2">
          Base URL
        </label>
        <input
          type="url"
          id="base_url"
          value={formData.base_url}
          onChange={(e) => setFormData(prev => ({ ...prev, base_url: e.target.value }))}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
          placeholder="https://api.example.com"
        />
        {errors.base_url && <p className="mt-1 text-sm text-red-600">{errors.base_url}</p>}
      </div>

      {/* Upload Method Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          OpenAPI Specification
        </label>
        <div className="flex space-x-4 mb-4">
          <label className="flex items-center">
            <input
              type="radio"
              value="file"
              checked={formData.upload_method === 'file'}
              onChange={(e) => setFormData(prev => ({ 
                ...prev, 
                upload_method: e.target.value as 'file' | 'text',
                openapi_spec: null,
                openapi_text: ''
              }))}
              className="mr-2"
            />
            <CloudArrowUpIcon className="h-4 w-4 mr-1" />
            Upload File
          </label>
          <label className="flex items-center">
            <input
              type="radio"
              value="text"
              checked={formData.upload_method === 'text'}
              onChange={(e) => setFormData(prev => ({ 
                ...prev, 
                upload_method: e.target.value as 'file' | 'text',
                openapi_spec: null,
                openapi_text: ''
              }))}
              className="mr-2"
            />
            <DocumentTextIcon className="h-4 w-4 mr-1" />
            Paste JSON
          </label>
        </div>

        {formData.upload_method === 'file' ? (
          <FileUpload onFileSelect={handleFileSelect} />
        ) : (
          <textarea
            value={formData.openapi_text}
            onChange={(e) => handleTextChange(e.target.value)}
            rows={10}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 font-mono text-sm"
            placeholder="Paste your OpenAPI JSON specification here..."
          />
        )}
        
        {errors.openapi_spec && <p className="mt-1 text-sm text-red-600">{errors.openapi_spec}</p>}
        {errors.openapi_text && <p className="mt-1 text-sm text-red-600">{errors.openapi_text}</p>}
      </div>

      {/* OpenAPI Preview */}
      {formData.openapi_spec && (
        <div className="bg-green-50 border border-green-200 rounded-md p-4">
          <h4 className="text-sm font-medium text-green-800 mb-2">OpenAPI Specification Loaded</h4>
          <div className="text-sm text-green-700">
            <p><strong>Title:</strong> {formData.openapi_spec.info.title}</p>
            <p><strong>Version:</strong> {formData.openapi_spec.info.version}</p>
            <p><strong>Endpoints:</strong> {Object.keys(formData.openapi_spec.paths || {}).length}</p>
          </div>
        </div>
      )}

      {/* Submit Error */}
      {errors.submit && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-sm text-red-600">{errors.submit}</p>
        </div>
      )}

      {/* Form Actions */}
      <div className="flex justify-end space-x-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          disabled={isSubmitting || isLoading}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={isSubmitting || isLoading || !formData.openapi_spec}
          className="px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 flex items-center"
        >
          {isSubmitting ? (
            <>
              <LoadingSpinner size="sm" className="mr-2" />
              Registering...
            </>
          ) : (
            <>
              <PlusIcon className="h-4 w-4 mr-2" />
              Register Service
            </>
          )}
        </button>
      </div>
    </form>
  );
};

export default ServiceRegistrationForm;
