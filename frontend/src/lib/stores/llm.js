import { writable } from 'svelte/store';
import { authenticatedFetch } from './auth.js';

// LLM state
export const chatHistory = writable([]);
export const isLLMLoading = writable(false);
export const llmError = writable(null);
export const atsAnalysis = writable(null);
export const inlineEditHistory = writable([]); // NEW: Track inline edit history
export const isInlineEditing = writable(false); // NEW: Separate loading state for inline edits

// LLM service functions
export const llmService = {
    // Function 1: Chat with LLM about CV
    async chatAboutCV(message, cvId = null, cvContent = null) {
        isLLMLoading.set(true);
        llmError.set(null);
        
        try {
            // Get current chat history
            let currentHistory;
            chatHistory.subscribe(value => currentHistory = value)();
            
            const response = await authenticatedFetch('/api/llm/chat', {
                method: 'POST',
                body: JSON.stringify({
                    message,
                    cv_id: cvId,
                    cv_content: cvContent,
                    conversation_history: currentHistory
                })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Chat failed');
            }
            
            const data = await response.json();
            
            // Update chat history
            chatHistory.update(history => [
                ...history,
                { role: 'user', content: message },
                { role: 'assistant', content: data.reply }
            ]);
            
            return { 
                success: true, 
                reply: data.reply, 
                suggestions: data.suggestions || [] 
            };
        } catch (err) {
            llmError.set(err.message);
            return { success: false, error: err.message };
        } finally {
            isLLMLoading.set(false);
        }
    },

    // Function 2: Inline edit CV content - NEW IMPLEMENTATION
    async inlineEdit(cvId, instruction, section = null, autoSave = true) {
        isInlineEditing.set(true);
        llmError.set(null);
        
        try {
            const response = await authenticatedFetch('/api/llm/inline-edit', {
                method: 'POST',
                body: JSON.stringify({
                    cv_id: cvId,
                    instruction,
                    section,
                    auto_save: autoSave
                })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Inline edit failed');
            }
            
            const data = await response.json();
            
            // Add to inline edit history
            inlineEditHistory.update(history => [
                ...history,
                {
                    timestamp: new Date().toISOString(),
                    instruction,
                    section,
                    changesMade: data.changes_made || [],
                    autoSaved: data.auto_saved
                }
            ]);
            
            return {
                success: true,
                editedContent: data.edited_content,
                changesMade: data.changes_made || [],
                autoSaved: data.auto_saved
            };
        } catch (err) {
            llmError.set(err.message);
            return { success: false, error: err.message };
        } finally {
            isInlineEditing.set(false);
        }
    },

    // Function 3: ATS Score Analysis
    async analyzeATS(cvId, cvContent, targetRole, jobDescription) {
        isLLMLoading.set(true);
        llmError.set(null);
        
        try {
            const response = await authenticatedFetch('/api/llm/ats-analysis', {
                method: 'POST',
                body: JSON.stringify({
                    cv_id: cvId,
                    cv_content: cvContent,
                    target_role: targetRole,
                    job_description: jobDescription
                })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'ATS analysis failed');
            }
            
            const data = await response.json();
            
            // Update ATS analysis store
            atsAnalysis.set(data.analysis);
            
            return { success: true, analysis: data.analysis };
        } catch (err) {
            llmError.set(err.message);
            return { success: false, error: err.message };
        } finally {
            isLLMLoading.set(false);
        }
    },

    // Clear chat history
    clearChat() {
        chatHistory.set([]);
    },

    // Clear ATS analysis
    clearATS() {
        atsAnalysis.set(null);
    },

    // Clear inline edit history - NEW
    clearInlineEditHistory() {
        inlineEditHistory.set([]);
    },

    // Add message to chat history manually
    addToChatHistory(role, content) {
        chatHistory.update(history => [
            ...history,
            { role, content }
        ]);
    }
};