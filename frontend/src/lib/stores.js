// Svelte stores for global state management
import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Theme store (light/dark)
function createTheme() {
  const { subscribe, set, update } = writable('light');
  
  return {
    subscribe,
    toggle: () => update(theme => {
      const newTheme = theme === 'light' ? 'dark' : 'light';
      if (browser) {
        localStorage.setItem('theme', newTheme);
        document.documentElement.setAttribute('data-theme', newTheme);
      }
      return newTheme;
    }),
    init: () => {
      if (browser) {
        const saved = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', saved);
        set(saved);
      }
    }
  };
}

// User store
function createUser() {
  const { subscribe, set } = writable(null);
  
  return {
    subscribe,
    set,
    clear: () => set(null)
  };
}

// Current CV store
function createCurrentCV() {
  const { subscribe, set, update } = writable(null);
  
  return {
    subscribe,
    set,
    update,
    clear: () => set(null),
    updateContent: (content) => update(cv => cv ? { ...cv, markdown_content: content } : null)
  };
}

// Loading states
export const loading = writable(false);
export const theme = createTheme();
export const user = createUser();
export const currentCV = createCurrentCV();

// Chat history for AI conversations
export const chatHistory = writable([]);