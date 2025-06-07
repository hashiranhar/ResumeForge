<script>
    import { onMount } from 'svelte';
    import { currentCV, draftCV, hasUnsavedChanges, cvService } from '$lib/stores/cv.js';
    import { addToast } from '$lib/stores/toast.js';
    import { Save, Download, Settings, MessageSquare, Edit3, Zap, Wand2 } from 'lucide-svelte';
    import Button from '$lib/components/common/Button.svelte';
    import MarkdownEditor from './MarkdownEditor.svelte';
    import PDFPreview from './PDFPreview.svelte';
    import SettingsPanel from './SettingsPanel.svelte';
    import ChatPanel from './ChatPanel.svelte';
    import ATSPanel from './ATSPanel.svelte';
    import InlineEditPanel from './InlineEditPanel.svelte';

    export let isDemo = false;
    export let onSave = () => {};
    export let saving = false;

    let activeTab = 'editor'; // 'editor', 'chat', 'inline-edit', 'ats'
    let showSettings = false;
    let leftPanelWidth = 50; // Percentage
    let isDragging = false;
    let splitContainer;
    let resizeHandle; // Added missing variable declaration

    // Resize functionality
    function handleMouseDown(event) {
        isDragging = true;
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);
        event.preventDefault();
    }

    function handleMouseMove(event) {
        if (!isDragging) return;
        
        if (!splitContainer) return;
        
        const rect = splitContainer.getBoundingClientRect();
        const newWidth = ((event.clientX - rect.left) / rect.width) * 100;
        
        // Constrain width between 20% and 80%
        leftPanelWidth = Math.min(Math.max(newWidth, 20), 80);
    }

    function handleMouseUp() {
        isDragging = false;
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
    }

    function handleKeydown(event) {
        const step = 5; // 5% steps
        
        switch (event.key) {
            case 'ArrowLeft':
                event.preventDefault();
                leftPanelWidth = Math.max(leftPanelWidth - step, 20);
                break;
            case 'ArrowRight':
                event.preventDefault();
                leftPanelWidth = Math.min(leftPanelWidth + step, 80);
                break;
            case 'Home':
                event.preventDefault();
                leftPanelWidth = 20;
                break;
            case 'End':
                event.preventDefault();
                leftPanelWidth = 80;
                break;
        }
    }

    // Auto-save functionality
    let saveTimeout;
    
    $: if ($hasUnsavedChanges && !isDemo) {
        clearTimeout(saveTimeout);
        saveTimeout = setTimeout(() => {
            handleAutoSave();
        }, 2000); // Auto-save after 2 seconds of inactivity
    }

    async function handleAutoSave() {
        if (!$hasUnsavedChanges || isDemo || saving) return;
        
        try {
            await onSave();
        } catch (error) {
            console.error('Auto-save failed:', error);
        }
    }

    // Keyboard shortcuts
    function handleKeyPress(event) {
        // Ctrl/Cmd + S to save
        if ((event.ctrlKey || event.metaKey) && event.key === 's') {
            event.preventDefault();
            if (!saving && ($hasUnsavedChanges || isDemo)) {
                onSave();
            }
        }
        
        // Ctrl/Cmd + Shift + P for PDF preview
        if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key === 'P') {
            event.preventDefault();
            // Focus on PDF preview or trigger download
        }
    }

    // Tab switching with keyboard shortcuts
    function handleTabSwitch(event) {
        if (event.ctrlKey || event.metaKey) {
            switch (event.key) {
                case '1':
                    event.preventDefault();
                    activeTab = 'editor';
                    break;
                case '2':
                    event.preventDefault();
                    activeTab = 'inline-edit';
                    break;
                case '3':
                    event.preventDefault();
                    activeTab = 'chat';
                    break;
                case '4':
                    event.preventDefault();
                    activeTab = 'ats';
                    break;
            }
        }
    }

    // Cleanup on component destroy
    onMount(() => {
        return () => {
            clearTimeout(saveTimeout);
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
        };
    });
</script>

<svelte:window on:keydown={handleKeyPress} on:keydown={handleTabSwitch} />

