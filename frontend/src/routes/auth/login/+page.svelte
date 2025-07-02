<script>
    import { authService, isAuthenticated } from '$lib/stores/auth.js';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { addToast } from '$lib/stores/toast.js';
    import { isValidEmail } from '$lib/utils/helpers.js';
    import Button from '$lib/components/common/Button.svelte';
    import Input from '$lib/components/common/Input.svelte';
    import { FileText, Mail, Lock } from 'lucide-svelte';

    let email = '';
    let password = '';
    let loading = false;
    let errors = {
        email: '',
        password: '',
        general: ''
    };

    // Redirect if already authenticated
    onMount(() => {
        if ($isAuthenticated) {
            goto('/dashboard');
        }
    });

    function validateForm() {
        errors = { email: '', password: '', general: '' };
        let isValid = true;

        if (!email) {
            errors.email = 'Email is required';
            isValid = false;
        } else if (!isValidEmail(email)) {
            errors.email = 'Please enter a valid email address';
            isValid = false;
        }

        if (!password) {
            errors.password = 'Password is required';
            isValid = false;
        }

        return isValid;
    }

    async function handleSubmit() {
        if (!validateForm()) return;

        loading = true;
        errors.general = '';

        try {
            const result = await authService.login(email, password);
            
            if (result.success) {
                addToast('Welcome back!', 'success');
                goto('/dashboard');
            } else {
                errors.general = result.error || 'Login failed';
            }
        } catch (error) {
            errors.general = 'An unexpected error occurred';
        } finally {
            loading = false;
        }
    }

    function handleKeydown(event) {
        if (event.key === 'Enter') {
            handleSubmit();
        }
    }
</script>

<svelte:head>
    <title>Sign In - ResumeForge</title>
</svelte:head>

<!-- FIXED: Added dark mode styling -->
<div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-black py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
        <!-- Header - FIXED: Added dark mode styling -->
        <div class="text-center">
            <div class="flex justify-center">
                <FileText class="h-12 w-12 text-primary-600 dark:text-primary-400" />
            </div>
            <h2 class="mt-6 text-3xl font-bold text-gray-900 dark:text-white">
                Sign in to your account
            </h2>
            <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">
                Or
                <a href="/auth/register" class="font-medium text-primary-600 dark:text-primary-400 hover:text-primary-500 dark:hover:text-primary-300">
                    create a new account
                </a>
            </p>
        </div>

        <!-- Form - FIXED: Added dark mode styling -->
        <form class="mt-8 space-y-6" on:submit|preventDefault={handleSubmit}>
            {#if errors.general}
                <div class="bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg p-4">
                    <p class="text-sm text-red-600 dark:text-red-300">{errors.general}</p>
                </div>
            {/if}

            <div class="space-y-4">
                <Input
                    id="email"
                    type="email"
                    label="Email address"
                    placeholder="Enter your email"
                    bind:value={email}
                    error={errors.email}
                    required
                    on:keydown={handleKeydown}
                />

                <Input
                    id="password"
                    type="password"
                    label="Password"
                    placeholder="Enter your password"
                    bind:value={password}
                    error={errors.password}
                    required
                    on:keydown={handleKeydown}
                />
            </div>

            <!-- FIXED: Added dark mode styling -->
            <div class="flex items-center justify-center">
                <div class="text-sm">
                    <a href="/auth/forgot-password" class="font-medium text-primary-600 dark:text-primary-400 hover:text-primary-500 dark:hover:text-primary-300">
                        Forgot your password?
                    </a>
                </div>
            </div>

            <!-- Centered sign in button -->
            <div class="flex justify-center">
                <Button 
                    type="submit" 
                    size="lg" 
                    variant="primary" 
                    {loading}
                    disabled={loading}
                >
                    {#if loading}
                        Signing in...
                    {:else}
                        Sign in
                    {/if}
                </Button>
            </div>
        </form>

        <!-- Demo option -->
        <div class="mt-6">
            <div class="relative">
                <div class="absolute inset-0 flex items-center">
                    <div class="w-full border-t border-gray-300 dark:border-gray-600" />
                </div>
                <div class="relative flex justify-center text-sm">
                    <span class="px-2 bg-gray-50 dark:bg-black text-gray-500 dark:text-gray-400">Or</span>
                </div>
            </div>

            <!-- Added flex container for centering -->
            <div class="mt-6 flex justify-center">
                <Button 
                    variant="outline" 
                    size="lg" 
                    href="/editor?demo=true"
                >
                    Try Demo (No Account Required)
                </Button>
            </div>
        </div>
    </div>
</div>