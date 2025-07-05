<script>
    export let type = 'text';
    export let value = '';
    export let placeholder = '';
    export let required = false;
    export let disabled = false;
    export let label = '';
    export let error = '';
    export let id = '';
    export let icon = null; // Add icon prop
    export let iconPosition = 'left'; // 'left' or 'right'
    
    // Generate a unique ID if none provided
    if (!id) {
        id = `input-${Math.random().toString(36).substr(2, 9)}`;
    }
    
    $: inputClasses = `
        block w-full ${icon ? (iconPosition === 'left' ? 'pl-10' : 'pr-10') : ''} px-3 py-2 
        border border-gray-300 dark:border-gray-600 rounded-md shadow-sm 
        bg-white dark:bg-gray-800 text-gray-900 dark:text-white
        placeholder-gray-500 dark:placeholder-gray-400
        focus:outline-none focus:ring-primary-500 focus:border-primary-500
        ${error ? 'border-red-300 focus:border-red-500 focus:ring-red-500' : ''}
        ${disabled ? 'bg-gray-50 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-not-allowed' : ''}
    `.trim();
</script>

<div class="relative">
    {#if label}
        <label for={id} class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            {label}
            {#if required}
                <span class="text-red-500">*</span>
            {/if}
        </label>
    {/if}

    <div class="relative">
        <!-- Icon -->
        {#if icon}
            <div class="absolute inset-y-0 {iconPosition === 'left' ? 'left-0 pl-3' : 'right-0 pr-3'} flex items-center pointer-events-none">
                <svelte:component this={icon} class="h-5 w-5 text-gray-400 dark:text-gray-500" />
            </div>
        {/if}

        <!-- Input field -->
        {#if type === 'textarea'}
            <textarea
                {id}
                {placeholder}
                {required}
                {disabled}
                bind:value
                class="block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 {error ? 'border-red-300 focus:border-red-500 focus:ring-red-500' : ''} {disabled ? 'bg-gray-50 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-not-allowed' : ''}"
                rows="4"
                on:input
                on:change
                on:focus
                on:blur
                on:keydown
            ></textarea>
        {:else if type === 'text'}
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
                on:keydown
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
                on:keydown
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
                on:keydown
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
                on:keydown
            />
        {:else if type === 'tel'}
            <input
                {id}
                type="tel"
                {placeholder}
                {required}
                {disabled}
                bind:value
                class={inputClasses}
                on:input
                on:change
                on:focus
                on:blur
                on:keydown
            />
        {:else if type === 'url'}
            <input
                {id}
                type="url"
                {placeholder}
                {required}
                {disabled}
                bind:value
                class={inputClasses}
                on:input
                on:change
                on:focus
                on:blur
                on:keydown
            />
        {:else if type === 'search'}
            <input
                {id}
                type="search"
                {placeholder}
                {required}
                {disabled}
                bind:value
                class={inputClasses}
                on:input
                on:change
                on:focus
                on:blur
                on:keydown
            />
        {:else}
            <!-- Fallback to text input -->
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
                on:keydown
            />
        {/if}
    </div>

    {#if error}
        <p class="mt-1 text-sm text-red-600 dark:text-red-400">{error}</p>
    {/if}
</div>