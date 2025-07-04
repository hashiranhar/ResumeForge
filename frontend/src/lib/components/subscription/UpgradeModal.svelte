<script>
    import { createEventDispatcher } from 'svelte';
    import { availablePlans, subscriptionService, isSubscriptionLoading } from '$lib/stores/subscription.js';
    import { addToast } from '$lib/stores/toast.js';
    import Modal from '$lib/components/common/Modal.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import { Zap, Check, Star } from 'lucide-svelte';

    export let open = false;
    export let triggerReason = 'limit_reached'; // 'limit_reached', 'cv_limit', 'api_limit'
    export let currentPlan = 'free';

    const dispatch = createEventDispatcher();
    
    let selectedPlan = 'basic';
    let billingCycle = 'monthly';

    // Get plan features
    const planFeatures = {
        free: [
            '5 API calls per day',
            '3 CVs maximum', 
            'Basic templates',
            'PDF export'
        ],
        basic: [
            '25 API calls per day',
            '10 CVs maximum',
            'AI suggestions',
            'ATS optimization',
            'Premium templates',
            'Priority support'
        ],
        pro: [
            '50 API calls per day',
            '50 CVs maximum',
            'Unlimited AI features',
            'Advanced ATS scoring',
            'All premium templates',
            'Chat support',
            'Multiple versions'
        ]
    };

    // Get upgrade messages based on trigger
    const upgradeMessages = {
        api_limit: {
            title: 'Daily API Limit Reached',
            description: 'You\'ve used all your daily AI calls. Upgrade to continue using AI features.',
            icon: Zap
        },
        cv_limit: {
            title: 'CV Limit Reached',
            description: 'You\'ve reached your CV limit. Upgrade to create more resumes.',
            icon: Star
        },
        limit_reached: {
            title: 'Upgrade to Continue',
            description: 'Unlock more features and higher limits with a premium plan.',
            icon: Zap
        }
    };

    $: currentMessage = upgradeMessages[triggerReason] || upgradeMessages.limit_reached;
    $: filteredPlans = $availablePlans.filter(plan => plan.name !== 'free');

    function close() {
        open = false;
        dispatch('close');
    }

    function formatPrice(pennies) {
        if (pennies === 0) return 'Free';
        const pounds = pennies / 100;
        return `£${pounds}`;
    }

    function getYearlyDiscount(monthlyPennies, yearlyPennies) {
        if (monthlyPennies === 0) return 0;
        const monthlyYearly = monthlyPennies * 12;
        const savings = ((monthlyYearly - yearlyPennies) / monthlyYearly) * 100;
        return Math.round(savings);
    }

    async function handleUpgrade() {
        if (!selectedPlan || selectedPlan === currentPlan) {
            addToast('Please select a different plan', 'error');
            return;
        }

        const plan = $availablePlans.find(p => p.name === selectedPlan);
        if (!plan) {
            addToast('Selected plan not found', 'error');
            return;
        }

        try {
            const result = await subscriptionService.createCheckoutSession(plan.id, billingCycle);
            if (!result.success) {
                addToast(result.error || 'Failed to start upgrade process', 'error');
            }
            // Note: If successful, user will be redirected to Stripe checkout
        } catch (error) {
            addToast('Failed to start upgrade process', 'error');
        }
    }
</script>

