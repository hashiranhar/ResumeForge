<script>
    import { FileText, Scale, Shield, Users, CreditCard, AlertTriangle, Mail, Gavel } from 'lucide-svelte';
    import Button from '$lib/components/common/Button.svelte';
    import { goto } from '$app/navigation';
</script>

<svelte:head>
    <title>Terms of Service - ResumeForge</title>
    <meta name="description" content="Terms of Service for ResumeForge - AI-powered resume builder. Learn about your rights and responsibilities." />
</svelte:head>

<div class="min-h-screen bg-white dark:bg-black">
    <!-- Header -->
    <div class="border-b border-gray-200 dark:border-gray-800">
        <div class="max-w-4xl mx-auto px-6 py-8">
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 bg-blue-500/20 border border-blue-500/30 rounded-xl flex items-center justify-center">
                        <Scale class="h-6 w-6 text-blue-500" />
                    </div>
                    <div>
                        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Terms of Service</h1>
                        <p class="text-gray-600 dark:text-gray-300">Your rights and responsibilities</p>
                    </div>
                </div>
                <Button variant="outline" on:click={() => goto('/')}>
                    ← Back to Home
                </Button>
            </div>
        </div>
    </div>

    <!-- Content -->
    <div class="max-w-4xl mx-auto px-6 py-12">
        <div class="prose prose-gray dark:prose-invert max-w-none">
            <!-- Last Updated -->
            <div class="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-4 mb-8">
                <p class="text-sm text-gray-600 dark:text-gray-300 mb-0">
                    <strong>Last updated:</strong> January 2024
                </p>
            </div>

            <!-- Agreement to Terms -->
            <section class="mb-12">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                    <Gavel class="h-6 w-6 mr-3 text-red-500" />
                    Agreement to Terms
                </h2>
                <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
                    <p class="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-0">
                        By accessing or using ResumeForge ("Service"), you agree to be bound by these Terms of Service ("Terms"). 
                        If you disagree with any part of these terms, you may not access the Service.
                    </p>
                </div>
            </section>

            <!-- Description of Service -->
            <section class="mb-12">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                    <FileText class="h-6 w-6 mr-3 text-primary-500" />
                    Description of Service
                </h2>
                <p class="text-lg text-gray-700 dark:text-gray-300 mb-6">
                    ResumeForge is an AI-powered resume building platform that provides:
                </p>
                
                <div class="grid md:grid-cols-2 gap-4">
                    <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                        <ul class="text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                            <li>• Markdown-based resume editor with real-time PDF preview</li>
                            <li>• AI-powered content suggestions and optimization</li>
                            <li>• ATS scoring and analysis</li>
                        </ul>
                    </div>
                    <div class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
                        <ul class="text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                            <li>• PDF import and conversion capabilities</li>
                            <li>• AI chat assistant for personalized advice</li>
                            <li>• Professional templates and formatting</li>
                        </ul>
                    </div>
                </div>
            </section>

            <!-- User Accounts -->
            <section class="mb-12">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                    <Users class="h-6 w-6 mr-3 text-green-500" />
                    User Accounts
                </h2>

                <div class="grid md:grid-cols-2 gap-6">
                    <div class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">Account Creation</h3>
                        <ul class="text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                            <li>• Provide accurate and complete information</li>
                            <li>• Must be at least 16 years old</li>
                            <li>• One account per person</li>
                            <li>• Maintain confidentiality of credentials</li>
                        </ul>
                    </div>

                    <div class="bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">Your Responsibility</h3>
                        <ul class="text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                            <li>• Responsible for all account activities</li>
                            <li>• Notify us of unauthorized use immediately</li>
                            <li>• We may suspend accounts violating Terms</li>
                        </ul>
                    </div>
                </div>
            </section>

            <!-- Acceptable Use -->
            <section class="mb-12">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                    <Shield class="h-6 w-6 mr-3 text-blue-500" />
                    Acceptable Use
                </h2>

                <div class="grid md:grid-cols-2 gap-6">
                    <!-- You May -->
                    <div class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-green-800 dark:text-green-200 mb-4 flex items-center">
                            ✅ You May
                        </h3>
                        <ul class="text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                            <li>• Create, edit, and export personal resumes</li>
                            <li>• Use AI features for resume improvement</li>
                            <li>• Upload PDF files for conversion</li>
                            <li>• Share resumes with employers</li>
                            <li>• Use templates for personal use</li>
                        </ul>
                    </div>

                    <!-- You May Not -->
                    <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-red-800 dark:text-red-200 mb-4 flex items-center">
                            ❌ You May Not
                        </h3>
                        <ul class="text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                            <li>• Use for illegal or unauthorized purposes</li>
                            <li>• Upload malicious files or viruses</li>
                            <li>• Attempt to hack or exploit systems</li>
                            <li>• Use automated scripts or bots</li>
                            <li>• Create fake or misleading content</li>
                            <li>• Resell or redistribute our features</li>
                        </ul>
                    </div>
                </div>
            </section>

            <!-- Content and Intellectual Property -->
            <section class="mb-12">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Content and Intellectual Property</h2>

                <div class="space-y-6">
                    <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">Your Content</h3>
                        <ul class="text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                            <li>• You retain ownership of all resume content you create</li>
                            <li>• You grant us license to process and store your content to provide the Service</li>
                            <li>• You're responsible for content accuracy and rights compliance</li>
                            <li>• You can delete your content at any time</li>
                        </ul>
                    </div>

                    <div class="bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">Our Content</h3>
                        <ul class="text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                            <li>• ResumeForge owns rights to templates, AI algorithms, and platform features</li>
                            <li>• You may not copy, modify, or redistribute our proprietary content</li>
                            <li>• Our brand, logos, and design elements are protected</li>
                        </ul>
                    </div>

                    <div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">AI-Generated Content</h3>
                        <ul class="text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                            <li>• AI suggestions are recommendations based on best practices</li>
                            <li>• We don't guarantee accuracy or effectiveness of AI recommendations</li>
                            <li>• Final responsibility for resume content remains with you</li>
                            <li>• AI suggestions provided "as-is" without warranties</li>
                        </ul>
                    </div>
                </div>
            </section>

            <!-- Payment and Billing -->
            <section class="mb-12">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                    <CreditCard class="h-6 w-6 mr-3 text-green-500" />
                    Payment and Billing
                </h2>

                <div class="grid md:grid-cols-3 gap-6">
                    <div class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">Free Tier</h3>
                        <ul class="text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                            <li>• Basic features at no cost</li>
                            <li>• Subject to reasonable limits</li>
                            <li>• Limits may be modified with notice</li>
                        </ul>
                    </div>

                    <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">Premium Features</h3>
                        <ul class="text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                            <li>• Advanced features require subscription</li>
                            <li>• Auto-renewal unless cancelled</li>
                            <li>• Clear terms before purchase</li>
                        </ul>
                    </div>

                    <div class="bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">Payment Security</h3>
                        <ul class="text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                            <li>• Processed by trusted providers</li>
                            <li>• We don't store payment info</li>
                            <li>• Subject to applicable taxes</li>
                        </ul>
                    </div>
                </div>
            </section>

            <!-- Limitation of Liability -->
            <section class="mb-12">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                    <AlertTriangle class="h-6 w-6 mr-3 text-yellow-500" />
                    Limitation of Liability
                </h2>

                <div class="bg-yellow-50 dark:bg-yellow-900/20 border-2 border-yellow-200 dark:border-yellow-800 rounded-lg p-6 mb-6">
                    <h3 class="text-lg font-bold text-yellow-800 dark:text-yellow-200 mb-3">Important Disclaimers</h3>
                    <ul class="text-yellow-700 dark:text-yellow-300 space-y-2 text-sm">
                        <li>• Service provided "as-is" without warranties</li>
                        <li>• We don't guarantee job offers or employment success</li>
                        <li>• Resume effectiveness depends on many factors beyond our control</li>
                        <li>• Our liability is limited to amounts paid in past 12 months</li>
                    </ul>
                </div>

                <div class="grid md:grid-cols-2 gap-6">
                    <div class="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">Service Availability</h3>
                        <ul class="text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                            <li>• We strive for high availability</li>
                            <li>• Maintenance announced when possible</li>
                            <li>• Not liable for temporary interruptions</li>
                        </ul>
                    </div>

                    <div class="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">Third-Party Services</h3>
                        <ul class="text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                            <li>• We integrate with external services</li>
                            <li>• Not responsible for third-party failures</li>
                            <li>• Third-parties have own terms</li>
                        </ul>
                    </div>
                </div>
            </section>

            <!-- Termination -->
            <section class="mb-12">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Termination</h2>

                <div class="grid md:grid-cols-2 gap-6">
                    <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">By You</h3>
                        <ul class="text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                            <li>• Delete account anytime through settings</li>
                            <li>• Data removed per Privacy Policy</li>
                            <li>• Responsible for outstanding payments</li>
                        </ul>
                    </div>

                    <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">By Us</h3>
                        <ul class="text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                            <li>• May suspend accounts violating Terms</li>
                            <li>• Service termination with 30 days notice</li>
                            <li>• Data export opportunities provided</li>
                        </ul>
                    </div>
                </div>
            </section>

            <!-- Contact -->
            <section class="mb-12">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                    <Mail class="h-6 w-6 mr-3 text-blue-500" />
                    Contact Information
                </h2>

                <div class="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                    <p class="text-gray-700 dark:text-gray-300 mb-4">
                        For questions about these Terms of Service:
                    </p>
                    
                    <div class="space-y-2 text-sm">
                        <div class="flex items-center space-x-2">
                            <Mail class="h-4 w-4 text-gray-500" />
                            <span class="text-gray-700 dark:text-gray-300">
                                <strong>Legal:</strong> legal@resumeforge.com
                            </span>
                        </div>
                        <div class="flex items-center space-x-2">
                            <Mail class="h-4 w-4 text-gray-500" />
                            <span class="text-gray-700 dark:text-gray-300">
                                <strong>Support:</strong> support@resumeforge.com
                            </span>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Footer note -->
            <div class="border-t border-gray-200 dark:border-gray-700 pt-8">
                <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
                    <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Updates to Terms</h3>
                    <p class="text-sm text-blue-800 dark:text-blue-200">
                        We may update these Terms to reflect changes in our practices or legal requirements. 
                        Material changes will be communicated via email and prominent notice in the Service. 
                        We'll provide at least 30 days' notice for significant changes.
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>