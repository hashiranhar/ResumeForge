<script>
    import { onMount } from 'svelte';
    import { marked } from 'marked';
    import DOMPurify from 'dompurify';
    import { draftCV, currentCV } from '$lib/stores/cv.js';
    import { authenticatedFetch } from '$lib/stores/auth.js';
    import { debounce } from '$lib/utils/helpers.js';
    import { addToast } from '$lib/stores/toast.js';
    import { Eye, ZoomIn, ZoomOut, RotateCcw } from 'lucide-svelte';

    let previewContainer;
    let previewContent = '';
    let zoomLevel = 100;
    let isLoading = false;

    marked.setOptions({
        mangle: false,        // Disable deprecated mangle
        headerIds: false,     // Disable deprecated headerIds
        breaks: true,
        gfm: true,
        silent: true
    });

    // Debounced preview update
    const updatePreview = debounce(async () => {
        await generatePreview();
    }, 1000);

    // Watch for content changes
    $: if ($draftCV.markdown_content || $draftCV.settings) {
        updatePreview();
    }

    onMount(() => {
        generatePreview();
    });

    async function generatePreview() {
        if (!$draftCV.markdown_content) {
            previewContent = '<div class="preview-placeholder">Start writing to see a preview...</div>';
            return;
        }

        isLoading = true;

        try {
            // Process markdown with ResumeForge special formatting
            const processedHtml = processMarkdownWithFormatting($draftCV.markdown_content);
            
            // Generate CSS based on settings
            const css = generatePreviewCSS($draftCV.settings || {});
            
            // Combine HTML and CSS
            previewContent = `
                <style>${css}</style>
                <div class="cv-content">${processedHtml}</div>
            `;
        } catch (error) {
            console.error('Preview generation failed:', error);
            previewContent = '<div class="preview-error">Preview generation failed. Please check your markdown syntax.</div>';
        } finally {
            isLoading = false;
        }
    }

    function processMarkdownWithFormatting(markdown) {
        // First convert markdown to HTML
        let html = marked(markdown);
        
        // Process ResumeForge special markers
        const lines = html.split('\n');
        const processedLines = [];
        
        for (let line of lines) {
            // Handle [CENTER] marker
            if (line.includes('[CENTER]')) {
                const cleanLine = line.replace('[CENTER]', '').trim();
                // If it's already in HTML tags, add center class
                if (cleanLine.includes('<')) {
                    const centeredLine = cleanLine.replace(/^<(\w+)([^>]*)>/, '<$1 class="center-text"$2>');
                    processedLines.push(centeredLine);
                } else {
                    processedLines.push(`<div class="center-text">${cleanLine}</div>`);
                }
            }
            // Handle [DATE: content] marker
            else if (line.includes('[DATE:')) {
                const dateMatch = line.match(/\[DATE:\s*([^\]]+)\]/);
                if (dateMatch) {
                    const dateContent = dateMatch[1].trim();
                    const cleanLine = line.replace(/\s*\[DATE:[^\]]+\]/, '').trim();
                    
                    // Check if it's a header
                    if (cleanLine.match(/^<h[1-6]/)) {
                        const headerMatch = cleanLine.match(/^(<h[1-6][^>]*>)(.*?)(<\/h[1-6]>)$/);
                        if (headerMatch) {
                            const [, openTag, content, closeTag] = headerMatch;
                            processedLines.push(`${openTag}${content}<span class="header-date">${dateContent}</span>${closeTag}`);
                        } else {
                            processedLines.push(cleanLine);
                        }
                    } else {
                        processedLines.push(`
                            <div class="date-line">
                                <span class="content">${cleanLine}</span>
                                <span class="date">${dateContent}</span>
                            </div>
                        `);
                    }
                } else {
                    processedLines.push(line);
                }
            } else {
                processedLines.push(line);
            }
        }
        
        return DOMPurify.sanitize(processedLines.join('\n'));
    }

    function generatePreviewCSS(settings) {
        const defaults = {
            font: 'Arial',
            fontSize: 11,
            margins: { top: 20, bottom: 20, left: 15, right: 15 },
            theme: 'professional',
            lineHeight: 1.4
        };

        const config = { ...defaults, ...settings };
        const margins = { ...defaults.margins, ...(settings.margins || {}) };

        const fontFamilies = {
            'Arial': 'Arial, sans-serif',
            'Helvetica': 'Helvetica, Arial, sans-serif',
            'Times New Roman': "'Times New Roman', Times, serif",
            'Georgia': 'Georgia, serif',
            'Verdana': 'Verdana, sans-serif'
        };

        const themes = {
            professional: {
                primary: '#2c3e50',
                secondary: '#34495e',
                accent: '#3498db',
                text: '#2c3e50'
            },
            modern: {
                primary: '#1a1a1a',
                secondary: '#4a4a4a',
                accent: '#007acc',
                text: '#333333'
            },
            minimal: {
                primary: '#000000',
                secondary: '#666666',
                accent: '#888888',
                text: '#333333'
            }
        };

        const themeColors = themes[config.theme] || themes.professional;
        const fontFamily = fontFamilies[config.font] || fontFamilies.Arial;

        return `
            .cv-content {
                font-family: ${fontFamily};
                font-size: ${config.fontSize}pt;
                line-height: ${config.lineHeight};
                color: ${themeColors.text};
                max-width: 210mm;
                margin: 0 auto;
                padding: ${margins.top}mm ${margins.right}mm ${margins.bottom}mm ${margins.left}mm;
                background: white;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                min-height: 297mm;
            }

            .cv-content h1 {
                color: ${themeColors.primary};
                font-size: ${config.fontSize + 6}pt;
                font-weight: bold;
                margin: 0 0 8pt 0;
                border-bottom: 2pt solid ${themeColors.accent};
                padding-bottom: 4pt;
            }

            .cv-content h2 {
                color: ${themeColors.primary};
                font-size: ${config.fontSize + 3}pt;
                font-weight: bold;
                margin: 16pt 0 6pt 0;
                border-bottom: 1pt solid ${themeColors.secondary};
                padding-bottom: 2pt;
            }

            .cv-content h3 {
                color: ${themeColors.secondary};
                font-size: ${config.fontSize - 1}pt;
                font-weight: bold;
                margin: 12pt 0 4pt 0;
            }

            .cv-content h4 {
                color: ${themeColors.secondary};
                font-size: ${config.fontSize}pt;
                font-weight: bold;
                margin: 8pt 0 4pt 0;
            }

            .cv-content p {
                margin: 4pt 0;
            }

            .cv-content ul, .cv-content ol {
            margin: 4pt 0;
            padding-left: 16pt;
        }

        .cv-content ul {
            list-style-type: disc;
            list-style-position: outside;
        }

        .cv-content ol {
            list-style-type: decimal;
            list-style-position: outside;
        }

        .cv-content li {
            margin: 2pt 0;
            display: list-item;
        }

            .center-text {
                text-align: center;
            }

            .date-line {
                display: flex;
                justify-content: space-between;
                align-items: baseline;
                margin: 8pt 0 4pt 0;
            }

            .date-line .content {
                font-weight: bold;
                color: ${themeColors.primary};
            }

            .date-line .date {
                font-style: italic;
                color: ${themeColors.secondary};
                font-size: ${config.fontSize - 1}pt;
            }

            .header-date {
                float: right;
                font-style: italic;
                color: ${themeColors.secondary};
                font-size: ${config.fontSize - 1}pt;
                font-weight: normal;
                line-height: 1.2;
            }

            .cv-content h1, .cv-content h2, .cv-content h3 {
                position: relative;
                overflow: hidden;
            }

            .preview-placeholder {
                display: flex;
                align-items: center;
                justify-content: center;
                height: 200px;
                color: #9ca3af;
                font-size: 16px;
                text-align: center;
            }

            .preview-error {
                display: flex;
                align-items: center;
                justify-content: center;
                height: 200px;
                color: #ef4444;
                font-size: 14px;
                text-align: center;
                padding: 20px;
            }
        `;
    }

    function handleZoomIn() {
        zoomLevel = Math.min(zoomLevel + 25, 200);
    }

    function handleZoomOut() {
        zoomLevel = Math.max(zoomLevel - 25, 50);
    }

    function handleResetZoom() {
        zoomLevel = 100;
    }

    async function handleGeneratePDF() {
        if (!$currentCV) {
            addToast('Please save your CV first', 'info');
            return;
        }

        try {
            const response = await authenticatedFetch(`/api/cvs/${$currentCV.id}/preview-pdf`);
            if (response.ok) {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                window.open(url, '_blank');
                URL.revokeObjectURL(url);
            }
        } catch (error) {
            console.error('Failed to generate PDF:', error);
        }
    }
