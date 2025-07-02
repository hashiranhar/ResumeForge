<script>
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { addToast } from '$lib/stores/toast.js';
    import Button from '$lib/components/common/Button.svelte';
    import Input from '$lib/components/common/Input.svelte';

    let password = '';
    let confirmPassword = '';
    let loading = false;
    let success = false;
    let error = '';
    let token = '';

    $: token = $page.url.searchParams.get('token') || '';

    async function handleSubmit() {
        error = '';
        if (!password || !confirmPassword) {
            error = 'Please fill in all fields.';
            return;
        }
        if (password !== confirmPassword) {
            error = 'Passwords do not match.';
            return;
        }
        if (password.length < 8) {
            error = 'Password must be at least 8 characters.';
            return;
        }
        loading = true;
        try {
            const res = await fetch('/api/auth/reset-password', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token, new_password: password })
            });
            if (res.ok) {
                success = true;
                addToast('Password reset successful! You can now sign in.', 'success');
                setTimeout(() => goto('/auth/login'), 2000);
            } else {
                const data = await res.json();
                error = data.detail || 'Failed to reset password.';
            }
        } catch {
            error = 'Failed to reset password.';
        }
        loading = false;
    }
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-black py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
        <div class="text-center">
            <h2 class="mt-6 text-3xl font-bold text-gray-900 dark:text-white">
                Reset your password
            </h2>
            <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">
                Enter your new password below.
            </p>
        </div>
        {#if success}
            <div class="text-green-600 dark:text-green-400 text-center">
                Password reset! Redirecting to sign in...
            </div>
        {:else}
            <form class="mt-8 space-y-6" on:submit|preventDefault={handleSubmit}>
                {#if error}
                    <div class="bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg p-4">
                        <p class="text-sm text-red-600 dark:text-red-300">{error}</p>
                    </div>
                {/if}
                <Input
                    id="password"
                    type="password"
                    label="New Password"
                    placeholder="Enter new password"
                    bind:value={password}
                    required
                />
                <Input
                    id="confirmPassword"
                    type="password"
                    label="Confirm Password"
                    placeholder="Confirm new password"
                    bind:value={confirmPassword}
                    required
                />
                <Button type="submit" size="lg" variant="primary" {loading} disabled={loading}>
                    Reset Password
                </Button>
            </form>
        {/if}
    </div>
</div>