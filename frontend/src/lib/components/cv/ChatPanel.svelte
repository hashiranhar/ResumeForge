<script>
    import { onMount, afterUpdate } from 'svelte';
    import { marked } from 'marked';
    import DOMPurify from 'dompurify';
    import { chatHistory, isLLMLoading, llmService } from '$lib/stores/llm.js';
    import { currentCV, draftCV } from '$lib/stores/cv.js';
    import { addToast } from '$lib/stores/toast.js';
    import { MessageSquare, Send, Bot, User, Lightbulb } from 'lucide-svelte';
    import Button from '$lib/components/common/Button.svelte';

    let messageInput = '';
    let chatContainer;
    let isTyping = false;

    // Configure marked for better formatting
    marked.setOptions({
        breaks: true,
        gfm: true
    });

    // Auto-scroll to bottom when new messages arrive
    afterUpdate(() => {
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    });

    onMount(() => {
        // Clear chat history when component mounts
        llmService.clearChat();
        
        // Add welcome message
        llmService.addToChatHistory('assistant', 'Hi! I\'m ForgeBot, your AI CV assistant. I can help you improve your CV content, suggest better phrasing, or answer questions about your resume. How can I help you today?');
    });

    async function sendMessage() {
        if (!messageInput.trim() || $isLLMLoading) return;

        const message = messageInput.trim();
        messageInput = '';

        try {
            const result = await llmService.chatAboutCV(
                message,
                $currentCV?.id,
                $draftCV.markdown_content
            );

            if (!result.success) {
                addToast(result.error || 'Failed to send message', 'error');
            }
        } catch (error) {
            addToast('Failed to send message', 'error');
        }
    }

    function handleKeyPress(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    }

    function handleSuggestionClick(suggestion) {
        messageInput = suggestion;
        sendMessage();
    }

    // Function to render markdown content safely
    function renderMarkdown(content) {
        try {
            const html = marked(content);
            return DOMPurify.sanitize(html);
        } catch (error) {
            console.error('Markdown rendering error:', error);
            return content; // Fallback to plain text
        }
    }

    // Quick action buttons
    const quickActions = [
        'How can I improve my professional summary?',
        'Make my experience section more impactful',
        'Suggest better action verbs for my achievements',
        'How can I quantify my accomplishments?',
        'Review my skills section',
        'Help me write a cover letter introduction'
    ];
</script>

