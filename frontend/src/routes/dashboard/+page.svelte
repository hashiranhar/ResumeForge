<script>
	import { onMount } from 'svelte';
	import { cvs } from '$lib/api.js';
	import { user, loading } from '$lib/stores.js';
	import { goto } from '$app/navigation';
	import { Plus, FileText, Calendar, Download } from 'lucide-svelte';
	
	let userCVs = [];
	let error = '';
	
	onMount(async () => {
		// Redirect if not logged in
		if (!$user) {
			goto('/login');
			return;
		}
		
		// Load user's CVs
		try {
			loading.set(true);
			userCVs = await cvs.list();
		} catch (err) {
			error = 'Failed to load CVs';
			console.error(err);
		} finally {
			loading.set(false);
		}
	});
	
	async function createNewCV() {
		try {
			const newCV = await cvs.create({
				name: `CV ${userCVs.length + 1}`,
				markdown_content: '# Your Name\n**Your Title**\n\n## Experience\n\n## Skills\n\n## Education'
			});
			goto(`/editor/${newCV.id}`);
		} catch (err) {
			error = 'Failed to create CV';
		}
	}
	
	function formatDate(dateString) {
		return new Date(dateString).toLocaleDateString();
	}
</script>

<svelte:head>
	<title>Dashboard - ResumeForge</title>
</svelte:head>

<div class="min-h-screen bg-primary">
	<div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
		<!-- Enhanced Header -->
		<div class="flex justify-between items-center mb-12">
			<div>
				<h1 class="text-4xl font-bold text-primary mb-2">Your CVs</h1>
				<p class="text-lg text-secondary">Create and manage your professional resumes with AI assistance</p>
			</div>
			
			<button
				on:click={createNewCV}
				class="flex items-center space-x-3 bg-accent hover:bg-accent-hover text-white px-6 py-3 rounded-xl transition-colors shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
			>
				<Plus size={20} />
				<span class="font-medium">Create New CV</span>
			</button>
		</div>

	<!-- Error Message -->
	{#if error}
		<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
			{error}
		</div>
	{/if}

	<!-- Loading State -->
	{#if $loading}
		<div class="text-center py-12">
			<div class="text-secondary">Loading your CVs...</div>
		</div>
	{:else if userCVs.length === 0}
		<!-- Enhanced Empty State -->
		<div class="text-center py-20">
			<div class="w-24 h-24 bg-gradient-to-br from-accent to-blue-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg">
				<FileText size={32} class="text-white" />
			</div>
			<h3 class="text-2xl font-semibold text-primary mb-3">Ready to create your first CV?</h3>
			<p class="text-secondary mb-8 max-w-md mx-auto">Build a professional resume with our AI-powered editor and get real-time feedback to land your dream job.</p>
			<button
				on:click={createNewCV}
				class="bg-accent hover:bg-accent-hover text-white px-8 py-4 rounded-xl transition-colors shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 font-medium text-lg"
			>
				Create Your First CV
			</button>
		</div>
	{:else}
		<!-- Enhanced CV Grid -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
			{#each userCVs as cv}
				<div class="bg-secondary border border-border rounded-xl p-6 hover:shadow-xl transition-all duration-300 hover:-translate-y-1 group">
					<!-- Enhanced CV Header -->
					<div class="flex items-start justify-between mb-6">
						<div class="flex-1">
							<h3 class="font-semibold text-primary text-lg truncate mb-2">{cv.name}</h3>
							<div class="flex items-center text-sm text-secondary">
								<Calendar size={14} class="mr-2" />
								<span>Updated {formatDate(cv.updated_at)}</span>
							</div>
						</div>
						<div class="w-12 h-12 bg-tertiary rounded-lg flex items-center justify-center group-hover:bg-accent group-hover:text-white transition-colors">
							<FileText size={20} />
						</div>
					</div>

					<!-- Enhanced CV Preview -->
					<div class="text-sm text-secondary mb-6 bg-tertiary rounded-lg p-4 min-h-[80px]">
						{cv.markdown_content ? cv.markdown_content.substring(0, 120) + '...' : 'No content yet - click Edit to start building your CV'}
					</div>

					<!-- Enhanced Actions -->
					<div class="flex space-x-3">
						<button
							on:click={() => goto(`/editor/${cv.id}`)}
							class="flex-1 bg-accent hover:bg-accent-hover text-white py-3 rounded-lg transition-colors font-medium shadow-sm hover:shadow-md"
						>
							Edit CV
						</button>
						
						<button
							on:click={async () => {
								try {
									const pdfBlob = await cvs.downloadPDF(cv.id);
									const url = window.URL.createObjectURL(pdfBlob);
									const a = document.createElement('a');
									a.href = url;
									a.download = `${cv.name}.pdf`;
									a.click();
									window.URL.revokeObjectURL(url);
								} catch (err) {
									error = 'Failed to download PDF';
								}
							}}
							class="p-3 border border-border hover:bg-tertiary hover:border-accent rounded-lg transition-colors group"
							title="Download PDF"
						>
							<Download size={18} class="group-hover:text-accent" />
						</button>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>

<style>
	.bg-primary { background-color: var(--bg-primary); }
	.bg-secondary { background-color: var(--bg-secondary); }
	.bg-tertiary { background-color: var(--bg-tertiary); }
	.text-primary { color: var(--text-primary); }
	.text-secondary { color: var(--text-secondary); }
	.border-border { border-color: var(--border); }
	.bg-accent { background-color: var(--accent); }
	.bg-accent-hover:hover { background-color: var(--accent-hover); }
	
	.line-clamp-3 {
		display: -webkit-box;
		-webkit-line-clamp: 3;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}
</style>