<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { subscriptionService } from '$lib/stores/subscription.js';
    import { addToast } from '$lib/stores/toast.js';
    import Button from '$lib/components/common/Button.svelte';
    import { CheckCircle, ArrowRight, Zap, FileText, Calendar } from 'lucide-svelte';

    let loading = true;
    let subscriptionData = null;
    let error = null;

    onMount(async () => {
        // Get session_id from URL
        const sessionId = $page.url.searchParams.get('session_id');
        
        if (!sessionId) {
            error = 'No session ID provided';
            loading = false;
            return;
        }

        try {
            // Refresh subscription data
            await subscriptionService.loadCurrentSubscription();
            await subscriptionService.loadUsage();
            
            // Get updated subscription
            const result = await subscriptionService.loadCurrentSubscription();
            if (result.success) {
                subscriptionData = result.data;
                addToast('Subscription activated successfully!', 'success');
            } else {
                error = 'Failed to load subscription details';
            }
        } catch (err) {
            error = 'Failed to activate subscription';
        } finally {
            loading = false;
        }
    });

    function handleContinue() {
        goto('/dashboard');
    }

    function handleViewSubscription() {
        goto('/subscription');
    }

    function formatPrice(pennies) {
        if (pennies === 0) return 'Free';
        const pounds = pennies / 100;
        return `£${pounds}`;
    }
</script>

<svelte:head>
    <title>Payment Success - ResumeForge</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 dark:bg-black flex items-center justify-center p-4">
    <div class="max-w-md w-full">
        {#if loading}
            <!-- Loading State -->
            <div class="bg-white dark:bg-gray-900 rounded-xl shadow-lg p-8 text-center">
                <div class="animate-spin w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full mx-auto mb-4"></div>
                <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                    Activating Your Subscription
                </h2>
                <p class="text-gray-600 dark:text-gray-400">
                    Please wait while we set up your account...
                </p>
            </div>

        {:else if error}
            <!-- Error State -->
            <div class="bg-white dark:bg-gray-900 rounded-xl shadow-lg p-8 text-center">
                <div class="w-16 h-16 bg-red-100 dark:bg-red-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </div>
                <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                    Payment Error
                </h2>
                <p class="text-gray-600 dark:text-gray-400 mb-6">
                    {error}
                </p>
                <div class="space-y-3">
                    <Button on:click={handleViewSubscription} className="w-full">
                        View Subscription
                    </Button>
                    <Button variant="outline" href="/support" className="w-full">
                        Contact Support
                    </Button>
                </div>
            </div>

        {:else}
            <!-- Success State -->
            <div class="bg-white dark:bg-gray-900 rounded-xl shadow-lg p-8 text-center">
                <!-- Success Icon -->
                <div class="w-16 h-16 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center mx-auto mb-6">
                    <CheckCircle class="w-10 h-10 text-green-500" />
                </div>

                <!-- Success Message -->
                <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                    Welcome to {subscriptionData?.display_name || 'Premium'}!
                </h1>
                <p class="text-gray-600 dark:text-gray-400 mb-8">
                    Your subscription has been activated successfully. You now have access to all premium features.
                </p>

                <!-- Subscription Details -->
                {#if subscriptionData}
                    <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 mb-8">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                            Your New Plan
                        </h3>
                        
                        <div class="space-y-4">
                            <!-- Plan Info -->
                            <div class="flex items-center justify-between">
                                <span class="text-gray-600 dark:text-gray-400">Plan</span>
                                <span class="font-medium text-gray-900 dark:text-white">
                                    {subscriptionData.display_name}
                                </span>
                            </div>
                            
                            <div class="flex items-center justify-between">
                                <span class="text-gray-600 dark:text-gray-400">Price</span>
                                <span class="font-medium text-gray-900 dark:text-white">
                                    {formatPrice(subscriptionData.monthly_price_pennies)}/month
                                </span>
                            </div>

                            <!-- Features -->
                            <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
                                <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3">
                                    What you get:
                                </h4>
                                <div class="space-y-2">
                                    <div class="flex items-center space-x-2 text-sm">
                                        <Zap class="h-4 w-4 text-primary-500" />
                                        <span class="text-gray-700 dark:text-gray-300">
                                            {subscriptionData.api_calls_per_day} AI calls per day
                                        </span>
                                    </div>
                                    <div class="flex items-center space-x-2 text-sm">
                                        <FileText class="h-4 w-4 text-primary-500" />
                                        <span class="text-gray-700 dark:text-gray-300">
                                            Up to {subscriptionData.max_cvs} CVs
                                        </span>
                                    </div>
                                    <div class="flex items-center space-x-2 text-sm">
                                        <Calendar class="h-4 w-4 text-primary-500" />
                                        <span class="text-gray-700 dark:text-gray-300">
                                            Premium templates & features
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                {/if}

                <!-- Action Buttons -->
                <div class="space-y-3">
                    <Button on:click={handleContinue} className="w-full">
                        <ArrowRight class="w-4 h-4 mr-2" />
                        Start Building CVs
                    </Button>
                    <Button variant="outline" on:click={handleViewSubscription} className="w-full">
                        View Subscription Details
                    </Button>
                </div>

                <!-- Additional Info -->
                <div class="mt-8 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
                    <h4 class="text-sm font-medium text-blue-900 dark:text-blue-100 mb-2">
                        🎉 What's next?
                    </h4>
                    <ul class="text-xs text-blue-800 dark:text-blue-200 text-left space-y-1">
                        <li>• Use AI features to enhance your CV content</li>
                        <li>• Try the ATS scoring to optimize for job applications</li>
                        <li>• Explore premium templates for different industries</li>
                        <li>• Chat with our AI assistant for personalized advice</li>
                    </ul>
                </div>
            </div>
        {/if}
    </div>
</div>