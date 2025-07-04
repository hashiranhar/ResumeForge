<script>
    import { onMount } from 'svelte';
    import { usageData, subscriptionService } from '$lib/stores/subscription.js';
    import { BarChart3, Zap, FileText, AlertTriangle, CheckCircle, Clock } from 'lucide-svelte';
    import Button from '$lib/components/common/Button.svelte';

    export let className = "";

    let loading = true;

    onMount(async () => {
        await subscriptionService.loadUsage();
        loading = false;
    });

    function getProgressColor(warningLevel) {
        switch (warningLevel) {
            case 'low': return 'bg-green-500';
            case 'medium': return 'bg-yellow-500';
            case 'high': return 'bg-red-500';
            default: return 'bg-gray-300';
        }
    }

    function getStatusIcon(warningLevel) {
        switch (warningLevel) {
            case 'low': return CheckCircle;
            case 'medium': return AlertTriangle;
            case 'high': return AlertTriangle;
            default: return CheckCircle;
        }
    }

    function getStatusIconColor(warningLevel) {
        switch (warningLevel) {
            case 'low': return 'text-green-500';
            case 'medium': return 'text-yellow-500';
            case 'high': return 'text-red-500';
            default: return 'text-gray-400';
        }
    }
</script>

<div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 {className}">
    {#if loading}
        <!-- Loading State -->
        <div class="animate-pulse">
            <div class="flex items-center space-x-3 mb-4">
                <div class="w-5 h-5 bg-gray-300 dark:bg-gray-600 rounded"></div>
                <div class="w-24 h-4 bg-gray-300 dark:bg-gray-600 rounded"></div>
            </div>
            <div class="space-y-3">
                <div class="w-full h-3 bg-gray-300 dark:bg-gray-600 rounded"></div>
                <div class="w-full h-3 bg-gray-300 dark:bg-gray-600 rounded"></div>
            </div>
        </div>
    {:else if $usageData}
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-2">
                <BarChart3 class="h-5 w-5 text-gray-500 dark:text-gray-400" />
                <h3 class="font-medium text-gray-900 dark:text-white">Usage Overview</h3>
            </div>
        </div>

        <!-- Usage Metrics -->
        <div class="space-y-4">
            <!-- API Calls -->
            <div class="space-y-2">
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-2">
                        <Zap class="h-4 w-4 text-blue-500" />
                        <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
                            API Calls
                        </span>
                        <svelte:component 
                            this={getStatusIcon($usageData.api_calls.warning_level)} 
                            class="h-4 w-4 {getStatusIconColor($usageData.api_calls.warning_level)}" 
                        />
                    </div>
                    <span class="text-sm text-gray-600 dark:text-gray-400">
                        {$usageData.api_calls.used}/{$usageData.api_calls.limit}
                    </span>
                </div>
                
                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div 
                        class="h-2 rounded-full transition-all duration-300 {getProgressColor($usageData.api_calls.warning_level)}"
                        style="width: {$usageData.api_calls.percentage}%"
                    ></div>
                </div>
                
                <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400">
                    <span>{$usageData.api_calls.remaining} remaining</span>
                    <span>{$usageData.api_calls.percentage}% used</span>
                </div>
            </div>

            <!-- CVs -->
            <div class="space-y-2">
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-2">
                        <FileText class="h-4 w-4 text-green-500" />
                        <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
                            CVs Created
                        </span>
                        <svelte:component 
                            this={getStatusIcon($usageData.cvs.warning_level)} 
                            class="h-4 w-4 {getStatusIconColor($usageData.cvs.warning_level)}" 
                        />
                    </div>
                    <span class="text-sm text-gray-600 dark:text-gray-400">
                        {$usageData.cvs.used}/{$usageData.cvs.limit}
                    </span>
                </div>
                
                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div 
                        class="h-2 rounded-full transition-all duration-300 {getProgressColor($usageData.cvs.warning_level)}"
                        style="width: {$usageData.cvs.percentage}%"
                    ></div>
                </div>
                
                <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400">
                    <span>{$usageData.cvs.remaining} remaining</span>
                    <span>{$usageData.cvs.percentage}% used</span>
                </div>
            </div>
        </div>

        <!-- Reset Info -->
        <div class="mt-4 pt-3 border-t border-gray-200 dark:border-gray-700">
            <div class="flex items-center space-x-2 text-xs text-gray-500 dark:text-gray-400">
                <Clock class="h-3 w-3" />
                <span>{$usageData.reset_info}</span>
            </div>
        </div>

        <!-- Action Buttons -->
        {#if ($usageData.api_calls.warning_level === 'high' || $usageData.cvs.warning_level === 'high')}
            <div class="mt-3">
                <Button className="w-full text-sm">
                    Upgrade Plan
                </Button>
            </div>
        {/if}
    {:else}
        <!-- Error/Empty State -->
        <div class="text-center py-8">
            <BarChart3 class="h-12 w-12 text-gray-300 dark:text-gray-600 mx-auto mb-2" />
            <p class="text-sm text-gray-500 dark:text-gray-400">Usage data unavailable</p>
        </div>
    {/if}
</div>