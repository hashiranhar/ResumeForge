<script>
    import { toasts, removeToast } from '$lib/stores/toast.js';
    import { CheckCircle, XCircle, AlertCircle, Info, X } from 'lucide-svelte';
    import { fade, fly } from 'svelte/transition';

    const icons = {
        success: CheckCircle,
        error: XCircle,
        warning: AlertCircle,
        info: Info
    };

    const colors = {
        success: 'bg-green-50 border-green-200 text-green-800',
        error: 'bg-red-50 border-red-200 text-red-800',
        warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
        info: 'bg-blue-50 border-blue-200 text-blue-800'
    };

    const iconColors = {
        success: 'text-green-500',
        error: 'text-red-500',
        warning: 'text-yellow-500',
        info: 'text-blue-500'
    };
</script>

<div class="fixed top-4 right-4 z-50 space-y-2">
    {#each $toasts as toast (toast.id)}
        <div 
            class="max-w-sm w-full bg-white shadow-lg rounded-lg border {colors[toast.type]} p-4"
            transition:fly="{{ y: -50, duration: 300 }}"
        >
            <div class="flex items-start">
                <div class="flex-shrink-0">
                    <svelte:component 
                        this={icons[toast.type]} 
                        class="h-5 w-5 {iconColors[toast.type]}" 
                    />
                </div>
                <div class="ml-3 w-0 flex-1">
                    <p class="text-sm font-medium">
                        {toast.message}
                    </p>
                </div>
                <div class="ml-4 flex-shrink-0 flex">
                    <button
                        class="inline-flex text-gray-400 hover:text-gray-600 focus:outline-none"
                        on:click={() => removeToast(toast.id)}
                    >
                        <X class="h-4 w-4" />
                    </button>
                </div>
            </div>
        </div>
    {/each}
</div>