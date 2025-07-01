<script>
    import { onMount, onDestroy } from 'svelte';
    import { draftCV } from '$lib/stores/cv.js';
    import { debounce } from '$lib/utils/helpers.js';
    import { FileText, HelpCircle } from 'lucide-svelte';

    let editorContainer;
    let editor;
    let showHelp = false;

    // Debounced update to prevent excessive reactivity
    const updateContent = debounce((value) => {
        draftCV.update(cv => ({
            ...cv,
            markdown_content: value
        }));
    }, 300);

    onMount(async () => {
        // Load Monaco Editor from CDN
        if (!window.monaco) {
            await loadMonacoEditor();
        }
        initializeEditor();
    });

    onDestroy(() => {
        if (editor) {
            editor.dispose();
        }
    });

    async function loadMonacoEditor() {
        return new Promise((resolve, reject) => {
            // Load Monaco Editor CSS
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs/editor/editor.main.min.css';
            document.head.appendChild(link);

            // Load Monaco Editor JS
            const script = document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs/loader.min.js';
            script.onload = () => {
                window.require.config({ 
                    paths: { 
                        'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' 
                    }
                });
                
                window.require(['vs/editor/editor.main'], () => {
                    resolve();
                });
            };
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    function initializeEditor() {
        if (!window.monaco || !editorContainer) return;

        // Custom markdown language configuration for ResumeForge
        window.monaco.languages.register({ id: 'resumeforge-markdown' });
        
        // Define custom tokens for ResumeForge syntax
        window.monaco.languages.setMonarchTokensProvider('resumeforge-markdown', {
            tokenizer: {
                root: [
                    // Headers
                    [/^#{1,6}\s.*$/, 'header'],
                    
                    // ResumeForge special syntax
                    [/\[CENTER\]/, 'custom.center'],
                    [/\[DATE:\s*[^\]]+\]/, 'custom.date'],
                    
                    // Bold
                    [/\*\*[^*]+\*\*/, 'strong'],
                    
                    // Italic
                    [/\*[^*]+\*/, 'emphasis'],
                    
                    // Lists
                    [/^\s*[-*+]\s/, 'list'],
                    [/^\s*\d+\.\s/, 'list'],
                    
                    // Email
                    [/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/, 'string.email'],
                    
                    // Phone
                    [/\b\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})\b/, 'string.phone'],
                    
                    // URLs
                    [/https?:\/\/[^\s]+/, 'string.url'],
                ]
            }
        });

        // Define custom theme
        window.monaco.editor.defineTheme('resumeforge-light', {
            base: 'vs',
            inherit: true,
            rules: [
                { token: 'header', foreground: '1d4ed8', fontStyle: 'bold' },
                { token: 'custom.center', foreground: '7c3aed', fontStyle: 'bold' },
                { token: 'custom.date', foreground: '059669', fontStyle: 'bold' },
                { token: 'strong', foreground: '1f2937', fontStyle: 'bold' },
                { token: 'emphasis', foreground: '6b7280', fontStyle: 'italic' },
                { token: 'list', foreground: 'dc2626' },
                { token: 'string.email', foreground: '2563eb' },
                { token: 'string.phone', foreground: '2563eb' },
                { token: 'string.url', foreground: '2563eb' },
            ],
            colors: {
                'editor.background': '#ffffff',
                'editor.lineHighlightBackground': '#f8fafc',
                'editorLineNumber.foreground': '#9ca3af',
                'editorLineNumber.activeForeground': '#374151',
            }
        });

        window.monaco.editor.defineTheme('resumeforge-dark', {
            base: 'vs-dark',
            inherit: true,
            rules: [
                { token: 'header', foreground: '60a5fa', fontStyle: 'bold' },
                { token: 'custom.center', foreground: 'a78bfa', fontStyle: 'bold' },
                { token: 'custom.date', foreground: '34d399', fontStyle: 'bold' },
                { token: 'strong', foreground: 'f9fafb', fontStyle: 'bold' },
                { token: 'emphasis', foreground: '9ca3af', fontStyle: 'italic' },
                { token: 'list', foreground: 'f87171' },
                { token: 'string.email', foreground: '60a5fa' },
                { token: 'string.phone', foreground: '60a5fa' },
                { token: 'string.url', foreground: '60a5fa' },
            ],
            colors: {
                'editor.background': '#111827',
                'editor.lineHighlightBackground': '#1f2937',
                'editorLineNumber.foreground': '#6b7280',
                'editorLineNumber.activeForeground': '#d1d5db',
            }
        });

        // Create the editor
        editor = window.monaco.editor.create(editorContainer, {
            value: $draftCV.markdown_content || '',
            language: 'resumeforge-markdown',
            theme: document.documentElement.classList.contains('dark') ? 'resumeforge-dark' : 'resumeforge-light',
            fontSize: 14,
            lineNumbers: 'on',
            minimap: {
                enabled: true,
                showSlider: 'mouseover'
            },
            scrollBeyondLastLine: false,
            wordWrap: 'on',
            automaticLayout: true,
            tabSize: 2,
            insertSpaces: true,
            bracketPairColorization: {
                enabled: true
            },
            guides: {
                indentation: true,
                bracketPairs: true
            },
            suggest: {
                showWords: true,
                showSnippets: true
            },
            folding: true,
            foldingHighlight: true,
            foldingImportsByDefault: false,
            renderLineHighlight: 'line',
            cursorBlinking: 'blink',
            cursorSmoothCaretAnimation: 'on',
            smoothScrolling: true,
            mouseWheelZoom: true,
            contextmenu: true,
            selectOnLineNumbers: true,
            glyphMargin: false,
            lineDecorationsWidth: 10,
            lineNumbersMinChars: 3,
            scrollbar: {
                vertical: 'visible',
                horizontal: 'visible',
                verticalScrollbarSize: 12,
                horizontalScrollbarSize: 12
            }
        });

        // Listen for content changes
        editor.onDidChangeModelContent(() => {
            const value = editor.getValue();
            updateContent(value);
        });

        // Theme change observer
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.attributeName === 'class') {
                    const isDark = document.documentElement.classList.contains('dark');
                    editor.updateOptions({
                        theme: isDark ? 'resumeforge-dark' : 'resumeforge-light'
                    });
                }
            });
        });

        observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['class']
        });

        // Add custom commands
        editor.addCommand(window.monaco.KeyMod.CtrlCmd | window.monaco.KeyCode.KeyB, () => {
            insertMarkdown('bold');
        });

        editor.addCommand(window.monaco.KeyMod.CtrlCmd | window.monaco.KeyCode.KeyI, () => {
            insertMarkdown('italic');
        });

        editor.addCommand(window.monaco.KeyMod.CtrlCmd | window.monaco.KeyCode.KeyH, () => {
            insertMarkdown('header');
        });

        // Focus the editor
        editor.focus();
    }

    function insertMarkdown(type) {
        if (!editor) return;

        const selection = editor.getSelection();
        const selectedText = editor.getModel().getValueInRange(selection);

        let insertText = '';
        let offsetStart = 0;
        let offsetEnd = 0;

        switch (type) {
            case 'header':
                insertText = `## ${selectedText || 'Header'}`;
                offsetStart = selectedText ? 0 : 3;
                offsetEnd = selectedText ? 0 : selectedText ? 0 : 6;
                break;
            case 'bold':
                insertText = `**${selectedText || 'bold text'}**`;
                offsetStart = selectedText ? 0 : 2;
                offsetEnd = selectedText ? 0 : selectedText ? 0 : 9;
                break;
            case 'italic':
                insertText = `*${selectedText || 'italic text'}*`;
                offsetStart = selectedText ? 0 : 1;
                offsetEnd = selectedText ? 0 : selectedText ? 0 : 11;
                break;
            case 'bullet':
                insertText = `- ${selectedText || 'List item'}`;
                offsetStart = selectedText ? 0 : 2;
                offsetEnd = selectedText ? 0 : selectedText ? 0 : 9;
                break;
            case 'center':
                insertText = `${selectedText || 'Centered text'} [CENTER]`;
                offsetStart = selectedText ? 0 : 0;
                offsetEnd = selectedText ? 0 : selectedText ? 0 : 13;
                break;
            case 'date':
                insertText = `${selectedText || 'Position Title'} [DATE: 2023 - Present]`;
                offsetStart = selectedText ? 0 : 0;
                offsetEnd = selectedText ? 0 : selectedText ? 0 : 14;
                break;
        }

        editor.executeEdits('insert-markdown', [{
            range: selection,
            text: insertText
        }]);

        // Set cursor position
        if (!selectedText) {
            const position = selection.getStartPosition();
            const newPosition = {
                lineNumber: position.lineNumber,
                column: position.column + offsetStart
            };
            editor.setSelection(new window.monaco.Selection(
                newPosition.lineNumber,
                newPosition.column,
                newPosition.lineNumber,
                newPosition.column + (offsetEnd - offsetStart)
            ));
        }

        editor.focus();
    }

    // React to draft CV changes from external sources
    $: if (editor && $draftCV.markdown_content !== editor.getValue()) {
        editor.setValue($draftCV.markdown_content || '');
    }
