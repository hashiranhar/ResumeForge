<script>
    export let variant = 'primary'; // primary, secondary, outline, ghost, danger
    export let size = 'md'; // sm, md, lg
    export let type = 'button';
    export let disabled = false;
    export let loading = false;
    export let href = null;
    export let target = null;
    export let download = null;
    export let title = ''; // Add title prop for tooltips
    
    // Handle class prop properly - accept both class and className
    let classNameProp = '';
    export { classNameProp as class };
    export let className = ''; // Accept className as well for compatibility

    // Base button styles
    const baseClasses = 'inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';

    // Variant styles
    const variants = {
        primary: 'bg-primary-600 hover:bg-primary-700 text-white focus:ring-primary-500 dark:bg-primary-500 dark:hover:bg-primary-600',
        secondary: 'bg-gray-600 hover:bg-gray-700 text-white focus:ring-gray-500 dark:bg-gray-500 dark:hover:bg-gray-600',
        outline: 'border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 focus:ring-primary-500',
        ghost: 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 focus:ring-primary-500',
        danger: 'bg-red-600 hover:bg-red-700 text-white focus:ring-red-500 dark:bg-red-500 dark:hover:bg-red-600',
        default: 'bg-primary-600 hover:bg-primary-700 text-white focus:ring-primary-500 dark:bg-primary-500 dark:hover:bg-primary-600'
    };

    // Size styles
    const sizes = {
        sm: 'px-3 py-1.5 text-sm',
        md: 'px-4 py-2 text-sm',
        lg: 'px-6 py-3 text-base'
    };

    // Use whichever class prop is provided
    $: customClasses = classNameProp || className || '';
    $: buttonClasses = `${baseClasses} ${variants[variant]} ${sizes[size]} ${customClasses}`.trim();
</script>

{#if href}
    <a
        {href}
        {target}
        {download}
        {title}
        class={buttonClasses}
        class:opacity-50={disabled}
        class:cursor-not-allowed={disabled}
        on:click
    >
        {#if loading}
            <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
        {/if}
        <slot />
    </a>
{:else}
    <button
        {type}
        {disabled}
        {title}
        class={buttonClasses}
        on:click
    >
        {#if loading}
            <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
        {/if}
        <slot />
    </button>
{/if}