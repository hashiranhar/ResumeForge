<script>
    export let variant = 'primary'; // primary, secondary, outline, ghost
    export let size = 'md'; // sm, md, lg
    export let href = null;
    export let type = 'button';
    export let disabled = false;
    export let loading = false;
    export let className = '';

    const variants = {
        primary: 'bg-primary-600 hover:bg-primary-700 text-white border-transparent dark:bg-primary-600 dark:hover:bg-primary-700',
        secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-900 border-transparent dark:bg-gray-600 dark:hover:bg-gray-700 dark:text-white',
        outline: 'border-gray-300 text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700',
        ghost: 'text-gray-700 hover:bg-gray-100 border-transparent dark:text-gray-300 dark:hover:bg-gray-700'
    };

    const sizes = {
        sm: 'px-3 py-1.5 text-sm',
        md: 'px-4 py-2 text-sm',
        lg: 'px-6 py-3 text-base'
    };

    const baseClasses = 'inline-flex items-center justify-center font-medium rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 dark:focus:ring-offset-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed border';
    
    $: classes = `${baseClasses} ${variants[variant]} ${sizes[size]} ${className}`.trim();
</script>

{#if href}
    <a {href} class={classes}>
        {#if loading}
            <div class="spinner mr-2"></div>
        {/if}
        <slot />
    </a>
{:else}
    <button 
        {type}
        {disabled}
        class={classes}
        on:click
    >
        {#if loading}
            <div class="spinner mr-2"></div>
        {/if}
        <slot />
    </button>
{/if}

<style>
    .spinner {
        width: 16px;
        height: 16px;
        border: 2px solid transparent;
        border-top: 2px solid currentColor;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>