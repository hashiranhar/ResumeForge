<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { fade } from 'svelte/transition';
    import { X } from 'lucide-svelte';

    export let open: boolean = false; // Control modal visibility
    export let title: string = ''; // Modal title
    export let size: 'sm' | 'md' | 'lg' | 'xl' = 'md'; // Modal size
    export let close: () => void; // Close function passed from parent

    const sizes = {
        sm: 'max-w-md',
        md: 'max-w-lg',
        lg: 'max-w-2xl',
        xl: 'max-w-4xl'
    };

    function handleKeydown(event: KeyboardEvent) {
        if (event.key === 'Escape') {
            close();
        }
    }

    function handleBackdropClick(event: MouseEvent) {
        if (event.target === event.currentTarget) {
            close();
        }
    }
</script>

<svelte:window on:keydown={handleKeydown} />

{#if open}
    <div 
        class="fixed inset-0 z-50 overflow-y-auto"
        transition:fade={{ duration: 200 }}
    >
        <div class="flex min-h-screen items-center justify-center p-4">
            <!-- Backdrop -->
            <div 
                class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
                on:click={handleBackdropClick}
            ></div>
            
            <!-- Modal -->
            <div class="relative bg-white rounded-lg shadow-xl w-full {sizes[size]}">
                <!-- Header -->
                {#if title || $$slots.header}
                    <div class="flex items-center justify-between p-6 pb-0">
                        <div class="flex-1">
                            {#if $$slots.header}
                                <slot name="header" />
                            {:else}
                                <h2 class="text-lg font-semibold text-gray-900">{title}</h2>
                            {/if}
                        </div>
                        <button
                            class="text-gray-400 hover:text-gray-600 focus:outline-none"
                            on:click={close}
                        >
                            <X class="h-5 w-5" />
                        </button>
                    </div>
                {/if}
                
                <!-- Body -->
                <div class="p-6">
                    <slot />
                </div>
                
                <!-- Footer -->
                {#if $$slots.footer}
                    <div class="px-6 py-4 bg-gray-50 rounded-b-lg">
                        <slot name="footer" />
                    </div>
                {/if}
            </div>
        </div>
    </div>
{/if}