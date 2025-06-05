<script>
    import { atsAnalysis, isLLMLoading, llmService } from '$lib/stores/llm.js';
    import { currentCV, draftCV } from '$lib/stores/cv.js';
    import { addToast } from '$lib/stores/toast.js';
    import { Zap, CheckCircle, AlertCircle, TrendingUp, Target, FileText } from 'lucide-svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Input from '$lib/components/common/Input.svelte';

    let targetRole = '';
    let jobDescription = '';
    let showJobDescription = false;

    async function analyzeATS() {
        if (!$draftCV.markdown_content?.trim()) {
            addToast('Please add some content to your CV first', 'error');
            return;
        }

        try {
            const result = await llmService.analyzeATS(
                $currentCV?.id,
                $draftCV.markdown_content,
                targetRole || null,
                jobDescription || null
            );

            if (!result.success) {
                addToast(result.error || 'ATS analysis failed', 'error');
            }
        } catch (error) {
            addToast('Failed to analyze CV', 'error');
        }
    }

    function getScoreColor(score) {
        if (score >= 80) return 'text-green-600';
        if (score >= 60) return 'text-yellow-600';
        return 'text-red-600';
    }

    function getScoreBgColor(score) {
        if (score >= 80) return 'bg-green-100';
        if (score >= 60) return 'bg-yellow-100';
        return 'bg-red-100';
    }
</script>

