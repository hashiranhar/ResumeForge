<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { isAuthenticated } from '$lib/stores/auth.js';
    import { 
        currentSubscription, 
        availablePlans, 
        usageData, 
        subscriptionService,
        isSubscriptionLoading 
    } from '$lib/stores/subscription.js';
    import { addToast } from '$lib/stores/toast.js';
    import UsageDashboardWidget from '$lib/components/subscription/UsageDashboardWidget.svelte';
    import UpgradeModal from '$lib/components/subscription/UpgradeModal.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import { 
        CreditCard, Calendar, DollarSign, Settings, AlertCircle, 
        CheckCircle, ArrowRight, Zap, FileText 
    } from 'lucide-svelte';

    let showUpgradeModal = false;
    let showCancelModal = false;
    let cancellingSubscription = false;

    // Redirect if not authenticated
    $: if (!$isAuthenticated) {
        goto('/auth/login');
    }

    onMount(async () => {
        if ($isAuthenticated) {
            await Promise.all([
                subscriptionService.loadCurrentSubscription(),
                subscriptionService.loadPlans(),
                subscriptionService.loadUsage()
            ]);
        }
    });

    function formatPrice(pennies, cycle = 'monthly') {
        if (pennies === 0) return 'Free';
        const pounds = pennies / 100;
        return `£${pounds}/${cycle === 'yearly' ? 'year' : 'month'}`;
    }

    function formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    function handleUpgrade() {
        showUpgradeModal = true;
    }

    function handleCancelSubscription() {
        showCancelModal = true;
    }

    async function confirmCancelSubscription() {
        cancellingSubscription = true;
        
        try {
            const result = await subscriptionService.cancelSubscription();
            if (result.success) {
                addToast('Subscription cancelled successfully', 'success');
                showCancelModal = false;
            } else {
                addToast(result.error || 'Failed to cancel subscription', 'error');
            }
        } catch (error) {
            addToast('Failed to cancel subscription', 'error');
        } finally {
            cancellingSubscription = false;
        }
    }

    async function handleManageSubscription() {
        try {
            const response = await authenticatedFetch("/api/subscription/customer-portal", {
                method: "POST",
            });
            if (!response.ok) {
                addToast("Failed to open customer portal", "error");
                return;
            }
            const data = await response.json();
            if (data.portal_url) {
                window.location.href = data.portal_url;
            }
        } catch (err) {
            addToast("Failed to open customer portal", "error");
        }
    }

    // Get subscription status info
    $: subscriptionStatus = getSubscriptionStatus($currentSubscription);

    function getSubscriptionStatus(subscription) {
        if (!subscription) return { status: 'none', message: 'No active subscription' };
        
        if (subscription.name === 'free') {
            return { 
                status: 'free', 
                message: 'Free plan',
                color: 'gray'
            };
        }
        
        if (subscription.cancel_at_period_end) {
            return { 
                status: 'cancelling', 
                message: `Cancels on ${formatDate(subscription.current_period_end)}`,
                color: 'yellow'
            };
        }
        
        return { 
            status: 'active', 
            message: `Renews on ${formatDate(subscription.current_period_end)}`,
            color: 'green'
        };
    }
</script>

