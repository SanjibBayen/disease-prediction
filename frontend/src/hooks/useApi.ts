import { useState, useCallback } from 'react';
import toast from 'react-hot-toast';

interface UseApiOptions {
  showSuccess?: boolean;
  showError?: boolean;
  successMessage?: string;
}

export function useApi<T = any>() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<T | null>(null);

  const execute = useCallback(
    async (
      promise: Promise<any>,
      options: UseApiOptions = {}
    ) => {
      const { showSuccess = false, showError = true, successMessage } = options;
      
      setLoading(true);
      setError(null);
      
      try {
        const response = await promise;
        setData(response.data);
        
        if (showSuccess) {
          toast.success(successMessage || 'Operation completed successfully');
        }
        
        return response.data;
      } catch (err: any) {
        const errorMessage = err.response?.data?.message || err.message || 'An error occurred';
        setError(errorMessage);
        
        if (showError) {
          toast.error(errorMessage);
        }
        
        throw err;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return { execute, loading, error, data, setData };
}