<Modal bind:open title={currentMessage.title} size="lg" {close}>
    <div class="space-y-6">
        <!-- Header with icon and description -->
        <div class="text-center">
            <div class="w-16 h-16 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center mx-auto mb-4">
                <svelte:component this={currentMessage.icon} class="h-8 w-8 text-primary-600 dark:text-primary-400" />
            </div>
            <p class="text-gray-600 dark:text-gray-300">
                {currentMessage.description}
            </p>
        </div>

        <!-- Billing Toggle -->
        <div class="flex justify-center">
            <div class="bg-gray-100 dark:bg-gray-800 p-1 rounded-lg">
                <button
                    on:click={() => billingCycle = 'monthly'}
                    class="px-4 py-2 rounded-md text-sm font-medium transition-colors {
                        billingCycle === 'monthly'
                            ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
                            : 'text-gray-600 dark:text-gray-400'
                    }"
                >
                    Monthly
                </button>
                <button
                    on:click={() => billingCycle = 'yearly'}
                    class="px-4 py-2 rounded-md text-sm font-medium transition-colors {
                        billingCycle === 'yearly'
                            ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
                            : 'text-gray-600 dark:text-gray-400'
                    }"
                >
                    Yearly
                    <span class="ml-1 text-xs text-green-600 dark:text-green-400 font-semibold">
                        Save 30%
                    </span>
                </button>
            </div>
        </div>

        <!-- Plan Selection -->
        <div class="grid md:grid-cols-2 gap-4">
            {#each filteredPlans as plan}
                {@const isSelected = selectedPlan === plan.name}
                {@const price = billingCycle === 'yearly' ? plan.yearly_price_pennies : plan.monthly_price_pennies}
                {@const yearlyDiscount = getYearlyDiscount(plan.monthly_price_pennies, plan.yearly_price_pennies)}
                
                <button
                    type="button"
                    class="relative p-6 border rounded-xl text-left transition-all hover:shadow-md {
                        isSelected
                            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 shadow-md'
                            : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                    }"
                    on:click={() => selectedPlan = plan.name}
                >
                    {#if plan.name === 'basic'}
                        <div class="absolute -top-3 left-1/2 transform -translate-x-1/2">
                            <span class="bg-primary-500 text-white px-3 py-1 text-xs font-semibold rounded-full">
                                Most Popular
                            </span>
                        </div>
                    {/if}

                    <div class="space-y-4">
                        <!-- Plan name and price -->
                        <div>
                            <h3 class="text-lg font-bold text-gray-900 dark:text-white capitalize">
                                {plan.display_name}
                            </h3>
                            <div class="mt-2">
                                <span class="text-3xl font-bold text-gray-900 dark:text-white">
                                    {formatPrice(price)}
                                </span>
                                <span class="text-gray-500 dark:text-gray-400">
                                    /{billingCycle === 'yearly' ? 'year' : 'month'}
                                </span>
                                {#if billingCycle === 'yearly' && yearlyDiscount > 0}
                                    <div class="text-sm text-green-600 dark:text-green-400 font-medium">
                                        Save {yearlyDiscount}% annually
                                    </div>
                                {/if}
                            </div>
                        </div>

                        <!-- Features -->
                        <div class="space-y-2">
                            {#each planFeatures[plan.name] || [] as feature}
                                <div class="flex items-center space-x-2 text-sm">
                                    <Check class="h-4 w-4 text-green-500 flex-shrink-0" />
                                    <span class="text-gray-700 dark:text-gray-300">{feature}</span>
                                </div>
                            {/each}
                        </div>
                    </div>
                </button>
            {/each}
        </div>

        <!-- Current plan comparison -->
        {#if currentPlan !== 'free'}
            <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                <p class="text-sm text-blue-800 dark:text-blue-200">
                    <strong>Current plan:</strong> {currentPlan} 
                    {#if selectedPlan !== currentPlan}
                        → Upgrading to <strong>{selectedPlan}</strong>
                    {/if}
                </p>
            </div>
        {/if}
    </div>

    <div slot="footer" class="flex items-center justify-between">
        <Button variant="outline" on:click={close}>
            Maybe Later
        </Button>
        <Button 
            on:click={handleUpgrade}
            loading={$isSubscriptionLoading}
            disabled={$isSubscriptionLoading || selectedPlan === currentPlan}
        >
            {#if selectedPlan === currentPlan}
                Current Plan
            {:else}
                Upgrade to {selectedPlan}
            {/if}
        </Button>
    </div>
</Modal>