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

<div class="bg-gradient-to-br from-primary-50 to-blue-100 min-h-screen">
    <!-- Hero Section -->
    <div class="relative overflow-hidden">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
            <div class="text-center">
                <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                    Create Professional CVs
                    <span class="text-primary-600">in Minutes</span>
                </h1>
                <p class="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
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

    <!-- Features Section -->
    <div class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-16">
                <h2 class="text-3xl font-bold text-gray-900 mb-4">
                    Everything you need to create the perfect CV
                </h2>
                <p class="text-lg text-gray-600">
                    Powerful features designed to make CV creation effortless
                </p>
            </div>

            <div class="grid md:grid-cols-3 gap-8">
                <!-- Real-time Preview -->
                <div class="text-center p-6">
                    <div class="w-16 h-16 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                        <FileText class="h-8 w-8 text-primary-600" />
                    </div>
                    <h3 class="text-xl font-semibold text-gray-900 mb-2">Real-time Preview</h3>
                    <p class="text-gray-600">
                        See your CV update instantly as you type with our live PDF preview
                    </p>
                </div>

                <!-- AI-Powered Editing -->
                <div class="text-center p-6">
                    <div class="w-16 h-16 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                        <Zap class="h-8 w-8 text-green-600" />
                    </div>
                    <h3 class="text-xl font-semibold text-gray-900 mb-2">AI-Powered Editing</h3>
                    <p class="text-gray-600">
                        Get intelligent suggestions and improvements with our built-in AI assistant
                    </p>
                </div>

                <!-- Professional Templates -->
                <div class="text-center p-6">
                    <div class="w-16 h-16 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                        <Edit3 class="h-8 w-8 text-purple-600" />
                    </div>
                    <h3 class="text-xl font-semibold text-gray-900 mb-2">Professional Templates</h3>
                    <p class="text-gray-600">
                        Choose from carefully designed templates for different industries
                    </p>
                </div>

                <!-- Easy Export -->
                <div class="text-center p-6">
                    <div class="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                        <Download class="h-8 w-8 text-blue-600" />
                    </div>
                    <h3 class="text-xl font-semibold text-gray-900 mb-2">Multiple Export Options</h3>
                    <p class="text-gray-600">
                        Download your CV as PDF or Markdown with custom styling options
                    </p>
                </div>

                <!-- ATS Optimization -->
                <div class="text-center p-6">
                    <div class="w-16 h-16 bg-orange-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                        <Shield class="h-8 w-8 text-orange-600" />
                    </div>
                    <h3 class="text-xl font-semibold text-gray-900 mb-2">ATS Optimization</h3>
                    <p class="text-gray-600">
                        Get scored and suggestions to make your CV ATS-friendly
                    </p>
                </div>

                <!-- Secure & Private -->
                <div class="text-center p-6">
                    <div class="w-16 h-16 bg-red-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                        <Users class="h-8 w-8 text-red-600" />
                    </div>
                    <h3 class="text-xl font-semibold text-gray-900 mb-2">Secure & Private</h3>
                    <p class="text-gray-600">
                        Your data is encrypted and stored securely. You own your content
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- CTA Section -->
    <div class="py-20 bg-primary-600">
        <div class="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
            <h2 class="text-3xl font-bold text-white mb-4">
                Ready to create your perfect CV?
            </h2>
            <p class="text-xl text-primary-100 mb-8">
                Join thousands of professionals who have already built their careers with ResumeForge
            </p>
            <Button size="lg" variant="secondary" on:click={handleGetStarted}>
                Get Started Now - It's Free
            </Button>
        </div>
    </div>
</div>