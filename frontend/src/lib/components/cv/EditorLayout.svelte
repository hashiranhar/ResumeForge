<script>
    import { onMount } from 'svelte';
    import { currentCV, draftCV, hasUnsavedChanges, cvService } from '$lib/stores/cv.js';
    import { addToast } from '$lib/stores/toast.js';
    import { Save, Download, Settings, MessageSquare, Edit3, Zap } from 'lucide-svelte';
    import Button from '$lib/components/common/Button.svelte';
    import MarkdownEditor from './MarkdownEditor.svelte';
    import PDFPreview from './PDFPreview.svelte';
    import SettingsPanel from './SettingsPanel.svelte';
    import ChatPanel from './ChatPanel.svelte';
    import ATSPanel from './ATSPanel.svelte';

    export let isDemo = false;
    export let onSave = () => {};
    export let saving = false;

    let activeTab = 'editor'; // 'editor', 'chat', 'ats'
    let showSettings = false;
    let leftPanelWidth = 50; // Percentage
    let isDragging = false;
    let splitContainer;

    onMount(() => {
        // Set up split pane resizing
        setupSplitPane();
    });

    function setupSplitPane() {
        if (!splitContainer) return;

        const handle = splitContainer.querySelector('.split-handle');
        if (!handle) return;

        let startX = 0;
        let startWidth = leftPanelWidth;

        function handleMouseDown(e) {
            isDragging = true;
            startX = e.clientX;
            startWidth = leftPanelWidth;
            document.addEventListener('mousemove', handleMouseMove);
            document.addEventListener('mouseup', handleMouseUp);
            e.preventDefault();
        }

        function handleMouseMove(e) {
            if (!isDragging) return;
            
            const deltaX = e.clientX - startX;
            const containerWidth = splitContainer.offsetWidth;
            const deltaPercent = (deltaX / containerWidth) * 100;
            
            leftPanelWidth = Math.min(Math.max(startWidth + deltaPercent, 30), 70);
        }

        function handleMouseUp() {
            isDragging = false;
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
        }

        handle.addEventListener('mousedown', handleMouseDown);
    }

    function handleDownloadPDF() {
        if ($currentCV) {
            // Download existing CV
            cvService.downloadPDF($currentCV.id, `${$currentCV.name}.pdf`);
        } else {
            // For demo or unsaved CV, we'd need to generate PDF from current content
            // This would require a different endpoint or approach
            addToast('Please save your CV first to download as PDF', 'info');
        }
    }

    function handleDownloadMarkdown() {
        // Create and download markdown file from current content
        const content = $draftCV.markdown_content || '';
        const blob = new Blob([content], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${$draftCV.name || 'cv'}.md`;
        document.body.appendChild(a);
        a.click();
        URL.revokeObjectURL(url);
        document.body.removeChild(a);
    }
</script>

<div class="flex flex-col h-full">
    <!-- Toolbar -->
    <div class="bg-white border-b border-gray-200 px-4 py-3">
        <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
                <!-- CV Title -->
                <h1 class="text-lg font-semibold text-gray-900">
                    {$draftCV.name || 'Untitled CV'}
                    {#if $hasUnsavedChanges && !isDemo}
                        <span class="text-orange-500 ml-2">•</span>
                    {/if}
                    {#if isDemo}
                        <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded ml-2">
                            DEMO
                        </span>
                    {/if}
                </h1>

                <!-- Save Status -->
                {#if !isDemo}
                    <span class="text-sm text-gray-500">
                        {#if saving}
                            Saving...
                        {:else if $hasUnsavedChanges}
                            Unsaved changes
                        {:else}
                            Saved
                        {/if}
                    </span>
                {/if}
            </div>

            <div class="flex items-center space-x-2">
                <!-- Download buttons -->
                <Button size="sm" variant="outline" on:click={handleDownloadMarkdown}>
                    <Download class="h-4 w-4 mr-1" />
                    .md
                </Button>
                
                <Button size="sm" variant="outline" on:click={handleDownloadPDF}>
                    <Download class="h-4 w-4 mr-1" />
                    PDF
                </Button>

                <!-- Settings -->
                <Button 
                    size="sm" 
                    variant="outline" 
                    on:click={() => showSettings = !showSettings}
                    class={showSettings ? 'bg-gray-100' : ''}
                >
                    <Settings class="h-4 w-4" />
                </Button>

                <!-- Save button -->
                <Button size="sm" on:click={onSave} loading={saving} disabled={saving}>
                    <Save class="h-4 w-4 mr-1" />
                    {isDemo ? 'Save' : 'Save'}
                </Button>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex overflow-hidden" bind:this={splitContainer}>
        <!-- Left Panel -->
        <div 
            class="flex flex-col bg-white border-r border-gray-200 overflow-hidden"
            style="width: {leftPanelWidth}%"
        >
            <!-- Tab Navigation -->
            <div class="border-b border-gray-200">
                <nav class="flex space-x-0">
                    <button
                        class="flex-1 px-4 py-3 text-sm font-medium border-r border-gray-200 transition-colors {activeTab === 'editor' ? 'bg-primary-50 text-primary-700 border-b-2 border-primary-600' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}"
                        on:click={() => activeTab = 'editor'}
                    >
                        <Edit3 class="h-4 w-4 inline mr-2" />
                        Editor
                    </button>
                    
                    {#if !isDemo}
                        <button
                            class="flex-1 px-4 py-3 text-sm font-medium border-r border-gray-200 transition-colors {activeTab === 'chat' ? 'bg-primary-50 text-primary-700 border-b-2 border-primary-600' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}"
                            on:click={() => activeTab = 'chat'}
                        >
                            <MessageSquare class="h-4 w-4 inline mr-2" />
                            AI Chat
                        </button>
                        
                        <button
                            class="flex-1 px-4 py-3 text-sm font-medium transition-colors {activeTab === 'ats' ? 'bg-primary-50 text-primary-700 border-b-2 border-primary-600' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}"
                            on:click={() => activeTab = 'ats'}
                        >
                            <Zap class="h-4 w-4 inline mr-2" />
                            ATS Score
                        </button>
                    {/if}
                </nav>
            </div>

            <!-- Tab Content -->
            <div class="flex-1 overflow-hidden">
                {#if activeTab === 'editor'}
                    <MarkdownEditor />
                {:else if activeTab === 'chat'}
                    <ChatPanel />
                {:else if activeTab === 'ats'}
                    <ATSPanel />
                {/if}
            </div>
        </div>

        <!-- Split Handle -->
        <div 
            class="split-handle bg-gray-200 hover:bg-gray-300 cursor-col-resize w-1 relative group"
            class:bg-primary-300={isDragging}
        >
            <div class="absolute inset-y-0 -left-1 -right-1 group-hover:bg-gray-300 group-hover:bg-opacity-50"></div>
        </div>

        <!-- Right Panel -->
        <div 
            class="flex overflow-hidden relative"
            style="width: {100 - leftPanelWidth}%"
        >
            <!-- PDF Preview -->
            <div class="flex-1 overflow-hidden">
                <PDFPreview />
            </div>

            <!-- Settings Panel -->
            {#if showSettings}
                <div class="w-80 bg-white border-l border-gray-200 overflow-y-auto">
                    <SettingsPanel onClose={() => showSettings = false} />
                </div>
            {/if}
        </div>
    </div>
</div>