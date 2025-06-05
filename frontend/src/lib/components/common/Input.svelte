<script>
    export let type = 'text';
    export let value = '';
    export let placeholder = '';
    export let required = false;
    export let disabled = false;
    export let label = '';
    export let error = '';
    export let id = '';
    
    // Generate a unique ID if none provided
    if (!id) {
        id = `input-${Math.random().toString(36).substr(2, 9)}`;
    }
    
    $: inputClasses = `
        block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm 
        focus:outline-none focus:ring-primary-500 focus:border-primary-500
        ${error ? 'border-red-300 focus:border-red-500 focus:ring-red-500' : ''}
        ${disabled ? 'bg-gray-50 text-gray-500 cursor-not-allowed' : ''}
    `.trim();
</script>

{#if label}
    <label for={id} class="block text-sm font-medium text-gray-700">
        {label}
        {#if required}
            <span class="text-red-500">*</span>
        {/if}
    </label>
{/if}

{#if type === 'text'}
    <input
        {id}
        type="text"
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
{:else if type === 'password'}
    <input
        {id}
        type="password"
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
{:else if type === 'email'}
    <input
        {id}
        type="email"
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
{:else if type === 'number'}
    <input
        {id}
        type="number"
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
{:else}
    <!-- Fallback for unsupported types -->
    <input
        {id}
        type="text"
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
{/if}

{#if error}
    <p class="text-sm text-red-600">{error}</p>
{/if}