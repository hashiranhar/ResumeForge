<script>
    import { authService, isAuthenticated } from '$lib/stores/auth.js';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { addToast } from '$lib/stores/toast.js';
    import { isValidEmail } from '$lib/utils/helpers.js';
    import Button from '$lib/components/common/Button.svelte';
    import Input from '$lib/components/common/Input.svelte';
    import { FileText } from 'lucide-svelte';

    let email = '';
    let password = '';
    let confirmPassword = '';
    let loading = false;
    let errors = {
        email: '',
        password: '',
        confirmPassword: '',
        general: ''
    };

    // Redirect if already authenticated
    onMount(() => {
        if ($isAuthenticated) {
            goto('/dashboard');
        }
    });

    function validateForm() {
        errors = { email: '', password: '', confirmPassword: '', general: '' };
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
        } else if (password.length < 6) {
            errors.password = 'Password must be at least 6 characters';
            isValid = false;
        }

        if (!confirmPassword) {
            errors.confirmPassword = 'Please confirm your password';
            isValid = false;
        } else if (password !== confirmPassword) {
            errors.confirmPassword = 'Passwords do not match';
            isValid = false;
        }

        return isValid;
    }

    async function handleSubmit() {
        if (!validateForm()) return;

        loading = true;
        errors.general = '';

        try {
            const result = await authService.register(email, password);
            
            if (result.success) {
                addToast('Account created successfully! Welcome to ResumeForge!', 'success');
                goto('/dashboard');
            } else {
                errors.general = result.error || 'Registration failed';
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
    <title>Sign Up - ResumeForge</title>
</svelte:head>

<div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
        <!-- Header -->
        <div class="text-center">
            <div class="flex justify-center">
                <FileText class="h-12 w-12 text-primary-600" />
            </div>
            <h2 class="mt-6 text-3xl font-bold text-gray-900">
                Create your account
            </h2>
            <p class="mt-2 text-sm text-gray-600">
                Or
                <a href="/auth/login" class="font-medium text-primary-600 hover:text-primary-500">
                    sign in to existing account
                </a>
            </p>
        </div>

        <!-- Form -->
        <form class="mt-8 space-y-6" on:submit|preventDefault={handleSubmit}>
            {#if errors.general}
                <div class="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p class="text-sm text-red-600">{errors.general}</p>
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
                    placeholder="Choose a password (min. 6 characters)"
                    bind:value={password}
                    error={errors.password}
                    required
                    on:keydown={handleKeydown}
                />

                <Input
                    id="confirmPassword"
                    type="password"
                    label="Confirm Password"
                    placeholder="Confirm your password"
                    bind:value={confirmPassword}
                    error={errors.confirmPassword}
                    required
                    on:keydown={handleKeydown}
                />
            </div>

            <div class="text-sm text-gray-600">
                By creating an account, you agree to our 
                <a href="/terms" class="text-primary-600 hover:text-primary-500">Terms of Service</a>
                and 
                <a href="/privacy" class="text-primary-600 hover:text-primary-500">Privacy Policy</a>.
            </div>

            <Button 
                type="submit" 
                size="lg" 
                variant="primary" 
                {loading}
                disabled={loading}
                class="w-full"
            >
                {#if loading}
                    Creating account...
                {:else}
                    Create account
                {/if}
            </Button>
        </form>

        <!-- Demo option -->
        <div class="mt-6">
            <div class="relative">
                <div class="absolute inset-0 flex items-center">
                    <div class="w-full border-t border-gray-300" />
                </div>
                <div class="relative flex justify-center text-sm">
                    <span class="px-2 bg-gray-50 text-gray-500">Or</span>
                </div>
            </div>

            <div class="mt-6">
                <Button 
                    variant="outline" 
                    size="lg" 
                    href="/editor?demo=true"
                    class="w-full"
                >
                    Try Demo (No Account Required)
                </Button>
            </div>
        </div>
    </div>
</div>