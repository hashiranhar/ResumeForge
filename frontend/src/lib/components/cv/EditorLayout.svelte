<script>
    import { onMount } from 'svelte';
    import { currentCV, draftCV, hasUnsavedChanges, cvService } from '$lib/stores/cv.js';
    import { addToast } from '$lib/stores/toast.js';
    import { Save, Download, Settings, MessageSquare, Edit3, Zap, Wand2, X, FileText } from 'lucide-svelte';
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

    let activeTab = 'editor';
    let showSettings = false;
    let leftPanelWidth = 50;
    let isDragging = false;
    let splitContainer;
    let settingsPanelWidth = 320;
    let downloadingPDF = false;
    let downloadingMarkdown = false;

    // Calculate main content width when settings panel is open
    $: mainContentWidth = showSettings ? `calc(100% - ${settingsPanelWidth}px)` : '100%';

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
        const step = 5;
        
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

    // Manual save function
    async function handleManualSave() {
        if (saving) return;
        
        try {
            await onSave();
            addToast('CV saved successfully!', 'success');
        } catch (error) {
            addToast('Failed to save CV', 'error');
        }
    }

    // Download functionality
    async function handleDownloadPDF() {
        if (!$currentCV) {
            addToast('Please save your CV first', 'info');
            return;
        }

        downloadingPDF = true;
        try {
            const result = await cvService.downloadPDF($currentCV.id, `${$currentCV.name}.pdf`);
            if (result.success) {
                addToast('PDF downloaded successfully', 'success');
            } else {
                addToast(result.error || 'Failed to download PDF', 'error');
            }
        } catch (error) {
            addToast('Failed to download PDF', 'error');
        } finally {
            downloadingPDF = false;
        }
    }

    async function handleDownloadMarkdown() {
        if (!$currentCV) {
            addToast('Please save your CV first', 'info');
            return;
        }

        downloadingMarkdown = true;
        try {
            const result = await cvService.downloadMarkdown($currentCV.id, `${$currentCV.name}.md`);
            if (result.success) {
                addToast('Markdown downloaded successfully', 'success');
            } else {
                addToast(result.error || 'Failed to download Markdown', 'error');
            }
        } catch (error) {
            addToast('Failed to download Markdown', 'error');
        } finally {
            downloadingMarkdown = false;
        }
    }

    // Keyboard shortcuts
    function handleKeyPress(event) {
        // Ctrl/Cmd + S to save
        if ((event.ctrlKey || event.metaKey) && event.key === 's') {
            event.preventDefault();
            if (!saving && ($hasUnsavedChanges || isDemo)) {
                handleManualSave();
            }
        }
        
        // Ctrl/Cmd + Shift + P for PDF download
        if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key === 'P') {
            event.preventDefault();
            handleDownloadPDF();
        }
        
        // Ctrl/Cmd + Shift + M for Markdown download
        if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key === 'M') {
            event.preventDefault();
            handleDownloadMarkdown();
        }
        
        // ESC to close settings panel
        if (event.key === 'Escape' && showSettings) {
            event.preventDefault();
            closeSettings();
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

    // Settings panel functions
    function openSettings() {
        showSettings = true;
    }

    function closeSettings() {
        showSettings = false;
    }

    // Cleanup on component destroy
    onMount(() => {
        return () => {
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
        };
    });
</script>

<svelte:window on:keydown={handleKeyPress} on:keydown={handleTabSwitch} />

<div class="flex h-screen bg-gray-50 dark:bg-black">
    <!-- Main Editor Area -->
    <div class="flex flex-col transition-all duration-300 ease-in-out" style="width: {mainContentWidth}">
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

                    <!-- Download buttons -->
                    {#if $currentCV && !isDemo}
                        <div class="flex items-center space-x-1">
                            <!-- Download PDF -->
                            <Button
                                variant="outline"
                                size="sm"
                                on:click={handleDownloadPDF}
                                loading={downloadingPDF}
                                disabled={downloadingPDF || downloadingMarkdown}
                                title="Download as PDF (Ctrl+Shift+P)"
                            >
                                <Download class="h-4 w-4 mr-1" />
                                PDF
                            </Button>

                            <!-- Download Markdown -->
                            <Button
                                variant="outline"
                                size="sm"
                                on:click={handleDownloadMarkdown}
                                loading={downloadingMarkdown}
                                disabled={downloadingPDF || downloadingMarkdown}
                                title="Download as Markdown (Ctrl+Shift+M)"
                            >
                                <FileText class="h-4 w-4 mr-1" />
                                Markdown
                            </Button>
                        </div>
                    {/if}

                    <!-- Settings button -->
                    <Button
                        variant={showSettings ? "default" : "outline"}
                        size="sm"
                        on:click={showSettings ? closeSettings : openSettings}
                        title={showSettings ? "Close settings panel (Esc)" : "Open settings panel"}
                        disabled={saving}
                        className={showSettings ? "bg-primary-600 text-white" : ""}
                    >
                        <Settings class="h-4 w-4 mr-1" />
                        Settings
                    </Button>
                    
                    <!-- Manual save button only -->
                    <Button
                        size="sm"
                        on:click={handleManualSave}
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
                class="bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 flex flex-col transition-all duration-300"
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
                class="w-1 bg-gray-200 dark:bg-gray-700 hover:bg-blue-300 dark:hover:bg-blue-600 cursor-col-resize transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-blue-300 dark:focus:bg-blue-600"
                aria-label="Resize panels. Current width: {Math.round(leftPanelWidth)}%. Use arrow keys to adjust."
                on:mousedown={handleMouseDown}
                on:keydown={handleKeydown}
                title="Drag to resize or use arrow keys"
            >
                <span class="sr-only">
                    Panel resizer. Left panel: {Math.round(leftPanelWidth)}%, Right panel: {Math.round(100 - leftPanelWidth)}%
                </span>
            </button>

            <!-- Right Panel - PDF Preview -->
            <div 
                class="bg-gray-100 dark:bg-gray-800 flex flex-col transition-all duration-300"
                style="width: {100 - leftPanelWidth}%"
            >
                <PDFPreview />
            </div>
        </div>
    </div>

    <!-- Settings Side Panel -->
    <div class="relative">
        <!-- Settings Panel -->
        <div 
            class="fixed top-0 right-0 h-full bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700 shadow-xl transform transition-transform duration-300 ease-in-out z-40 {showSettings ? 'translate-x-0' : 'translate-x-full'}"
            style="width: {settingsPanelWidth}px"
            role="complementary"
            aria-label="Settings panel"
        >
            <!-- Settings Header -->
            <div class="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
                <h2 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                    <Settings class="h-5 w-5 mr-2 text-gray-500 dark:text-gray-400" />
                    CV Settings
                </h2>
                <button
                    type="button"
                    class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors"
                    on:click={closeSettings}
                    aria-label="Close settings panel"
                    title="Close settings (Esc)"
                >
                    <X class="h-5 w-5" />
                </button>
            </div>

            <!-- Settings Content -->
            <div class="flex-1 overflow-y-auto">
                <SettingsPanel {closeSettings} />
            </div>

            <!-- Settings Footer -->
            <div class="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
                <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
                    <div class="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
                    Changes are applied in real-time
                </div>
            </div>
        </div>

        <!-- Backdrop for mobile/smaller screens -->
        {#if showSettings}
            <div 
                class="fixed inset-0 bg-black bg-opacity-25 z-30 md:hidden"
                on:click={closeSettings}
                aria-hidden="true"
            ></div>
        {/if}
    </div>
</div>

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
        outline: 2px solid rgb(59 130 246);
        outline-offset: 2px;
    }

    /* Smooth transitions for panel resizing */
    .transition-all {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Ensure the settings panel stays above other content */
    .z-40 {
        z-index: 40;
    }
    
    .z-30 {
        z-index: 30;
    }
</style>