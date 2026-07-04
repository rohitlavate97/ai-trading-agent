const BASE_URL = 'http://localhost:8000/api/v1';

export class ApiClient {
  static async request(endpoint: string, options: RequestInit = {}) {
    const token = localStorage.getItem('token');
    
    const headers = new Headers(options.headers || {});
    if (token) {
      headers.set('Authorization', `Bearer ${token}`);
    }
    // Only set Content-Type to JSON if it's not a FormData request
    if (!headers.has('Content-Type') && !(options.body instanceof FormData)) {
      headers.set('Content-Type', 'application/json');
    }

    const config: RequestInit = {
      ...options,
      headers,
    };

    const response = await fetch(`${BASE_URL}${endpoint}`, config);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'API request failed');
    }
    
    return response.json();
  }

  static get(endpoint: string, options?: RequestInit) {
    return this.request(endpoint, { ...options, method: 'GET' });
  }

  static post(endpoint: string, data?: any, options?: RequestInit) {
    const isFormData = data instanceof FormData;
    return this.request(endpoint, {
      ...options,
      method: 'POST',
      body: isFormData ? data : JSON.stringify(data),
    });
  }
}
