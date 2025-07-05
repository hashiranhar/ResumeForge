<script>
    import { authService, isAuthenticated } from '$lib/stores/auth.js';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { addToast } from '$lib/stores/toast.js';
    import { isValidEmail } from '$lib/utils/helpers.js';
    import Button from '$lib/components/common/Button.svelte';
    import Input from '$lib/components/common/Input.svelte';
    import { FileText, Mail, Lock, AlertCircle } from 'lucide-svelte';

    let email = '';
    let password = '';
    let loading = false;
    let showVerificationPrompt = false;
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
        showVerificationPrompt = false;

        try {
            const result = await authService.login(email, password);
            
            if (result.success) {
                addToast('Welcome back!', 'success');
                goto('/dashboard');
            } else if (result.requiresVerification) {
                showVerificationPrompt = true;
                errors.general = result.error;
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

    function goToVerification() {
        goto(`/auth/verify-email?email=${encodeURIComponent(email)}`);
    }
</script>

<svelte:head>
    <title>Sign In - ResumeForge</title>
</svelte:head>

<div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-black py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
        <!-- Header -->
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

        <!-- Form -->
        <form class="mt-8 space-y-6" on:submit|preventDefault={handleSubmit}>
            <!-- General Error -->
            {#if errors.general && !showVerificationPrompt}
                <div class="bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg p-4">
                    <div class="flex">
                        <AlertCircle class="h-5 w-5 text-red-400 dark:text-red-300" />
                        <p class="ml-3 text-sm text-red-600 dark:text-red-300">{errors.general}</p>
                    </div>
                </div>
            {/if}

            <!-- Email Verification Prompt -->
            {#if showVerificationPrompt}
                <div class="bg-yellow-50 dark:bg-yellow-900 border border-yellow-200 dark:border-yellow-700 rounded-lg p-4">
                    <div class="flex">
                        <Mail class="h-5 w-5 text-yellow-400 dark:text-yellow-300" />
                        <div class="ml-3">
                            <h3 class="text-sm font-medium text-yellow-800 dark:text-yellow-200">
                                Email Verification Required
                            </h3>
                            <p class="mt-2 text-sm text-yellow-700 dark:text-yellow-300">
                                {errors.general}
                            </p>
                            <div class="mt-4">
                                <Button
                                    type="button"
                                    variant="secondary"
                                    size="sm"
                                    on:click={goToVerification}
                                >
                                    Verify Email Now
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
            {/if}

            <div class="space-y-4">
                <div>
                    <Input
                        id="email"
                        type="email"
                        label="Email address"
                        placeholder="Enter your email"
                        bind:value={email}
                        error={errors.email}
                        required
                        on:keydown={handleKeydown}
                        icon={Mail}
                    />
                </div>

                <div>
                    <Input
                        id="password"
                        type="password"
                        label="Password"
                        placeholder="Enter your password"
                        bind:value={password}
                        error={errors.password}
                        required
                        on:keydown={handleKeydown}
                        icon={Lock}
                    />
                </div>
            </div>

            <div class="flex items-center justify-between">
                <div class="text-sm">
                    <a href="/auth/forgot-password" class="font-medium text-primary-600 dark:text-primary-400 hover:text-primary-500 dark:hover:text-primary-300">
                        Forgot your password?
                    </a>
                </div>
            </div>

            <div>
                <Button
                    type="submit"
                    variant="primary"
                    size="lg"
                    {loading}
                    disabled={loading}
                    class="w-full"
                >
                    {#if loading}
                        Signing in...
                    {:else}
                        Sign in
                    {/if}
                </Button>
            </div>
        </form>

        <!-- Additional Help -->
        <div class="mt-6 text-center">
            <p class="text-xs text-gray-500 dark:text-gray-400">
                Having trouble? Make sure your email is verified before signing in.
            </p>
        </div>
    </div>
</div>