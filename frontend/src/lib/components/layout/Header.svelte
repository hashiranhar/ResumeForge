<script>
    import { user, isAuthenticated, authService } from '$lib/stores/auth.js';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { User, LogOut, FileText, Plus } from 'lucide-svelte';
    import Button from '$lib/components/common/Button.svelte';

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
        goto('/editor?new=true');
    }

    // Close menu when clicking outside
    function handleClickOutside(event) {
        if (!event.target.closest('.user-menu')) {
            showUserMenu = false;
        }
    }
</script>

<svelte:window on:click={handleClickOutside} />

<header class="bg-white shadow-sm border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
            <!-- Logo and title -->
            <div class="flex items-center">
                <a href="/" class="flex items-center space-x-2">
                    <FileText class="h-8 w-8 text-primary-600" />
                    <span class="text-xl font-bold text-gray-900">ResumeForge</span>
                </a>
            </div>

            <!-- Navigation and actions -->
            <div class="flex items-center space-x-4">
                {#if $isAuthenticated}
                    <!-- New CV button -->
                    <Button variant="primary" size="sm" on:click={handleNewCV}>
                        <Plus class="h-4 w-4 mr-1" />
                        New CV
                    </Button>

                    <!-- Dashboard link -->
                    <a 
                        href="/dashboard" 
                        class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                        class:text-primary-600={$page.url.pathname === '/dashboard'}
                        class:font-semibold={$page.url.pathname === '/dashboard'}
                    >
                        Dashboard
                    </a>

                    <!-- User menu -->
                    <div class="relative user-menu">
                        <button
                            class="flex items-center space-x-2 text-gray-700 hover:text-gray-900 focus:outline-none"
                            on:click={toggleUserMenu}
                        >
                            <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                                <User class="h-5 w-5 text-primary-600" />
                            </div>
                            <span class="text-sm font-medium">{$user?.email}</span>
                        </button>

                        {#if showUserMenu}
                            <div class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 z-10">
                                <div class="py-1">
                                    <div class="px-4 py-2 text-sm text-gray-500 border-b border-gray-100">
                                        Signed in as<br />
                                        <span class="font-medium text-gray-900">{$user?.email}</span>
                                    </div>
                                    <a 
                                        href="/dashboard" 
                                        class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                                        on:click={closeUserMenu}
                                    >
                                        <FileText class="inline h-4 w-4 mr-2" />
                                        My CVs
                                    </a>
                                    <button
                                        class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                                        on:click={handleLogout}
                                    >
                                        <LogOut class="inline h-4 w-4 mr-2" />
                                        Sign out
                                    </button>
                                </div>
                            </div>
                        {/if}
                    </div>
                {:else}
                    <!-- Auth buttons for non-authenticated users -->
                    <div class="flex items-center space-x-2">
                        <Button variant="outline" size="sm" href="/auth/login">
                            Sign In
                        </Button>
                        <Button variant="primary" size="sm" href="/auth/register">
                            Sign Up
                        </Button>
                    </div>
                {/if}
            </div>
        </div>
    </div>
</header>