export async function onRequest(context) {
    const { env, request } = context;
    const token = env.GITHUB_TOKEN;

    if (!token || token === 'undefined') {
        return new Response('Missing GITHUB_TOKEN env var', { status: 500 });
    }

    // Redirect through callback to simulate the OAuth redirect chain
    const url = new URL(request.url);
    const callbackUrl = url.origin + '/api/callback' +
        '?access_token=' + encodeURIComponent(token) +
        '&provider=github' +
        '&scope=repo,user';

    return Response.redirect(callbackUrl, 302);
}