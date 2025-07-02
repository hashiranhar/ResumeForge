<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { browser } from '$app/environment';
    import { isAuthenticated, user, authenticatedFetch } from '$lib/stores/auth.js';
    import { cvs, templates, cvService, isLoading } from '$lib/stores/cv.js';
    import { addToast } from '$lib/stores/toast.js';
    import { formatRelativeTime, formatDate } from '$lib/utils/helpers.js';
    import Button from '$lib/components/common/Button.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import Input from '$lib/components/common/Input.svelte';
    import { Plus, FileText, Edit, Trash2, Download, Eye, Upload, Clock, Calendar, Copy } from 'lucide-svelte';

    // Modal state variables
    let showTemplateModal = false;
    let showNewCVModal = false;
    let showDeleteModal = false;
    let showPDFImportModal = false;
    
    // CV creation variables
    let selectedTemplate = null;
    let newCVName = '';
    let creatingCV = false;
    
    // Delete variables
    let cvToDelete = null;
    let deletingCV = false;
    let duplicatingCV = false;


    // PDF import variables
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

    function handleImportPDF() {
        showTemplateModal = false;
        showPDFImportModal = true;
    }

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
                
                if (browser && result.data) {
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
        if (browser) {
            goto(`/editor?cv=${cv.id}`);
        }
    }

    function handleDeleteCV(cv) {
        cvToDelete = cv;
        showDeleteModal = true;
    }

    async function confirmDeleteCV() {
        if (!cvToDelete) return;

        deletingCV = true;

        try {
            const result = await cvService.deleteCV(cvToDelete.id);
            if (result.success) {
                addToast('CV deleted successfully', 'success');
                showDeleteModal = false;
                cvToDelete = null;
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
        console.log('Download button clicked for CV:', cv.name);
        
        try {
            addToast('Generating PDF...', 'info');
            
            const response = await authenticatedFetch(`/api/cvs/${cv.id}/pdf`);
            
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`Failed to generate PDF: ${response.status}`);
            }

            const blob = await response.blob();
            console.log('Blob size:', blob.size);
            
            if (blob.size === 0) {
                throw new Error('Generated PDF is empty');
            }
            
            // Create download
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${cv.name}.pdf`;
            a.style.display = 'none';
            
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            window.URL.revokeObjectURL(url);
            
            addToast('PDF downloaded successfully!', 'success');
            
        } catch (error) {
            console.error('PDF download error:', error);
            addToast(error.message || 'Failed to download PDF', 'error');
        }
    }

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
            const currentToken = localStorage.getItem('resumeforge_token');
            
            const response = await fetch('/api/pdf/create-cv', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${currentToken}`
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

                // Show success message
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

    async function handleDuplicateCV(cv) {
        duplicatingCV = true;
        
        try {
            // First, get the full CV data
            const currentToken = localStorage.getItem('resumeforge_token');
            const response = await fetch(`/api/cvs/${cv.id}`, {
                headers: {
                    'Authorization': `Bearer ${currentToken}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch CV data');
            }

            const fullCV = await response.json();
            
            // Create new CV with duplicated content
            const duplicateName = `Copy of ${cv.name}`;
            const result = await cvService.createCV(
                duplicateName,
                fullCV.markdown_content,
                fullCV.settings
            );

            if (result.success) {
                addToast('CV duplicated successfully!', 'success');
                // Refresh the list to show the new duplicated CV
                await cvService.loadCVs();
            } else {
                addToast(result.error || 'Failed to duplicate CV', 'error');
            }
        } catch (error) {
            console.error('Duplicate error:', error);
            addToast('Failed to duplicate CV', 'error');
        } finally {
            duplicatingCV = false;
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
                                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                                    {cv.name}
                                </h3>
                                
                                <!-- Date Information -->
                                <div class="space-y-1">
                                    <div class="flex items-center text-sm text-gray-500 dark:text-gray-400">
                                        <Calendar class="h-4 w-4 mr-2" />
                                        <span>Created {formatDate(cv.created_at)}</span>
                                    </div>
                                    <div class="flex items-center text-sm text-gray-500 dark:text-gray-400">
                                        <Clock class="h-4 w-4 mr-2" />
                                        <span>Updated {formatRelativeTime(cv.updated_at)}</span>
                                    </div>
                                </div>
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
                            
                            <div class="flex items-center space-x-2">
                                <button
                                    class="text-gray-400 dark:text-gray-500 hover:text-blue-600 dark:hover:text-blue-400 transition-colors disabled:opacity-50"
                                    on:click={() => handleDuplicateCV(cv)}
                                    disabled={duplicatingCV}
                                    title="Duplicate CV"
                                >
                                    <Copy class="h-4 w-4" />
                                </button>
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
                                class="w-full p-4 border border-gray-200 dark:border-gray-600 rounded-lg text-left hover:border-primary-300 dark:hover:border-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
                                on:click={() => handleTemplateSelect(template)}
                                aria-describedby="template-{template.id}-desc"
                            >
                                <h5 class="font-medium text-gray-900 dark:text-white mb-1">
                                    {template.name}
                                </h5>
                                <p class="text-sm text-gray-600 dark:text-gray-300" id="template-{template.id}-desc">
                                    {template.description || 'Professional template'}
                                </p>
                            </button>
                        </li>
                    {/each}
                </ul>
            </div>
        {/if}
    </div>
</Modal>

<!-- CV Name Modal -->
<Modal
    bind:open={showNewCVModal}
    title={selectedTemplate ? `Create CV from ${selectedTemplate.name}` : 'Create New CV'}
    size="md"
    close={() => {
        showNewCVModal = false;
        newCVName = '';
        selectedTemplate = null;
    }}
>
    <form on:submit|preventDefault={handleCreateCV} class="space-y-4">
        <Input
            label="CV Name"
            placeholder="e.g. Senior Software Engineer Resume"
            bind:value={newCVName}
            required
            autofocus
        />

        <div class="flex justify-end space-x-3">
            <Button
                variant="outline"
                on:click={() => {
                    showNewCVModal = false;
                    newCVName = '';
                    selectedTemplate = null;
                }}
            >
                Cancel
            </Button>
            <Button type="submit" disabled={creatingCV || !newCVName.trim()}>
                {#if creatingCV}
                    Creating...
                {:else}
                    Create CV
                {/if}
            </Button>
        </div>
    </form>
</Modal>

<!-- Delete Confirmation Modal -->
<Modal
    bind:open={showDeleteModal}
    title="Delete CV"
    size="sm"
    close={() => {
        showDeleteModal = false;
        cvToDelete = null;
    }}
>
    <div class="space-y-4">
        <p class="text-gray-600 dark:text-gray-300">
            Are you sure you want to delete "<strong>{cvToDelete?.name}</strong>"? This action cannot be undone.
        </p>

        <div class="flex justify-end space-x-3">
            <Button
                variant="outline"
                on:click={() => {
                    showDeleteModal = false;
                    cvToDelete = null;
                }}
            >
                Cancel
            </Button>
            <Button variant="danger" on:click={confirmDeleteCV} disabled={deletingCV}>
                {#if deletingCV}
                    Deleting...
                {:else}
                    Delete CV
                {/if}
            </Button>
        </div>
    </div>
</Modal>

<!-- PDF Import Modal -->
<Modal
    bind:open={showPDFImportModal}
    title="Import CV from PDF"
    size="lg"
    close={() => {
        showPDFImportModal = false;
        pdfFile = null;
        pdfFileName = '';
        pdfCVName = '';
        pdfPreferences = 'professional';
    }}
>
    <form on:submit|preventDefault={handlePDFImport} class="space-y-6">
        <!-- File Upload -->
        <div>
            <label for="pdf-file-input" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                Select PDF File
            </label>
            
            <div ß
                class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center cursor-pointer hover:border-gray-400 dark:hover:border-gray-500 transition-colors"
                on:click={() => document.getElementById('pdf-file-input').click()}
                on:keydown={(e) => handleKeydown(e, () => document.getElementById('pdf-file-input').click())}
                role="button"
                tabindex="0"
                aria-describedby="file-upload-desc"
            >
                {#if pdfFile}
                    <!-- File Selected -->
                    <div class="space-y-2">
                        <FileText class="h-12 w-12 text-green-500 mx-auto" />
                        <div class="text-sm">
                            <p class="font-medium text-gray-900 dark:text-white">
                                {pdfFileName}
                            </p>
                            <p class="text-gray-500 dark:text-gray-400">
                                {(pdfFile.size / 1024 / 1024).toFixed(2)} MB
                            </p>
                        </div>
                        <button
                            type="button"
                            class="text-sm text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300"
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
                            <p class="text-gray-500 dark:text-gray-400" id="file-upload-desc">
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
                                    ? 'border-orange-500 bg-orange-50 dark:bg-orange-900/20' 
                                    : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'}"
                                on:click={() => pdfPreferences = style.value}
                            >
                                <div class="font-medium text-gray-900 dark:text-white text-sm">
                                    {style.label}
                                </div>
                                <div class="text-xs text-gray-500 dark:text-gray-400">
                                    {style.desc}
                                </div>
                            </button>
                        {/each}
                    </div>
                </div>

                <div class="flex justify-end space-x-3">
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
                    <Button type="submit" disabled={importingPDF || !pdfCVName.trim()}>
                        {#if importingPDF}
                            Importing...
                        {:else}
                            Import CV
                        {/if}
                    </Button>
                </div>
            </div>
        {/if}
    </form>
</Modal>