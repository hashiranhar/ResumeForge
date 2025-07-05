<script>
    import { user, isAuthenticated, authService } from '$lib/stores/auth.js';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { User, LogOut, Plus } from 'lucide-svelte';
    import Button from '$lib/components/common/Button.svelte';
    import DarkModeToggle from '$lib/components/common/DarkModeToggle.svelte';
    import Logo from '$lib/components/common/Logo.svelte';

    let showUserMenu = false;

    function toggleUserMenu() {
        showUserMenu = !showUserMenu;
    }

    function closeUserMenu() {
        showUserMenu = false;
    }

    function handleLogout() {
        authService.logout();
        closeUserMenu();
        goto('/auth/login');
    }

    function handleNewCV() {
        goto('/dashboard');
    }

    function handleClickOutside(event) {
        if (!event.target.closest('.user-menu')) {
            showUserMenu = false;
        }
    }
</script>

<svelte:window on:click={handleClickOutside} />

<header class="bg-white dark:bg-black shadow-sm border-b border-gray-200 dark:border-gray-800">
    <div class="px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
            <div class="flex items-center">
                <Logo size="xl" showText={true} />
            </div>

            <!-- RIGHT SIDE - Navigation (sticks to right edge) -->
            <div class="flex items-center space-x-4">
                {#if $isAuthenticated}

                    <!-- Dashboard link -->
                    <a 
                        href="/dashboard" 
                        class="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
                        class:text-primary-600={$page.url.pathname === '/dashboard'}
                        class:dark:text-primary-400={$page.url.pathname === '/dashboard'}
                    >
                        Dashboard
                    </a>

                    <!-- New CV Button -->
                    <Button
                        variant="primary"
                        size="sm"
                        on:click={handleNewCV}
                        class="flex items-center space-x-1"
                    >
                        <Plus class="h-4 w-4" />
                        <span class="hidden sm:inline">New CV</span>
                    </Button>

                    <!-- Dark Mode Toggle -->
                    <DarkModeToggle />

                    <!-- User Menu -->
                    <div class="relative user-menu">
                        <button
                            on:click={toggleUserMenu}
                            class="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
                        >
                            <div class="w-8 h-8 bg-primary-600 dark:bg-primary-500 rounded-full flex items-center justify-center">
                                <User class="h-4 w-4 text-white" />
                            </div>
                            <span class="hidden md:inline text-sm font-medium">
                                {$user?.email || 'User'}
                            </span>
                        </button>

                        <!-- Dropdown Menu -->
                        {#if showUserMenu}
                            <div class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-50">
                                <div class="py-1">
                                    <div class="px-4 py-2 border-b border-gray-200 dark:border-gray-700">
                                        <p class="text-sm font-medium text-gray-900 dark:text-white">
                                            {$user?.email || 'User'}
                                        </p>
                                    </div>
                                    <button
                                        on:click={handleLogout}
                                        class="w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center space-x-2"
                                    >
                                        <LogOut class="h-4 w-4" />
                                        <span>Sign Out</span>
                                    </button>
                                </div>
                            </div>
                        {/if}
                    </div>
                {:else}
                    <!-- Dark Mode Toggle for non-authenticated users -->
                    <DarkModeToggle />

                    <!-- Auth buttons -->
                    <div class="flex items-center space-x-3">
                        <a 
                            href="/auth/login"
                            class="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
                        >
                            Sign In
                        </a>
                        <Button
                            href="/auth/register"
                            variant="primary"
                            size="sm"
                        >
                            Get Started
                        </Button>
                    </div>
                {/if}
            </div>
        </div>
    </div>
</header>