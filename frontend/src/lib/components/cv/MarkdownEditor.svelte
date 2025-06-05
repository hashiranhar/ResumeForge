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

<div class="flex flex-col h-full">
    <!-- Toolbar -->
    <div class="border-b border-gray-200 p-3">
        <div class="flex items-center justify-between mb-3">
            <h3 class="text-sm font-medium text-gray-900 flex items-center">
                <FileText class="h-4 w-4 mr-2" />
                Markdown Editor
            </h3>
            <button
                class="text-gray-400 hover:text-gray-600"
                on:click={() => showHelp = !showHelp}
                title="Show markdown help"
            >
                <HelpCircle class="h-4 w-4" />
            </button>
        </div>

        <!-- Quick actions -->
        <div class="grid grid-cols-3 gap-1">
            <button
                class="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors"
                on:click={() => insertMarkdown('header')}
                title="Insert Header"
            >
                ## Header
            </button>
            <button
                class="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors"
                on:click={() => insertMarkdown('bold')}
                title="Bold Text"
            >
                **Bold**
            </button>
            <button
                class="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors"
                on:click={() => insertMarkdown('italic')}
                title="Italic Text"
            >
                *Italic*
            </button>
            <button
                class="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors"
                on:click={() => insertMarkdown('bullet')}
                title="Bullet List"
            >
                • List
            </button>
            <button
                class="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors"
                on:click={() => insertMarkdown('center')}
                title="Center Text"
            >
                [CENTER]
            </button>
            <button
                class="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors"
                on:click={() => insertMarkdown('date')}
                title="Add Date"
            >
                [DATE:]
            </button>
        </div>

        <!-- Help panel -->
        {#if showHelp}
            <div class="mt-3 p-3 bg-blue-50 border border-blue-200 rounded text-xs space-y-2">
                <div><strong>Special ResumeForge formatting:</strong></div>
                <div><code>[CENTER]</code> - Centers the text on that line</div>
                <div><code>[DATE: 2023 - Present]</code> - Aligns date to the right</div>
                <div class="pt-2"><strong>Markdown basics:</strong></div>
                <div><code># Header 1</code>, <code>## Header 2</code></div>
                <div><code>**Bold**</code>, <code>*Italic*</code></div>
                <div><code>- Bullet point</code></div>
            </div>
        {/if}
    </div>

    <!-- Editor -->
    <div class="flex-1 p-4">
        <textarea
            bind:this={textarea}
            value={$draftCV.markdown_content || ''}
            on:input={handleInput}
            on:keydown={handleKeyDown}
            class="w-full h-full resize-none border-none outline-none font-mono text-sm leading-relaxed"
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