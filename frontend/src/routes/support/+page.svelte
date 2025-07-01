<script>
    import { 
        MessageCircle, 
        Mail, 
        Phone, 
        Clock, 
        Send, 
        ChevronDown, 
        ChevronUp, 
        HelpCircle, 
        Book, 
        Video, 
        Users,
        Star,
        Search,
        ExternalLink,
        HeadphonesIcon,
        CheckCircle,
        AlertCircle
    } from 'lucide-svelte';
    import Button from '$lib/components/common/Button.svelte';
    import { goto } from '$app/navigation';

    // State management
    let activeTab = 'contact';
    let expandedFaq = null;
    let searchQuery = '';
    let contactForm = {
        name: '',
        email: '',
        subject: '',
        message: '',
        priority: 'normal'
    };
    let isSubmitting = false;

    // FAQ data
    const faqs = [
        {
            id: 1,
            question: "How do I create my first resume?",
            answer: "Getting started is easy! Click the 'Create New Resume' button, choose a template that suits your style, and start filling in your information using our markdown editor. Our real-time preview shows how your resume looks as you build it."
        },
        {
            id: 2,
            question: "Can I customize the design and layout?",
            answer: "Absolutely! You can customize fonts, colors, margins, line spacing, and choose from multiple themes. Use the settings panel to adjust the layout to match your personal style or industry requirements."
        },
        {
            id: 3,
            question: "What is ATS optimization and how does it work?",
            answer: "ATS (Applicant Tracking System) optimization ensures your resume can be properly read by automated systems that many employers use. Our AI analyzes your resume and provides suggestions to improve keyword usage, formatting, and structure for better ATS compatibility."
        },
        {
            id: 4,
            question: "How do I export my resume to PDF?",
            answer: "Once you're happy with your resume, click the 'Export PDF' button in the editor. Your resume will be generated as a professional PDF that's ready to send to employers or upload to job portals."
        },
        {
            id: 5,
            question: "Can I save multiple versions of my resume?",
            answer: "Yes! You can create and save multiple resumes for different roles or industries. Each resume can have its own content, formatting, and design to target specific opportunities."
        },
        {
            id: 6,
            question: "How does the AI chat assistant work?",
            answer: "Our AI assistant provides personalized suggestions for improving your resume content, helps with wording, and offers industry-specific advice. Simply ask questions about your resume and get instant, helpful responses."
        },
        {
            id: 7,
            question: "Can I import an existing PDF resume?",
            answer: "Yes! Our PDF import feature can convert your existing resume into editable format. Upload your PDF and our system will extract the content, which you can then edit and improve using our tools."
        },
        {
            id: 8,
            question: "Is my data secure and private?",
            answer: "Your privacy is our priority. All data is encrypted and stored securely. We never share your personal information with third parties, and you have full control over your data at all times."
        }
    ];

    // Support channels data
    const supportChannels = [
        {
            icon: Mail,
            title: "Email Support",
            description: "Get detailed help via email",
            contact: "support@resumeforge.com",
            response: "Within 24 hours",
            availability: "24/7",
            color: "blue"
        },
        {
            icon: MessageCircle,
            title: "Live Chat",
            description: "Instant help from our team",
            contact: "Chat widget (bottom right)",
            response: "Immediate",
            availability: "Mon-Fri, 9AM-6PM EST",
            color: "green"
        },
        {
            icon: Phone,
            title: "Phone Support",
            description: "Speak directly with support",
            contact: "+1 (555) 123-4567",
            response: "Immediate",
            availability: "Mon-Fri, 9AM-5PM EST",
            color: "purple"
        }
    ];

    // Resources data
    const resources = [
        {
            icon: Book,
            title: "User Guide",
            description: "Complete documentation and step-by-step tutorials",
            link: "/docs",
            color: "blue"
        },
        {
            icon: Video,
            title: "Video Tutorials",
            description: "Watch our comprehensive video guides",
            link: "/tutorials",
            color: "red"
        },
        {
            icon: Users,
            title: "Community Forum",
            description: "Connect with other users and share tips",
            link: "/community",
            color: "green"
        },
        {
            icon: HelpCircle,
            title: "Knowledge Base",
            description: "Search our extensive help articles",
            link: "/kb",
            color: "purple"
        }
    ];

    // Computed
    $: filteredFaqs = faqs.filter(faq => 
        faq.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
        faq.answer.toLowerCase().includes(searchQuery.toLowerCase())
    );

    // Functions
    function toggleFaq(id) {
        expandedFaq = expandedFaq === id ? null : id;
    }

    async function handleContactSubmit() {
        if (isSubmitting) return;
        
        isSubmitting = true;
        
        try {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Reset form
            contactForm = {
                name: '',
                email: '',
                subject: '',
                message: '',
                priority: 'normal'
            };
            
            alert('Thank you for your message! We\'ll get back to you soon.');
        } catch (error) {
            alert('There was an error sending your message. Please try again.');
        } finally {
            isSubmitting = false;
        }
    }

    function getColorClasses(color) {
        const colors = {
            blue: 'text-blue-500 bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800',
            green: 'text-green-500 bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800',
            purple: 'text-purple-500 bg-purple-50 dark:bg-purple-900/20 border-purple-200 dark:border-purple-800',
            red: 'text-red-500 bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800'
        };
        return colors[color] || colors.blue;
    }
