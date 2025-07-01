<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { browser } from '$app/environment';
    import { isAuthenticated, user } from '$lib/stores/auth.js';
    import { authenticatedFetch } from '$lib/stores/auth.js';
    import { cvs, templates, cvService, isLoading } from '$lib/stores/cv.js';
    import { addToast } from '$lib/stores/toast.js';
    import { formatRelativeTime } from '$lib/utils/helpers.js';
    import Button from '$lib/components/common/Button.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import Input from '$lib/components/common/Input.svelte';
    import { Plus, FileText, Edit, Trash2, Download, Eye, Upload } from 'lucide-svelte'; // Added Upload

    // Modal state variables
    let showTemplateModal = false;
    let showNewCVModal = false;
    let showDeleteModal = false;
    let showPDFImportModal = false; // NEW: PDF import modal state
    
    // CV creation variables
    let selectedTemplate = null;
    let newCVName = '';
    let creatingCV = false;
    
    // Delete variables
    let cvToDelete = null;
    let deletingCV = false;

    // NEW: PDF import variables
    let pdfFile = null;
    let pdfFileName = '';
    let pdfCVName = '';
    let pdfPreferences = 'professional';
    let importingPDF = false;

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

    // NEW: Handle PDF import flow
    function handleImportPDF() {
        showTemplateModal = false;
        showPDFImportModal = true;
    }

    // NEW: Handle PDF file selection
    function handlePDFFileSelect(event) {
        const file = event.target.files[0];
        if (!file) return;

        // Validate file type
        if (file.type !== 'application/pdf') {
            addToast('Please select a PDF file', 'error');
            return;
        }

        // Validate file size (5MB max)
        const maxSize = 5 * 1024 * 1024; // 5MB in bytes
        if (file.size > maxSize) {
            addToast('File size must be less than 5MB', 'error');
            return;
        }

        pdfFile = file;
        pdfFileName = file.name;
        
        // Auto-generate CV name from filename (remove .pdf extension)
        pdfCVName = file.name.replace(/\.pdf$/i, '');
    }

    // Keyboard event handler
    function handleKeydown(event, callback) {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            callback();
        }
    }

    // Existing functions continue below...
    async function handleCreateCV() {
        if (!newCVName.trim()) {
            addToast('Please enter a name for your CV', 'error');
            return;
        }

        creatingCV = true;

        try {
            let result;
            
            if (selectedTemplate) {
                result = await cvService.createCVFromTemplate(selectedTemplate.id, newCVName.trim());
            } else {
                const blankContent = `# ${newCVName}\n\n## Contact Information\n\n## Summary\n\n## Experience\n\n## Education\n\n## Skills`;
                result = await cvService.createCV(
                    newCVName.trim(),
                    blankContent,
                    { 
                        fontSize: 12,
                        fontFamily: 'Arial',
                        theme: 'professional' 
                    }
                );
            }

            if (result.success) {
                showNewCVModal = false;
                newCVName = '';
                selectedTemplate = null;
                addToast('CV created successfully!', 'success');
                if (browser) {
                    goto(`/editor?cv=${result.data.id}`);
                }
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
            const result = await cvService.downloadPDF(cv.id, `${cv.name}.pdf`);
            
            if (result.success) {
                addToast('PDF downloaded successfully', 'success');
            } else {
                addToast(result.error || 'Failed to generate PDF', 'error');
            }
        } catch (error) {
            addToast('Failed to download PDF', 'error');
        }
    }

    // NEW: Handle PDF import and conversion
    async function handlePDFImport() {
        if (!pdfFile || !pdfCVName.trim()) {
            addToast('Please select a PDF file and enter a CV name', 'error');
            return;
        }

        importingPDF = true;

        try {
            // Create FormData for file upload
            const formData = new FormData();
            formData.append('file', pdfFile);
            formData.append('cv_name', pdfCVName.trim());
            formData.append('preferences', pdfPreferences);

            // Make API call to convert PDF
            // Note: For FormData uploads, we need to manually handle the request to avoid Content-Type issues
            const currentToken = localStorage.getItem('resumeforge_token');
            
            const response = await fetch('/api/pdf/create-cv', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${currentToken}`
                    // DON'T set Content-Type - let browser handle it for FormData
                },
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to import PDF');
            }

            const result = await response.json();

            if (result.success) {
                // Refresh the CVs list to include the new CV
                await cvService.loadCVs();
                
                // Close modal and reset state
                showPDFImportModal = false;
                pdfFile = null;
                pdfFileName = '';
                pdfCVName = '';
                pdfPreferences = 'professional';

                // Show success message with processing info
                addToast('PDF imported successfully! Review and edit as needed.', 'success');
                
                // Redirect to editor with the new CV
                if (browser) {
                    goto(`/editor?cv=${result.cv.id}`);
                }
            } else {
                throw new Error('Import failed');
            }

        } catch (error) {
            console.error('PDF import error:', error);
            addToast(error.message || 'Failed to import PDF. Please try again.', 'error');
        } finally {
            importingPDF = false;
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
            Start with a professional template, create a blank CV, or import from an existing PDF
        </p>

        <!-- Split Options: Blank + PDF Import -->
        <div class="grid grid-cols-2 gap-4">
            <!-- Blank CV Option -->
            <button
                type="button"
                class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center hover:border-primary-300 dark:hover:border-primary-500 cursor-pointer transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
                on:click={handleCreateBlank}
                aria-describedby="blank-template-desc"
            >
                <Plus class="h-12 w-12 text-gray-400 dark:text-gray-500 mx-auto mb-3" />
                <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-1">Start from Blank</h3>
                <p class="text-sm text-gray-600 dark:text-gray-300" id="blank-template-desc">
                    Create a CV from scratch with your own content
                </p>
            </button>

            <!-- PDF Import Option -->
            <button
                type="button"
                class="border-2 border-dashed border-orange-300 dark:border-orange-600 rounded-lg p-6 text-center hover:border-orange-400 dark:hover:border-orange-500 cursor-pointer transition-colors focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2"
                on:click={handleImportPDF}
                aria-describedby="pdf-import-desc"
            >
                <Upload class="h-12 w-12 text-orange-400 dark:text-orange-500 mx-auto mb-3" />
                <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-1">Import from PDF</h3>
                <p class="text-sm text-gray-600 dark:text-gray-300" id="pdf-import-desc">
                    Upload an existing PDF resume to convert
                </p>
            </button>
        </div>

        <!-- Templates (existing code remains the same) -->
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

<!-- PDF Import Modal -->
<Modal 
    bind:open={showPDFImportModal} 
    title="Import from PDF" 
    size="lg"
    close={() => {
        showPDFImportModal = false;
        // Reset PDF import state
        pdfFile = null;
        pdfFileName = '';
        pdfCVName = '';
        pdfPreferences = 'professional';
    }}
>
    <div class="space-y-6">
        <p class="text-gray-600 dark:text-gray-300">
            Upload your existing PDF resume and we'll convert it to an editable CV
        </p>

        <!-- File Upload Area -->
        <div class="space-y-4">
            <div class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                PDF File *
            </div>
            
            <!-- Drag & Drop Zone -->
            <div 
                class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center hover:border-orange-400 dark:hover:border-orange-500 transition-colors cursor-pointer"
                class:border-orange-400={pdfFile}
                class:bg-orange-50={pdfFile}
                class:dark:bg-orange-900={pdfFile}
                on:click={() => document.getElementById('pdf-file-input').click()}
                on:keydown={(e) => handleKeydown(e, () => document.getElementById('pdf-file-input').click())}
                role="button"
                tabindex="0"
                aria-label="Click to select PDF file"
            >
                {#if pdfFile}
                    <!-- File Selected State -->
                    <div class="space-y-2">
                        <FileText class="h-12 w-12 text-orange-500 mx-auto" />
                        <div class="text-sm">
                            <p class="font-medium text-gray-900 dark:text-white">{pdfFileName}</p>
                            <p class="text-gray-500 dark:text-gray-400">
                                {(pdfFile.size / 1024 / 1024).toFixed(2)} MB
                            </p>
                        </div>
                        <button 
                            type="button"
                            class="text-sm text-orange-600 dark:text-orange-400 hover:text-orange-700 dark:hover:text-orange-300"
                            on:click|stopPropagation={() => {
                                pdfFile = null;
                                pdfFileName = '';
                                pdfCVName = '';
                            }}
                        >
                            Remove file
                        </button>
                    </div>
                {:else}
                    <!-- Empty State -->
                    <div class="space-y-2">
                        <Upload class="h-12 w-12 text-gray-400 dark:text-gray-500 mx-auto" />
                        <div class="text-sm">
                            <p class="font-medium text-gray-900 dark:text-white">
                                Click to upload or drag and drop
                            </p>
                            <p class="text-gray-500 dark:text-gray-400">
                                PDF files up to 5MB
                            </p>
                        </div>
                    </div>
                {/if}
            </div>

            <!-- Hidden File Input -->
            <input
                id="pdf-file-input"
                type="file"
                accept=".pdf,application/pdf"
                class="hidden"
                on:change={handlePDFFileSelect}
            />
        </div>

        <!-- CV Name Input -->
        {#if pdfFile}
            <div class="space-y-4">
                <Input
                    label="CV Name"
                    placeholder="e.g. Software Engineer Resume"
                    bind:value={pdfCVName}
                    required
                />

                <!-- Style Preferences -->
                <div>
                    <div class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                        Style Preference
                    </div>
                    <div class="grid grid-cols-2 gap-3">
                        {#each [
                            { value: 'professional', label: 'Professional', desc: 'Clean and corporate' },
                            { value: 'technical', label: 'Technical', desc: 'Tech-focused layout' },
                            { value: 'creative', label: 'Creative', desc: 'Modern and stylish' },
                            { value: 'academic', label: 'Academic', desc: 'Research-oriented' }
                        ] as style}
                            <button
                                type="button"
                                class="p-3 border rounded-lg text-left transition-colors focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 {pdfPreferences === style.value 
                                    ? 'border-orange-500 bg-orange-50 dark:bg-orange-900' 
                                    : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'}"
                                on:click={() => pdfPreferences = style.value}
                            >
                                <p class="font-medium text-gray-900 dark:text-white text-sm">
                                    {style.label}
                                </p>
                                <p class="text-xs text-gray-500 dark:text-gray-400">
                                    {style.desc}
                                </p>
                            </button>
                        {/each}
                    </div>
                </div>
            </div>
        {/if}
    </div>

    <div slot="footer" class="flex justify-end space-x-3">
        <Button 
            variant="outline" 
            on:click={() => {
                showPDFImportModal = false;
                pdfFile = null;
                pdfFileName = '';
                pdfCVName = '';
                pdfPreferences = 'professional';
            }}
        >
            Cancel
        </Button>
        <Button 
            on:click={handlePDFImport}
            loading={importingPDF}
            disabled={importingPDF || !pdfFile || !pdfCVName.trim()}
        >
            {importingPDF ? 'Converting...' : 'Import & Convert'}
        </Button>
    </div>
</Modal>