</script>

<!-- FIXED: Added dark mode styling to entire component -->
<div class="flex flex-col h-full bg-gray-100 dark:bg-gray-900">
    <!-- Preview Header - FIXED: Added dark mode styling -->
    <div class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 py-3">
        <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
                <Eye class="h-4 w-4 text-gray-500 dark:text-gray-400" />
                <span class="text-sm font-medium text-gray-900 dark:text-white">PDF Preview</span>
                {#if isLoading}
                    <div class="spinner text-gray-500 dark:text-gray-400"></div>
                {/if}
            </div>

            <div class="flex items-center space-x-2">
                <!-- Zoom controls - FIXED: Added dark mode styling -->
                <div class="flex items-center space-x-1">
                    <button
                        class="p-1 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 disabled:opacity-50 transition-colors"
                        on:click={handleZoomOut}
                        disabled={zoomLevel <= 50}
                        title="Zoom out"
                    >
                        <ZoomOut class="h-4 w-4" />
                    </button>
                    
                    <span class="text-sm text-gray-600 dark:text-gray-300 min-w-12 text-center">
                        {zoomLevel}%
                    </span>
                    
                    <button
                        class="p-1 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 disabled:opacity-50 transition-colors"
                        on:click={handleZoomIn}
                        disabled={zoomLevel >= 200}
                        title="Zoom in"
                    >
                        <ZoomIn class="h-4 w-4" />
                    </button>
                    
                    <button
                        class="p-1 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-colors"
                        on:click={handleResetZoom}
                        title="Reset zoom"
                    >
                        <RotateCcw class="h-4 w-4" />
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Preview Content - FIXED: Added dark mode styling -->
    <div class="flex-1 overflow-auto p-4 bg-gray-100 dark:bg-gray-900">
        <div 
            class="mx-auto transition-transform duration-200"
            style="transform: scale({zoomLevel / 100}); transform-origin: top center;"
            bind:this={previewContainer}
        >
            <!-- PDF Preview stays white (as it should be like a real document) -->
            <div class="bg-white shadow-lg dark:shadow-2xl">
                {@html previewContent}
            </div>
        </div>
    </div>
</div>