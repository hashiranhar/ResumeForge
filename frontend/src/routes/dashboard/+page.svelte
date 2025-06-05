<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { isAuthenticated, user } from '$lib/stores/auth.js';
    import { cvs, templates, cvService, isLoading } from '$lib/stores/cv.js';
    import { addToast } from '$lib/stores/toast.js';
    import { formatRelativeTime } from '$lib/utils/helpers.js';
    import Button from '$lib/components/common/Button.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import Input from '$lib/components/common/Input.svelte';
    import { Plus, FileText, Edit, Trash2, Download, Eye } from 'lucide-svelte';

    let showNewCVModal = false;
    let showDeleteModal = false;
    let showTemplateModal = false;
    let newCVName = '';
    let selectedTemplate = null;
    let cvToDelete = null;
    let creatingCV = false;
    let deletingCV = false;

    // Redirect if not authenticated
    onMount(async () => {
        if (!$isAuthenticated) {
            goto('/auth/login');
            return;
        }

        // Load user's CVs and templates
        await Promise.all([
            cvService.loadCVs(),
            cvService.loadTemplates()
        ]);
    });

    function handleNewCV() {
        newCVName = '';
        selectedTemplate = null;
        showTemplateModal = true;
    }

    function handleTemplateSelect(template) {
        selectedTemplate = template;
        showTemplateModal = false;
        showNewCVModal = true;
    }

    function handleCreateBlank() {
        selectedTemplate = null;
        showTemplateModal = false;
        showNewCVModal = true;
    }

    async function handleCreateCV() {
        if (!newCVName.trim()) {
            addToast('Please enter a name for your CV', 'error');
            return;
        }

        creatingCV = true;

        try {
            const result = await cvService.createCV(
                newCVName.trim(),
                '',
                null,
                selectedTemplate?.id
            );

            if (result.success) {
                showNewCVModal = false;
                addToast('CV created successfully!', 'success');
                goto(`/editor?cv=${result.data.id}`);
            } else {
                addToast(result.error || 'Failed to create CV', 'error');
            }
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
            } else {
                addToast(result.error || 'Failed to delete CV', 'error');
            }
        } finally {
            deletingCV = false;
        }
    }

    async function handleDownloadPDF(cv) {
        const result = await cvService.downloadPDF(cv.id, `${cv.name}.pdf`);
        if (!result.success) {
            addToast(result.error || 'Failed to download PDF', 'error');
        }
    }

    async function handleDownloadMarkdown(cv) {
        const result = await cvService.downloadMarkdown(cv.id, `${cv.name}.md`);
        if (!result.success) {
            addToast(result.error || 'Failed to download Markdown', 'error');
        }
    }
</script>

<svelte:head>
    <title>Dashboard - ResumeForge</title>
</svelte:head>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {$user?.email}
        </h1>
        <p class="text-gray-600">
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
            <span class="ml-2 text-gray-600">Loading your CVs...</span>
        </div>
    {:else if $cvs.length === 0}
        <div class="text-center py-12">
            <FileText class="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h3 class="text-lg font-medium text-gray-900 mb-2">
                No CVs yet
            </h3>
            <p class="text-gray-600 mb-6">
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
                <div class="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                    <div class="p-6">
                        <div class="flex items-start justify-between mb-4">
                            <div class="flex-1">
                                <h3 class="text-lg font-semibold text-gray-900 mb-1">
                                    {cv.name}
                                </h3>
                                <p class="text-sm text-gray-500">
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
                                class="text-gray-400 hover:text-red-600 transition-colors"
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
<Modal bind:open={showTemplateModal} title="Choose a Template" size="lg">
    <div class="space-y-6">
        <p class="text-gray-600">
            Start with a professional template or create a blank CV
        </p>

        <!-- Blank option -->
        <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-primary-300 cursor-pointer transition-colors"
             on:click={handleCreateBlank}>
            <Plus class="h-12 w-12 text-gray-400 mx-auto mb-3" />
            <h3 class="text-lg font-medium text-gray-900 mb-1">Start from Blank</h3>
            <p class="text-gray-600">Create a CV from scratch with your own content</p>
        </div>

        <!-- Templates -->
        {#if $templates.length > 0}
            <div class="grid md:grid-cols-2 gap-4">
                {#each $templates as template (template.id)}
                    <div class="border border-gray-200 rounded-lg p-4 hover:border-primary-300 cursor-pointer transition-colors"
                         on:click={() => handleTemplateSelect(template)}>
                        <h3 class="font-medium text-gray-900 mb-1">{template.name}</h3>
                        <p class="text-sm text-gray-600 mb-2">{template.description}</p>
                        {#if template.is_default === 'true'}
                            <span class="inline-block bg-primary-100 text-primary-800 text-xs px-2 py-1 rounded">
                                Recommended
                            </span>
                        {/if}
                    </div>
                {/each}
            </div>
        {/if}
    </div>
</Modal>

<!-- New CV Modal -->
<Modal bind:open={showNewCVModal} title="Create New CV">
    <div class="space-y-4">
        {#if selectedTemplate}
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p class="text-sm text-blue-800">
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

    <div slot="footer" class="flex justify-end space-x-3">
        <Button variant="outline" on:click={() => showNewCVModal = false}>
            Cancel
        </Button>
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
        <p class="text-gray-600">
            Are you sure you want to delete <strong>{cvToDelete?.name}</strong>? 
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