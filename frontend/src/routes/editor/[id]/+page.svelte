<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { cvs, llm } from '$lib/api.js';
	import { currentCV, loading } from '$lib/stores.js';
	import { Save, Download, MessageSquare, BarChart3, Wand2 } from 'lucide-svelte';
	import ChatPanel from '$lib/components/ChatPanel.svelte';
	import ATSPanel from '$lib/components/ATSPanel.svelte';
	
	let markdownContent = '';
	let pdfPreviewUrl = '';
	let showChat = false;
	let showATS = false;
	let quickEditInstruction = '';
	
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
	
	async function quickEdit() {
		if (!quickEditInstruction.trim()) return;
		
		loading.set(true);
		try {
			const response = await llm.inlineEdit(cvId, quickEditInstruction, null, true);
			if (response.success) {
				markdownContent = response.edited_content;
				currentCV.updateContent(markdownContent);
				generatePDFPreview();
			}
			quickEditInstruction = '';
		} catch (err) {
			console.error('Quick edit failed');
		} finally {
			loading.set(false);
		}
	}
</script>

<svelte:head>
	<title>Edit CV - ResumeForge</title>
</svelte:head>

<div class="h-screen flex flex-col bg-primary">
	<!-- Enhanced Responsive Toolbar -->
	<div class="bg-secondary border-b border-border px-4 lg:px-6 py-3 lg:py-4 flex flex-col lg:flex-row lg:justify-between lg:items-center shadow-sm space-y-3 lg:space-y-0">
		<div class="flex items-center space-x-4 lg:space-x-6">
			<div>
				<h1 class="text-base lg:text-lg font-semibold text-primary truncate">{$currentCV?.name || 'Loading...'}</h1>
				<div class="flex items-center space-x-2 mt-1">
					<div class="w-2 h-2 rounded-full {$loading ? 'bg-yellow-500' : 'bg-green-500'}"></div>
					<span class="text-xs text-secondary">
						{$loading ? 'Saving...' : 'All changes saved'}
					</span>
				</div>
			</div>
		</div>
		
		<div class="flex items-center space-x-2 lg:space-x-3 overflow-x-auto pb-1">
			<!-- Mobile: Show/Hide Panels -->
			<div class="flex lg:hidden space-x-2">
				<button
					on:click={() => showATS = !showATS}
					class="flex items-center space-x-1 px-3 py-2 {showATS ? 'bg-accent text-white' : 'bg-tertiary text-primary'} rounded-lg transition-colors text-sm whitespace-nowrap"
				>
					<BarChart3 size={16} />
					<span>ATS</span>
				</button>
				
				<button
					on:click={() => showChat = !showChat}
					class="flex items-center space-x-1 px-3 py-2 {showChat ? 'bg-accent text-white' : 'bg-tertiary text-primary'} rounded-lg transition-colors text-sm whitespace-nowrap"
				>
					<MessageSquare size={16} />
					<span>AI</span>
				</button>
			</div>
			
			<!-- Desktop: Full Buttons -->
			<div class="hidden lg:flex space-x-3">
				<button
					on:click={() => showATS = !showATS}
					class="flex items-center space-x-2 px-4 py-2 {showATS ? 'bg-accent text-white' : 'bg-tertiary text-primary hover:bg-accent hover:text-white'} rounded-lg transition-colors shadow-sm"
				>
					<BarChart3 size={18} />
					<span class="font-medium">ATS Score</span>
				</button>
				
				<button
					on:click={() => showChat = !showChat}
					class="flex items-center space-x-2 px-4 py-2 {showChat ? 'bg-accent text-white' : 'bg-tertiary text-primary hover:bg-accent hover:text-white'} rounded-lg transition-colors shadow-sm"
				>
					<MessageSquare size={18} />
					<span class="font-medium">AI Chat</span>
				</button>
			</div>
			
			<!-- Save Button -->
			<button
				on:click={saveCV}
				disabled={$loading}
				class="flex items-center space-x-1 lg:space-x-2 px-3 lg:px-4 py-2 bg-accent hover:bg-accent-hover disabled:opacity-50 text-white rounded-lg transition-colors shadow-sm text-sm lg:text-base whitespace-nowrap"
			>
				<Save size={16} lg:size={18} />
				<span class="hidden sm:inline font-medium">Save</span>
			</button>
			
			<!-- Download Button -->
			<button
				on:click={downloadPDF}
				class="flex items-center space-x-1 lg:space-x-2 px-3 lg:px-4 py-2 border border-border hover:bg-tertiary rounded-lg transition-colors shadow-sm text-sm lg:text-base whitespace-nowrap"
			>
				<Download size={16} lg:size={18} />
				<span class="hidden sm:inline font-medium">PDF</span>
			</button>
		</div>
	</div>
	
	<!-- Responsive Main Content -->
	<div class="flex-1 flex flex-col lg:flex-row overflow-hidden">
		<!-- Mobile: Tabbed Interface -->
		<div class="lg:hidden bg-tertiary border-b border-border px-4 py-2">
			<div class="flex space-x-1">
				<button class="px-3 py-1 bg-accent text-white rounded text-sm">Editor</button>
				<button class="px-3 py-1 bg-secondary text-primary rounded text-sm">Preview</button>
			</div>
		</div>
		
		<!-- Editor Panel -->
		<div class="flex-1 flex flex-col bg-primary {showChat || showATS ? 'hidden lg:flex' : 'flex'}">
			<!-- Editor Header -->
			<div class="bg-tertiary px-4 lg:px-6 py-2 lg:py-3 border-b border-border flex items-center justify-between">
				<div class="flex items-center space-x-3">
					<div class="w-2 h-2 bg-accent rounded-full"></div>
					<span class="text-sm font-medium text-primary">Markdown Editor</span>
				</div>
				<div class="hidden lg:block text-xs text-secondary">
					Use [CENTER] and [DATE: content] for formatting
				</div>
			</div>
			
			<!-- Responsive Quick Edit Bar -->
			<div class="bg-secondary px-4 lg:px-6 py-3 lg:py-4 border-b border-border">
				<div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3">
					<div class="flex-1 relative">
						<input
							bind:value={quickEditInstruction}
							placeholder="✨ Quick AI edit: 'make skills more technical'..."
							class="w-full px-3 lg:px-4 py-2 lg:py-3 text-sm border border-border rounded-lg bg-primary text-primary placeholder-secondary focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent transition-all"
						/>
					</div>
					<button
						on:click={quickEdit}
						disabled={!quickEditInstruction.trim() || $loading}
						class="px-4 lg:px-6 py-2 lg:py-3 bg-accent hover:bg-accent-hover disabled:opacity-50 text-white rounded-lg text-sm font-medium flex items-center justify-center space-x-2 transition-colors shadow-sm"
					>
						<Wand2 size={16} />
						<span>Apply Edit</span>
					</button>
				</div>
			</div>
			
			<!-- Responsive Textarea -->
			<textarea
				bind:value={markdownContent}
				on:input={handleContentChange}
				class="flex-1 p-4 lg:p-6 bg-primary text-primary border-none resize-none focus:outline-none font-mono text-sm lg:text-sm leading-relaxed"
				placeholder="# Your Name &#123;.center&#125;&#10;**Your Professional Title** &#123;.center&#125;&#10;&#10;📧 email@example.com | 📱 +1 (555) 123-4567 &#123;.center&#125;&#10;&#10;## Professional Experience&#10;&#10;### Senior Software Engineer | Company Name &#123;.date-right: 2020 - Present&#125;&#10;- Led development of scalable web applications&#10;- Improved system performance by 40%&#10;- Managed team of 5 developers"
			></textarea>
		</div>
		
		<!-- PDF Preview Panel -->
		<div class="flex-1 flex flex-col bg-gray-50 border-l border-border {showChat || showATS ? 'hidden xl:flex' : 'hidden lg:flex'}">
			<!-- Preview Header -->
			<div class="bg-tertiary px-4 lg:px-6 py-2 lg:py-3 border-b border-border flex items-center justify-between">
				<div class="flex items-center space-x-3">
					<div class="w-2 h-2 bg-green-500 rounded-full"></div>
					<span class="text-sm font-medium text-primary">Live PDF Preview</span>
				</div>
				<div class="hidden lg:block text-xs text-secondary">
					Updates automatically as you type
				</div>
			</div>
			
			<!-- Responsive Preview Content -->
			<div class="flex-1 p-2 lg:p-4 bg-gray-50">
				{#if pdfPreviewUrl}
					<div class="h-full bg-white rounded-lg shadow-lg overflow-hidden">
						<iframe
							src={pdfPreviewUrl}
							class="w-full h-full"
							title="PDF Preview"
						></iframe>
					</div>
				{:else}
					<div class="flex flex-col items-center justify-center h-full text-secondary bg-white rounded-lg shadow-lg">
						<div class="animate-spin w-6 lg:w-8 h-6 lg:h-8 border-2 border-accent border-t-transparent rounded-full mb-4"></div>
						<p class="text-sm">Generating your beautiful PDF...</p>
					</div>
				{/if}
			</div>
		</div>
		
		<!-- Responsive AI Chat Sidebar -->
		{#if showChat}
			<div class="fixed inset-0 lg:relative lg:inset-auto w-full lg:w-96 bg-secondary border-l border-border shadow-lg z-50 lg:z-auto">
				<!-- Mobile: Close Button -->
				<div class="lg:hidden flex justify-between items-center p-4 border-b border-border">
					<h3 class="font-medium text-primary">AI Assistant</h3>
					<button 
						on:click={() => showChat = false}
						class="p-2 hover:bg-tertiary rounded-lg transition-colors"
					>
						<MessageSquare size={20} />
					</button>
				</div>
				<ChatPanel {cvId} />
			</div>
		{/if}
		
		<!-- Responsive ATS Score Sidebar -->
		{#if showATS}
			<div class="fixed inset-0 lg:relative lg:inset-auto w-full lg:w-96 bg-secondary border-l border-border shadow-lg z-50 lg:z-auto">
				<!-- Mobile: Close Button -->
				<div class="lg:hidden flex justify-between items-center p-4 border-b border-border">
					<h3 class="font-medium text-primary">ATS Analysis</h3>
					<button 
						on:click={() => showATS = false}
						class="p-2 hover:bg-tertiary rounded-lg transition-colors"
					>
						<BarChart3 size={20} />
					</button>
				</div>
				<ATSPanel {cvId} />
			</div>
		{/if}
	</div>
	
	<!-- Mobile Overlay -->
	{#if (showChat || showATS)}
		<div 
			class="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
			on:click={() => {showChat = false; showATS = false;}}
		></div>
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
</style>