// API service for communicating with your FastAPI backend
import axios from 'axios';
import { browser } from '$app/environment';

const API_BASE = 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  if (browser) {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Auth API calls
export const auth = {
  async login(email, password) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    
    if (browser) {
      localStorage.setItem('auth_token', response.data.access_token);
    }
    return response.data;
  },
  
  async register(email, password) {
    const response = await api.post('/auth/register', { email, password });
    return response.data;
  },
  
  async me() {
    const response = await api.get('/auth/me');
    return response.data;
  },
  
  logout() {
    if (browser) {
      localStorage.removeItem('auth_token');
    }
  }
};

// CV API calls
export const cvs = {
  async list() {
    const response = await api.get('/cvs');
    return response.data;
  },
  
  async get(id) {
    const response = await api.get(`/cvs/${id}`);
    return response.data;
  },
  
  async create(data) {
    const response = await api.post('/cvs', data);
    return response.data;
  },
  
  async update(id, data) {
    const response = await api.put(`/cvs/${id}`, data);
    return response.data;
  },
  
  async delete(id) {
    const response = await api.delete(`/cvs/${id}`);
    return response.data;
  },
  
  async downloadPDF(id) {
    const response = await api.get(`/cvs/${id}/pdf`, {
      responseType: 'blob'
    });
    return response.data;
  }
};

// LLM API calls
export const llm = {
  async chat(message, cvId, conversationHistory = []) {
    const response = await api.post('/llm/chat', {
      message,
      cv_id: cvId,
      conversation_history: conversationHistory
    });
    return response.data;
  },
  
  async inlineEdit(cvId, instruction, section = null, autoSave = true) {
    const response = await api.post('/llm/inline-edit', {
      cv_id: cvId,
      instruction,
      section,
      auto_save: autoSave
    });
    return response.data;
  },
  
  async atsScore(cvId, targetRole = null, jobDescription = null) {
    const response = await api.post('/llm/ats-score', {
      cv_id: cvId,
      target_role: targetRole,
      job_description: jobDescription
    });
    return response.data;
  }
};

export default api;