</script>

<div class="flex flex-col h-full bg-white dark:bg-gray-900">
    <!-- Toolbar -->
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

        <!-- Quick actions -->
        <div class="grid grid-cols-3 gap-1">
            <button
                class="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded transition-colors"
                on:click={() => insertMarkdown('header')}
                title="Insert Header (Ctrl+H)"
            >
                ## Header
            </button>
            <button
                class="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded transition-colors"
                on:click={() => insertMarkdown('bold')}
                title="Bold Text (Ctrl+B)"
            >
                **Bold**
            </button>
            <button
                class="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded transition-colors"
                on:click={() => insertMarkdown('italic')}
                title="Italic Text (Ctrl+I)"
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

        <!-- Help panel -->
        {#if showHelp}
            <div class="mt-3 p-3 bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded text-xs space-y-2">
                <div class="text-blue-900 dark:text-blue-100"><strong>Special ResumeForge formatting:</strong></div>
                <div class="text-blue-800 dark:text-blue-200"><code class="bg-blue-100 dark:bg-blue-800 px-1 rounded">[CENTER]</code> - Centers the text on that line</div>
                <div class="text-blue-800 dark:text-blue-200"><code class="bg-blue-100 dark:bg-blue-800 px-1 rounded">[DATE: 2023 - Present]</code> - Aligns date to the right</div>
                <div class="pt-2 text-blue-900 dark:text-blue-100"><strong>Keyboard shortcuts:</strong></div>
                <div class="text-blue-800 dark:text-blue-200">Ctrl+B: Bold, Ctrl+I: Italic, Ctrl+H: Header</div>
                <div class="text-blue-800 dark:text-blue-200">Ctrl+Wheel: Zoom, F1: Command palette</div>
            </div>
        {/if}
    </div>

    <!-- Monaco Editor Container -->
    <div class="flex-1 relative">
        <div bind:this={editorContainer} class="w-full h-full"></div>
    </div>
</div>

<style>
    /* Ensure Monaco Editor container has proper sizing */
    :global(.monaco-editor) {
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
    }

    /* Custom scrollbar for the editor area */
    :global(.monaco-editor .monaco-scrollable-element > .scrollbar > .slider) {
        background: rgba(0, 0, 0, 0.3) !important;
    }

    :global(.dark .monaco-editor .monaco-scrollable-element > .scrollbar > .slider) {
        background: rgba(255, 255, 255, 0.3) !important;
    }
</style>