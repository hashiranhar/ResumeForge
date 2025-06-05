<script>
    import { darkMode } from '$lib/stores/theme.js';
    import { Sun, Moon } from 'lucide-svelte';
    
    export let size = 'md'; // 'sm', 'md', 'lg'
    
    const sizes = {
        sm: 'h-4 w-4',
        md: 'h-5 w-5',
        lg: 'h-6 w-6'
    };
    
    function toggle() {
        darkMode.toggle();
    }
</script>

<button
    on:click={toggle}
    class="p-2 rounded-lg transition-colors hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
    aria-label={$darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
    title={$darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
>
    {#if $darkMode}
        <Sun class="{sizes[size]} text-yellow-500" />
    {:else}
        <Moon class="{sizes[size]} text-gray-600 dark:text-gray-300" />
    {/if}
</button>