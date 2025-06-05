<script>
	import { auth } from '$lib/api.js';
	import { user, loading } from '$lib/stores.js';
	import { goto } from '$app/navigation';
	
	let email = '';
	let password = '';
	let error = '';
	
	async function handleLogin() {
		if (!email || !password) {
			error = 'Please fill in all fields';
			return;
		}
		
		loading.set(true);
		error = '';
		
		try {
			await auth.login(email, password);
			const userData = await auth.me();
			user.set(userData);
			goto('/dashboard');
		} catch (err) {
			error = err.response?.data?.detail || 'Login failed';
		} finally {
			loading.set(false);
		}
	}
</script>

<svelte:head>
	<title>Login - ResumeForge</title>
</svelte:head>

<div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
	<div class="max-w-md w-full space-y-8">
		<!-- Header -->
		<div class="text-center">
			<h2 class="text-3xl font-bold text-primary">Sign in to ResumeForge</h2>
			<p class="mt-2 text-secondary">Create professional CVs with AI assistance</p>
		</div>

		<!-- Form -->
		<form on:submit|preventDefault={handleLogin} class="mt-8 space-y-6">
			<div class="space-y-4">
				<!-- Email -->
				<div>
					<label for="email" class="block text-sm font-medium text-primary">
						Email address
					</label>
					<input
						id="email"
						type="email"
						bind:value={email}
						required
						class="mt-1 w-full px-3 py-2 border border-border rounded-lg bg-primary text-primary placeholder-secondary focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent"
						placeholder="Enter your email"
					/>
				</div>

				<!-- Password -->
				<div>
					<label for="password" class="block text-sm font-medium text-primary">
						Password
					</label>
					<input
						id="password"
						type="password"
						bind:value={password}
						required
						class="mt-1 w-full px-3 py-2 border border-border rounded-lg bg-primary text-primary placeholder-secondary focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent"
						placeholder="Enter your password"
					/>
				</div>
			</div>

			<!-- Error Message -->
			{#if error}
				<div class="text-red-500 text-sm text-center">{error}</div>
			{/if}

			<!-- Submit Button -->
			<button
				type="submit"
				disabled={$loading}
				class="w-full py-2 px-4 bg-accent hover:bg-accent-hover text-white font-medium rounded-lg transition-colors disabled:opacity-50"
			>
				{$loading ? 'Signing in...' : 'Sign in'}
			</button>

			<!-- Register Link -->
			<p class="text-center text-sm text-secondary">
				Don't have an account?
				<a href="/register" class="text-accent hover:underline">Register here</a>
			</p>
		</form>
	</div>
</div>

<style>
	.bg-primary { background-color: var(--bg-primary); }
	.text-primary { color: var(--text-primary); }
	.text-secondary { color: var(--text-secondary); }
	.border-border { border-color: var(--border); }
	.bg-accent { background-color: var(--accent); }
	.bg-accent-hover:hover { background-color: var(--accent-hover); }
	.text-accent { color: var(--accent); }
</style>