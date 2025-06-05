<script lang="ts">
    import { atsAnalysis, isLLMLoading, llmService } from '$lib/stores/llm.js';
    import { currentCV, draftCV } from '$lib/stores/cv.js';
    import { addToast } from '$lib/stores/toast.js';
    import { Zap, CheckCircle, AlertCircle, TrendingUp, Target, FileText } from 'lucide-svelte';
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
                 <label for="job-description" class="block text-sm font-medium text-gray-700 mb-2">
                    Job Description
                </label>
                <textarea
                    id="job-description"
                    bind:value={jobDescription}
                    placeholder="Paste the job description here for more targeted analysis..."
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    rows="4"
                />
            </div>
        {/if}

        <div class="w-full">
            <Button
                on:click={analyzeATS}
                loading={$isLLMLoading}
                disabled={$isLLMLoading || !$draftCV?.markdown_content?.trim()}
            >
                {#if $isLLMLoading}
                    Analyzing...
                {:else}
                    Analyze ATS Score
                {/if}
            </Button>
        </div>
    </div>

    <!-- Results -->
    <div class="flex-1 overflow-y-auto p-4">
        {#if typedATSAnalysis}
            <div class="space-y-6">
                <!-- Overall Score -->
                <div class="text-center">
                    <div class="inline-flex items-center justify-center w-20 h-20 rounded-full {getScoreBgColor(typedATSAnalysis.ats_score)} mb-3">
                        <span class="text-2xl font-bold {getScoreColor(typedATSAnalysis.ats_score)}">
                            {typedATSAnalysis.ats_score}
                        </span>
                    </div>
                    <h4 class="text-lg font-semibold text-gray-900">
                        ATS Compatibility Score
                    </h4>
                    <p class="text-sm text-gray-600">
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
                        <h5 class="font-medium text-gray-900 mb-3 flex items-center">
                            <Target class="h-4 w-4 mr-2" />
                            Score Breakdown
                        </h5>
                        <div class="space-y-2">
                            {#each Object.entries(typedATSAnalysis.score_breakdown) as [category, score]}
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

                <!-- Rest of your template remains the same, just replace $atsAnalysis with typedATSAnalysis -->
                
                <!-- Re-analyze Button -->
                <div class="pt-4 border-t border-gray-200">
                    <div class="w-full">
                        <Button
                            variant="outline"
                            on:click={analyzeATS}
                            loading={$isLLMLoading}
                            disabled={$isLLMLoading}
                        >
                            Re-analyze CV
                        </Button>
                    </div>
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