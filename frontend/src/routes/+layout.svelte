<script>
	import '../app.html';
	import { onMount } from 'svelte';
	import { theme, user } from '$lib/stores.js';
	import { auth } from '$lib/api.js';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { Moon, Sun, LogOut } from 'lucide-svelte';

	// Initialize theme on mount
	onMount(() => {
		theme.init();
		
		// Check if user is logged in
		const token = localStorage.getItem('auth_token');
		if (token) {
			auth.me().then(userData => {
				user.set(userData);
			}).catch(() => {
				// Token expired or invalid
				auth.logout();
				if ($page.url.pathname !== '/login' && $page.url.pathname !== '/register') {
					goto('/login');
				}
			});
		}
	});

	function handleLogout() {
		auth.logout();
		user.clear();
		goto('/login');
	}
</script>

<!-- Header -->
<header class="bg-secondary border-b border-border">
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="flex justify-between h-16">
			<!-- Logo -->
			<div class="flex items-center">
				<a href="/dashboard" class="text-xl font-bold text-primary">
					ResumeForge
				</a>
			</div>

			<!-- Right side -->
			<div class="flex items-center space-x-4">
				<!-- Theme Toggle -->
				<button
					on:click={theme.toggle}
					class="p-2 rounded-lg hover:bg-tertiary transition-colors"
					aria-label="Toggle theme"
				>
					{#if $theme === 'light'}
						<Moon size={20} />
					{:else}
						<Sun size={20} />
					{/if}
				</button>

				<!-- User Menu -->
				{#if $user}
					<div class="flex items-center space-x-2">
						<span class="text-sm text-secondary">{$user.email}</span>
						<button
							on:click={handleLogout}
							class="p-2 rounded-lg hover:bg-tertiary transition-colors"
							aria-label="Logout"
						>
							<LogOut size={20} />
						</button>
					</div>
				{/if}
			</div>
		</div>
	</div>
</header>

<!-- Main Content -->
<main class="min-h-screen bg-primary">
	<slot />
</main>

<style>
	.bg-primary { background-color: var(--bg-primary); }
	.bg-secondary { background-color: var(--bg-secondary); }
	.bg-tertiary { background-color: var(--bg-tertiary); }
	.text-primary { color: var(--text-primary); }
	.text-secondary { color: var(--text-secondary); }
	.border-border { border-color: var(--border); }
</style>