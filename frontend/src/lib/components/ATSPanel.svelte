<script>
	import { onMount } from 'svelte';
	import { llm } from '$lib/api.js';
	import { BarChart3, TrendingUp, AlertCircle, CheckCircle, RefreshCw } from 'lucide-svelte';
	
	export let cvId;
	
	let atsData = null;
	let isLoading = false;
	let targetRole = '';
	
	onMount(() => {
		analyzeCV();
	});
	
	async function analyzeCV() {
		if (!cvId) return;
		
		isLoading = true;
		try {
			atsData = await llm.atsScore(cvId, targetRole || null);
		} catch (error) {
			console.error('ATS analysis failed:', error);
		} finally {
			isLoading = false;
		}
	}
	
	function getScoreColor(score) {
		if (score >= 80) return 'text-green-500';
		if (score >= 60) return 'text-yellow-500';
		return 'text-red-500';
	}
	
	function getProgressWidth(current, max) {
		return `${(current / max) * 100}%`;
	}
</script>

<div class="flex flex-col h-full">
	<div class="bg-tertiary px-4 py-2 border-b border-border">
		<span class="text-sm font-medium text-primary">ATS Analysis</span>
	</div>
	
	<div class="flex-1 overflow-y-auto p-4">
		<!-- Target Role Input -->
		<div class="mb-4">
			<label class="block text-xs font-medium text-secondary mb-1">
				Target Role (Optional)
			</label>
			<div class="flex space-x-2">
				<input
					bind:value={targetRole}
					placeholder="e.g. Software Engineer"
					class="flex-1 px-2 py-1 text-xs border border-border rounded bg-primary text-primary"
				/>
				<button
					on:click={analyzeCV}
					disabled={isLoading}
					class="px-2 py-1 bg-accent hover:bg-accent-hover disabled:opacity-50 text-white rounded text-xs"
				>
					<RefreshCw size={12} class={isLoading ? 'animate-spin' : ''} />
				</button>
			</div>
		</div>
		
		{#if isLoading}
			<div class="text-center py-8">
				<BarChart3 size={32} class="mx-auto mb-2 opacity-50 animate-pulse" />
				<p class="text-sm text-secondary">Analyzing your CV...</p>
			</div>
		{:else if atsData && atsData.success}
			<!-- Overall Score -->
			<div class="text-center mb-6">
				<div class="text-4xl font-bold {getScoreColor(atsData.ats_score)}">
					{atsData.ats_score}
				</div>
				<div class="text-sm text-secondary">ATS Score</div>
				<div class="text-xs text-secondary mt-1">
					{#if atsData.ats_score >= 80}
						Excellent ATS compatibility
					{:else if atsData.ats_score >= 60}
						Good, but room for improvement
					{:else}
						Needs significant improvements
					{/if}
				</div>
			</div>
			
			<!-- Score Breakdown -->
			<div class="space-y-3 mb-6">
				<h4 class="text-sm font-medium text-primary">Score Breakdown</h4>
				
				{#each Object.entries(atsData.score_breakdown) as [category, score]}
					<div class="text-sm">
						<div class="flex justify-between mb-1">
							<span class="capitalize">{category}</span>
							<span>{score}/25</span>
						</div>
						<div class="w-full bg-gray-200 rounded-full h-2">
							<div 
								class="bg-accent h-2 rounded-full transition-all duration-300" 
								style="width: {getProgressWidth(score, 25)}"
							></div>
						</div>
					</div>
				{/each}
			</div>
			
			<!-- Strengths -->
			{#if atsData.strengths && atsData.strengths.length > 0}
				<div class="mb-4">
					<h4 class="text-sm font-medium text-primary mb-2 flex items-center">
						<CheckCircle size={14} class="mr-1 text-green-500" />
						Strengths
					</h4>
					<div class="space-y-1">
						{#each atsData.strengths.slice(0, 3) as strength}
							<div class="text-xs text-secondary flex items-start">
								<div class="w-1 h-1 bg-green-500 rounded-full mt-1.5 mr-2 flex-shrink-0"></div>
								{strength}
							</div>
						{/each}
					</div>
				</div>
			{/if}
			
			<!-- Weaknesses -->
			{#if atsData.weaknesses && atsData.weaknesses.length > 0}
				<div class="mb-4">
					<h4 class="text-sm font-medium text-primary mb-2 flex items-center">
						<AlertCircle size={14} class="mr-1 text-red-500" />
						Areas to Improve
					</h4>
					<div class="space-y-1">
						{#each atsData.weaknesses.slice(0, 3) as weakness}
							<div class="text-xs text-secondary flex items-start">
								<div class="w-1 h-1 bg-red-500 rounded-full mt-1.5 mr-2 flex-shrink-0"></div>
								{weakness}
							</div>
						{/each}
					</div>
				</div>
			{/if}
			
			<!-- Upgrade Suggestions -->
			{#if atsData.upgrade_suggestions && atsData.upgrade_suggestions.length > 0}
				<div class="mb-4">
					<h4 class="text-sm font-medium text-primary mb-2 flex items-center">
						<TrendingUp size={14} class="mr-1 text-blue-500" />
						Quick Improvements
					</h4>
					<div class="space-y-2">
						{#each atsData.upgrade_suggestions.slice(0, 4) as suggestion}
							<button 
								class="w-full text-left text-xs p-2 bg-secondary hover:bg-tertiary rounded border border-border transition-colors"
								on:click={() => {
									// Could integrate with inline edit here
									console.log('Apply suggestion:', suggestion);
								}}
							>
								{suggestion}
							</button>
						{/each}
					</div>
				</div>
			{/if}
		{:else}
			<div class="text-center py-8">
				<AlertCircle size={32} class="mx-auto mb-2 opacity-50" />
				<p class="text-sm text-secondary">Failed to analyze CV</p>
				<button
					on:click={analyzeCV}
					class="mt-2 text-xs text-accent hover:underline"
				>
					Try again
				</button>
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