</script>

<svelte:head>
    <title>Support - ResumeForge</title>
    <meta name="description" content="Get help with ResumeForge. Contact support, browse FAQs, and access resources to make the most of your AI-powered resume builder." />
</svelte:head>

<div class="min-h-screen bg-white dark:bg-black">
    <!-- Header -->
    <div class="border-b border-gray-200 dark:border-gray-800">
        <div class="max-w-6xl mx-auto px-6 py-8">
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 bg-blue-500/20 border border-blue-500/30 rounded-xl flex items-center justify-center">
                        <HeadphonesIcon class="h-6 w-6 text-blue-500" />
                    </div>
                    <div>
                        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Support Center</h1>
                        <p class="text-gray-600 dark:text-gray-300">Get the help you need to create amazing resumes</p>
                    </div>
                </div>
                <Button variant="outline" on:click={() => goto('/')}>
                    ← Back to Home
                </Button>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-6xl mx-auto px-6 py-12">
        <!-- Navigation Tabs -->
        <div class="flex flex-wrap justify-center mb-12 border-b border-gray-200 dark:border-gray-700">
            {#each [
                { id: 'contact', label: 'Contact Us', icon: Mail },
                { id: 'faq', label: 'FAQ', icon: HelpCircle },
                { id: 'resources', label: 'Resources', icon: Book }
            ] as tab}
                <button
                    on:click={() => activeTab = tab.id}
                    class="flex items-center space-x-2 px-6 py-3 font-medium text-sm border-b-2 transition-colors {
                        activeTab === tab.id
                            ? 'border-blue-600 text-blue-600 dark:text-blue-400'
                            : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
                    }"
                >
                    <svelte:component this={tab.icon} class="h-5 w-5" />
                    <span>{tab.label}</span>
                </button>
            {/each}
        </div>

        <!-- Contact Tab -->
        {#if activeTab === 'contact'}
            <div class="space-y-12">
                <!-- Support Channels -->
                <div>
                    <h2 class="text-3xl font-bold text-gray-900 dark:text-white text-center mb-8">Get in Touch</h2>
                    <div class="grid md:grid-cols-3 gap-8">
                        {#each supportChannels as channel}
                            <div class="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 text-center hover:shadow-lg transition-all duration-200 border border-gray-200 dark:border-gray-700">
                                <div class="w-12 h-12 mx-auto mb-4 {getColorClasses(channel.color)} rounded-xl flex items-center justify-center">
                                    <svelte:component this={channel.icon} class="h-6 w-6" />
                                </div>
                                <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">{channel.title}</h3>
                                <p class="text-gray-600 dark:text-gray-400 mb-4">{channel.description}</p>
                                <div class="space-y-2 text-sm">
                                    <p class="text-gray-700 dark:text-gray-300"><strong>Contact:</strong> {channel.contact}</p>
                                    <p class="text-gray-700 dark:text-gray-300"><strong>Response:</strong> {channel.response}</p>
                                    <p class="text-gray-700 dark:text-gray-300"><strong>Available:</strong> {channel.availability}</p>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>

                <!-- Contact Form -->
                <div class="max-w-2xl mx-auto">
                    <div class="bg-white dark:bg-gray-900 rounded-xl shadow-lg p-8 border border-gray-200 dark:border-gray-700">
                        <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center">Send us a Message</h3>
                        <form on:submit|preventDefault={handleContactSubmit} class="space-y-6">
                            <div class="grid md:grid-cols-2 gap-6">
                                <div>
                                    <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Name *</label>
                                    <input
                                        id="name"
                                        type="text"
                                        required
                                        bind:value={contactForm.name}
                                        class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                        placeholder="Your full name"
                                    />
                                </div>
                                <div>
                                    <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Email *</label>
                                    <input
                                        id="email"
                                        type="email"
                                        required
                                        bind:value={contactForm.email}
                                        class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                        placeholder="your.email@example.com"
                                    />
                                </div>
                            </div>
                            
                            <div class="grid md:grid-cols-2 gap-6">
                                <div>
                                    <label for="subject" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Subject *</label>
                                    <input
                                        id="subject"
                                        type="text"
                                        required
                                        bind:value={contactForm.subject}
                                        class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                        placeholder="Brief description of your issue"
                                    />
                                </div>
                                <div>
                                    <label for="priority" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Priority</label>
                                    <select
                                        id="priority"
                                        bind:value={contactForm.priority}
                                        class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    >
                                        <option value="low">Low</option>
                                        <option value="normal">Normal</option>
                                        <option value="high">High</option>
                                        <option value="urgent">Urgent</option>
                                    </select>
                                </div>
                            </div>

                            <div>
                                <label for="message" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Message *</label>
                                <textarea
                                    id="message"
                                    required
                                    rows="6"
                                    bind:value={contactForm.message}
                                    class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    placeholder="Please describe your issue or question in detail..."
                                ></textarea>
                            </div>

                            <Button 
                                type="submit" 
                                variant="primary" 
                                disabled={isSubmitting}
                                class="w-full flex items-center justify-center space-x-2"
                            >
                                {#if isSubmitting}
                                    <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                                    <span>Sending...</span>
                                {:else}
                                    <Send class="h-4 w-4" />
                                    <span>Send Message</span>
                                {/if}
                            </Button>
                        </form>
                    </div>
                </div>
            </div>
        {/if}

        <!-- FAQ Tab -->
        {#if activeTab === 'faq'}
            <div class="space-y-8">
                <div class="text-center">
                    <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Frequently Asked Questions</h2>
                    <p class="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                        Find quick answers to common questions about ResumeForge
                    </p>
                </div>

                <!-- Search bar moved here -->
                <div class="max-w-2xl mx-auto relative">
                    <Search class="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                    <input
                        type="text"
                        placeholder="Search FAQs..."
                        bind:value={searchQuery}
                        class="w-full pl-12 pr-4 py-4 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
                    />
                </div>

                {#if searchQuery}
                    <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                        <p class="text-sm text-blue-800 dark:text-blue-200">
                            Found {filteredFaqs.length} result{filteredFaqs.length !== 1 ? 's' : ''} for "{searchQuery}"
                        </p>
                    </div>
                {/if}

                <div class="max-w-4xl mx-auto space-y-4">
                    {#each filteredFaqs as faq}
                        <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden">
                            <button
                                on:click={() => toggleFaq(faq.id)}
                                class="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                            >
                                <h3 class="text-lg font-semibold text-gray-900 dark:text-white pr-4">{faq.question}</h3>
                                {#if expandedFaq === faq.id}
                                    <ChevronUp class="h-5 w-5 text-gray-500 flex-shrink-0" />
                                {:else}
                                    <ChevronDown class="h-5 w-5 text-gray-500 flex-shrink-0" />
                                {/if}
                            </button>
                            {#if expandedFaq === faq.id}
                                <div class="px-6 pb-4 border-t border-gray-200 dark:border-gray-700">
                                    <p class="text-gray-700 dark:text-gray-300 pt-4 leading-relaxed">{faq.answer}</p>
                                </div>
                            {/if}
                        </div>
                    {/each}

                    {#if filteredFaqs.length === 0}
                        <div class="text-center py-12">
                            <Search class="h-12 w-12 text-gray-400 mx-auto mb-4" />
                            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No results found</h3>
                            <p class="text-gray-600 dark:text-gray-400">Try adjusting your search terms or contact our support team.</p>
                        </div>
                    {/if}
                </div>
            </div>
        {/if}

        <!-- Resources Tab -->
        {#if activeTab === 'resources'}
            <div class="space-y-12">
                <div class="text-center">
                    <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Help Resources</h2>
                    <p class="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                        Explore our comprehensive resources to master ResumeForge
                    </p>
                </div>

                <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {#each resources as resource}
                        <a 
                            href={resource.link}
                            class="group bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl p-6 hover:shadow-lg transition-all duration-200 hover:border-gray-300 dark:hover:border-gray-600"
                        >
                            <div class="w-12 h-12 {getColorClasses(resource.color)} rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                <svelte:component this={resource.icon} class="h-6 w-6" />
                            </div>
                            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2 flex items-center">
                                {resource.title}
                                <ExternalLink class="h-4 w-4 ml-2 opacity-0 group-hover:opacity-100 transition-opacity" />
                            </h3>
                            <p class="text-gray-600 dark:text-gray-400 text-sm">{resource.description}</p>
                        </a>
                    {/each}
                </div>

                <!-- Quick Links -->
                <div class="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-xl p-8 border border-gray-200 dark:border-gray-700">
                    <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center">Quick Start Guide</h3>
                    <div class="grid md:grid-cols-3 gap-6">
                        <div class="text-center">
                            <div class="w-10 h-10 bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 rounded-full flex items-center justify-center mx-auto mb-3">
                                <span class="font-bold">1</span>
                            </div>
                            <h4 class="font-semibold text-gray-900 dark:text-white mb-2">Create Account</h4>
                            <p class="text-sm text-gray-600 dark:text-gray-400">Sign up for free and access all basic features</p>
                        </div>
                        <div class="text-center">
                            <div class="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center mx-auto mb-3">
                                <span class="font-bold">2</span>
                            </div>
                            <h4 class="font-semibold text-gray-900 dark:text-white mb-2">Choose Template</h4>
                            <p class="text-sm text-gray-600 dark:text-gray-400">Pick from our professional templates</p>
                        </div>
                        <div class="text-center">
                            <div class="w-10 h-10 bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 rounded-full flex items-center justify-center mx-auto mb-3">
                                <span class="font-bold">3</span>
                            </div>
                            <h4 class="font-semibold text-gray-900 dark:text-white mb-2">Build & Export</h4>
                            <p class="text-sm text-gray-600 dark:text-gray-400">Create your resume and export as PDF</p>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>