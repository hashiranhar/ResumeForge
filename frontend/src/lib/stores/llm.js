import { writable } from 'svelte/store';
import { authenticatedFetch } from './auth.js';

// LLM state
export const chatHistory = writable([]);
export const isLLMLoading = writable(false);
export const llmError = writable(null);
export const atsAnalysis = writable(null);

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

    // Function 2: Inline edit CV content
    async inlineEdit(cvId, instruction, section = null, autoSave = true) {
        isLLMLoading.set(true);
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
            isLLMLoading.set(false);
        }
    },

    // Function 3: ATS Score Analysis
    async analyzeATS(cvId, cvContent, targetRole, jobDescription) {
        isLLMLoading.set(true);
        llmError.set(null);
        
        try {
            // Prepare the payload with proper null handling
            const payload = {
                cv_id: cvId || null,
                cv_content: cvContent || null,
                target_role: targetRole && targetRole.trim() ? targetRole.trim() : null,
                job_description: jobDescription && jobDescription.trim() ? jobDescription.trim() : null
            };

            const response = await authenticatedFetch('/api/llm/ats-score', {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'ATS analysis failed');
            }
            
            const data = await response.json();
            
            // Store the analysis result
            atsAnalysis.set(data);
            
            return {
                success: true,
                atsScore: data.ats_score,
                scoreBreakdown: data.score_breakdown,
                strengths: data.strengths,
                weaknesses: data.weaknesses,
                upgradeSuggestions: data.upgrade_suggestions,
                keywordAnalysis: data.keyword_analysis
            };
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

    // Add message to chat history manually
    addToChatHistory(role, content) {
        chatHistory.update(history => [
            ...history,
            { role, content }
        ]);
    }
};