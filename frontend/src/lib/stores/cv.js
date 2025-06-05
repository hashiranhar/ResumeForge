import { writable, derived } from 'svelte/store';
import { authenticatedFetch } from './auth.js';

// CV stores
export const cvs = writable([]);
export const currentCV = writable(null);
export const templates = writable([]);
export const isLoading = writable(false);
export const error = writable(null);

// Draft CV for non-authenticated users
export const draftCV = writable({
    name: 'My CV',
    markdown_content: '',
    settings: {
        font: 'Arial',
        fontSize: 11,
        margins: { top: 20, bottom: 20, left: 15, right: 15 },
        theme: 'professional'
    }
});

// Derived store to check if current CV has unsaved changes
export const hasUnsavedChanges = derived(
    [currentCV, draftCV],
    ([current, draft]) => {
        if (!current) return false;
        return current.markdown_content !== draft.markdown_content ||
               JSON.stringify(current.settings) !== JSON.stringify(draft.settings);
    }
);

// CV service functions
export const cvService = {
    // Load user's CVs
    async loadCVs() {
        isLoading.set(true);
        error.set(null);
        
        try {
            const response = await authenticatedFetch('/api/cvs/');
            if (!response.ok) {
                throw new Error('Failed to load CVs');
            }
            
            const data = await response.json();
            cvs.set(data);
            return { success: true, data };
        } catch (err) {
            error.set(err.message);
            return { success: false, error: err.message };
        } finally {
            isLoading.set(false);
        }
    },

    // Load a specific CV
    async loadCV(cvId) {
        isLoading.set(true);
        error.set(null);
        
        try {
            const response = await authenticatedFetch(`/api/cvs/${cvId}`);
            if (!response.ok) {
                throw new Error('Failed to load CV');
            }
            
            const data = await response.json();
            currentCV.set(data);
            draftCV.set({
                name: data.name,
                markdown_content: data.markdown_content || '',
                settings: data.settings || {
                    font: 'Arial',
                    fontSize: 11,
                    margins: { top: 20, bottom: 20, left: 15, right: 15 },
                    theme: 'professional'
                }
            });
            return { success: true, data };
        } catch (err) {
            error.set(err.message);
            return { success: false, error: err.message };
        } finally {
            isLoading.set(false);
        }
    },

    // Create new CV
    async createCV(name, content = '', settings = null, templateId = null) {
        isLoading.set(true);
        error.set(null);
        
        try {
            let response;
            
            if (templateId) {
                // Create from template
                response = await authenticatedFetch('/api/templates/create-cv', {
                    method: 'POST',
                    body: JSON.stringify({
                        template_id: templateId,
                        cv_name: name
                    })
                });
            } else {
                // Create blank CV
                response = await authenticatedFetch('/api/cvs/', {
                    method: 'POST',
                    body: JSON.stringify({
                        name,
                        markdown_content: content,
                        settings: settings || {
                            font: 'Arial',
                            fontSize: 11,
                            margins: { top: 20, bottom: 20, left: 15, right: 15 },
                            theme: 'professional'
                        }
                    })
                });
            }
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to create CV');
            }
            
            const data = await response.json();
            
            // Update stores
            cvs.update(list => [data, ...list]);
            currentCV.set(data);
            draftCV.set({
                name: data.name,
                markdown_content: data.markdown_content || '',
                settings: data.settings
            });
            
            return { success: true, data };
        } catch (err) {
            error.set(err.message);
            return { success: false, error: err.message };
        } finally {
            isLoading.set(false);
        }
    },

    // Update CV
    async updateCV(cvId, name, content, settings) {
        isLoading.set(true);
        error.set(null);
        
        try {
            const response = await authenticatedFetch(`/api/cvs/${cvId}`, {
                method: 'PUT',
                body: JSON.stringify({
                    name,
                    markdown_content: content,
                    settings
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to update CV');
            }
            
            const data = await response.json();
            
            // Update stores
            currentCV.set(data);
            cvs.update(list => list.map(cv => cv.id === cvId ? data : cv));
            
            return { success: true, data };
        } catch (err) {
            error.set(err.message);
            return { success: false, error: err.message };
        } finally {
            isLoading.set(false);
        }
    },

    // Delete CV
    async deleteCV(cvId) {
        isLoading.set(true);
        error.set(null);
        
        try {
            const response = await authenticatedFetch(`/api/cvs/${cvId}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error('Failed to delete CV');
            }
            
            // Update stores
            cvs.update(list => list.filter(cv => cv.id !== cvId));
            
            // Clear current CV if it was deleted
            currentCV.update(current => current?.id === cvId ? null : current);
            
            return { success: true };
        } catch (err) {
            error.set(err.message);
            return { success: false, error: err.message };
        } finally {
            isLoading.set(false);
        }
    },

    // Load templates
    async loadTemplates() {
        isLoading.set(true);
        error.set(null);
        
        try {
            const response = await fetch('/api/templates/');
            if (!response.ok) {
                throw new Error('Failed to load templates');
            }
            
            const data = await response.json();
            templates.set(data);
            return { success: true, data };
        } catch (err) {
            error.set(err.message);
            return { success: false, error: err.message };
        } finally {
            isLoading.set(false);
        }
    },

    // Download PDF
    async downloadPDF(cvId, filename) {
        try {
            const response = await authenticatedFetch(`/api/cvs/${cvId}/pdf`);
            if (!response.ok) {
                throw new Error('Failed to generate PDF');
            }
            
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename || 'cv.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            return { success: true };
        } catch (err) {
            return { success: false, error: err.message };
        }
    },

    // Download Markdown
    async downloadMarkdown(cvId, filename) {
        try {
            const response = await authenticatedFetch(`/api/cvs/${cvId}/markdown`);
            if (!response.ok) {
                throw new Error('Failed to download markdown');
            }
            
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename || 'cv.md';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            return { success: true };
        } catch (err) {
            return { success: false, error: err.message };
        }
    },

    // Auto-save functionality
    async autoSave(cvId, content, settings) {
        if (!cvId) return { success: false };
        
        try {
            const response = await authenticatedFetch(`/api/cvs/${cvId}`, {
                method: 'PUT',
                body: JSON.stringify({
                    markdown_content: content,
                    settings
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                currentCV.set(data);
                return { success: true };
            }
            return { success: false };
        } catch (err) {
            return { success: false, error: err.message };
        }
    },

    // Clear current CV (for new draft)
    clearCurrent() {
        currentCV.set(null);
        draftCV.set({
            name: 'My CV',
            markdown_content: '',
            settings: {
                font: 'Arial',
                fontSize: 11,
                margins: { top: 20, bottom: 20, left: 15, right: 15 },
                theme: 'professional'
            }
        });
    }
};