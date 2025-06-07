<script lang="ts">
    import { atsAnalysis, isLLMLoading, llmService } from '$lib/stores/llm.js';
    import { currentCV, draftCV } from '$lib/stores/cv.js';
    import { addToast } from '$lib/stores/toast.js';
    import { Zap, CheckCircle, AlertCircle, TrendingUp, Target, FileText, ArrowUp, ArrowDown, Hash } from 'lucide-svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Input from '$lib/components/common/Input.svelte';

    // Define types for ATS analysis
    interface ATSAnalysis {
        ats_score: number;
        score_breakdown?: Record<string, number>;
        strengths?: string[];
        weaknesses?: string[];
        upgrade_suggestions?: string[];
        keyword_analysis?: {
            present_keywords?: string[];
            missing_keywords?: string[];
        };
    }

    let targetRole = '';
    let jobDescription = '';
    let showJobDescription = false;

    // Type the reactive variable
    $: typedATSAnalysis = $atsAnalysis as ATSAnalysis | null;

    async function analyzeATS() {
        if (!$draftCV?.markdown_content?.trim()) {
            addToast('Please add some content to your CV first', 'error');
            return;
        }

        try {
            const result = await llmService.analyzeATS(
                $currentCV?.id,
                $draftCV.markdown_content,
                targetRole.trim() || undefined,
                jobDescription.trim() || undefined
            );

            if (!result.success) {
                addToast(result.error || 'ATS analysis failed', 'error');
            }
        } catch (error) {
            addToast('Failed to analyze CV', 'error');
        }
    }

    function getScoreColor(score: number): string {
        if (score >= 80) return 'text-green-600';
        if (score >= 60) return 'text-yellow-600';
        return 'text-red-600';
    }

    function getScoreBgColor(score: number): string {
        if (score >= 80) return 'bg-green-100 dark:bg-green-900';
        if (score >= 60) return 'bg-yellow-100 dark:bg-yellow-900';
        return 'bg-red-100 dark:bg-red-900';
    }

    function getProgressBarColor(score: number): string {
        if (score >= 20) return 'bg-green-500';
        if (score >= 15) return 'bg-yellow-500';
        return 'bg-red-500';
    }
</script>

