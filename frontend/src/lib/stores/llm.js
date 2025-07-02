import { writable, get } from 'svelte/store';
import { authenticatedFetch } from './auth.js';

// LLM state
export const chatHistory = writable([]);
export const isLLMLoading = writable(false);
export const llmError = writable(null);
export const atsAnalysis = writable(null);
export const inlineEditHistory = writable([]);
export const isInlineEditing = writable(false);

// LLM service functions
export const llmService = {
    // Function 1: Chat with LLM about CV
    async chatAboutCV(message, cvId = null, cvContent = null) {
        isLLMLoading.set(true);
        llmError.set(null);
        
        try {
            // Get current chat history (exclude timestamps for API)
            let currentHistory;
            chatHistory.subscribe(value => {
                currentHistory = value.map(msg => ({
                    role: msg.role,
                    content: msg.content
                }));
            })();
            
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
    async inlineEdit(cvId, instruction, section = null) {
        isInlineEditing.set(true);
        llmError.set(null);
        
        try {
            // Import draftCV from cv store to get current content
            const { draftCV } = await import('./cv.js');
            const currentContent = get(draftCV).markdown_content;
            
            const response = await authenticatedFetch('/api/llm/inline-edit', {
                method: 'POST',
                body: JSON.stringify({
                    cv_id: cvId,
                    instruction,
                    section,
                    auto_save: false // Always false - no auto-save
                })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Inline edit failed');
            }
            
            const data = await response.json();
            
            // Add to inline edit history with previous content
            inlineEditHistory.update(history => [
                ...history,
                {
                    id: Date.now().toString(),
                    timestamp: new Date().toISOString(),
                    instruction,
                    section,
                    changesMade: data.changes_made || [],
                    previousContent: currentContent
                }
            ]);
            
            return {
                success: true,
                editedContent: data.edited_content,
                changesMade: data.changes_made || []
            };
        } catch (err) {
            llmError.set(err.message);
            return { success: false, error: err.message };
        } finally {
            isInlineEditing.set(false);
        }
    },

    // Undo inline edit with cascading logic
    async undoInlineEdit(editId) {
        try {
            // Import draftCV from cv store
            const { draftCV } = await import('./cv.js');
            
            const history = get(inlineEditHistory);
            const editIndex = history.findIndex(edit => edit.id === editId);
            
            if (editIndex === -1) {
                return { success: false, error: 'Edit not found' };
            }
            
            const editToUndo = history[editIndex];
            
            // Count how many edits will be undone (the selected edit + all newer ones)
            const editsToUndo = history.length - editIndex;
            
            // Update draft CV with the content from before the selected edit
            draftCV.update(draft => ({
                ...draft,
                markdown_content: editToUndo.previousContent
            }));
            
            // Remove the selected edit and all edits that came after it
            inlineEditHistory.update(history => 
                history.slice(0, editIndex)
            );
            
            return { 
                success: true, 
                undoneCount: editsToUndo 
            };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    // Function 3: ATS Score Analysis
    async analyzeATS(cvId, cvContent, targetRole, jobDescription) {
        isLLMLoading.set(true);
        llmError.set(null);
        
        try {
            console.log('Starting ATS analysis...', { cvId, hasContent: !!cvContent, targetRole, hasJobDescription: !!jobDescription });
            
            const response = await authenticatedFetch('/api/llm/ats-score', {
                method: 'POST',
                body: JSON.stringify({
                    cv_id: cvId,
                    cv_content: cvContent,
                    target_role: targetRole,
                    job_description: jobDescription
                })
            });
            
            console.log('ATS API response status:', response.status);
            
            if (!response.ok) {
                const errorData = await response.json();
                console.error('ATS API error:', errorData);
                throw new Error(errorData.detail || 'ATS analysis failed');
            }
            
            const data = await response.json();
            console.log('ATS API response data:', data);
            
            // FIXED: Set the ATS analysis data directly from the response
            // The backend returns the analysis data directly, not nested under 'analysis'
            const analysisData = {
                ats_score: data.ats_score,
                score_breakdown: data.score_breakdown,
                strengths: data.strengths,
                weaknesses: data.weaknesses,
                upgrade_suggestions: data.upgrade_suggestions,
                keyword_analysis: data.keyword_analysis
            };
            
            console.log('Setting ATS analysis data:', analysisData);
            atsAnalysis.set(analysisData);
            
            return { success: true, analysis: analysisData };
        } catch (err) {
            console.error('ATS analysis error:', err);
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

    // Clear inline edit history
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