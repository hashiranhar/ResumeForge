<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { cvs } from '$lib/api.js';
	import { currentCV, loading } from '$lib/stores.js';
	import { Save, Download, MessageSquare, BarChart3 } from 'lucide-svelte';
	
	let markdownContent = '';
	let pdfPreviewUrl = '';
	let showChat = false;
	let showATS = false;
	
	const cvId = $page.params.id;
	
	onMount(async () => {
		// Load CV
		try {
			const cv = await cvs.get(cvId);
			currentCV.set(cv);
			markdownContent = cv.markdown_content || '';
			generatePDFPreview();
		} catch (err) {
			console.error('Failed to load CV');
		}
	});
	
	let previewTimeout;
	function handleContentChange() {
		currentCV.updateContent(markdownContent);
		clearTimeout(previewTimeout);
		previewTimeout = setTimeout(generatePDFPreview, 1000);
	}
	
	async function generatePDFPreview() {
		try {
			const blob = await cvs.downloadPDF(cvId);
			if (pdfPreviewUrl) URL.revokeObjectURL(pdfPreviewUrl);
			pdfPreviewUrl = URL.createObjectURL(blob);
		} catch (err) {
			console.error('Failed to generate preview');
		}
	}
	
	async function saveCV() {
		if (!$currentCV) return;
		loading.set(true);
		try {
			await cvs.update(cvId, {
				markdown_content: markdownContent
			});
		} finally {
			loading.set(false);
		}
	}
	
	async function downloadPDF() {
		try {
			const blob = await cvs.downloadPDF(cvId);
			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = `${$currentCV?.name || 'CV'}.pdf`;
			a.click();
			URL.revokeObjectURL(url);
		} catch (err) {
			console.error('Download failed');
		}
	}
</script>

<svelte:head>
	<title>Edit CV - ResumeForge</title>
</svelte:head>

<div class="h-screen flex flex-col">
	<!-- Toolbar -->
	<div class="bg-secondary border-b border-border px-4 py-3 flex justify-between items-center">
		<div class="flex items-center space-x-4">
			<h1 class="font-medium text-primary">{$currentCV?.name || 'Loading...'}</h1>
			<span class="text-sm text-secondary">
				{$loading ? 'Saving...' : 'Auto-saved'}
			</span>
		</div>
		
		<div class="flex items-center space-x-2">
			<!-- ATS Score -->
			<button
				on:click={() => showATS = !showATS}
				class="flex items-center space-x-2 px-3 py-2 bg-tertiary hover:bg-accent text-primary hover:text-white rounded-lg transition-colors"
			>
				<BarChart3 size={16} />
				<span>ATS Score</span>
			</button>
			
			<!-- Chat Toggle -->
			<button
				on:click={() => showChat = !showChat}
				class="flex items-center space-x-2 px-3 py-2 bg-tertiary hover:bg-accent text-primary hover:text-white rounded-lg transition-colors"
			>
				<MessageSquare size={16} />
				<span>AI Chat</span>
			</button>
			
			<!-- Save -->
			<button
				on:click={saveCV}
				class="flex items-center space-x-2 px-3 py-2 bg-accent hover:bg-accent-hover text-white rounded-lg transition-colors"
			>
				<Save size={16} />
				<span>Save</span>
			</button>
			
			<!-- Download -->
			<button
				on:click={downloadPDF}
				class="flex items-center space-x-2 px-3 py-2 border border-border hover:bg-tertiary rounded-lg transition-colors"
			>
				<Download size={16} />
				<span>PDF</span>
			</button>
		</div>
	</div>
	
	<!-- Main Content -->
	<div class="flex-1 flex overflow-hidden">
		<!-- Editor Panel -->
		<div class="flex-1 flex flex-col">
			<div class="bg-tertiary px-4 py-2 border-b border-border">
				<span class="text-sm font-medium text-primary">Markdown Editor</span>
			</div>
			<textarea
				bind:value={markdownContent}
				on:input={handleContentChange}
				class="flex-1 p-4 bg-primary text-primary border-none resize-none focus:outline-none font-mono text-sm"
				placeholder="# Your Name
**Your Title**

## Experience

## Skills

## Education"
			></textarea>
		</div>
		
		<!-- PDF Preview Panel -->
		<div class="flex-1 flex flex-col border-l border-border">
			<div class="bg-tertiary px-4 py-2 border-b border-border">
				<span class="text-sm font-medium text-primary">PDF Preview</span>
			</div>
			<div class="flex-1 bg-gray-100">
				{#if pdfPreviewUrl}
					<iframe
						src={pdfPreviewUrl}
						class="w-full h-full"
						title="PDF Preview"
					></iframe>
				{:else}
					<div class="flex items-center justify-center h-full text-secondary">
						Generating preview...
					</div>
				{/if}
			</div>
		</div>
		
		<!-- AI Chat Sidebar -->
		{#if showChat}
			<div class="w-80 bg-secondary border-l border-border flex flex-col">
				<div class="bg-tertiary px-4 py-2 border-b border-border">
					<span class="text-sm font-medium text-primary">AI Assistant</span>
				</div>
				<div class="flex-1 p-4">
					<div class="text-sm text-secondary mb-4">
						Ask me anything about your CV!
					</div>
					<!-- Chat interface will go here -->
					<div class="space-y-2">
						<div class="text-sm bg-accent/10 p-3 rounded-lg">
							<strong>AI:</strong> How can I help improve your CV today?
						</div>
					</div>
					
					<!-- Chat Input -->
					<div class="mt-4">
						<input
							type="text"
							placeholder="Ask about your CV..."
							class="w-full px-3 py-2 border border-border rounded-lg bg-primary text-primary"
						/>
					</div>
				</div>
			</div>
		{/if}
		
		<!-- ATS Score Sidebar -->
		{#if showATS}
			<div class="w-80 bg-secondary border-l border-border flex flex-col">
				<div class="bg-tertiary px-4 py-2 border-b border-border">
					<span class="text-sm font-medium text-primary">ATS Analysis</span>
				</div>
				<div class="flex-1 p-4">
					<div class="text-center mb-4">
						<div class="text-3xl font-bold text-accent">85</div>
						<div class="text-sm text-secondary">ATS Score</div>
					</div>
					
					<div class="space-y-3">
						<div class="text-sm">
							<div class="flex justify-between mb-1">
								<span>Formatting</span>
								<span>22/25</span>
							</div>
							<div class="w-full bg-gray-200 rounded-full h-2">
								<div class="bg-accent h-2 rounded-full" style="width: 88%"></div>
							</div>
						</div>
						
						<div class="text-sm">
							<div class="flex justify-between mb-1">
								<span>Keywords</span>
								<span>20/25</span>
							</div>
							<div class="w-full bg-gray-200 rounded-full h-2">
								<div class="bg-accent h-2 rounded-full" style="width: 80%"></div>
							</div>
						</div>
					</div>
				</div>
			</div>
		{/if}
	</div>
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
</style>