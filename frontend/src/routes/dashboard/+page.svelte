<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { browser } from '$app/environment';
    import { isAuthenticated, user } from '$lib/stores/auth.js';
    import { cvs, templates, cvService, isLoading } from '$lib/stores/cv.js';
    import { addToast } from '$lib/stores/toast.js';
    import { formatRelativeTime } from '$lib/utils/helpers.js';
    import Button from '$lib/components/common/Button.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import Input from '$lib/components/common/Input.svelte';
    import { Plus, FileText, Edit, Trash2, Download, Eye } from 'lucide-svelte';

    // Modal state variables
    let showTemplateModal = false;
    let showNewCVModal = false;
    let showDeleteModal = false;
    
    // CV creation variables
    let selectedTemplate = null;
    let newCVName = '';
    let creatingCV = false;
    
    // Delete variables
    let cvToDelete = null;
    let deletingCV = false;

    // Redirect if not authenticated (with browser check)
    $: if (browser && !$isAuthenticated) {
        goto('/auth/login');
    }

    onMount(async () => {
        if ($isAuthenticated) {
            await cvService.loadCVs();
            await cvService.loadTemplates();
        }
    });

    function handleNewCV() {
        showTemplateModal = true;
    }

    function handleCreateBlank() {
        selectedTemplate = null;
        showTemplateModal = false;
        showNewCVModal = true;
    }

    function handleTemplateSelect(template) {
        selectedTemplate = template;
        showTemplateModal = false;
        showNewCVModal = true;
    }

    // FIXED: Added keyboard event handler
    function handleKeydown(event, callback) {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            callback();
        }
    }

    async function handleCreateCV() {
        if (!newCVName.trim()) {
            addToast('Please enter a name for your CV', 'error');
            return;
        }

        creatingCV = true;

        try {
            const templateContent = selectedTemplate?.content || `# ${newCVName}\n\n## Contact Information\n\n## Summary\n\n## Experience\n\n## Education\n\n## Skills`;
            
            const result = await cvService.createCV(
                newCVName.trim(),
                templateContent,
                { 
                    fontSize: 12,
                    fontFamily: 'Arial',
                    theme: 'professional' 
                }
            );

            if (result.success) {
                showNewCVModal = false;
                newCVName = '';
                selectedTemplate = null;
                addToast('CV created successfully!', 'success');
                goto(`/editor?cv=${result.data.id}`);
            } else {
                addToast(result.error || 'Failed to create CV', 'error');
            }
        } catch (error) {
            addToast('Failed to create CV', 'error');
        } finally {
            creatingCV = false;
        }
    }

    function handleEditCV(cv) {
        goto(`/editor?cv=${cv.id}`);
    }

    function handleDeleteCV(cv) {
        cvToDelete = cv;
        showDeleteModal = true;
    }

    async function confirmDelete() {
        if (!cvToDelete) return;

        deletingCV = true;

        try {
            const result = await cvService.deleteCV(cvToDelete.id);

            if (result.success) {
                showDeleteModal = false;
                cvToDelete = null;
                addToast('CV deleted successfully', 'success');
                await cvService.loadCVs();
            } else {
                addToast(result.error || 'Failed to delete CV', 'error');
            }
        } catch (error) {
            addToast('Failed to delete CV', 'error');
        } finally {
            deletingCV = false;
        }
    }

    async function handleDownloadPDF(cv) {
        try {
            const result = await cvService.generatePDF(cv.id);
            
            if (result.success) {
                const blob = new Blob([result.data], { type: 'application/pdf' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${cv.name}.pdf`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                addToast('PDF downloaded successfully', 'success');
            } else {
                addToast(result.error || 'Failed to generate PDF', 'error');
            }
        } catch (error) {
            addToast('Failed to download PDF', 'error');
        }
    }
</script>

<svelte:head>
    <title>Dashboard - ResumeForge</title>
</svelte:head>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 bg-white dark:bg-black min-h-screen">
    <!-- Header -->
    <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Welcome back, {$user?.email}
        </h1>
        <p class="text-gray-600 dark:text-gray-300">
            Manage your CVs and create new ones
        </p>
    </div>

    <!-- Actions -->
    <div class="mb-8">
        <Button size="lg" on:click={handleNewCV}>
            <Plus class="h-5 w-5 mr-2" />
            Create New CV
        </Button>
    </div>

    <!-- CVs Grid -->
    {#if $isLoading}
        <div class="flex items-center justify-center py-12">
            <div class="spinner"></div>
            <span class="ml-2 text-gray-600 dark:text-gray-300">Loading your CVs...</span>
        </div>
    {:else if $cvs.length === 0}
        <div class="text-center py-12">
            <FileText class="h-16 w-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
                No CVs yet
            </h3>
            <p class="text-gray-600 dark:text-gray-300 mb-6">
                Get started by creating your first professional CV
            </p>
            <Button on:click={handleNewCV}>
                <Plus class="h-4 w-4 mr-2" />
                Create Your First CV
            </Button>
        </div>
    {:else}
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each $cvs as cv (cv.id)}
                <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow">
                    <div class="p-6">
                        <div class="flex items-start justify-between mb-4">
                            <div class="flex-1">
                                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                                    {cv.name}
                                </h3>
                                <p class="text-sm text-gray-500 dark:text-gray-400">
                                    Updated {formatRelativeTime(cv.updated_at)}
                                </p>
                            </div>
                        </div>

                        <div class="flex items-center justify-between">
                            <div class="flex space-x-2">
                                <Button size="sm" on:click={() => handleEditCV(cv)}>
                                    <Edit class="h-4 w-4 mr-1" />
                                    Edit
                                </Button>
                                <Button 
                                    size="sm" 
                                    variant="outline" 
                                    on:click={() => handleDownloadPDF(cv)}
                                >
                                    <Download class="h-4 w-4 mr-1" />
                                    PDF
                                </Button>
                            </div>
                            
                            <button
                                class="text-gray-400 dark:text-gray-500 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                                on:click={() => handleDeleteCV(cv)}
                                title="Delete CV"
                            >
                                <Trash2 class="h-4 w-4" />
                            </button>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>

<!-- Template Selection Modal -->
<Modal 
    bind:open={showTemplateModal} 
    title="Choose a Template" 
    size="lg"
    close={() => showTemplateModal = false}
>
    <div class="space-y-6">
        <p class="text-gray-600 dark:text-gray-300">
            Start with a professional template or create a blank CV
        </p>

        <!-- Blank option -->
        <button
            type="button"
            class="w-full border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center hover:border-primary-300 dark:hover:border-primary-500 cursor-pointer transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            on:click={handleCreateBlank}
            aria-describedby="blank-template-desc"
        >
            <Plus class="h-12 w-12 text-gray-400 dark:text-gray-500 mx-auto mb-3" />
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-1">Start from Blank</h3>
            <p class="text-gray-600 dark:text-gray-300" id="blank-template-desc">
                Create a CV from scratch with your own content
            </p>
        </button>

        <!-- Templates -->
        {#if $templates.length > 0}
            <div>
                <h4 class="text-md font-medium text-gray-900 dark:text-white mb-4">
                    Or choose from a template:
                </h4>
                <ul class="grid md:grid-cols-2 gap-4 list-none" aria-label="Available CV templates">
                    {#each $templates as template (template.id)}
                        <li>
                            <button
                                type="button"
                                class="border border-gray-200 dark:border-gray-600 rounded-lg p-4 hover:border-primary-300 dark:hover:border-primary-500 cursor-pointer transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 text-left w-full"
                                on:click={() => handleTemplateSelect(template)}
                                aria-describedby="template-{template.id}-desc"
                            >
                                <h3 class="font-medium text-gray-900 dark:text-white mb-1">
                                    {template.name}
                                </h3>
                                <p class="text-sm text-gray-600 dark:text-gray-300 mb-2" id="template-{template.id}-desc">
                                    {template.description}
                                </p>
                                {#if template.is_default === 'true'}
                                    <span 
                                        class="inline-block bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 text-xs px-2 py-1 rounded"
                                        aria-label="Recommended template"
                                    >
                                        Recommended
                                    </span>
                                {/if}
                            </button>
                        </li>
                    {/each}
                </ul>
            </div>
        {/if}
    </div>
</Modal>

<!-- New CV Modal -->
<Modal 
    bind:open={showNewCVModal} 
    title="Create New CV"
    close={() => showNewCVModal = false}
>
    <div class="space-y-4">
        {#if selectedTemplate}
            <div class="bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded-lg p-4">
                <p class="text-sm text-blue-800 dark:text-blue-200">
                    Using template: <strong>{selectedTemplate.name}</strong>
                </p>
            </div>
        {/if}

        <Input
            label="CV Name"
            placeholder="e.g. Software Engineer Resume"
            bind:value={newCVName}
            required
        />
    </div>

    <div slot="footer" class="flex justify-end">
        <Button 
            on:click={handleCreateCV}
            loading={creatingCV}
            disabled={creatingCV || !newCVName.trim()}
        >
            Create CV
        </Button>
    </div>
</Modal>

<!-- Delete Confirmation Modal -->
<Modal bind:open={showDeleteModal} title="Delete CV">
    <div class="space-y-4">
        <p class="text-gray-600 dark:text-gray-300">
            Are you sure you want to delete <strong class="text-gray-900 dark:text-white">{cvToDelete?.name}</strong>? 
            This action cannot be undone.
        </p>
    </div>

    <div slot="footer" class="flex justify-end space-x-3">
        <Button variant="outline" on:click={() => showDeleteModal = false}>
            Cancel
        </Button>
        <Button 
            variant="danger"
            on:click={confirmDelete}
            loading={deletingCV}
            disabled={deletingCV}
        >
            Delete CV
        </Button>
    </div>
</Modal>