<!-- FIXED: Added dark mode styling throughout -->
<div class="flex flex-col h-full bg-white dark:bg-gray-900">
    <!-- Header -->
    <div class="border-b border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-900">
        <div class="flex items-center space-x-2">
            <Zap class="h-4 w-4 text-gray-500 dark:text-gray-400" />
            <h3 class="font-medium text-gray-900 dark:text-white">ATS Score Analysis</h3>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-300 mt-1">
            Get your CV scored for Applicant Tracking Systems
        </p>
    </div>

    <!-- Analysis Form -->
    <div class="p-4 border-b border-gray-200 dark:border-gray-700 space-y-4 bg-white dark:bg-gray-900">
        <Input
            label="Target Role (Optional)"
            placeholder="e.g. Software Engineer, Marketing Manager"
            bind:value={targetRole}
        />

        <div>
            <button
                class="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300"
                on:click={() => showJobDescription = !showJobDescription}
            >
                {showJobDescription ? 'Hide' : 'Add'} Job Description (Optional)
            </button>

            {#if showJobDescription}
                <div class="mt-2">
                    <textarea
                        bind:value={jobDescription}
                        placeholder="Paste the job description here for more accurate analysis..."
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 rounded-lg resize-none focus:ring-2 focus:ring-primary-500 dark:focus:ring-primary-400 focus:border-primary-500 dark:focus:border-primary-400"
                        rows="4"
                    ></textarea>
                </div>
            {/if}
        </div>

        <Button
            on:click={analyzeATS}
            loading={$isLLMLoading}
            disabled={$isLLMLoading || !$draftCV?.markdown_content?.trim()}
            className="w-full"
        >
            <Zap class="h-4 w-4 mr-2" />
            Analyze ATS Score
        </Button>
    </div>

    <!-- Results -->
    <div class="flex-1 overflow-y-auto p-4 bg-white dark:bg-gray-900">
        {#if typedATSAnalysis}
            <div class="space-y-6">
                <!-- Overall Score -->
                <div class="text-center">
                    <div class="inline-flex items-center justify-center w-20 h-20 rounded-full {getScoreBgColor(typedATSAnalysis.ats_score)} mb-3">
                        <span class="text-2xl font-bold {getScoreColor(typedATSAnalysis.ats_score)}">
                            {typedATSAnalysis.ats_score}
                        </span>
                    </div>
                    <h4 class="text-lg font-semibold text-gray-900 dark:text-white">
                        ATS Compatibility Score
                    </h4>
                    <p class="text-sm text-gray-600 dark:text-gray-300">
                        {#if typedATSAnalysis.ats_score >= 80}
                            Excellent! Your CV is highly ATS-friendly.
                        {:else if typedATSAnalysis.ats_score >= 60}
                            Good, but there's room for improvement.
                        {:else}
                            Needs improvement to pass ATS screening.
                        {/if}
                    </p>
                </div>

                <!-- Score Breakdown -->
                {#if typedATSAnalysis.score_breakdown}
                    <div>
                        <h5 class="font-medium text-gray-900 dark:text-white mb-3 flex items-center">
                            <Target class="h-4 w-4 mr-2" />
                            Score Breakdown
                        </h5>
                        <div class="space-y-2">
                            {#each Object.entries(typedATSAnalysis.score_breakdown) as [category, score]}
                                <div class="flex items-center justify-between">
                                    <span class="text-sm text-gray-600 dark:text-gray-300 capitalize">{category}</span>
                                    <div class="flex items-center space-x-2">
                                        <div class="w-20 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                                            <div 
                                                class="h-2 rounded-full {getProgressBarColor(score)}"
                                                style="width: {(score / 25) * 100}%"
                                            ></div>
                                        </div>
                                        <span class="text-sm font-medium w-8 text-gray-900 dark:text-white">{score}/25</span>
                                    </div>
                                </div>
                            {/each}
                        </div>
                    </div>
                {/if}

                <!-- FIXED: Added Strengths Section -->
                {#if typedATSAnalysis.strengths && typedATSAnalysis.strengths.length > 0}
                    <div>
                        <h5 class="font-medium text-gray-900 dark:text-white mb-3 flex items-center">
                            <CheckCircle class="h-4 w-4 mr-2 text-green-500" />
                            Strengths
                        </h5>
                        <div class="space-y-2">
                            {#each typedATSAnalysis.strengths as strength}
                                <div class="flex items-start space-x-2">
                                    <CheckCircle class="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                                    <span class="text-sm text-gray-700 dark:text-gray-300">{strength}</span>
                                </div>
                            {/each}
                        </div>
                    </div>
                {/if}

                <!-- FIXED: Added Weaknesses Section -->
                {#if typedATSAnalysis.weaknesses && typedATSAnalysis.weaknesses.length > 0}
                    <div>
                        <h5 class="font-medium text-gray-900 dark:text-white mb-3 flex items-center">
                            <AlertCircle class="h-4 w-4 mr-2 text-red-500" />
                            Areas for Improvement
                        </h5>
                        <div class="space-y-2">
                            {#each typedATSAnalysis.weaknesses as weakness}
                                <div class="flex items-start space-x-2">
                                    <AlertCircle class="h-4 w-4 text-red-500 mt-0.5 flex-shrink-0" />
                                    <span class="text-sm text-gray-700 dark:text-gray-300">{weakness}</span>
                                </div>
                            {/each}
                        </div>
                    </div>
                {/if}

                <!-- FIXED: Added Upgrade Suggestions Section -->
                {#if typedATSAnalysis.upgrade_suggestions && typedATSAnalysis.upgrade_suggestions.length > 0}
                    <div>
                        <h5 class="font-medium text-gray-900 dark:text-white mb-3 flex items-center">
                            <TrendingUp class="h-4 w-4 mr-2 text-blue-500" />
                            Upgrade Suggestions
                        </h5>
                        <div class="space-y-3">
                            {#each typedATSAnalysis.upgrade_suggestions as suggestion}
                                <div class="bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded-lg p-3">
                                    <div class="flex items-start space-x-2">
                                        <ArrowUp class="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                                        <span class="text-sm text-blue-800 dark:text-blue-200">{suggestion}</span>
                                    </div>
                                </div>
                            {/each}
                        </div>
                    </div>
                {/if}

                <!-- FIXED: Added Keyword Analysis Section -->
                {#if typedATSAnalysis.keyword_analysis}
                    <div>
                        <h5 class="font-medium text-gray-900 dark:text-white mb-3 flex items-center">
                            <Hash class="h-4 w-4 mr-2 text-purple-500" />
                            Keyword Analysis
                        </h5>
                        <div class="space-y-4">
                            <!-- Present Keywords -->
                            {#if typedATSAnalysis.keyword_analysis.present_keywords && typedATSAnalysis.keyword_analysis.present_keywords.length > 0}
                                <div>
                                    <h6 class="text-sm font-medium text-gray-900 dark:text-white mb-2 flex items-center">
                                        <CheckCircle class="h-3 w-3 mr-1 text-green-500" />
                                        Keywords Found
                                    </h6>
                                    <div class="flex flex-wrap gap-2">
                                        {#each typedATSAnalysis.keyword_analysis.present_keywords as keyword}
                                            <span class="inline-block bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 text-xs px-2 py-1 rounded-full">
                                                {keyword}
                                            </span>
                                        {/each}
                                    </div>
                                </div>
                            {/if}

                            <!-- Missing Keywords -->
                            {#if typedATSAnalysis.keyword_analysis.missing_keywords && typedATSAnalysis.keyword_analysis.missing_keywords.length > 0}
                                <div>
                                    <h6 class="text-sm font-medium text-gray-900 dark:text-white mb-2 flex items-center">
                                        <ArrowDown class="h-3 w-3 mr-1 text-red-500" />
                                        Suggested Keywords to Add
                                    </h6>
                                    <div class="flex flex-wrap gap-2">
                                        {#each typedATSAnalysis.keyword_analysis.missing_keywords as keyword}
                                            <span class="inline-block bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 text-xs px-2 py-1 rounded-full">
                                                {keyword}
                                            </span>
                                        {/each}
                                    </div>
                                </div>
                            {/if}
                        </div>
                    </div>
                {/if}
                
                <!-- Re-analyze Button -->
                <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
                    <div class="w-full">
                        <Button
                            variant="outline"
                            on:click={analyzeATS}
                            loading={$isLLMLoading}
                            disabled={$isLLMLoading}
                            className="w-full"
                        >
                            Re-analyze CV
                        </Button>
                    </div>
                </div>
            </div>
        {:else}
            <!-- Empty State -->
            <div class="text-center py-12">
                <Zap class="h-16 w-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
                <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    Get Your ATS Score
                </h4>
                <p class="text-gray-600 dark:text-gray-300 mb-6 max-w-sm mx-auto">
                    Analyze your CV to see how well it performs with Applicant Tracking Systems used by employers.
                </p>
                <div class="space-y-2 text-sm text-gray-500 dark:text-gray-400">
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