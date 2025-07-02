<script lang="ts">
    import { X, CheckCircle, XCircle, AlertTriangle, Info } from 'lucide-svelte'; // Import icons
    import { fly } from 'svelte/transition';

    export let toasts: { id: string; type: 'success' | 'error' | 'warning' | 'info'; message: string }[] = [];
    export let colors: { success: string; error: string; warning: string; info: string } = {
        success: 'border-green-500',
        error: 'border-red-500',
        warning: 'border-yellow-500',
        info: 'border-blue-500'
    };
    export let icons: { success: typeof CheckCircle; error: typeof XCircle; warning: typeof AlertTriangle; info: typeof Info } = {
        success: CheckCircle,
        error: XCircle,
        warning: AlertTriangle,
        info: Info
    };
    export let iconColors: { success: string; error: string; warning: string; info: string } = {
        success: 'text-green-500',
        error: 'text-red-500',
        warning: 'text-yellow-500',
        info: 'text-blue-500'
    };

    function removeToast(id: string) {
        toasts = toasts.filter(toast => toast.id !== id);
    }
</script>

<div class="fixed top-4 right-4 z-50 space-y-2">
    {#each toasts as toast (toast.id)}
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