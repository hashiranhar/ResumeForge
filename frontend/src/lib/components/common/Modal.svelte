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

    function handleBackdropClick(event: MouseEvent) {
        if (event.target === event.currentTarget) {
            close();
        }
    }

    function handleBackdropKeydown(event: KeyboardEvent) {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            close();
        }
    }

    function handleKeydown(event: KeyboardEvent) {
        if (event.key === 'Escape' && open) {
            close();
        }
    }
</script>

<svelte:window on:keydown={handleKeydown} />

{#if open}
    <div 
        class="fixed inset-0 z-50 overflow-y-auto"
        transition:fade={{ duration: 200 }}
        role="dialog"
        aria-modal="true"
        aria-labelledby={title ? 'modal-title' : undefined}
        aria-describedby="modal-content"
    >
        <div class="flex min-h-screen items-center justify-center p-4">
            <!-- Backdrop -->
            <div 
                class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
                role="button"
                tabindex="0"
                aria-label="Close modal"
                on:click={handleBackdropClick}
                on:keydown={handleBackdropKeydown}
            ></div>
            
            <!-- Modal -->
            <div 
                class="relative bg-white rounded-lg shadow-xl w-full {sizes[size]}"
                id="modal-content"
            >
                <!-- Header -->
                {#if title || $$slots.header}
                    <div class="flex items-center justify-between p-6 pb-0">
                        <div class="flex-1">
                            {#if $$slots.header}
                                <slot name="header" />
                            {:else if title}
                                <h2 id="modal-title" class="text-lg font-semibold text-gray-900">
                                    {title}
                                </h2>
                            {/if}
                        </div>
                        
                        <!-- Close button -->
                        <button
                            type="button"
                            class="ml-4 text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
                            on:click={close}
                            aria-label="Close modal"
                        >
                            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>
                {/if}

                <!-- Content -->
                <div class="p-6">
                    <slot />
                </div>

                <!-- Footer -->
                {#if $$slots.footer}
                    <div class="flex items-center justify-end space-x-2 p-6 pt-0">
                        <slot name="footer" />
                    </div>
                {/if}
            </div>
        </div>
    </div>
{/if}