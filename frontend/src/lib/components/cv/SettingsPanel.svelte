<script>
    import { draftCV } from '$lib/stores/cv.js';
    import { Palette, Type, Ruler, FileText } from 'lucide-svelte';
    import Button from '$lib/components/common/Button.svelte';

    export const closeSettings = () => {};

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

<!-- REMOVED: Duplicate header - the EditorLayout already has the "CV Settings" header -->
<div class="p-4 space-y-6">
    <!-- CV Information Section -->
    <div class="space-y-4">
        <div class="flex items-center space-x-2">
            <FileText class="h-4 w-4 text-gray-500 dark:text-gray-400" />
            <h4 class="text-md font-medium text-gray-900 dark:text-white">CV Information</h4>
        </div>
        
        <!-- CV Name -->
        <div>
            <label for="cv-name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                CV Name
            </label>
            <input
                id="cv-name"
                type="text"
                value={$draftCV.name || ''}
                on:input={(e) => updateCVName(e.target.value)}
                placeholder="Enter CV name..."
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            />
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                This name will be used for downloads and organization
            </p>
        </div>
    </div>

    <!-- Typography Section -->
    <div class="space-y-4">
        <div class="flex items-center space-x-2">
            <Type class="h-4 w-4 text-gray-500 dark:text-gray-400" />
            <h4 class="text-md font-medium text-gray-900 dark:text-white">Typography</h4>
        </div>
        
        <!-- Font Family -->
        <div>
            <label for="font-family" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Font Family
            </label>
            <select
                id="font-family"
                value={settings.font || 'Arial'}
                on:change={(e) => updateSettings('font', e.target.value)}
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            >
                {#each fontOptions as option}
                    <option value={option.value}>{option.label}</option>
                {/each}
            </select>
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
                class="w-full h-2 bg-gray-200 dark:bg-gray-600 rounded-lg appearance-none cursor-pointer"
            />
            <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
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
                class="w-full h-2 bg-gray-200 dark:bg-gray-600 rounded-lg appearance-none cursor-pointer"
            />
            <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
                <span>1.0</span>
                <span>2.0</span>
            </div>
        </div>
    </div>

    <!-- Theme Section -->
    <div class="space-y-4">
        <div class="flex items-center space-x-2">
            <Palette class="h-4 w-4 text-gray-500 dark:text-gray-400" />
            <h4 class="text-md font-medium text-gray-900 dark:text-white">Theme</h4>
        </div>
        
        <div class="grid grid-cols-2 gap-3">
            {#each themeOptions as theme}
                <button
                    type="button"
                    class="p-3 border rounded-lg text-left transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 {settings.theme === theme.value 
                        ? 'border-primary-500 bg-primary-50 dark:bg-primary-900' 
                        : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'}"
                    on:click={() => updateSettings('theme', theme.value)}
                >
                    <div class="flex items-center space-x-2">
                        <div 
                            class="w-4 h-4 rounded-full border border-gray-300 dark:border-gray-600"
                            style="background-color: {theme.color}"
                        ></div>
                        <span class="font-medium text-gray-900 dark:text-white text-sm">{theme.label}</span>
                    </div>
                </button>
            {/each}
        </div>
    </div>

    <!-- Layout Section -->
    <div class="space-y-4">
        <div class="flex items-center space-x-2">
            <Ruler class="h-4 w-4 text-gray-500 dark:text-gray-400" />
            <h4 class="text-md font-medium text-gray-900 dark:text-white">Page Layout</h4>
        </div>
        
        <!-- Margins -->
        <fieldset>
            <legend class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                Margins (mm)
            </legend>
            <div class="grid grid-cols-2 gap-3">
                <div>
                    <label for="margin-top" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Top
                    </label>
                    <input
                        id="margin-top"
                        type="number"
                        min="10"
                        max="40"
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
                        max="40"
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
        </fieldset>
    </div>
</div>