<script>
    import '../app.css';
    import { onMount } from 'svelte';
    import { authService } from '$lib/stores/auth.js';
    import Header from '$lib/components/layout/Header.svelte';
    import Toast from '$lib/components/common/Toast.svelte';

    onMount(() => {
        // Check authentication status on app load
        authService.checkAuth();
    });
</script>

<div class="min-h-screen bg-gray-50">
    <Header />
    
    <main>
        <slot />
    </main>
    
    <Toast />
</div>