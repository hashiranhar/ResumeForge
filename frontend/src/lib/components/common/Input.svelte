<script>
    export let type = 'text';
    export let placeholder = '';
    export let value = '';
    export let label = '';
    export let error = '';
    export let required = false;
    export let disabled = false;
    export let id = '';

    $: inputClasses = `block w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 transition-colors ${
        error 
            ? 'border-red-300 focus:ring-red-500 focus:border-red-500' 
            : 'border-gray-300 focus:ring-primary-500 focus:border-primary-500'
    } ${disabled ? 'bg-gray-50 cursor-not-allowed' : 'bg-white'}`;
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
    
    <input
        {id}
        {type}
        {placeholder}
        {required}
        {disabled}
        bind:value
        class={inputClasses}
        on:input
        on:change
        on:focus
        on:blur
    />
    
    {#if error}
        <p class="text-sm text-red-600">{error}</p>
    {/if}
</div>