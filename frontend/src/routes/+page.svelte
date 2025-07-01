<script>
    import { isAuthenticated } from '$lib/stores/auth.js';
    import { goto } from '$app/navigation';
    import { 
        FileText, Edit3, Download, Zap, ArrowRight, Play, 
        CheckCircle, Sparkles, Brain, Target, Clock, MessageSquare, Scan
    } from 'lucide-svelte';
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

    function handleLogin() {
        goto('/auth/login');
    }

    // Feature demos
    const featureDemos = [
        {
            title: "Edit Markdown → PDF Generated",
            description: "Write in markdown, see instant PDF preview",
            icon: Edit3,
            color: "blue"
        },
        {
            title: "Inline Editor",
            description: "Smart AI suggestions as you type",
            icon: Sparkles,
            color: "purple"
        },
        {
            title: "Chat Bot Assistant",
            description: "Get personalized resume advice",
            icon: MessageSquare,
            color: "green"
        },
        {
            title: "ATS Scanner",
            description: "Real-time optimization scoring",
            icon: Scan,
            color: "orange"
        }
    ];
</script>

<svelte:head>
    <title>ResumeForge - AI-Powered Professional Resume Builder</title>
    <meta name="description" content="Build resumes that get you hired. AI-powered editor with real-time optimization and ATS scoring." />
</svelte:head>

