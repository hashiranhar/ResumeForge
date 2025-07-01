<script>
    import { isAuthenticated } from '$lib/stores/auth.js';
    import { goto } from '$app/navigation';
    import { FileText, Edit3, Download, Zap, Users, Shield } from 'lucide-svelte';
    import Button from '$lib/components/common/Button.svelte';

    function handleGetStarted() {
        if ($isAuthenticated) {
            goto('/dashboard');
        } else {
            goto('/auth/register');
        }
    }

    function handleTryDemo() {
        goto('/editor?demo=true');
    }
</script>

<svelte:head>
    <title>ResumeForge - Professional CV Builder</title>
    <meta name="description" content="Create professional CVs with our AI-powered Markdown editor. Build, customize, and export beautiful resumes in minutes." />
</svelte:head>

<div class="bg-gradient-to-br from-primary-50 to-blue-100 dark:from-black dark:to-black min-h-screen">
    <!-- Hero Section -->
    <div class="relative overflow-hidden">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
            <div class="text-center">
                <h1 class="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
                    Create Professional CVs
                    <span class="text-primary-600 dark:text-primary-400">in Minutes</span>
                </h1>
                <p class="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
                    Build stunning resumes with our AI-powered Markdown editor. 
                    Real-time PDF preview, professional templates, and intelligent suggestions.
                </p>
                <div class="flex flex-col sm:flex-row gap-4 justify-center">
                    <Button size="lg" on:click={handleGetStarted}>
                        <FileText class="h-5 w-5 mr-2" />
                        Get Started Free
                    </Button>
                    <Button variant="outline" size="lg" on:click={handleTryDemo}>
                        <Edit3 class="h-5 w-5 mr-2" />
                        Try Demo
                    </Button>
                </div>
            </div>
        </div>
    </div>

    <!-- Video Section -->
    <div class="py-20 bg-white dark:bg-black">
        <div class="relative w-full py-20 bg-white dark:bg-black flex items-center justify-center">
        <video
            src="/demo-showcase.mp4"
            autoplay
            loop
            muted
            playsinline
            class="rounded-xl shadow-2xl w-full max-w-5xl object-cover pointer-events-none select-none"
            style="aspect-ratio: 16/9;"
        ></video>
        <!-- Optional: Overlay for subtle darkening effect -->
        <div class="absolute inset-0 bg-black bg-opacity-10 pointer-events-none rounded-xl"></div>
        </div>
    </div>

</div>