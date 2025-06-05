<script>
    export let variant = 'primary'; // primary, secondary, outline, danger
    export let size = 'md'; // sm, md, lg
    export let disabled = false;
    export let loading = false;
    export let type = 'button';
    export let href = null;

    const variants = {
        primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500',
        secondary: 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500',
        outline: 'border border-gray-300 text-gray-700 bg-white hover:bg-gray-50 focus:ring-primary-500',
        danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500'
    };

    const sizes = {
        sm: 'px-3 py-1.5 text-sm',
        md: 'px-4 py-2 text-sm',
        lg: 'px-6 py-3 text-base'
    };

    const baseClasses = 'inline-flex items-center justify-center font-medium rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed';
    
    $: classes = `${baseClasses} ${variants[variant]} ${sizes[size]}`;
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