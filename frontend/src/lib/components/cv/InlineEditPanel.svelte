<script lang="ts">
    import { onMount } from 'svelte';
    import { inlineEditHistory, isInlineEditing, llmService } from '$lib/stores/llm.js';
    import { currentCV, draftCV } from '$lib/stores/cv.js';
    import { addToast } from '$lib/stores/toast.js';
    import { Edit3, Wand2, Send, History, CheckCircle, Clock, Sparkles, Target, Undo2 } from 'lucide-svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Input from '$lib/components/common/Input.svelte';

    let editInstruction = '';
    let selectedSection = '';

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
                selectedSection || null
            );

            if (result.success) {
                // Update the draft CV with the edited content
                draftCV.update(draft => ({
                    ...draft,
                    markdown_content: result.editedContent
                }));

                addToast('CV edited successfully! Use Ctrl+S to save changes.', 'success');

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

    async function handleUndoEdit(editId: string) {
        try {
            // Find the edit index to determine how many edits will be undone
            const editIndex = $inlineEditHistory.findIndex(edit => edit.id === editId);
            const editsToUndo = $inlineEditHistory.length - editIndex;
            
            // Show confirmation if multiple edits will be undone
            if (editsToUndo > 1) {
                const confirmed = confirm(
                    `This will undo ${editsToUndo} edits (including all edits made after this one). Continue?`
                );
                if (!confirmed) return;
            }
            
            const result = await llmService.undoInlineEdit(editId);
            
            if (result.success) {
                const message = result.undoneCount === 1 
                    ? 'Edit undone successfully' 
                    : `${result.undoneCount} edits undone successfully`;
                addToast(message, 'success');
            } else {
                addToast(result.error || 'Failed to undo edit', 'error');
            }
        } catch (error) {
            addToast('Failed to undo edit', 'error');
        }
    }

    function getUndoTooltip(edit: any, history: any[]): string {
        const editIndex = history.findIndex(e => e.id === edit.id);
        const editsToUndo = history.length - editIndex;
        
        if (editsToUndo === 1) {
            return 'Undo this edit';
        } else {
            return `Undo this edit and ${editsToUndo - 1} newer edit${editsToUndo - 1 > 1 ? 's' : ''}`;
        }
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
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-2">
                Changes will be applied to the editor. Use Ctrl+S or the Save button to save to your CV. Note: Multiple unsaved edits will override each other.
            </p>
            
            <!-- Textarea with integrated send button -->
            <div class="relative">
                <textarea
                    id="edit-instruction"
                    bind:value={editInstruction}
                    on:keypress={handleKeyPress}
                    placeholder="e.g. Make my experience section more quantified and impactful..."
                    class="w-full px-3 py-3 pr-16 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 rounded-lg resize-none focus:ring-2 focus:ring-primary-500 dark:focus:ring-primary-400 focus:border-primary-500 dark:focus:border-primary-400"
                    rows="3"
                    disabled={$isInlineEditing}
                ></textarea>
                
                <!-- Send Button - positioned inside textarea -->
                <div class="absolute bottom-3 right-3">
                    <Button
                        size="sm"
                        on:click={handleInlineEdit}
                        disabled={!editInstruction.trim() || $isInlineEditing}
                        loading={$isInlineEditing}
                        className="h-8 w-8 p-0 rounded-full"
                    >
                        {#if $isInlineEditing}
                            <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        {:else}
                            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                        {/if}
                    </Button>
                </div>
            </div>
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
                            </div>
                            <div class="flex items-center space-x-2">
                                {#if edit.section}
                                    <span class="text-xs bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 px-2 py-1 rounded-full">
                                        {cvSections.find(s => s.value === edit.section)?.label || edit.section}
                                    </span>
                                {/if}
                                <!-- Undo Button -->
                                <span title={getUndoTooltip(edit, $inlineEditHistory)}>
                                    <Button
                                        variant="outline"
                                        size="sm"
                                        on:click={() => handleUndoEdit(edit.id)}
                                        className="text-xs px-2 py-1 h-6"
                                    >
                                        <Undo2 class="h-3 w-3 mr-1" />
                                        Undo
                                    </Button>
                                </span>
                            </div>
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