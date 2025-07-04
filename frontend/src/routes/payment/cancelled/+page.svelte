<script>
    import { goto } from '$app/navigation';
    import Button from '$lib/components/common/Button.svelte';
    import { X, ArrowLeft, MessageCircle, ArrowRight } from 'lucide-svelte';

    function handleGoBack() {
        goto('/subscription');
    }

    function handleTryAgain() {
        goto('/subscription');
    }

    function handleContactSupport() {
        goto('/support');
    }

    function handleContinueFree() {
        goto('/dashboard');
    }
</script>

<svelte:head>
    <title>Payment Cancelled - ResumeForge</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 dark:bg-black flex items-center justify-center p-4">
    <div class="max-w-md w-full">
        <div class="bg-white dark:bg-gray-900 rounded-xl shadow-lg p-8 text-center">
            <!-- Cancelled Icon -->
            <div class="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-6">
                <X class="w-10 h-10 text-gray-500 dark:text-gray-400" />
            </div>

            <!-- Cancelled Message -->
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                Payment Cancelled
            </h1>
            <p class="text-gray-600 dark:text-gray-400 mb-8">
                No charges were made to your account. You can continue using ResumeForge with the free plan or try upgrading again.
            </p>

            <!-- What you can still do -->
            <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6 mb-8">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                    Continue with Free Plan
                </h3>
                
                <div class="space-y-2 text-sm text-gray-700 dark:text-gray-300">
                    <div class="flex items-center space-x-2">
                        <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span>5 AI calls per day</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span>Up to 3 CVs</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span>Basic templates</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span>PDF export</span>
                    </div>
                </div>
            </div>

            <!-- Action Buttons -->
            <div class="space-y-3">
                <Button on:click={handleContinueFree} className="w-full">
                    <ArrowRight class="w-4 h-4 mr-2" />
                    Continue with Free Plan
                </Button>
                
                <Button variant="outline" on:click={handleTryAgain} className="w-full">
                    <ArrowLeft class="w-4 h-4 mr-2" />
                    Try Upgrading Again
                </Button>
                
                <Button variant="outline" on:click={handleContactSupport} className="w-full">
                    <MessageCircle class="w-4 h-4 mr-2" />
                    Contact Support
                </Button>
            </div>

            <!-- Help Text -->
            <div class="mt-8 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">
                    Need help with payment?
                </h4>
                <p class="text-xs text-gray-600 dark:text-gray-400">
                    If you experienced any issues during checkout, our support team is here to help. 
                    You can also try again later or upgrade at any time from your dashboard.
                </p>
            </div>
        </div>
    </div>
</div>