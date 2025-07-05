<script>
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { addToast } from '$lib/stores/toast.js';
    import Button from '$lib/components/common/Button.svelte';
    import Input from '$lib/components/common/Input.svelte';
    import { Mail, CheckCircle, AlertCircle, RefreshCw } from 'lucide-svelte';

    let email = '';
    let verificationCode = '';
    let loading = false;
    let resendLoading = false;
    let verified = false;
    let errors = {
        verificationCode: '',
        general: ''
    };

    // Get email from URL params if available
    onMount(() => {
        const urlParams = new URLSearchParams(window.location.search);
        email = urlParams.get('email') || '';
        
        if (!email) {
            goto('/auth/register');
        }
    });

    function validateForm() {
        errors = { verificationCode: '', general: '' };
        let isValid = true;

        if (!verificationCode) {
            errors.verificationCode = 'Verification code is required';
            isValid = false;
        } else if (verificationCode.length !== 6) {
            errors.verificationCode = 'Verification code must be 6 digits';
            isValid = false;
        } else if (!/^\d{6}$/.test(verificationCode)) {
            errors.verificationCode = 'Verification code must contain only numbers';
            isValid = false;
        }

        return isValid;
    }

    async function handleVerification() {
        if (!validateForm()) return;

        loading = true;
        errors.general = '';

        try {
            const response = await fetch('/api/auth/verify-email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email,
                    verification_code: verificationCode
                })
            });

            const data = await response.json();

            if (data.success) {
                verified = true;
                addToast('Email verified successfully! You can now log in.', 'success');
                
                // Redirect to login after a short delay
                setTimeout(() => {
                    goto('/auth/login');
                }, 2000);
            } else {
                errors.general = data.error || 'Verification failed';
            }
        } catch (error) {
            errors.general = 'An unexpected error occurred';
        } finally {
            loading = false;
        }
    }

    async function handleResendCode() {
        resendLoading = true;
        errors.general = '';

        try {
            const response = await fetch('/api/auth/resend-verification', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email })
            });

            const data = await response.json();

            if (data.success) {
                addToast('Verification code sent successfully!', 'success');
                verificationCode = ''; // Clear the input
            } else {
                errors.general = data.error || 'Failed to resend verification code';
            }
        } catch (error) {
            errors.general = 'An unexpected error occurred';
        } finally {
            resendLoading = false;
        }
    }

    function handleKeydown(event) {
        if (event.key === 'Enter') {
            handleVerification();
        }
    }

    // Auto-format verification code input
    function formatVerificationCode(value) {
        return value.replace(/\D/g, '').slice(0, 6);
    }

    function handleCodeInput(event) {
        verificationCode = formatVerificationCode(event.target.value);
    }
</script>

<svelte:head>
    <title>Verify Email - ResumeForge</title>
</svelte:head>

<div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-black py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
        <!-- Header -->
        <div class="text-center">
            <div class="flex justify-center">
                {#if verified}
                    <CheckCircle class="h-12 w-12 text-green-600 dark:text-green-400" />
                {:else}
                    <Mail class="h-12 w-12 text-primary-600 dark:text-primary-400" />
                {/if}
            </div>
            <h2 class="mt-6 text-3xl font-bold text-gray-900 dark:text-white">
                {#if verified}
                    Email Verified!
                {:else}
                    Verify Your Email
                {/if}
            </h2>
            <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">
                {#if verified}
                    Your email has been successfully verified. Redirecting to login...
                {:else}
                    We've sent a verification code to <strong>{email}</strong>
                {/if}
            </p>
        </div>

        {#if !verified}
            <!-- Verification Form -->
            <form class="mt-8 space-y-6" on:submit|preventDefault={handleVerification}>
                {#if errors.general}
                    <div class="bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg p-4">
                        <div class="flex">
                            <AlertCircle class="h-5 w-5 text-red-400 dark:text-red-300" />
                            <p class="ml-3 text-sm text-red-600 dark:text-red-300">{errors.general}</p>
                        </div>
                    </div>
                {/if}

                <div class="space-y-4">
                    <div>
                        <label for="verification-code" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Verification Code
                        </label>
                        <input
                            id="verification-code"
                            type="text"
                            inputmode="numeric"
                            placeholder="Enter 6-digit code"
                            bind:value={verificationCode}
                            on:input={handleCodeInput}
                            on:keydown={handleKeydown}
                            class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg text-center text-2xl font-mono tracking-widest bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:focus:ring-primary-400 dark:focus:border-primary-400"
                            class:border-red-500={errors.verificationCode}
                            class:dark:border-red-400={errors.verificationCode}
                            maxlength="6"
                            required
                        />
                        {#if errors.verificationCode}
                            <p class="mt-2 text-sm text-red-600 dark:text-red-400">{errors.verificationCode}</p>
                        {/if}
                    </div>
                </div>

                <div class="space-y-4">
                    <Button
                        type="submit"
                        variant="primary"
                        size="lg"
                        {loading}
                        disabled={loading}
                        class="w-full"
                    >
                        {#if loading}
                            Verifying...
                        {:else}
                            Verify Email
                        {/if}
                    </Button>

                    <!-- Resend Code Button -->
                    <div class="text-center">
                        <p class="text-sm text-gray-600 dark:text-gray-300 mb-2">
                            Didn't receive the code?
                        </p>
                        <button
                            type="button"
                            on:click={handleResendCode}
                            disabled={resendLoading}
                            class="inline-flex items-center text-sm font-medium text-primary-600 dark:text-primary-400 hover:text-primary-500 dark:hover:text-primary-300 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {#if resendLoading}
                                <RefreshCw class="h-4 w-4 mr-2 animate-spin" />
                                Sending...
                            {:else}
                                <RefreshCw class="h-4 w-4 mr-2" />
                                Resend Code
                            {/if}
                        </button>
                    </div>
                </div>
            </form>

            <!-- Help Text -->
            <div class="mt-6 p-4 bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded-lg">
                <div class="flex">
                    <AlertCircle class="h-5 w-5 text-blue-400 dark:text-blue-300" />
                    <div class="ml-3">
                        <h3 class="text-sm font-medium text-blue-800 dark:text-blue-200">
                            Need Help?
                        </h3>
                        <p class="mt-1 text-sm text-blue-700 dark:text-blue-300">
                            • Check your spam/junk folder<br>
                            • Make sure you entered the correct email<br>
                            • The code expires in 15 minutes<br>
                            • You have 3 attempts per code
                        </p>
                    </div>
                </div>
            </div>
        {:else}
            <!-- Success State -->
            <div class="mt-8 p-6 bg-green-50 dark:bg-green-900 border border-green-200 dark:border-green-700 rounded-lg text-center">
                <CheckCircle class="h-16 w-16 text-green-600 dark:text-green-400 mx-auto mb-4" />
                <h3 class="text-lg font-medium text-green-800 dark:text-green-200 mb-2">
                    Verification Complete!
                </h3>
                <p class="text-sm text-green-700 dark:text-green-300">
                    Your email has been verified successfully. You will be redirected to the login page in a moment.
                </p>
            </div>
        {/if}

        <!-- Back to Login -->
        <div class="text-center">
            <a 
                href="/auth/login" 
                class="text-sm font-medium text-primary-600 dark:text-primary-400 hover:text-primary-500 dark:hover:text-primary-300"
            >
                ← Back to Login
            </a>
        </div>
    </div>
</div>