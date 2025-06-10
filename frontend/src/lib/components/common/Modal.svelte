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
            <!-- Backdrop - FIXED: Added dark mode styling -->
            <div 
                class="fixed inset-0 bg-black bg-opacity-50 dark:bg-opacity-75 transition-opacity"
                role="button"
                tabindex="0"
                aria-label="Close modal"
                on:click={handleBackdropClick}
                on:keydown={handleBackdropKeydown}
            ></div>
            
            <!-- Modal - FIXED: Added dark mode styling -->
            <div 
                class="relative bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full {sizes[size]} border border-gray-200 dark:border-gray-700"
                id="modal-content"
            >
                <!-- Header -->
                {#if title || $$slots.header}
                    <div class="flex items-center justify-between p-6 pb-0">
                        <div class="flex-1">
                            {#if $$slots.header}
                                <slot name="header" />
                            {:else if title}
                                <h2 id="modal-title" class="text-lg font-semibold text-gray-900 dark:text-white">
                                    {title}
                                </h2>
                            {/if}
                        </div>
                        
                        <!-- Close button - FIXED: Added dark mode styling -->
                        <button
                            type="button"
                            class="ml-4 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 transition-colors"
                            on:click={close}
                            aria-label="Close modal"
                        >
                            <X class="h-6 w-6" />
                        </button>
                    </div>
                {/if}

                <!-- Content - FIXED: Added dark mode styling -->
                <div class="p-6">
                    <slot />
                </div>

                <!-- Footer - FIXED: Added dark mode styling -->
                {#if $$slots.footer}
                    <div class="flex items-center justify-end space-x-2 p-6 pt-0 border-t border-gray-200 dark:border-gray-700">
                        <slot name="footer" />
                    </div>
                {/if}
            </div>
        </div>
    </div>
{/if}