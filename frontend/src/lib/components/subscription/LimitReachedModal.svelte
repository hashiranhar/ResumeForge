<script>
    import { createEventDispatcher } from 'svelte';
    import { currentSubscription, usageData } from '$lib/stores/subscription.js';
    import Modal from '$lib/components/common/Modal.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import UpgradeModal from './UpgradeModal.svelte';
    import { AlertTriangle, Clock, Zap, FileText } from 'lucide-svelte';

    export let open = false;
    export let limitType = 'api'; // 'api', 'cv', 'general'
    export let currentUsage = 0;
    export let limit = 0;

    const dispatch = createEventDispatcher();
    
    let showUpgradeModal = false;

    // Determine if user can upgrade or just needs to wait
    $: canUpgrade = !$currentSubscription || $currentSubscription.name !== 'pro';
    $: isProUser = $currentSubscription?.name === 'pro';

    // Get appropriate messaging based on limit type and user tier
    $: limitInfo = getLimitInfo(limitType, canUpgrade, isProUser);

    function getLimitInfo(type, canUpgrade, isPro) {
        const baseInfo = {
            api: {
                title: 'Daily API Limit Reached',
                icon: Zap,
                description: `You've used all ${limit} of your daily AI calls.`,
                iconColor: 'text-yellow-500 bg-yellow-100 dark:bg-yellow-900/20'
            },
            cv: {
                title: 'CV Limit Reached',
                icon: FileText,
                description: `You've reached your limit of ${limit} CVs.`,
                iconColor: 'text-blue-500 bg-blue-100 dark:bg-blue-900/20'
            },
            general: {
                title: 'Usage Limit Reached',
                icon: AlertTriangle,
                description: 'You\'ve reached your usage limit.',
                iconColor: 'text-red-500 bg-red-100 dark:bg-red-900/20'
            }
        };

        const info = baseInfo[type] || baseInfo.general;

        if (isPro) {
            info.actionText = 'Your limits will reset at midnight UK time.';
            info.showUpgrade = false;
        } else if (canUpgrade) {
            info.actionText = 'Upgrade to continue using premium features.';
            info.showUpgrade = true;
        } else {
            info.actionText = 'Please wait for your limits to reset.';
            info.showUpgrade = false;
        }

        return info;
    }

    function getTimeUntilReset() {
        const now = new Date();
        const tomorrow = new Date();
        tomorrow.setUTCDate(tomorrow.getUTCDate() + 1);
        tomorrow.setUTCHours(0, 0, 0, 0); // Midnight UK time (UTC)
        
        const diff = tomorrow - now;
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        
        if (hours > 0) {
            return `${hours}h ${minutes}m`;
        }
        return `${minutes}m`;
    }

    function close() {
        open = false;
        dispatch('close');
    }

    function handleUpgrade() {
        close();
        showUpgradeModal = true;
    }
</script>

<Modal bind:open title={limitInfo.title} size="md" {close}>
    <div class="space-y-6">
        <!-- Icon and description -->
        <div class="text-center">
            <div class="w-16 h-16 {limitInfo.iconColor} rounded-full flex items-center justify-center mx-auto mb-4">
                <svelte:component this={limitInfo.icon} class="h-8 w-8" />
            </div>
            <p class="text-gray-600 dark:text-gray-300 mb-4">
                {limitInfo.description}
            </p>
            <p class="text-gray-700 dark:text-gray-200">
                {limitInfo.actionText}
            </p>
        </div>

        <!-- Usage progress bar -->
        <div class="bg-gray-100 dark:bg-gray-800 rounded-lg p-4">
            <div class="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
                <span>Current Usage</span>
                <span>{currentUsage} / {limit}</span>
            </div>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                    class="h-2 bg-red-500 rounded-full transition-all duration-300"
                    style="width: {Math.min((currentUsage / limit) * 100, 100)}%"
                ></div>
            </div>
        </div>

        <!-- Reset timer for Pro users or non-upgradeable situations -->
        {#if isProUser || !canUpgrade}
            <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                <div class="flex items-center space-x-3">
                    <Clock class="h-5 w-5 text-blue-500" />
                    <div>
                        <p class="text-sm font-medium text-blue-900 dark:text-blue-100">
                            Limits reset in {getTimeUntilReset()}
                        </p>
                        <p class="text-xs text-blue-700 dark:text-blue-300">
                            Daily limits reset at midnight UK time
                        </p>
                    </div>
                </div>
            </div>
        {/if}

        <!-- Plan comparison for upgradeable users -->
        {#if canUpgrade && limitType === 'api'}
            <div class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
                <h4 class="text-sm font-medium text-green-900 dark:text-green-100 mb-2">
                    Get more with premium:
                </h4>
                <div class="space-y-1 text-xs text-green-800 dark:text-green-200">
                    <div class="flex justify-between">
                        <span>Basic Plan:</span>
                        <span>25 API calls/day</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Pro Plan:</span>
                        <span>50 API calls/day</span>
                    </div>
                </div>
            </div>
        {:else if canUpgrade && limitType === 'cv'}
            <div class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
                <h4 class="text-sm font-medium text-green-900 dark:text-green-100 mb-2">
                    Get more with premium:
                </h4>
                <div class="space-y-1 text-xs text-green-800 dark:text-green-200">
                    <div class="flex justify-between">
                        <span>Basic Plan:</span>
                        <span>10 CVs</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Pro Plan:</span>
                        <span>50 CVs</span>
                    </div>
                </div>
            </div>
        {/if}
    </div>

    <div slot="footer" class="flex items-center justify-between">
        <Button variant="outline" on:click={close}>
            {isProUser ? 'Got it' : 'Maybe Later'}
        </Button>
        
        {#if limitInfo.showUpgrade}
            <Button on:click={handleUpgrade}>
                Upgrade Now
            </Button>
        {:else if isProUser}
            <Button variant="outline" on:click={close}>
                OK
            </Button>
        {/if}
    </div>
</Modal>

<UpgradeModal 
    bind:open={showUpgradeModal}
    triggerReason={limitType + '_limit'}
    currentPlan={$currentSubscription?.name || 'free'}
    on:close={() => showUpgradeModal = false}
/>