<div class="flex flex-col h-screen bg-gray-50 dark:bg-black">
    <!-- Toolbar -->
    <div class="flex-shrink-0 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 px-4 py-3">
        <div class="flex items-center justify-between">
            <!-- Left: Tabs -->
            <div class="flex items-center space-x-1" role="tablist" aria-label="Editor sections">
                <button
                    class="px-3 py-2 rounded-lg text-sm font-medium transition-colors {activeTab === 'editor' 
                        ? 'bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300' 
                        : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800'}"
                    on:click={() => activeTab = 'editor'}
                    role="tab"
                    aria-selected={activeTab === 'editor'}
                    aria-controls="editor-panel"
                    title="Switch to Markdown editor (Ctrl+1)"
                >
                    <Edit3 class="h-4 w-4 mr-1 inline" />
                    Editor
                </button>
                
                <button
                    class="px-3 py-2 rounded-lg text-sm font-medium transition-colors {activeTab === 'inline-edit' 
                        ? 'bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300' 
                        : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800'}"
                    on:click={() => activeTab = 'inline-edit'}
                    role="tab"
                    aria-selected={activeTab === 'inline-edit'}
                    aria-controls="inline-edit-panel"
                    title="Switch to AI inline editor (Ctrl+2)"
                >
                    <Wand2 class="h-4 w-4 mr-1 inline" />
                    AI Edit
                </button>
                
                <button
                    class="px-3 py-2 rounded-lg text-sm font-medium transition-colors {activeTab === 'chat' 
                        ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300' 
                        : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800'}"
                    on:click={() => activeTab = 'chat'}
                    role="tab"
                    aria-selected={activeTab === 'chat'}
                    aria-controls="chat-panel"
                    title="Switch to AI chat assistant (Ctrl+3)"
                >
                    <MessageSquare class="h-4 w-4 mr-1 inline" />
                    AI Chat
                </button>
                
                <button
                    class="px-3 py-2 rounded-lg text-sm font-medium transition-colors {activeTab === 'ats' 
                        ? 'bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300' 
                        : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800'}"
                    on:click={() => activeTab = 'ats'}
                    role="tab"
                    aria-selected={activeTab === 'ats'}
                    aria-controls="ats-panel"
                    title="Switch to ATS score analysis (Ctrl+4)"
                >
                    <Zap class="h-4 w-4 mr-1 inline" />
                    ATS Score
                </button>
            </div>

            <!-- Right: Action buttons -->
            <div class="flex items-center space-x-2">
                <!-- Unsaved changes indicator -->
                {#if $hasUnsavedChanges && !isDemo}
                    <div class="flex items-center text-amber-600 dark:text-amber-400 text-sm">
                        <div class="w-2 h-2 bg-amber-500 rounded-full mr-2 animate-pulse"></div>
                        Unsaved changes
                    </div>
                {/if}

                <Button
                    variant="outline"
                    size="sm"
                    on:click={() => showSettings = true}
                    title="Open settings panel"
                >
                    <Settings class="h-4 w-4 mr-1" />
                    Settings
                </Button>
                
                <Button
                    size="sm"
                    on:click={onSave}
                    loading={saving}
                    disabled={saving || (!$hasUnsavedChanges && !isDemo)}
                    title={isDemo ? 'Save your CV' : saving ? 'Saving...' : 'Save changes (Ctrl+S)'}
                >
                    <Save class="h-4 w-4 mr-1" />
                    {isDemo ? 'Save CV' : saving ? 'Saving...' : 'Save'}
                </Button>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex overflow-hidden" bind:this={splitContainer}>
        <!-- Left Panel -->
        <div 
            class="bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 flex flex-col"
            style="width: {leftPanelWidth}%"
        >
            {#if activeTab === 'editor'}
                <div id="editor-panel" role="tabpanel" aria-labelledby="editor-tab" class="h-full">
                    <MarkdownEditor />
                </div>
            {:else if activeTab === 'inline-edit'}
                <div id="inline-edit-panel" role="tabpanel" aria-labelledby="inline-edit-tab" class="h-full">
                    <InlineEditPanel />
                </div>
            {:else if activeTab === 'chat'}
                <div id="chat-panel" role="tabpanel" aria-labelledby="chat-tab" class="h-full">
                    <ChatPanel />
                </div>
            {:else if activeTab === 'ats'}
                <div id="ats-panel" role="tabpanel" aria-labelledby="ats-tab" class="h-full">
                    <ATSPanel />
                </div>
            {/if}
        </div>

        <!-- Resize Handle -->
        <button
            type="button"
            class="w-1 bg-gray-200 dark:bg-gray-700 hover:bg-blue-300 dark:hover:bg-blue-600 cursor-col-resize transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-blue-300"
            aria-label="Resize panels. Use arrow keys to adjust width. Current: {Math.round(leftPanelWidth)}%"
            on:mousedown={handleMouseDown}
            on:keydown={handleKeydown}
            title="Drag to resize panels or use arrow keys"
        >
            <span class="sr-only">
                Panel resizer. Current width: {Math.round(leftPanelWidth)}%. Use left/right arrows to adjust.
            </span>
        </button>

        <!-- Right Panel - PDF Preview -->
        <div 
            class="bg-gray-100 dark:bg-gray-800 flex flex-col"
            style="width: {100 - leftPanelWidth}%"
            aria-label="PDF Preview"
        >
            <PDFPreview />
        </div>
    </div>
</div>

<!-- Settings Modal -->
{#if showSettings}
    <SettingsPanel bind:open={showSettings} />
{/if}

<style>
    /* Custom scrollbar styling for better dark mode support */
    :global(.dark) :global(::-webkit-scrollbar) {
        width: 8px;
        height: 8px;
    }

    :global(.dark) :global(::-webkit-scrollbar-track) {
        background: #374151;
    }

    :global(.dark) :global(::-webkit-scrollbar-thumb) {
        background: #6b7280;
        border-radius: 4px;
    }

    :global(.dark) :global(::-webkit-scrollbar-thumb:hover) {
        background: #9ca3af;
    }

    /* Dragging state */
    :global(.dragging) {
        user-select: none;
        cursor: col-resize !important;
    }

    /* Tab focus styles */
    button[role="tab"]:focus {
        outline: 2px solid rgb(59 130 246); /* Blue-500 equivalent */
        outline-offset: 2px;
    }

    /* Or use CSS custom properties if you have them defined */
    button[role="tab"]:focus {
        outline: 2px solid var(--color-primary-500, #3b82f6);
        outline-offset: 2px;
    }
</style>