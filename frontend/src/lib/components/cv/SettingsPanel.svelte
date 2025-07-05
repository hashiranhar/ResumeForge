<script>
    import { draftCV } from '$lib/stores/cv.js';
    import { Palette, Type, Ruler, FileText, X } from 'lucide-svelte';
    import Button from '$lib/components/common/Button.svelte';

    export let closeSettings = () => {}; // Add closeSettings prop

    // Reactive settings
    $: settings = $draftCV.settings || {};

    function updateCVName(name) {
        draftCV.update(cv => ({
            ...cv,
            name: name
        }));
    }

    function updateSettings(key, value) {
        draftCV.update(cv => ({
            ...cv,
            settings: {
                ...cv.settings,
                [key]: value
            }
        }));
    }

    function updateMargin(side, value) {
        const margins = { ...settings.margins };
        margins[side] = parseInt(value) || 0;
        updateSettings('margins', margins);
    }

    const fontOptions = [
        { value: 'Arial', label: 'Arial' },
        { value: 'Helvetica', label: 'Helvetica' },
        { value: 'Times New Roman', label: 'Times New Roman' },
        { value: 'Georgia', label: 'Georgia' },
        { value: 'Verdana', label: 'Verdana' }
    ];

    const themeOptions = [
        { value: 'professional', label: 'Professional', color: '#2c3e50' },
        { value: 'modern', label: 'Modern', color: '#1a1a1a' },
        { value: 'minimal', label: 'Minimal', color: '#000000' },
        { value: 'creative', label: 'Creative', color: '#8e44ad' }
    ];
</script>

<div class="h-full bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700 overflow-y-auto">
    <!-- Header -->
    <div class="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">CV Settings</h3>
        <button
            on:click={closeSettings}
            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
            title="Close settings"
        >
            <X class="h-5 w-5" />
        </button>
    </div>

    <!-- Settings Content -->
    <div class="p-4 space-y-6">
        <!-- CV Name -->
        <div class="space-y-2">
            <div class="flex items-center space-x-2">
                <FileText class="h-4 w-4 text-gray-500 dark:text-gray-400" />
                <label for="cv-name" class="text-sm font-medium text-gray-700 dark:text-gray-300">CV Name</label>
            </div>
            <input
                id="cv-name"
                type="text"
                value={$draftCV.name || ''}
                on:input={e => updateCVName(e.target.value)}
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                placeholder="Enter CV name"
            />
        </div>

        <!-- Font Selection -->
        <div class="space-y-2">
            <div class="flex items-center space-x-2">
                <Type class="h-4 w-4 text-gray-500 dark:text-gray-400" />
                <label for="font-family" class="text-sm font-medium text-gray-700 dark:text-gray-300">Font Family</label>
            </div>
            <select
                id="font-family"
                value={settings.font || 'Arial'}
                on:change={e => updateSettings('font', e.target.value)}
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
                {#each fontOptions as font}
                    <option value={font.value}>{font.label}</option>
                {/each}
            </select>
        </div>

        <!-- Font Size -->
        <div class="space-y-2">
            <label for="font-size" class="text-sm font-medium text-gray-700 dark:text-gray-300">Font Size</label>
            <div class="flex items-center space-x-2">
                <input
                    id="font-size"
                    type="range"
                    min="8"
                    max="16"
                    value={settings.fontSize || 11}
                    on:input={e => updateSettings('fontSize', parseInt(e.target.value))}
                    class="flex-1"
                />
                <span class="text-sm text-gray-600 dark:text-gray-400 w-8 text-right">
                    {settings.fontSize || 11}pt
                </span>
            </div>
        </div>

        <!-- Line Height -->
        <div class="space-y-2">
            <label for="line-height" class="text-sm font-medium text-gray-700 dark:text-gray-300">Line Height</label>
            <div class="flex items-center space-x-2">
                <input
                    id="line-height"
                    type="range"
                    min="1.0"
                    max="2.0"
                    step="0.1"
                    value={settings.lineHeight || 1.4}
                    on:input={e => updateSettings('lineHeight', parseFloat(e.target.value))}
                    class="flex-1"
                />
                <span class="text-sm text-gray-600 dark:text-gray-400 w-8 text-right">
                    {settings.lineHeight || 1.4}
                </span>
            </div>
        </div>

        <!-- Theme -->
        <div class="space-y-2">
            <div class="flex items-center space-x-2">
                <Palette class="h-4 w-4 text-gray-500 dark:text-gray-400" />
                <label for="theme-selection" class="text-sm font-medium text-gray-700 dark:text-gray-300">Theme</label>
            </div>
            <div id="theme-selection" class="grid grid-cols-2 gap-2">
                {#each themeOptions as theme}
                    <button
                        on:click={() => updateSettings('theme', theme.value)}
                        class="p-2 border rounded-md text-left transition-all {
                            (settings.theme || 'professional') === theme.value
                                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                                : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
                        }"
                    >
                        <div class="flex items-center space-x-2">
                            <div
                                class="w-3 h-3 rounded-full"
                                style="background-color: {theme.color}"
                            ></div>
                            <span class="text-sm text-gray-900 dark:text-white">{theme.label}</span>
                        </div>
                    </button>
                {/each}
            </div>
        </div>

        <!-- Margins -->
        <div class="space-y-3">
            <div class="flex items-center space-x-2">
                <Ruler class="h-4 w-4 text-gray-500 dark:text-gray-400" />
                <label for="margins" class="text-sm font-medium text-gray-700 dark:text-gray-300">Margins (mm)</label>
            </div>
            
            <div class="grid grid-cols-2 gap-3">
                <div>
                    <label for="margin-top" class="text-xs text-gray-600 dark:text-gray-400">Top</label>
                    <input
                        id="margin-top"
                        type="number"
                        min="5"
                        max="50"
                        value={settings.margins?.top || 20}
                        on:input={e => updateMargin('top', e.target.value)}
                        class="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                </div>
                <div>
                    <label for="margin-bottom" class="text-xs text-gray-600 dark:text-gray-400">Bottom</label>
                    <input
                        id="margin-bottom"
                        type="number"
                        min="5"
                        max="50"
                        value={settings.margins?.bottom || 20}
                        on:input={e => updateMargin('bottom', e.target.value)}
                        class="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                </div>
                <div>
                    <label for="margin-left" class="text-xs text-gray-600 dark:text-gray-400">Left</label>
                    <input
                        id="margin-left"
                        type="number"
                        min="5"
                        max="50"
                        value={settings.margins?.left || 15}
                        on:input={e => updateMargin('left', e.target.value)}
                        class="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                </div>
                <div>
                    <label for="margin-right" class="text-xs text-gray-600 dark:text-gray-400">Right</label>
                    <input
                        id="margin-right"
                        type="number"
                        min="5"
                        max="50"
                        value={settings.margins?.right || 15}
                        on:input={e => updateMargin('right', e.target.value)}
                        class="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                </div>
            </div>
        </div>

        <!-- Reset Button -->
        <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
            <Button
                variant="outline"
                size="sm"
                class="w-full"
                on:click={() => {
                    updateSettings('font', 'Arial');
                    updateSettings('fontSize', 11);
                    updateSettings('theme', 'professional');
                    updateSettings('margins', { top: 20, bottom: 20, left: 15, right: 15 });
                }}
            >
                Reset to Defaults
            </Button>
        </div>
    </div>
</div>