const API_BASE_URL = import.meta.env.VITE_API_URL || '';

class ApiService {
  constructor() {
    this.token = localStorage.getItem('auth_token');
  }

  async getToken() {
    const urlParams = new URLSearchParams(window.location.search);
    const gclid = urlParams.get('gclid');
    const utm_source = urlParams.get('utm_source');
    
    if (!gclid && !utm_source) {
      throw new Error('Missing required parameters: gclid or utm_source');
    }

    const params = new URLSearchParams();
    if (gclid) params.append('gclid', gclid);
    if (utm_source) params.append('utm_source', utm_source);

    const response = await fetch(`${API_BASE_URL}/api/get_token?${params}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    this.token = data.token;
    localStorage.setItem('auth_token', this.token);
    return data;
  }

  async trackEvent(eventType, meta = {}) {
    if (!this.token) {
      throw new Error('No token available');
    }

    const response = await fetch(`${API_BASE_URL}/api/track`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      },
      body: JSON.stringify({
        event_type: eventType,
        meta: meta
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async convert(inputValue) {
    if (!this.token) {
      throw new Error('No token available');
    }

    const response = await fetch(`${API_BASE_URL}/api/convert`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      },
      body: JSON.stringify({
        input_value: inputValue
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
}

export default new ApiService();