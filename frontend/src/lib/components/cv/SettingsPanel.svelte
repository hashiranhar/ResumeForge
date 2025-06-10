<script>
    import { draftCV } from '$lib/stores/cv.js';
    import { X, Palette, Type, Ruler } from 'lucide-svelte';
    import Button from '$lib/components/common/Button.svelte';

    export let onClose = () => {};

    // Reactive settings
    $: settings = $draftCV.settings || {};

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

<div class="h-full flex flex-col bg-white dark:bg-gray-800">
    <!-- Header -->
    <div class="border-b border-gray-200 dark:border-gray-700 p-4">
        <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">CV Settings</h3>
            <button
                class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 rounded"
                on:click={onClose}
                aria-label="Close settings panel"
            >
                <X class="h-5 w-5" />
            </button>
        </div>
    </div>

    <!-- Settings Content -->
    <div class="flex-1 overflow-y-auto p-4 space-y-6">
        <!-- Font Settings -->
        <div class="space-y-4">
            <div class="flex items-center space-x-2">
                <Type class="h-4 w-4 text-gray-500 dark:text-gray-400" aria-hidden="true" />
                <h4 class="font-medium text-gray-900 dark:text-white">Typography</h4>
            </div>

            <!-- Font Family -->
            <div>
                <label for="font-family" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Font Family
                </label>
                <select
                    id="font-family"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    value={settings.font || 'Arial'}
                    on:change={(e) => updateSettings('font', e.target.value)}
                    aria-describedby="font-family-help"
                >
                    {#each fontOptions as option}
                        <option value={option.value}>{option.label}</option>
                    {/each}
                </select>
                <p id="font-family-help" class="sr-only">Select a font family for your CV</p>
            </div>

            <!-- Font Size -->
            <div>
                <label for="font-size" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Font Size: {settings.fontSize || 11}pt
                </label>
                <input
                    id="font-size"
                    type="range"
                    min="9"
                    max="14"
                    step="0.5"
                    value={settings.fontSize || 11}
                    on:input={(e) => updateSettings('fontSize', parseFloat(e.target.value))}
                    class="w-full"
                    aria-describedby="font-size-range"
                />
                <div id="font-size-range" class="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
                    <span>9pt</span>
                    <span>14pt</span>
                </div>
            </div>

            <!-- Line Height -->
            <div>
                <label for="line-height" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Line Height: {settings.lineHeight || 1.4}
                </label>
                <input
                    id="line-height"
                    type="range"
                    min="1.0"
                    max="2.0"
                    step="0.1"
                    value={settings.lineHeight || 1.4}
                    on:input={(e) => updateSettings('lineHeight', parseFloat(e.target.value))}
                    class="w-full"
                    aria-describedby="line-height-range"
                />
                <div id="line-height-range" class="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
                    <span>1.0</span>
                    <span>2.0</span>
                </div>
            </div>
        </div>

        <!-- Theme Settings -->
        <div class="space-y-4">
            <div class="flex items-center space-x-2">
                <Palette class="h-4 w-4 text-gray-500 dark:text-gray-400" aria-hidden="true" />
                <h4 class="font-medium text-gray-900 dark:text-white">Theme</h4>
            </div>

            <div class="grid grid-cols-2 gap-3" role="radiogroup" aria-labelledby="theme-heading">
                <h5 id="theme-heading" class="sr-only">Select a theme for your CV</h5>
                {#each themeOptions as theme}
                    <button
                        type="button"
                        class="p-3 border-2 rounded-lg text-left transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 {settings.theme === theme.value ? 'border-primary-500 bg-primary-50 dark:bg-primary-900' : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500 bg-white dark:bg-gray-700'}"
                        on:click={() => updateSettings('theme', theme.value)}
                        role="radio"
                        aria-checked={settings.theme === theme.value}
                    >
                        <div class="flex items-center space-x-2">
                            <div 
                                class="w-4 h-4 rounded-full"
                                style="background-color: {theme.color}"
                                aria-hidden="true"
                            ></div>
                            <span class="text-sm font-medium text-gray-900 dark:text-white">{theme.label}</span>
                        </div>
                    </button>
                {/each}
            </div>
        </div>

        <!-- Margin Settings -->
        <div class="space-y-4">
            <div class="flex items-center space-x-2">
                <Ruler class="h-4 w-4 text-gray-500 dark:text-gray-400" aria-hidden="true" />
                <h4 class="font-medium text-gray-900 dark:text-white">Margins (mm)</h4>
            </div>

            <div class="grid grid-cols-2 gap-3">
                <div>
                    <label for="margin-top" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Top
                    </label>
                    <input
                        id="margin-top"
                        type="number"
                        min="10"
                        max="50"
                        value={settings.margins?.top || 20}
                        on:input={(e) => updateMargin('top', e.target.value)}
                        class="w-full px-3 py-1 border border-gray-300 dark:border-gray-600 rounded focus:ring-1 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                        aria-describedby="margin-help"
                    />
                </div>
                <div>
                    <label for="margin-bottom" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Bottom
                    </label>
                    <input
                        id="margin-bottom"
                        type="number"
                        min="10"
                        max="50"
                        value={settings.margins?.bottom || 20}
                        on:input={(e) => updateMargin('bottom', e.target.value)}
                        class="w-full px-3 py-1 border border-gray-300 dark:border-gray-600 rounded focus:ring-1 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                        aria-describedby="margin-help"
                    />
                </div>
                <div>
                    <label for="margin-left" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Left
                    </label>
                    <input
                        id="margin-left"
                        type="number"
                        min="10"
                        max="40"
                        value={settings.margins?.left || 15}
                        on:input={(e) => updateMargin('left', e.target.value)}
                        class="w-full px-3 py-1 border border-gray-300 dark:border-gray-600 rounded focus:ring-1 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                        aria-describedby="margin-help"
                    />
                </div>
                <div>
                    <label for="margin-right" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Right
                    </label>
                    <input
                        id="margin-right"
                        type="number"
                        min="10"
                        max="40"
                        value={settings.margins?.right || 15}
                        on:input={(e) => updateMargin('right', e.target.value)}
                        class="w-full px-3 py-1 border border-gray-300 dark:border-gray-600 rounded focus:ring-1 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                        aria-describedby="margin-help"
                    />
                </div>
            </div>
            <p id="margin-help" class="sr-only">Set the page margins for your CV in millimeters</p>
        </div>

        <!-- Reset to Defaults -->
        <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
            <Button 
                variant="outline" 
                size="sm"
                on:click={() => updateSettings('', {
                    font: 'Arial',
                    fontSize: 11,
                    lineHeight: 1.4,
                    margins: { top: 20, bottom: 20, left: 15, right: 15 },
                    theme: 'professional'
                })}
                class="w-full"
            >
                Reset to Defaults
            </Button>
        </div>
    </div>
</div>