<svelte:head>
    <title>Subscription - ResumeForge</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 dark:bg-black">
    <div class="max-w-6xl mx-auto px-6 py-8">
        <!-- Header -->
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                Subscription Management
            </h1>
            <p class="text-gray-600 dark:text-gray-300">
                Manage your plan and monitor your usage
            </p>
        </div>

        {#if $isSubscriptionLoading}
            <div class="flex items-center justify-center py-12">
                <div class="animate-spin w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full"></div>
                <span class="ml-2 text-gray-600 dark:text-gray-300">Loading subscription details...</span>
            </div>
        {:else}
            <div class="grid lg:grid-cols-3 gap-8">
                <!-- Main Content -->
                <div class="lg:col-span-2 space-y-6">
                    <!-- Current Subscription Status -->
                    {#if $currentSubscription}
                        <div class="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
                            <div class="flex items-start justify-between mb-6">
                                <div>
                                    <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                                        Current Plan: {$currentSubscription.display_name}
                                    </h2>
                                    <div class="flex items-center space-x-2">
                                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {
                                            subscriptionStatus.color === 'green' ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400' :
                                            subscriptionStatus.color === 'yellow' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400' :
                                            'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
                                        }">
                                            {subscriptionStatus.status === 'active' ? 'Active' : 
                                             subscriptionStatus.status === 'cancelling' ? 'Cancelling' : 'Free'}
                                        </span>
                                        <span class="text-sm text-gray-500 dark:text-gray-400">
                                            {subscriptionStatus.message}
                                        </span>
                                    </div>
                                </div>
                                
                                {#if $currentSubscription.name !== 'free'}
                                    <div class="text-right">
                                        <div class="text-2xl font-bold text-gray-900 dark:text-white">
                                            {formatPrice($currentSubscription.monthly_price_pennies)}
                                        </div>
                                        <div class="text-sm text-gray-500 dark:text-gray-400">
                                            Billed monthly
                                        </div>
                                    </div>
                                {/if}
                            </div>

                            <!-- Plan Features -->
                            <div class="grid md:grid-cols-2 gap-4 mb-6">
                                <div class="flex items-center space-x-3">
                                    <Zap class="h-5 w-5 text-blue-500" />
                                    <span class="text-gray-700 dark:text-gray-300">
                                        {$currentSubscription.api_calls_per_day} API calls per day
                                    </span>
                                </div>
                                <div class="flex items-center space-x-3">
                                    <FileText class="h-5 w-5 text-green-500" />
                                    <span class="text-gray-700 dark:text-gray-300">
                                        {$currentSubscription.max_cvs} CVs maximum
                                    </span>
                                </div>
                            </div>

                            <!-- Action Buttons -->
                            <div class="flex items-center space-x-3">
                                {#if $currentSubscription.name === 'free'}
                                    <Button on:click={handleUpgrade}>
                                        <ArrowRight class="h-4 w-4 mr-2" />
                                        Upgrade Plan
                                    </Button>
                                {:else if $currentSubscription.name === 'basic'}
                                    <Button on:click={handleUpgrade}>
                                        <ArrowRight class="h-4 w-4 mr-2" />
                                        Upgrade to Pro
                                    </Button>
                                    <Button variant="outline" on:click={handleCancelSubscription}>
                                        Cancel Subscription
                                    </Button>
                                {:else}
                                    <Button variant="outline" on:click={handleCancelSubscription}>
                                        Cancel Subscription
                                    </Button>
                                {/if}
                            </div>
                        </div>
                    {/if}

                    <!-- Billing Management -->
                    {#if $currentSubscription && $currentSubscription.name !== 'free'}
                        <div class="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
                            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                                <Settings class="h-5 w-5 mr-2" />
                                Billing Management
                            </h3>
                            
                            <div class="grid md:grid-cols-2 gap-4">
                                <Button variant="outline" className="flex items-center justify-center">
                                    <CreditCard class="h-4 w-4 mr-2" />
                                    Update Payment Method
                                </Button>
                                
                                <Button variant="outline" className="flex items-center justify-center">
                                    <DollarSign class="h-4 w-4 mr-2" />
                                    Billing History
                                </Button>
                            </div>
                        </div>
                    {/if}

                    <!-- Plan Comparison -->
                    {#if $availablePlans.length > 0}
                        <div class="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
                            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">
                                Available Plans
                            </h3>
                            
                            <div class="grid md:grid-cols-3 gap-4">
                                {#each $availablePlans as plan}
                                    {@const isCurrentPlan = $currentSubscription?.name === plan.name}
                                    
                                    <div class="border rounded-lg p-4 {
                                        isCurrentPlan 
                                            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' 
                                            : 'border-gray-200 dark:border-gray-700'
                                    }">
                                        <div class="text-center">
                                            <h4 class="font-semibold text-gray-900 dark:text-white mb-2">
                                                {plan.display_name}
                                            </h4>
                                            <div class="text-2xl font-bold text-gray-900 dark:text-white mb-1">
                                                {formatPrice(plan.monthly_price_pennies)}
                                            </div>
                                            <div class="text-sm text-gray-500 dark:text-gray-400 mb-4">
                                                {plan.api_calls_per_day} calls/day • {plan.max_cvs} CVs
                                            </div>
                                            
                                            {#if isCurrentPlan}
                                                <div class="flex items-center justify-center text-sm text-primary-600 dark:text-primary-400">
                                                    <CheckCircle class="h-4 w-4 mr-1" />
                                                    Current Plan
                                                </div>
                                            {:else if plan.name === 'free'}
                                                <Button 
                                                    variant="outline" 
                                                    size="sm" 
                                                    disabled={$currentSubscription?.name === 'free'}
                                                >
                                                    Downgrade
                                                </Button>
                                            {:else}
                                                <Button size="sm" on:click={handleUpgrade}>
                                                    {$currentSubscription?.name === 'free' ? 'Upgrade' : 'Switch'}
                                                </Button>
                                            {/if}
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        </div>
                    {/if}
                </div>

                <!-- Sidebar -->
                <div class="space-y-6">
                    <!-- Usage Widget -->
                    <UsageDashboardWidget />

                    <!-- Quick Actions -->
                    <div class="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                            Quick Actions
                        </h3>
                        <div class="space-y-3">
                            <Button variant="outline" className="w-full justify-start">
                                <Calendar class="h-4 w-4 mr-2" />
                                View Billing History
                            </Button>
                            <Button variant="outline" className="w-full justify-start">
                                <CreditCard class="h-4 w-4 mr-2" />
                                Update Payment
                            </Button>
                            <Button variant="outline" href="/support" className="w-full justify-start">
                                <AlertCircle class="h-4 w-4 mr-2" />
                                Contact Support
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>

<!-- Upgrade Modal -->
<UpgradeModal 
    bind:open={showUpgradeModal}
    currentPlan={$currentSubscription?.name || 'free'}
    on:close={() => showUpgradeModal = false}
/>

<!-- Cancel Subscription Modal -->
<Modal bind:open={showCancelModal} title="Cancel Subscription" size="md" close={() => showCancelModal = false}>
    <div class="space-y-4">
        <div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
            <div class="flex items-start space-x-3">
                <AlertCircle class="h-5 w-5 text-yellow-600 dark:text-yellow-400 mt-0.5 flex-shrink-0" />
                <div>
                    <h4 class="text-sm font-medium text-yellow-800 dark:text-yellow-200">
                        Before you cancel
                    </h4>
                    <div class="text-sm text-yellow-700 dark:text-yellow-300 mt-1">
                        <p>Your subscription will remain active until the end of your current billing period.</p>
                        <p class="mt-2">You'll lose access to:</p>
                        <ul class="list-disc list-inside mt-1 space-y-1">
                            <li>AI-powered features</li>
                            <li>Premium templates</li>
                            <li>Advanced export options</li>
                            <li>Priority support</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <p class="text-gray-600 dark:text-gray-300">
            Are you sure you want to cancel your subscription?
        </p>
    </div>

    <div slot="footer" class="flex items-center justify-between">
        <Button variant="outline" on:click={() => showCancelModal = false}>
            Keep Subscription
        </Button>
        <Button 
            variant="danger" 
            on:click={confirmCancelSubscription}
            loading={cancellingSubscription}
            disabled={cancellingSubscription}
        >
            {cancellingSubscription ? 'Cancelling...' : 'Cancel Subscription'}
        </Button>
    </div>
</Modal>