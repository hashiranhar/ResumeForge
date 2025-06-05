import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Initialize darkMode from localStorage or system preference
function createDarkMode() {
    const initialValue = browser 
        ? localStorage.getItem('darkMode') === 'true' || 
          (localStorage.getItem('darkMode') === null && 
           window.matchMedia('(prefers-color-scheme: dark)').matches)
        : false;
    
    const { subscribe, set, update } = writable(initialValue);

    return {
        subscribe,
        set: (value) => {
            if (browser) {
                localStorage.setItem('darkMode', value.toString());
                if (value) {
                    document.documentElement.classList.add('dark');
                    document.body.style.backgroundColor = '#0a0a0a';
                    document.body.style.color = '#ffffff';
                } else {
                    document.documentElement.classList.remove('dark');
                    document.body.style.backgroundColor = '#ffffff';
                    document.body.style.color = '#000000';
                }
            }
            set(value);
        },
        toggle: () => update(n => {
            const newValue = !n;
            if (browser) {
                localStorage.setItem('darkMode', newValue.toString());
                if (newValue) {
                    document.documentElement.classList.add('dark');
                    document.body.style.backgroundColor = '#0a0a0a';
                    document.body.style.color = '#ffffff';
                } else {
                    document.documentElement.classList.remove('dark');
                    document.body.style.backgroundColor = '#ffffff';
                    document.body.style.color = '#000000';
                }
            }
            return newValue;
        })
    };
}

export const darkMode = createDarkMode();