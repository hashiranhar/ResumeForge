import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Auth state
export const user = writable(null);
export const token = writable(null);
export const isAuthenticated = writable(false);

// Initialize auth state from localStorage
if (browser) {
    const storedToken = localStorage.getItem('resumeforge_token');
    const storedUser = localStorage.getItem('resumeforge_user');
    
    if (storedToken && storedUser) {
        try {
            token.set(storedToken);
            user.set(JSON.parse(storedUser));
            isAuthenticated.set(true);
        } catch (e) {
            // Clear invalid data
            localStorage.removeItem('resumeforge_token');
            localStorage.removeItem('resumeforge_user');
        }
    }
}

// Auth functions
export const authService = {
    async login(email, password) {
        try {
            const formData = new FormData();
            formData.append('username', email); // OAuth2 uses 'username' field
            formData.append('password', password);

            const response = await fetch('/api/auth/login', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Login failed');
            }

            const data = await response.json();
            
            // Get user info
            const userResponse = await fetch('/api/auth/me', {
                headers: {
                    'Authorization': `Bearer ${data.access_token}`
                }
            });

            if (!userResponse.ok) {
                throw new Error('Failed to get user info');
            }

            const userData = await userResponse.json();

            // Update stores and localStorage
            token.set(data.access_token);
            user.set(userData);
            isAuthenticated.set(true);

            if (browser) {
                localStorage.setItem('resumeforge_token', data.access_token);
                localStorage.setItem('resumeforge_user', JSON.stringify(userData));
            }

            return { success: true };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    async register(email, password) {
        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Registration failed');
            }

            // Auto-login after registration
            return await this.login(email, password);
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    logout() {
        token.set(null);
        user.set(null);
        isAuthenticated.set(false);
        
        if (browser) {
            localStorage.removeItem('resumeforge_token');
            localStorage.removeItem('resumeforge_user');
        }
    },

    async checkAuth() {
        const currentToken = getTokenValue();
        if (!currentToken) return false;

        try {
            const response = await fetch('/api/auth/me', {
                headers: {
                    'Authorization': `Bearer ${currentToken}`
                }
            });

            if (response.ok) {
                const userData = await response.json();
                user.set(userData);
                isAuthenticated.set(true);
                return true;
            } else {
                this.logout();
                return false;
            }
        } catch (error) {
            this.logout();
            return false;
        }
    }
};

// Helper to get current token value
export function getTokenValue() {
    let currentToken;
    token.subscribe(value => currentToken = value)();
    return currentToken;
}

// Helper to make authenticated requests
export async function authenticatedFetch(url, options = {}) {
    const currentToken = getTokenValue();
    
    if (!currentToken) {
        throw new Error('No authentication token');
    }

    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${currentToken}`,
        ...options.headers
    };

    const response = await fetch(url, {
        ...options,
        headers
    });

    if (response.status === 401) {
        // Token expired or invalid
        authService.logout();
        throw new Error('Authentication expired');
    }

    return response;
}