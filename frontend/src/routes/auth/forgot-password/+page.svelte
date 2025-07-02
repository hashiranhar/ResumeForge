<script>
    import { onMount } from 'svelte';
    import { addToast } from '$lib/stores/toast.js';
    import Button from '$lib/components/common/Button.svelte';
    import Input from '$lib/components/common/Input.svelte';

    let email = '';
    let loading = false;
    let success = false;

    async function handleSubmit() {
        loading = true;
        try {
            const res = await fetch('/api/auth/forgot-password', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });
            if (res.ok) {
                success = true;
            } else {
                addToast('Failed to send reset email', 'error');
            }
        } catch {
            addToast('Failed to send reset email', 'error');
        }
        loading = false;
    }
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-black py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
        <div class="text-center">
            <h2 class="mt-6 text-3xl font-bold text-gray-900 dark:text-white">
                Forgot your password?
            </h2>
            <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">
                Enter your email and we'll send you a reset link.
            </p>
        </div>
        {#if success}
            <div class="text-green-600 dark:text-green-400 text-center">
                If your email is registered, a reset link has been sent.
            </div>
        {:else}
            <form class="mt-8 space-y-6" on:submit|preventDefault={handleSubmit}>
                <Input
                    id="email"
                    type="email"
                    label="Email address"
                    placeholder="Enter your email"
                    bind:value={email}
                    required
                />
                <Button type="submit" size="lg" variant="primary" {loading} disabled={loading}>
                    Send Reset Link
                </Button>
            </form>
        {/if}
    </div>
</div>