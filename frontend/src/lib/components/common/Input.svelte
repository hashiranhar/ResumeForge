<script lang="ts">
    export let id: string;
    export let label: string | null = null;
    export let type: 'text' | 'password' | 'email' | 'number' = 'text'; // Restrict to valid input types
    export let placeholder: string | null = null;
    export let required: boolean = false;
    export let disabled: boolean = false;
    export let value: string | number = '';
    export let error: string | null = null;

    const inputClasses = 'block w-full px-3 py-2 border rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500';
</script>

<div class="space-y-1">
    {#if label}
        <label for={id} class="block text-sm font-medium text-gray-700">
            {label}
            {#if required}
                <span class="text-red-500">*</span>
            {/if}
        </label>
    {/if}
    
    {#if type === 'text' || type === 'password' || type === 'email' || type === 'number'}
        <input
            id={id}
            type={type}
            placeholder={placeholder}
            required={required}
            disabled={disabled}
            bind:value
            class={inputClasses}
            on:input
            on:change
            on:focus
            on:blur
        />
    {/if}
    
    {#if error}
        <p class="text-sm text-red-600">{error}</p>
    {/if}
</div>