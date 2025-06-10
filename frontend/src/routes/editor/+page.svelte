<script>
    import { onMount, onDestroy } from 'svelte';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { isAuthenticated } from '$lib/stores/auth.js';
    import { currentCV, draftCV, cvService, hasUnsavedChanges } from '$lib/stores/cv.js';
    import { addToast } from '$lib/stores/toast.js';
    import { debounce } from '$lib/utils/helpers.js';
    import EditorLayout from '$lib/components/cv/EditorLayout.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Input from '$lib/components/common/Input.svelte';

    let isDemo = false;
    let showSaveModal = false;
    let newCVName = '';
    let saving = false;
    let autoSaveTimeout;

    // Get URL parameters
    $: cvId = $page.url.searchParams.get('cv');
    $: isNewCV = $page.url.searchParams.get('new') === 'true';
    $: isDemoMode = $page.url.searchParams.get('demo') === 'true';

    // Reactive statement for dynamic title - THIS FIXES THE ERROR
    $: pageTitle = isDemo 
        ? 'Demo Editor - ResumeForge'
        : $currentCV?.name 
            ? `${$currentCV.name} - ResumeForge`
            : 'New CV - ResumeForge';

    onMount(async () => {
        isDemo = isDemoMode;

        if (isDemo) {
            // Demo mode - load with sample content
            loadDemoContent();
        } else if (cvId) {
            // Load existing CV
            if (!$isAuthenticated) {
                goto('/auth/login');
                return;
            }
            await loadCV(cvId);
        } else if (isNewCV) {
            // New CV
            if (!$isAuthenticated) {
                goto('/auth/login');
                return;
            }
            cvService.clearCurrent();
        } else {
            // No specific CV or demo - redirect to dashboard
            if ($isAuthenticated) {
                goto('/dashboard');
            } else {
                goto('/');
            }
        }

        // Set up auto-save for authenticated users
        if ($isAuthenticated && !isDemo) {
            setupAutoSave();
        }
    });

    onDestroy(() => {
        if (autoSaveTimeout) {
            clearTimeout(autoSaveTimeout);
        }
    });

    function loadDemoContent() {
        draftCV.set({
            name: 'Demo CV',
            markdown_content: `# John Doe
**Software Engineer** [CENTER]

📧 john.doe@email.com | 📱 (555) 123-4567 | 🌐 linkedin.com/in/johndoe [CENTER]

## Professional Summary
Experienced software engineer with 5+ years of expertise in full-stack development, specializing in React and Node.js. Passionate about building scalable applications and solving complex technical challenges.

## Technical Skills
- **Languages:** JavaScript, TypeScript, Python, Java
- **Frontend:** React, Vue.js, HTML5, CSS3, Tailwind CSS
- **Backend:** Node.js, Express, FastAPI, Django
- **Databases:** PostgreSQL, MongoDB, Redis
- **Tools:** Docker, Git, AWS, CI/CD

## Professional Experience

### Senior Software Engineer | TechCorp Inc. [DATE: 2022 - Present]
- Developed and maintained microservices architecture serving 100k+ daily active users
- Improved system performance by 40% through database optimization and caching strategies
- Led a team of 4 developers on a major product redesign project
- Technologies used: React, Node.js, PostgreSQL, Docker, AWS

### Software Engineer | StartupXYZ [DATE: 2020 - 2022]
- Built responsive web applications using React and TypeScript
- Collaborated with cross-functional teams to deliver features on tight deadlines
- Implemented automated testing reducing bug reports by 30%
- Technologies used: React, TypeScript, Express, MongoDB

## Education
**Bachelor of Science in Computer Science** | University of Technology [DATE: 2020]
*Graduated Magna Cum Laude*

## Projects
- **E-commerce Platform:** Full-stack application with React frontend and Node.js backend
- **Task Management App:** Progressive web app with offline capabilities
- **API Gateway:** Microservices orchestration platform built with Node.js and Docker`,
            settings: {
                font: 'Arial',
                fontSize: 11,
                margins: { top: 20, bottom: 20, left: 15, right: 15 },
                theme: 'professional'
            }
        });
        addToast('Demo mode loaded! Try editing the content or using AI features.', 'info');
    }

    async function loadCV(id) {
        const result = await cvService.loadCV(id);
        if (!result.success) {
            addToast(result.error || 'Failed to load CV', 'error');
            goto('/dashboard');
        }
    }

    function setupAutoSave() {
        // Auto-save every 30 seconds if there are changes
        const autoSave = debounce(async () => {
            if ($currentCV && $hasUnsavedChanges) {
                await cvService.autoSave(
                    $currentCV.id,
                    $draftCV.markdown_content,
                    $draftCV.settings
                );
            }
        }, 30000);

        // Set up the interval
        autoSaveTimeout = setInterval(autoSave, 30000);
    }

    function handleSave() {
        if (isDemo) {
            // Demo mode - show save modal to create account
            showSaveModal = true;
        } else if ($currentCV) {
            // Update existing CV
            saveCurrentCV();
        } else {
            // New CV - show name modal
            newCVName = $draftCV.name || 'My CV';
            showSaveModal = true;
        }
    }

    async function saveCurrentCV() {
    // ADD VALIDATION HERE
        if (!$currentCV || !$currentCV.id) {
            // For new CVs, show the name modal instead
            newCVName = $draftCV.name || 'My CV';
            showSaveModal = true;
            return;
        }

        saving = true;

        try {
            const result = await cvService.updateCV(
                $currentCV.id,
                $draftCV.name,
                $draftCV.markdown_content,
                $draftCV.settings
            );

            if (result.success) {
                addToast('CV saved successfully!', 'success');
            } else {
                addToast(result.error || 'Failed to save CV', 'error');
            }
        } finally {
            saving = false;
        }
    }

    async function handleCreateNewCV() {
        if (!newCVName.trim()) {
            addToast('Please enter a name for your CV', 'error');
            return;
        }

        saving = true;

        try {
            const result = await cvService.createCV(
                newCVName.trim(),
                $draftCV.markdown_content,
                $draftCV.settings
            );

            if (result.success) {
                showSaveModal = false;
                addToast('CV created successfully!', 'success');
                goto(`/editor?cv=${result.data.id}`);
            } else {
                addToast(result.error || 'Failed to create CV', 'error');
            }
        } finally {
            saving = false;
        }
    }

    function handleDemoSave() {
        showSaveModal = false;
        goto('/auth/register');
    }

    // Handle browser navigation warnings for unsaved changes
    function handleBeforeUnload(event) {
        if (!isDemo && $hasUnsavedChanges) {
            event.preventDefault();
            event.returnValue = '';
        }
    }