<!-- FIXED: Added dark mode styling to entire component -->
<div class="flex flex-col h-full bg-white dark:bg-gray-900">
    <!-- Chat Header - FIXED: Added dark mode styling -->
    <div class="border-b border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-900">
        <div class="flex items-center space-x-2">
            <MessageSquare class="h-4 w-4 text-gray-500 dark:text-gray-400" />
            <h3 class="font-medium text-gray-900 dark:text-white">ForgeBot - AI CV Assistant</h3>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-300 mt-1">
            Get personalized advice and improvements for your CV
        </p>
    </div>

    <!-- Chat Messages - FIXED: Added dark mode styling -->
    <div 
        class="flex-1 overflow-y-auto p-4 space-y-4 bg-white dark:bg-gray-900"
        bind:this={chatContainer}
    >
        {#if $chatHistory.length === 0}
            <!-- Welcome state - FIXED: Added dark mode styling -->
            <div class="text-center py-8">
                <Bot class="h-12 w-12 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
                <p class="text-gray-600 dark:text-gray-300">Start a conversation with ForgeBot</p>
            </div>
        {:else}
            {#each $chatHistory as message}
                <div class="flex {message.role === 'user' ? 'justify-end' : 'justify-start'}">
                    <div class="flex items-start space-x-2 max-w-xs lg:max-w-md">
                        {#if message.role === 'assistant'}
                            <!-- AI avatar - FIXED: Added dark mode styling -->
                            <div class="flex-shrink-0 w-6 h-6 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center">
                                <Bot class="h-4 w-4 text-primary-600 dark:text-primary-400" />
                            </div>
                        {/if}
                        
                        <!-- Message bubble - FIXED: Added markdown rendering and better styling -->
                        <div class="px-3 py-2 rounded-lg {message.role === 'user' 
                            ? 'bg-primary-600 dark:bg-primary-700 text-white' 
                            : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white'}">
                            {#if message.role === 'assistant'}
                                <!-- Render markdown for assistant messages -->
                                <div class="text-sm prose prose-sm dark:prose-invert max-w-none
                                    prose-headings:text-gray-900 dark:prose-headings:text-white
                                    prose-strong:text-gray-900 dark:prose-strong:text-white
                                    prose-code:text-gray-900 dark:prose-code:text-white
                                    prose-code:bg-gray-200 dark:prose-code:bg-gray-700
                                    prose-pre:bg-gray-200 dark:prose-pre:bg-gray-700
                                    prose-blockquote:text-gray-700 dark:prose-blockquote:text-gray-300
                                    prose-li:text-gray-900 dark:prose-li:text-white">
                                    {@html renderMarkdown(message.content)}
                                </div>
                            {:else}
                                <!-- Plain text for user messages -->
                                <p class="text-sm whitespace-pre-wrap">{message.content}</p>
                            {/if}
                        </div>
                        
                        {#if message.role === 'user'}
                            <!-- User avatar - FIXED: Added dark mode styling -->
                            <div class="flex-shrink-0 w-6 h-6 bg-gray-600 dark:bg-gray-500 rounded-full flex items-center justify-center">
                                <User class="h-4 w-4 text-white" />
                            </div>
                        {/if}
                    </div>
                </div>
            {/each}
        {/if}

        <!-- Loading indicator - FIXED: Added dark mode styling -->
        {#if $isLLMLoading}
            <div class="flex justify-start">
                <div class="flex items-start space-x-2">
                    <div class="flex-shrink-0 w-6 h-6 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center">
                        <Bot class="h-4 w-4 text-primary-600 dark:text-primary-400" />
                    </div>
                    <div class="bg-gray-100 dark:bg-gray-800 rounded-lg px-3 py-2">
                        <div class="flex space-x-1">
                            <div class="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce"></div>
                            <div class="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                            <div class="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    </div>

    <!-- Quick Actions - FIXED: Added dark mode styling -->
    {#if $chatHistory.length <= 1}
        <div class="border-t border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-900">
            <div class="flex items-center space-x-2 mb-3">
                <Lightbulb class="h-4 w-4 text-yellow-500 dark:text-yellow-400" />
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Quick suggestions:</span>
            </div>
            <div class="space-y-2">
                {#each quickActions.slice(0, 3) as action}
                    <button
                        class="w-full text-left p-2 text-sm bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-900 dark:text-white rounded-lg transition-colors"
                        on:click={() => handleSuggestionClick(action)}
                    >
                        {action}
                    </button>
                {/each}
            </div>
        </div>
    {/if}

    <!-- Message Input - FIXED: Added dark mode styling -->
    <div class="border-t border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-900">
        <div class="flex space-x-2">
            <div class="flex-1">
                <textarea
                    bind:value={messageInput}
                    on:keypress={handleKeyPress}
                    placeholder="Ask ForgeBot anything about your CV..."
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 rounded-lg resize-none focus:ring-2 focus:ring-primary-500 dark:focus:ring-primary-400 focus:border-primary-500 dark:focus:border-primary-400"
                    rows="2"
                    disabled={$isLLMLoading}
                />
            </div>
            <Button
                size="sm"
                on:click={sendMessage}
                disabled={!messageInput.trim() || $isLLMLoading}
                loading={$isLLMLoading}
            >
                <Send class="h-4 w-4" />
            </Button>
        </div>
        <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">
            Press Enter to send, Shift+Enter for new line
        </p>
    </div>
</div>

<style>
    /* Custom styles for better markdown rendering in chat */
    :global(.prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6) {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
        line-height: 1.3 !important;
    }
    
    :global(.prose p) {
        margin-top: 0.25rem !important;
        margin-bottom: 0.25rem !important;
    }
    
    :global(.prose ul, .prose ol) {
        margin-top: 0.25rem !important;
        margin-bottom: 0.25rem !important;
    }
    
    :global(.prose li) {
        margin-top: 0.1rem !important;
        margin-bottom: 0.1rem !important;
    }

    :global(.prose strong) {
        font-weight: 600 !important;
    }

    :global(.prose code) {
        padding: 0.125rem 0.25rem !important;
        border-radius: 0.25rem !important;
        font-size: 0.875rem !important;
    }

    :global(.prose blockquote) {
        border-left: 3px solid #e5e7eb !important;
        padding-left: 0.75rem !important;
        font-style: italic !important;
        margin: 0.5rem 0 !important;
    }

    :global(.dark .prose blockquote) {
        border-left-color: #4b5563 !important;
    }
</style>