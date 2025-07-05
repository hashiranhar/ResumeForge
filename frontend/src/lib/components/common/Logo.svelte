
<script>
    export let size = 'xl'; 
    export let showText = true;
    export let href = '/';
    export let className = '';

    // Size configurations
    const sizes = {
        sm: { img: 'h-6 w-6', text: 'text-lg' },
        md: { img: 'h-8 w-8', text: 'text-xl' },
        lg: { img: 'h-12 w-12', text: 'text-2xl' },
        xl: { img: 'h-16 w-16', text: 'text-3xl' }
    };

    $: sizeConfig = sizes[size] || sizes.md;
</script>

<a {href} class="flex items-center space-x-2 {className}">
    <!-- Logo Image -->
    <img 
        src="/logo.png" 
        alt="ResumeForge Logo" 
        class="{sizeConfig.img} object-contain"
    />
    
    <!-- Logo Text (optional) -->
    {#if showText}
        <span class="{sizeConfig.text} font-bold text-gray-900 dark:text-white">
            ResumeForge
        </span>
    {/if}
</a>