<script>
    import { onMount } from 'svelte';
    import { draftCV } from '$lib/stores/cv.js';
    import { debounce } from '$lib/utils/helpers.js';
    import { FileText, HelpCircle } from 'lucide-svelte';

    let textarea;
    let showHelp = false;

    // Debounced update to prevent excessive reactivity
    const updateContent = debounce((value) => {
        draftCV.update(cv => ({
            ...cv,
            markdown_content: value
        }));
    }, 300);

    onMount(() => {
        // Focus on the editor when mounted
        if (textarea) {
            textarea.focus();
        }
    });

    function handleInput(event) {
        updateContent(event.target.value);
    }

    function handleKeyDown(event) {
        // Handle tab key for indentation
        if (event.key === 'Tab') {
            event.preventDefault();
            const start = event.target.selectionStart;
            const end = event.target.selectionEnd;
            const value = event.target.value;
            
            // Insert tab (or spaces)
            const newValue = value.substring(0, start) + '  ' + value.substring(end);
            event.target.value = newValue;
            event.target.selectionStart = event.target.selectionEnd = start + 2;
            
            updateContent(newValue);
        }
    }

    function insertMarkdown(type) {
        if (!textarea) return;

        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const value = textarea.value;
        const selectedText = value.substring(start, end);

        let insertText = '';
        let cursorOffset = 0;

        switch (type) {
            case 'header':
                insertText = `## ${selectedText || 'Header'}`;
                cursorOffset = selectedText ? 0 : -6;
                break;
            case 'bold':
                insertText = `**${selectedText || 'bold text'}**`;
                cursorOffset = selectedText ? 0 : -9;
                break;
            case 'italic':
                insertText = `*${selectedText || 'italic text'}*`;
                cursorOffset = selectedText ? 0 : -11;
                break;
            case 'bullet':
                insertText = `- ${selectedText || 'List item'}`;
                cursorOffset = selectedText ? 0 : -9;
                break;
            case 'center':
                insertText = `${selectedText || 'Centered text'} [CENTER]`;
                cursorOffset = selectedText ? 0 : -18;
                break;
            case 'date':
                insertText = `${selectedText || 'Position Title'} [DATE: 2023 - Present]`;
                cursorOffset = selectedText ? 0 : -21;
                break;
        }

        const newValue = value.substring(0, start) + insertText + value.substring(end);
        textarea.value = newValue;
        
        // Set cursor position
        const newCursorPos = start + insertText.length + cursorOffset;
        textarea.selectionStart = textarea.selectionEnd = newCursorPos;
        textarea.focus();

        updateContent(newValue);
    }
</script>

<div class="flex flex-col h-full bg-white dark:bg-gray-900">
    <!-- Toolbar - FIXED: Added dark mode styling -->
    <div class="border-b border-gray-200 dark:border-gray-700 p-3 bg-white dark:bg-gray-900">
        <div class="flex items-center justify-between mb-3">
            <h3 class="text-sm font-medium text-gray-900 dark:text-white flex items-center">
                <FileText class="h-4 w-4 mr-2" />
                Markdown Editor
            </h3>
            <button
                class="text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                on:click={() => showHelp = !showHelp}
                title="Show markdown help"
            >
                <HelpCircle class="h-4 w-4" />
            </button>
        </div>

        <!-- Quick actions - FIXED: Added dark mode styling -->
        <div class="grid grid-cols-3 gap-1">
            <button
                class="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded transition-colors"
                on:click={() => insertMarkdown('header')}
                title="Insert Header"
            >
                ## Header
            </button>
            <button
                class="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded transition-colors"
                on:click={() => insertMarkdown('bold')}
                title="Bold Text"
            >
                **Bold**
            </button>
            <button
                class="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded transition-colors"
                on:click={() => insertMarkdown('italic')}
                title="Italic Text"
            >
                *Italic*
            </button>
            <button
                class="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded transition-colors"
                on:click={() => insertMarkdown('bullet')}
                title="Bullet List"
            >
                • List
            </button>
            <button
                class="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded transition-colors"
                on:click={() => insertMarkdown('center')}
                title="Center Text"
            >
                [CENTER]
            </button>
            <button
                class="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded transition-colors"
                on:click={() => insertMarkdown('date')}
                title="Add Date"
            >
                [DATE:]
            </button>
        </div>

        <!-- Help panel - FIXED: Added dark mode styling -->
        {#if showHelp}
            <div class="mt-3 p-3 bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded text-xs space-y-2">
                <div class="text-blue-900 dark:text-blue-100"><strong>Special ResumeForge formatting:</strong></div>
                <div class="text-blue-800 dark:text-blue-200"><code class="bg-blue-100 dark:bg-blue-800 px-1 rounded">[CENTER]</code> - Centers the text on that line</div>
                <div class="text-blue-800 dark:text-blue-200"><code class="bg-blue-100 dark:bg-blue-800 px-1 rounded">[DATE: 2023 - Present]</code> - Aligns date to the right</div>
                <div class="pt-2 text-blue-900 dark:text-blue-100"><strong>Markdown basics:</strong></div>
                <div class="text-blue-800 dark:text-blue-200"><code class="bg-blue-100 dark:bg-blue-800 px-1 rounded"># Header 1</code>, <code class="bg-blue-100 dark:bg-blue-800 px-1 rounded">## Header 2</code></div>
                <div class="text-blue-800 dark:text-blue-200"><code class="bg-blue-100 dark:bg-blue-800 px-1 rounded">**Bold**</code>, <code class="bg-blue-100 dark:bg-blue-800 px-1 rounded">*Italic*</code></div>
                <div class="text-blue-800 dark:text-blue-200"><code class="bg-blue-100 dark:bg-blue-800 px-1 rounded">- Bullet point</code></div>
            </div>
        {/if}
    </div>

    <!-- Editor - FIXED: Added dark mode styling -->
    <div class="flex-1 p-4 bg-white dark:bg-gray-900">
        <textarea
            bind:this={textarea}
            value={$draftCV.markdown_content || ''}
            on:input={handleInput}
            on:keydown={handleKeyDown}
            class="w-full h-full resize-none border-none outline-none font-mono text-sm leading-relaxed bg-white dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
            placeholder="Start writing your CV in Markdown...

Example:
# Your Name
**Your Title** [CENTER]

📧 email@example.com | 📱 (555) 123-4567 [CENTER]

## Professional Summary
Write a brief summary of your experience and skills...

## Experience

### Job Title | Company Name [DATE: 2023 - Present]
- Achievement or responsibility
- Another achievement with metrics
- Key technology or skill used

## Skills
- **Category:** Skill 1, Skill 2, Skill 3"
            spellcheck="true"
        />
    </div>
</div>