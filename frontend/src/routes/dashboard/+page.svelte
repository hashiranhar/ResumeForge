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
	<div class="max-w-7xl mx-auto py-6 lg:py-12 px-4 sm:px-6 lg:px-8">
		<!-- Responsive Header -->
		<div class="flex flex-col lg:flex-row lg:justify-between lg:items-center mb-8 lg:mb-12 space-y-4 lg:space-y-0">
			<div class="text-center lg:text-left">
				<h1 class="text-3xl lg:text-4xl font-bold text-primary mb-2">Your CVs</h1>
				<p class="text-base lg:text-lg text-secondary">Create and manage your professional resumes with AI assistance</p>
			</div>
			
			<button
				on:click={createNewCV}
				class="flex items-center justify-center space-x-2 lg:space-x-3 bg-accent hover:bg-accent-hover text-white px-4 lg:px-6 py-2 lg:py-3 rounded-xl transition-colors shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 w-full lg:w-auto"
			>
				<Plus size={18} lg:size={20} />
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
		<!-- Responsive Empty State -->
		<div class="text-center py-12 lg:py-20 px-4">
			<div class="w-20 lg:w-24 h-20 lg:h-24 bg-gradient-to-br from-accent to-blue-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg">
				<FileText size={28} lg:size={32} class="text-white" />
			</div>
			<h3 class="text-xl lg:text-2xl font-semibold text-primary mb-3">Ready to create your first CV?</h3>
			<p class="text-secondary mb-8 max-w-md mx-auto text-sm lg:text-base">Build a professional resume with our AI-powered editor and get real-time feedback to land your dream job.</p>
			<button
				on:click={createNewCV}
				class="bg-accent hover:bg-accent-hover text-white px-6 lg:px-8 py-3 lg:py-4 rounded-xl transition-colors shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 font-medium text-base lg:text-lg w-full sm:w-auto"
			>
				Create Your First CV
			</button>
		</div>
	{:else}
		<!-- Responsive CV Grid -->
		<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-8">
			{#each userCVs as cv}
				<div class="bg-secondary border border-border rounded-xl p-4 lg:p-6 hover:shadow-xl transition-all duration-300 hover:-translate-y-1 group">
					<!-- Responsive CV Header -->
					<div class="flex items-start justify-between mb-4 lg:mb-6">
						<div class="flex-1 min-w-0">
							<h3 class="font-semibold text-primary text-base lg:text-lg truncate mb-2">{cv.name}</h3>
							<div class="flex items-center text-xs lg:text-sm text-secondary">
								<Calendar size={12} lg:size={14} class="mr-2 flex-shrink-0" />
								<span class="truncate">Updated {formatDate(cv.updated_at)}</span>
							</div>
						</div>
						<div class="w-10 lg:w-12 h-10 lg:h-12 bg-tertiary rounded-lg flex items-center justify-center group-hover:bg-accent group-hover:text-white transition-colors ml-3">
							<FileText size={18} lg:size={20} />
						</div>
					</div>

					<!-- Responsive CV Preview -->
					<div class="text-xs lg:text-sm text-secondary mb-4 lg:mb-6 bg-tertiary rounded-lg p-3 lg:p-4 min-h-[60px] lg:min-h-[80px]">
						{cv.markdown_content ? cv.markdown_content.substring(0, 100) + '...' : 'No content yet - click Edit to start building your CV'}
					</div>

					<!-- Responsive Actions -->
					<div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3">
						<button
							on:click={() => goto(`/editor/${cv.id}`)}
							class="flex-1 bg-accent hover:bg-accent-hover text-white py-2 lg:py-3 rounded-lg transition-colors font-medium shadow-sm hover:shadow-md text-sm lg:text-base"
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
							class="sm:w-auto w-full flex items-center justify-center p-2 lg:p-3 border border-border hover:bg-tertiary hover:border-accent rounded-lg transition-colors group"
							title="Download PDF"
						>
							<Download size={16} lg:size={18} class="group-hover:text-accent" />
							<span class="ml-2 sm:hidden text-sm">Download PDF</span>
						</button>
					</div>
				</div>
			{/each}
		</div>
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