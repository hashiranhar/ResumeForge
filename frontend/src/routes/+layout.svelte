<script>
    import '../app.css';
    import { onMount } from 'svelte';
    import { darkMode } from '$lib/stores/theme.js';
    import Header from '$lib/components/layout/Header.svelte';
    import Toast from '$lib/components/common/Toast.svelte';
    
    onMount(() => {
        // Ensure theme is applied correctly
        const isDark = localStorage.getItem('darkMode') === 'true' || 
                      (localStorage.getItem('darkMode') === null && 
                       window.matchMedia('(prefers-color-scheme: dark)').matches);
        
        darkMode.set(isDark);
        
        if (isDark) {
            document.documentElement.classList.add('dark');
            document.body.style.backgroundColor = '#0a0a0a';
            document.body.style.color = '#ffffff';
        } else {
            document.documentElement.classList.remove('dark');
            document.body.style.backgroundColor = '#ffffff';
            document.body.style.color = '#000000';
        }
    });
</script>

<div class="min-h-screen bg-white dark:bg-black text-gray-900 dark:text-white">
    <Header />
    <main>
        <slot />
    </main>
    <Toast />
</div>