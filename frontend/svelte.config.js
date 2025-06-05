import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    preprocess: vitePreprocess(),
    kit: {
        adapter: adapter(),
        typescript: {
            config: (config) => {
                config.compilerOptions.strict = false;
                config.compilerOptions.noImplicitAny = false;
                return config;
            }
        }
    }
};

export default config;