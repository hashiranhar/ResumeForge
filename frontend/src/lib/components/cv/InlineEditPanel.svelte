<script lang="ts">
    import { onMount } from 'svelte';
    import { inlineEditHistory, isInlineEditing, llmService } from '$lib/stores/llm.js';
    import { currentCV, draftCV } from '$lib/stores/cv.js';
    import { addToast } from '$lib/stores/toast.js';
    import { Edit3, Wand2, Send, History, CheckCircle, Clock, Sparkles, Target } from 'lucide-svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Input from '$lib/components/common/Input.svelte';

    let editInstruction = '';
    let selectedSection = '';
    let autoSave = true;

    // CV sections for targeting specific areas
    const cvSections = [
        { value: '', label: 'Entire CV' },
        { value: 'summary', label: 'Professional Summary' },
        { value: 'experience', label: 'Work Experience' },
        { value: 'education', label: 'Education' },
        { value: 'skills', label: 'Skills' },
        { value: 'projects', label: 'Projects' },
        { value: 'achievements', label: 'Achievements' },
        { value: 'contact', label: 'Contact Information' }
    ];

    // Quick edit suggestions
    const quickEdits = [
        'Make this more professional and impactful',
        'Add more specific achievements with numbers',
        'Improve the action verbs and language',
        'Make it more concise and focused',
        'Add missing industry keywords',
        'Improve formatting and structure'
    ];

    onMount(() => {
        // Clear edit history when component mounts
        llmService.clearInlineEditHistory();
    });

    async function handleInlineEdit() {
        if (!editInstruction.trim()) {
            addToast('Please enter an editing instruction', 'error');
            return;
        }

        if (!$currentCV?.id) {
            addToast('Please save your CV first', 'error');
            return;
        }

        try {
            const result = await llmService.inlineEdit(
                $currentCV.id,
                editInstruction.trim(),
                selectedSection || null,
                autoSave
            );

            if (result.success) {
                // Update the draft CV with the edited content
                draftCV.update(draft => ({
                    ...draft,
                    markdown_content: result.editedContent
                }));

                addToast(
                    result.autoSaved 
                        ? 'CV edited and saved successfully!' 
                        : 'CV edited successfully!', 
                    'success'
                );

                // Clear the instruction
                editInstruction = '';
            } else {
                addToast(result.error || 'Failed to edit CV', 'error');
            }
        } catch (error) {
            addToast('Failed to edit CV', 'error');
        }
    }

    function handleQuickEdit(instruction: string) {
        editInstruction = instruction;
        handleInlineEdit();
    }

    function handleKeyPress(event: KeyboardEvent) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            handleInlineEdit();
        }
    }

    function formatTimestamp(timestamp: string): string {
        return new Date(timestamp).toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }
</script>