</script>

<svelte:head>
    <title>{pageTitle}</title>
</svelte:head>

<svelte:window on:beforeunload={handleBeforeUnload} />

<!-- FIXED: Added dark mode background -->
<div class="h-screen flex flex-col bg-gray-50 dark:bg-black">
    <!-- Editor Layout -->
    <EditorLayout 
        {isDemo}
        onSave={handleSave}
        {saving}
    />
</div>

<!-- Save Modal - FIXED: Added dark mode styling -->
<Modal bind:open={showSaveModal} title={isDemo ? 'Save Your CV' : 'Name Your CV'}>
    <div class="space-y-4">
        {#if isDemo}
            <p class="text-gray-600 dark:text-gray-300">
                To save your CV, you'll need to create a free account. Your work will be preserved!
            </p>
            <div class="bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded-lg p-4">
                <h4 class="font-medium text-blue-900 dark:text-blue-100 mb-2">What you'll get:</h4>
                <ul class="text-sm text-blue-800 dark:text-blue-200 space-y-1">
                    <li>• Save unlimited CVs</li>
                    <li>• AI-powered editing assistance</li>
                    <li>• Professional templates</li>
                    <li>• ATS scoring and optimization</li>
                </ul>
            </div>
        {:else}
            <Input
                label="CV Name"
                placeholder="e.g. Software Engineer Resume"
                bind:value={newCVName}
                required
            />
        {/if}
    </div>

    <div slot="footer" class="flex justify-end space-x-3">
        <Button variant="outline" on:click={() => showSaveModal = false}>
            Cancel
        </Button>
        {#if isDemo}
            <Button on:click={handleDemoSave}>
                Create Free Account
            </Button>
        {:else}
            <Button 
                on:click={handleCreateNewCV}
                loading={saving}
                disabled={saving || !newCVName.trim()}
            >
                Save CV
            </Button>
        {/if}
    </div>
</Modal>