<div class="flex flex-col h-full">
    <!-- Header -->
    <div class="border-b border-gray-200 p-4">
        <div class="flex items-center space-x-2">
            <Zap class="h-4 w-4 text-gray-500" />
            <h3 class="font-medium text-gray-900">ATS Score Analysis</h3>
        </div>
        <p class="text-sm text-gray-600 mt-1">
            Get your CV scored for Applicant Tracking Systems
        </p>
    </div>

    <!-- Analysis Form -->
    <div class="p-4 border-b border-gray-200 space-y-4">
        <Input
            label="Target Role (Optional)"
            placeholder="e.g. Software Engineer, Marketing Manager"
            bind:value={targetRole}
        />

        <div>
            <button
                class="text-sm text-primary-600 hover:text-primary-700"
                on:click={() => showJobDescription = !showJobDescription}
            >
                {showJobDescription ? 'Hide' : 'Add'} Job Description (Optional)
            </button>
        </div>

        {#if showJobDescription}
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                    Job Description
                </label>
                <textarea
                    bind:value={jobDescription}
                    placeholder="Paste the job description here for more targeted analysis..."
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    rows="4"
                />
            </div>
        {/if}

        <Button
            on:click={analyzeATS}
            loading={$isLLMLoading}
            disabled={$isLLMLoading || !$draftCV.markdown_content?.trim()}
            class="w-full"
        >
            {#if $isLLMLoading}
                Analyzing...
            {:else}
                Analyze ATS Score
            {/if}
        </Button>
    </div>

    <!-- Results -->
    <div class="flex-1 overflow-y-auto p-4">
        {#if $atsAnalysis}
            <div class="space-y-6">
                <!-- Overall Score -->
                <div class="text-center">
                    <div class="inline-flex items-center justify-center w-20 h-20 rounded-full {getScoreBgColor($atsAnalysis.ats_score)} mb-3">
                        <span class="text-2xl font-bold {getScoreColor($atsAnalysis.ats_score)}">
                            {$atsAnalysis.ats_score}
                        </span>
                    </div>
                    <h4 class="text-lg font-semibold text-gray-900">
                        ATS Compatibility Score
                    </h4>
                    <p class="text-sm text-gray-600">
                        {#if $atsAnalysis.ats_score >= 80}
                            Excellent! Your CV is highly ATS-friendly.
                        {:else if $atsAnalysis.ats_score >= 60}
                            Good, but there's room for improvement.
                        {:else}
                            Needs improvement to pass ATS screening.
                        {/if}
                    </p>
                </div>

                <!-- Score Breakdown -->
                {#if $atsAnalysis.score_breakdown}
                    <div>
                        <h5 class="font-medium text-gray-900 mb-3 flex items-center">
                            <Target class="h-4 w-4 mr-2" />
                            Score Breakdown
                        </h5>
                        <div class="space-y-2">
                            {#each Object.entries($atsAnalysis.score_breakdown) as [category, score]}
                                <div class="flex items-center justify-between">
                                    <span class="text-sm text-gray-600 capitalize">{category}</span>
                                    <div class="flex items-center space-x-2">
                                        <div class="w-20 bg-gray-200 rounded-full h-2">
                                            <div 
                                                class="h-2 rounded-full {score >= 20 ? 'bg-green-500' : score >= 15 ? 'bg-yellow-500' : 'bg-red-500'}"
                                                style="width: {(score / 25) * 100}%"
                                            ></div>
                                        </div>
                                        <span class="text-sm font-medium w-8">{score}/25</span>
                                    </div>
                                </div>
                            {/each}
                        </div>
                    </div>
                {/if}

                <!-- Strengths -->
                {#if $atsAnalysis.strengths?.length > 0}
                    <div>
                        <h5 class="font-medium text-gray-900 mb-3 flex items-center">
                            <CheckCircle class="h-4 w-4 mr-2 text-green-500" />
                            Strengths
                        </h5>
                        <ul class="space-y-2">
                            {#each $atsAnalysis.strengths as strength}
                                <li class="flex items-start space-x-2">
                                    <CheckCircle class="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                                    <span class="text-sm text-gray-700">{strength}</span>
                                </li>
                            {/each}
                        </ul>
                    </div>
                {/if}

                <!-- Weaknesses -->
                {#if $atsAnalysis.weaknesses?.length > 0}
                    <div>
                        <h5 class="font-medium text-gray-900 mb-3 flex items-center">
                            <AlertCircle class="h-4 w-4 mr-2 text-red-500" />
                            Areas for Improvement
                        </h5>
                        <ul class="space-y-2">
                            {#each $atsAnalysis.weaknesses as weakness}
                                <li class="flex items-start space-x-2">
                                    <AlertCircle class="h-4 w-4 text-red-500 mt-0.5 flex-shrink-0" />
                                    <span class="text-sm text-gray-700">{weakness}</span>
                                </li>
                            {/each}
                        </ul>
                    </div>
                {/if}

                <!-- Upgrade Suggestions -->
                {#if $atsAnalysis.upgrade_suggestions?.length > 0}
                    <div>
                        <h5 class="font-medium text-gray-900 mb-3 flex items-center">
                            <TrendingUp class="h-4 w-4 mr-2 text-blue-500" />
                            Upgrade Suggestions
                        </h5>
                        <ul class="space-y-3">
                            {#each $atsAnalysis.upgrade_suggestions as suggestion}
                                <li class="bg-blue-50 border border-blue-200 rounded-lg p-3">
                                    <div class="flex items-start space-x-2">
                                        <TrendingUp class="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                                        <span class="text-sm text-blue-900">{suggestion}</span>
                                    </div>
                                </li>
                            {/each}
                        </ul>
                    </div>
                {/if}

                <!-- Keyword Analysis -->
                {#if $atsAnalysis.keyword_analysis && ($atsAnalysis.keyword_analysis.missing_keywords?.length > 0 || $atsAnalysis.keyword_analysis.present_keywords?.length > 0)}
                    <div>
                        <h5 class="font-medium text-gray-900 mb-3 flex items-center">
                            <FileText class="h-4 w-4 mr-2 text-purple-500" />
                            Keyword Analysis
                        </h5>
                        
                        {#if $atsAnalysis.keyword_analysis.present_keywords?.length > 0}
                            <div class="mb-4">
                                <h6 class="text-sm font-medium text-green-700 mb-2">Found Keywords</h6>
                                <div class="flex flex-wrap gap-1">
                                    {#each $atsAnalysis.keyword_analysis.present_keywords as keyword}
                                        <span class="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                                            {keyword}
                                        </span>
                                    {/each}
                                </div>
                            </div>
                        {/if}

                        {#if $atsAnalysis.keyword_analysis.missing_keywords?.length > 0}
                            <div>
                                <h6 class="text-sm font-medium text-orange-700 mb-2">Consider Adding</h6>
                                <div class="flex flex-wrap gap-1">
                                    {#each $atsAnalysis.keyword_analysis.missing_keywords as keyword}
                                        <span class="inline-block bg-orange-100 text-orange-800 text-xs px-2 py-1 rounded">
                                            {keyword}
                                        </span>
                                    {/each}
                                </div>
                            </div>
                        {/if}
                    </div>
                {/if}

                <!-- Re-analyze Button -->
                <div class="pt-4 border-t border-gray-200">
                    <Button
                        variant="outline"
                        on:click={analyzeATS}
                        loading={$isLLMLoading}
                        disabled={$isLLMLoading}
                        class="w-full"
                    >
                        Re-analyze CV
                    </Button>
                </div>
            </div>
        {:else}
            <!-- Empty State -->
            <div class="text-center py-12">
                <Zap class="h-16 w-16 text-gray-300 mx-auto mb-4" />
                <h4 class="text-lg font-medium text-gray-900 mb-2">
                    Get Your ATS Score
                </h4>
                <p class="text-gray-600 mb-6 max-w-sm mx-auto">
                    Analyze your CV to see how well it performs with Applicant Tracking Systems used by employers.
                </p>
                <div class="space-y-2 text-sm text-gray-500">
                    <div class="flex items-center justify-center space-x-2">
                        <CheckCircle class="h-4 w-4 text-green-500" />
                        <span>Keyword optimization analysis</span>
                    </div>
                    <div class="flex items-center justify-center space-x-2">
                        <CheckCircle class="h-4 w-4 text-green-500" />
                        <span>Formatting and structure review</span>
                    </div>
                    <div class="flex items-center justify-center space-x-2">
                        <CheckCircle class="h-4 w-4 text-green-500" />
                        <span>Actionable improvement suggestions</span>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>