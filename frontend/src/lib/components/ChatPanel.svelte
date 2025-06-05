<script>
	import { llm } from '$lib/api.js';
	import { currentCV, chatHistory } from '$lib/stores.js';
	import { Send, User, Bot } from 'lucide-svelte';
	
	export let cvId;
	
	let messageInput = '';
	let isLoading = false;
	let messages = [];
	
	async function sendMessage() {
		if (!messageInput.trim() || isLoading) return;
		
		const userMessage = messageInput.trim();
		messageInput = '';
		
		// Add user message
		messages = [...messages, { role: 'user', content: userMessage }];
		isLoading = true;
		
		try {
			// Call chat API
			const response = await llm.chat(userMessage, cvId, messages);
			
			// Add AI response
			messages = [...messages, { role: 'assistant', content: response.reply }];
			chatHistory.set(messages);
		} catch (error) {
			messages = [...messages, { 
				role: 'assistant', 
				content: 'Sorry, I encountered an error. Please try again.' 
			}];
		} finally {
			isLoading = false;
		}
	}
	
	function handleKeyPress(event) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			sendMessage();
		}
	}
</script>

<div class="flex flex-col h-full bg-secondary">
	<!-- Enhanced Header -->
	<div class="bg-tertiary px-6 py-4 border-b border-border">
		<div class="flex items-center space-x-3">
			<div class="w-8 h-8 bg-accent rounded-full flex items-center justify-center">
				<Bot size={16} class="text-white" />
			</div>
			<div>
				<h3 class="text-sm font-semibold text-primary">AI Career Advisor</h3>
				<p class="text-xs text-secondary">Get personalized CV feedback</p>
			</div>
		</div>
	</div>
	
	<!-- Enhanced Messages Area -->
	<div class="flex-1 overflow-y-auto p-6 space-y-4">
		{#if messages.length === 0}
			<div class="text-center text-secondary py-12">
				<div class="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center mx-auto mb-4">
					<Bot size={24} class="text-accent" />
				</div>
				<h4 class="font-medium text-primary mb-2">Hi! I'm your AI career advisor</h4>
				<p class="text-sm mb-6">I can help you improve your CV and answer career questions.</p>
				
				<div class="space-y-3">
					<div class="text-xs text-left space-y-2 bg-tertiary/50 rounded-lg p-4">
						<p class="font-medium text-primary">Try asking me:</p>
						<div class="space-y-1 text-secondary">
							<p>• "How can I improve my experience section?"</p>
							<p>• "What skills should I add for tech roles?"</p>
							<p>• "How do I make this sound more professional?"</p>
							<p>• "What's missing from my CV?"</p>
						</div>
					</div>
				</div>
			</div>
		{/if}
		
		{#each messages as message}
			<div class="flex {message.role === 'user' ? 'justify-end' : 'justify-start'}">
				<div class="flex max-w-[85%] {message.role === 'user' ? 'flex-row-reverse' : 'flex-row'} gap-3">
					<!-- Enhanced Avatar -->
					<div class="flex-shrink-0 w-8 h-8 rounded-full {message.role === 'user' ? 'bg-accent' : 'bg-tertiary'} flex items-center justify-center shadow-sm">
						{#if message.role === 'user'}
							<User size={14} class="text-white" />
						{:else}
							<Bot size={14} class="text-primary" />
						{/if}
					</div>
					
					<!-- Enhanced Message -->
					<div class="px-4 py-3 rounded-xl text-sm {message.role === 'user' ? 'bg-accent text-white' : 'bg-tertiary text-primary'} shadow-sm">
						{message.content}
					</div>
				</div>
			</div>
		{/each}
		
		{#if isLoading}
			<div class="flex justify-start">
				<div class="flex max-w-[85%] gap-3">
					<div class="flex-shrink-0 w-8 h-8 rounded-full bg-tertiary flex items-center justify-center shadow-sm">
						<Bot size={14} class="text-primary" />
					</div>
					<div class="px-4 py-3 rounded-xl text-sm bg-tertiary text-primary shadow-sm">
						<div class="flex space-x-1">
							<div class="w-2 h-2 bg-accent rounded-full animate-bounce"></div>
							<div class="w-2 h-2 bg-accent rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
							<div class="w-2 h-2 bg-accent rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
						</div>
					</div>
				</div>
			</div>
		{/if}
	</div>
	
	<!-- Enhanced Input Area -->
	<div class="border-t border-border p-6 bg-secondary">
		<div class="flex space-x-3">
			<input
				bind:value={messageInput}
				on:keypress={handleKeyPress}
				placeholder="Ask me anything about your CV..."
				disabled={isLoading}
				class="flex-1 px-4 py-3 border border-border rounded-lg bg-primary text-primary text-sm focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent transition-all placeholder-secondary"
			/>
			<button
				on:click={sendMessage}
				disabled={!messageInput.trim() || isLoading}
				class="px-4 py-3 bg-accent hover:bg-accent-hover disabled:opacity-50 text-white rounded-lg transition-colors shadow-sm"
			>
				<Send size={16} />
			</button>
		</div>
		<div class="text-xs text-secondary mt-3 flex items-center space-x-4">
			<span>💡 Press Enter to send, Shift+Enter for new line</span>
		</div>
	</div>
</div>

<style>
	.bg-primary { background-color: var(--bg-primary); }
	.bg-secondary { background-color: var(--bg-secondary); }
	.bg-tertiary { background-color: var(--bg-tertiary); }
	.text-primary { color: var(--text-primary); }
	.text-secondary { color: var(--text-secondary); }
	.border-border { border-color: var(--border); }
	.bg-accent { background-color: var(--accent); }
	.bg-accent-hover:hover { background-color: var(--accent-hover); }
</style>