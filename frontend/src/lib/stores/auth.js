import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Auth stores
export const isAuthenticated = writable(false);
export const user = writable(null);
export const token = writable(null);

// Initialize auth state from localStorage
if (browser) {
    const storedToken = localStorage.getItem('resumeforge_token');
    const storedUser = localStorage.getItem('resumeforge_user');
    
    if (storedToken && storedUser) {
        try {
            token.set(storedToken);
            user.set(JSON.parse(storedUser));
            isAuthenticated.set(true);
        } catch (error) {
            // Clear invalid stored data
            localStorage.removeItem('resumeforge_token');
            localStorage.removeItem('resumeforge_user');
        }
    }
}

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
                if (response.status === 403) {
                    // Email not verified
                    return { 
                        success: false, 
                        error: error.detail,
                        requiresVerification: true,
                        email: email
                    };
                }
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

            // Registration successful - user needs to verify email
            return { 
                success: true, 
                message: 'Registration successful. Please verify your email.',
                requiresVerification: true,
                email: email
            };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    async verifyEmail(email, verificationCode) {
        try {
            const response = await fetch('/api/auth/verify-email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    email, 
                    verification_code: verificationCode 
                })
            });

            const data = await response.json();

            if (!response.ok) {
                return { 
                    success: false, 
                    error: data.error || 'Verification failed' 
                };
            }

            return { success: true, message: data.message };
        } catch (error) {
            return { success: false, error: 'Verification failed' };
        }
    },

    async resendVerificationCode(email) {
        try {
            const response = await fetch('/api/auth/resend-verification', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email })
            });

            const data = await response.json();

            if (!response.ok) {
                return { 
                    success: false, 
                    error: data.error || 'Failed to resend verification code' 
                };
            }

            return { success: true, message: data.message };
        } catch (error) {
            return { success: false, error: 'Failed to resend verification code' };
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

    async refreshUserData() {
        try {
            const currentToken = browser ? localStorage.getItem('resumeforge_token') : null;
            if (!currentToken) {
                return { success: false, error: 'No token found' };
            }

            const response = await fetch('/api/auth/me', {
                headers: {
                    'Authorization': `Bearer ${currentToken}`
                }
            });

            if (!response.ok) {
                // Token might be invalid, logout user
                this.logout();
                return { success: false, error: 'Session expired' };
            }

            const userData = await response.json();
            
            user.set(userData);
            if (browser) {
                localStorage.setItem('resumeforge_user', JSON.stringify(userData));
            }

            return { success: true, user: userData };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
};

// Authenticated fetch helper
export async function authenticatedFetch(url, options = {}) {
    let currentToken;
    
    // Get current token value
    token.subscribe(value => {
        currentToken = value;
    })();
    
    // If no token and we're in browser, try to get from localStorage
    if (!currentToken && browser) {
        currentToken = localStorage.getItem('resumeforge_token');
    }
    
    if (!currentToken) {
        throw new Error('No authentication token available');
    }
    
    // Add authorization header
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${currentToken}`,
        ...options.headers
    };
    
    const response = await fetch(url, {
        ...options,
        headers
    });
    
    // If unauthorized, clear auth state and redirect to login
    if (response.status === 401) {
        authService.logout();
        if (browser) {
            window.location.href = '/auth/login';
        }
        throw new Error('Authentication failed');
    }
    
    return response;
}