<div class="flex flex-col h-full bg-white dark:bg-gray-900">
    <!-- Header -->
    <div class="border-b border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-900">
        <div class="flex items-center space-x-2">
            <Edit3 class="h-4 w-4 text-gray-500 dark:text-gray-400" />
            <h3 class="font-medium text-gray-900 dark:text-white">AI Inline Editor</h3>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-300 mt-1">
            Make instant improvements to your CV content with AI assistance
        </p>
    </div>

    <!-- Edit Controls -->
    <div class="p-4 border-b border-gray-200 dark:border-gray-700 space-y-4 bg-white dark:bg-gray-900">
        <!-- Section Selector -->
        <div>
            <label for="section-select" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Target Section (Optional)
            </label>
            <select
                id="section-select"
                bind:value={selectedSection}
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 dark:focus:ring-primary-400 focus:border-primary-500 dark:focus:border-primary-400"
            >
                {#each cvSections as section}
                    <option value={section.value}>{section.label}</option>
                {/each}
            </select>
        </div>

        <!-- Edit Instruction -->
        <div>
            <label for="edit-instruction" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                What would you like to improve?
            </label>
            <div class="flex space-x-2">
                <div class="flex-1">
                    <textarea
                        id="edit-instruction"
                        bind:value={editInstruction}
                        on:keypress={handleKeyPress}
                        placeholder="e.g. Make my experience section more quantified and impactful..."
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 rounded-lg resize-none focus:ring-2 focus:ring-primary-500 dark:focus:ring-primary-400 focus:border-primary-500 dark:focus:border-primary-400"
                        rows="3"
                        disabled={$isInlineEditing}
                    ></textarea>
                </div>
                <Button
                    size="sm"
                    on:click={handleInlineEdit}
                    disabled={!editInstruction.trim() || $isInlineEditing}
                    loading={$isInlineEditing}
                    className="self-end"
                >
                    <Wand2 class="h-4 w-4" />
                </Button>
            </div>
        </div>

        <!-- Auto-save Toggle -->
        <div class="flex items-center space-x-2">
            <input
                type="checkbox"
                id="auto-save"
                bind:checked={autoSave}
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600 rounded"
            />
            <label for="auto-save" class="text-sm text-gray-700 dark:text-gray-300">
                Auto-save changes
            </label>
        </div>
    </div>

    <!-- Content Area -->
    <div class="flex-1 overflow-y-auto p-4 bg-white dark:bg-gray-900">
        {#if $inlineEditHistory.length === 0}
            <!-- Empty State -->
            <div class="text-center py-12">
                <Sparkles class="h-16 w-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
                <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    AI-Powered Editing
                </h4>
                <p class="text-gray-600 dark:text-gray-300 mb-6 max-w-sm mx-auto">
                    Get instant, intelligent improvements to your CV content. Just describe what you want to change.
                </p>

                <!-- Quick Edit Suggestions -->
                <div class="space-y-3">
                    <div class="flex items-center justify-center space-x-2 mb-4">
                        <Target class="h-4 w-4 text-primary-500" />
                        <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Quick improvements:</span>
                    </div>
                    {#each quickEdits.slice(0, 3) as quickEdit}
                        <button
                            class="w-full text-left p-3 text-sm bg-gray-50 dark:bg-gray-800 hover:bg-primary-50 dark:hover:bg-primary-900 text-gray-900 dark:text-white border border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-600 rounded-lg transition-colors"
                            on:click={() => handleQuickEdit(quickEdit)}
                            disabled={$isInlineEditing}
                        >
                            <div class="flex items-center space-x-2">
                                <Wand2 class="h-4 w-4 text-primary-500" />
                                <span>{quickEdit}</span>
                            </div>
                        </button>
                    {/each}
                </div>

                <!-- Features -->
                <div class="mt-8 space-y-2 text-sm text-gray-500 dark:text-gray-400">
                    <div class="flex items-center justify-center space-x-2">
                        <CheckCircle class="h-4 w-4 text-green-500" />
                        <span>Real-time content editing</span>
                    </div>
                    <div class="flex items-center justify-center space-x-2">
                        <CheckCircle class="h-4 w-4 text-green-500" />
                        <span>Section-specific improvements</span>
                    </div>
                    <div class="flex items-center justify-center space-x-2">
                        <CheckCircle class="h-4 w-4 text-green-500" />
                        <span>Professional language enhancement</span>
                    </div>
                </div>
            </div>
        {:else}
            <!-- Edit History -->
            <div class="space-y-4">
                <div class="flex items-center space-x-2">
                    <History class="h-4 w-4 text-gray-500 dark:text-gray-400" />
                    <h5 class="font-medium text-gray-900 dark:text-white">Recent Edits</h5>
                </div>

                {#each $inlineEditHistory.slice().reverse() as edit}
                    <div class="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                        <div class="flex items-start justify-between mb-2">
                            <div class="flex items-center space-x-2">
                                <Clock class="h-4 w-4 text-gray-400 dark:text-gray-500" />
                                <span class="text-sm text-gray-600 dark:text-gray-300">
                                    {formatTimestamp(edit.timestamp)}
                                </span>
                                {#if edit.autoSaved}
                                    <span class="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200">
                                        <CheckCircle class="h-3 w-3 mr-1" />
                                        Saved
                                    </span>
                                {/if}
                            </div>
                            {#if edit.section}
                                <span class="text-xs bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 px-2 py-1 rounded-full">
                                    {cvSections.find(s => s.value === edit.section)?.label || edit.section}
                                </span>
                            {/if}
                        </div>

                        <p class="text-sm text-gray-900 dark:text-white mb-2">
                            "{edit.instruction}"
                        </p>

                        {#if edit.changesMade.length > 0}
                            <div class="space-y-1">
                                {#each edit.changesMade as change}
                                    <div class="flex items-center space-x-2">
                                        <CheckCircle class="h-3 w-3 text-green-500 flex-shrink-0" />
                                        <span class="text-xs text-gray-600 dark:text-gray-300">{change}</span>
                                    </div>
                                {/each}
                            </div>
                        {/if}
                    </div>
                {/each}

                <!-- Clear History Button -->
                <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
                    <Button
                        variant="outline"
                        size="sm"
                        on:click={() => llmService.clearInlineEditHistory()}
                        className="w-full"
                    >
                        Clear History
                    </Button>
                </div>
            </div>
        {/if}

        <!-- Loading State -->
        {#if $isInlineEditing}
            <div class="mt-4 flex items-center justify-center space-x-2 text-primary-600 dark:text-primary-400">
                <div class="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
                <span class="text-sm">AI is editing your CV...</span>
            </div>
        {/if}
    </div>
</div>