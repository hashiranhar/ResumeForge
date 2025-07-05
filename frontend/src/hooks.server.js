export async function handle({ event, resolve }) {
    // Handle Chrome DevTools requests silently
    if (event.url.pathname === '/.well-known/appspecific/com.chrome.devtools.json') {
        return new Response('{}', {
            status: 200,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }

    return await resolve(event);
}