<div class="min-h-screen bg-white dark:bg-black">


    <!-- Hero Section -->
    <section class="relative overflow-hidden bg-gradient-to-br from-primary-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-gray-900 dark:to-black">
        <!-- Background Effects -->
        <div class="absolute inset-0 bg-grid-pattern opacity-5"></div>
        <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl"></div>
        <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
        
        <div class="relative max-w-6xl mx-auto px-6 lg:px-8 pt-20 lg:pt-32 pb-20">
            <div class="text-center">
                <!-- Main Headline -->
                <h1 class="text-5xl lg:text-7xl font-bold mb-6 leading-tight text-gray-900 dark:text-white">
                    The Resume Editor
                    <br />
                    <span class="bg-gradient-to-r from-primary-600 to-blue-600 bg-clip-text text-transparent">
                        That Gets You Hired
                    </span>
                </h1>
                
                <!-- Subheadline -->
                <p class="text-xl lg:text-2xl text-gray-600 dark:text-gray-300 mb-10 max-w-3xl mx-auto leading-relaxed">
                    AI-powered resume builder with real-time ATS optimization. 
                    Write better, score higher, land interviews faster.
                </p>
                
                <!-- CTA Buttons -->
                <div class="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
                    <Button size="lg" on:click={handleGetStarted} className="px-8 py-4 text-lg font-medium">
                        Start Building Free
                        <ArrowRight class="h-5 w-5 ml-2" />
                    </Button>
                    
                    <Button size="lg" variant="outline" on:click={handleTryDemo} className="px-8 py-4 text-lg">
                        <Play class="h-5 w-5 mr-2" />
                        Try Demo
                    </Button>
                </div>


            </div>
        </div>
    </section>

    <!-- Feature Demos Section -->
    <section id="demo" class="py-20 bg-gray-50 dark:bg-gray-900">
        <div class="max-w-6xl mx-auto px-6 lg:px-8">
            <div class="text-center mb-16">
                <h2 class="text-3xl lg:text-4xl font-bold mb-4 text-gray-900 dark:text-white">See It In Action</h2>
                <p class="text-gray-600 dark:text-gray-300 text-lg">Watch how ResumeForge's features work in real-time</p>
            </div>
            
            <!-- Feature Demo Rows -->
            <div class="space-y-20">
                <!-- Feature 1: Edit Markdown → PDF Generated (Left text, Right video) -->
                <div class="grid lg:grid-cols-2 gap-12 items-center">
                    <div class="space-y-6">
                        <div class="flex items-center space-x-3">
                            <div class="w-12 h-12 bg-blue-500/20 border border-blue-500/30 rounded-xl flex items-center justify-center">
                                <Edit3 class="h-6 w-6 text-blue-500" />
                            </div>
                            <span class="text-sm font-medium text-blue-600 dark:text-blue-400 uppercase tracking-wide">Markdown Editor</span>
                        </div>
                        <h3 class="text-3xl font-bold text-gray-900 dark:text-white">Edit Markdown → PDF Generated</h3>
                        <p class="text-lg text-gray-600 dark:text-gray-300 leading-relaxed">
                            Write your resume in clean markdown syntax and watch as it transforms into a beautifully formatted PDF in real-time. 
                            No more wrestling with complex formatting tools.
                        </p>
                        <div class="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
                            <div class="flex items-center space-x-2">
                                <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                                <span>Real-time preview</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
                                <span>Auto-formatting</span>
                            </div>
                        </div>
                    </div>
                    <div class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden shadow-xl">
                        <div class="aspect-video bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center relative">
                            <!-- Auto-playing placeholder -->
                            <div class="text-center">
                                <div class="w-16 h-16 bg-blue-500/20 border border-blue-500/30 rounded-2xl flex items-center justify-center mb-4 mx-auto animate-pulse">
                                    <Edit3 class="h-8 w-8 text-blue-500" />
                                </div>
                                <p class="text-gray-600 dark:text-gray-300 font-medium">Markdown → PDF Demo</p>
                                <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">Auto-playing</p>
                            </div>
                            <!-- Auto-play indicator -->
                            <div class="absolute top-4 left-4 bg-green-500/20 backdrop-blur-sm rounded-lg px-3 py-1.5 text-sm">
                                <div class="flex items-center space-x-2">
                                    <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                                    <span class="text-green-600 dark:text-green-400 font-medium">Live</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Feature 2: Inline Editor (Right text, Left video) -->
                <div class="grid lg:grid-cols-2 gap-12 items-center">
                    <div class="lg:order-2 space-y-6">
                        <div class="flex items-center space-x-3">
                            <div class="w-12 h-12 bg-purple-500/20 border border-purple-500/30 rounded-xl flex items-center justify-center">
                                <Sparkles class="h-6 w-6 text-purple-500" />
                            </div>
                            <span class="text-sm font-medium text-purple-600 dark:text-purple-400 uppercase tracking-wide">AI Assistant</span>
                        </div>
                        <h3 class="text-3xl font-bold text-gray-900 dark:text-white">Inline Editor</h3>
                        <p class="text-lg text-gray-600 dark:text-gray-300 leading-relaxed">
                            Get intelligent suggestions as you type. Our AI analyzes your content and provides real-time recommendations 
                            to improve impact, clarity, and keyword optimization.
                        </p>
                        <div class="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
                            <div class="flex items-center space-x-2">
                                <div class="w-2 h-2 bg-purple-500 rounded-full"></div>
                                <span>Smart suggestions</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <div class="w-2 h-2 bg-pink-500 rounded-full"></div>
                                <span>Keyword optimization</span>
                            </div>
                        </div>
                    </div>
                    <div class="lg:order-1 bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden shadow-xl">
                        <div class="aspect-video bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center relative">
                            <div class="text-center">
                                <div class="w-16 h-16 bg-purple-500/20 border border-purple-500/30 rounded-2xl flex items-center justify-center mb-4 mx-auto animate-pulse">
                                    <Sparkles class="h-8 w-8 text-purple-500" />
                                </div>
                                <p class="text-gray-600 dark:text-gray-300 font-medium">AI Suggestions Demo</p>
                                <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">Auto-playing</p>
                            </div>
                            <div class="absolute top-4 left-4 bg-green-500/20 backdrop-blur-sm rounded-lg px-3 py-1.5 text-sm">
                                <div class="flex items-center space-x-2">
                                    <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                                    <span class="text-green-600 dark:text-green-400 font-medium">Live</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Feature 3: Chat Bot Assistant (Left text, Right video) -->
                <div class="grid lg:grid-cols-2 gap-12 items-center">
                    <div class="space-y-6">
                        <div class="flex items-center space-x-3">
                            <div class="w-12 h-12 bg-green-500/20 border border-green-500/30 rounded-xl flex items-center justify-center">
                                <MessageSquare class="h-6 w-6 text-green-500" />
                            </div>
                            <span class="text-sm font-medium text-green-600 dark:text-green-400 uppercase tracking-wide">AI Chat</span>
                        </div>
                        <h3 class="text-3xl font-bold text-gray-900 dark:text-white">Chat Bot Assistant</h3>
                        <p class="text-lg text-gray-600 dark:text-gray-300 leading-relaxed">
                            Have a conversation with our AI about your resume. Ask questions, get personalized advice, 
                            and receive targeted recommendations to improve your job application success.
                        </p>
                        <div class="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
                            <div class="flex items-center space-x-2">
                                <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                                <span>Personalized advice</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
                                <span>Industry insights</span>
                            </div>
                        </div>
                    </div>
                    <div class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden shadow-xl">
                        <div class="aspect-video bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center relative">
                            <div class="text-center">
                                <div class="w-16 h-16 bg-green-500/20 border border-green-500/30 rounded-2xl flex items-center justify-center mb-4 mx-auto animate-pulse">
                                    <MessageSquare class="h-8 w-8 text-green-500" />
                                </div>
                                <p class="text-gray-600 dark:text-gray-300 font-medium">AI Chat Demo</p>
                                <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">Auto-playing</p>
                            </div>
                            <div class="absolute top-4 left-4 bg-green-500/20 backdrop-blur-sm rounded-lg px-3 py-1.5 text-sm">
                                <div class="flex items-center space-x-2">
                                    <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                                    <span class="text-green-600 dark:text-green-400 font-medium">Live</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Feature 4: ATS Scanner (Right text, Left video) -->
                <div class="grid lg:grid-cols-2 gap-12 items-center">
                    <div class="lg:order-2 space-y-6">
                        <div class="flex items-center space-x-3">
                            <div class="w-12 h-12 bg-orange-500/20 border border-orange-500/30 rounded-xl flex items-center justify-center">
                                <Scan class="h-6 w-6 text-orange-500" />
                            </div>
                            <span class="text-sm font-medium text-orange-600 dark:text-orange-400 uppercase tracking-wide">ATS Optimization</span>
                        </div>
                        <h3 class="text-3xl font-bold text-gray-900 dark:text-white">ATS Scanner</h3>
                        <p class="text-lg text-gray-600 dark:text-gray-300 leading-relaxed">
                            Get instant feedback on how well your resume performs against Applicant Tracking Systems. 
                            See your score, identify weaknesses, and get specific recommendations for improvement.
                        </p>
                        <div class="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
                            <div class="flex items-center space-x-2">
                                <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
                                <span>ATS scoring</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <div class="w-2 h-2 bg-red-500 rounded-full"></div>
                                <span>Optimization tips</span>
                            </div>
                        </div>
                    </div>
                    <div class="lg:order-1 bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden shadow-xl">
                        <div class="aspect-video bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center relative">
                            <div class="text-center">
                                <div class="w-16 h-16 bg-orange-500/20 border border-orange-500/30 rounded-2xl flex items-center justify-center mb-4 mx-auto animate-pulse">
                                    <Scan class="h-8 w-8 text-orange-500" />
                                </div>
                                <p class="text-gray-600 dark:text-gray-300 font-medium">ATS Scanner Demo</p>
                                <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">Auto-playing</p>
                            </div>
                            <div class="absolute top-4 left-4 bg-green-500/20 backdrop-blur-sm rounded-lg px-3 py-1.5 text-sm">
                                <div class="flex items-center space-x-2">
                                    <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                                    <span class="text-green-600 dark:text-green-400 font-medium">Live</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>



    <!-- Footer -->
    <footer class="border-t border-gray-200 dark:border-gray-800 py-12 bg-white dark:bg-black">
        <div class="max-w-6xl mx-auto px-6 lg:px-8">
            <div class="flex flex-col md:flex-row justify-between items-center">
                <div class="flex items-center space-x-3 mb-4 md:mb-0">
                    <FileText class="h-6 w-6 text-primary-600 dark:text-primary-400" />
                    <span class="font-semibold text-gray-900 dark:text-white">ResumeForge</span>
                </div>
                
                <div class="flex items-center space-x-6 text-gray-600 dark:text-gray-300 text-sm">
                    <a href="/privacy" class="hover:text-primary-600 dark:hover:text-primary-400 transition-colors">Privacy</a>
                    <a href="/terms" class="hover:text-primary-600 dark:hover:text-primary-400 transition-colors">Terms</a>
                    <a href="/support" class="hover:text-primary-600 dark:hover:text-primary-400 transition-colors">Support</a>
                </div>
            </div>
            
            <div class="mt-8 pt-8 border-t border-gray-200 dark:border-gray-800 text-center text-gray-500 dark:text-gray-400 text-sm">
                © 2024 ResumeForge. All rights reserved.
            </div>
        </div>
    </footer>
</div>