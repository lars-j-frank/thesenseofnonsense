export async function onRequest(context) {
    const { env, request } = context;
    const url = new URL(request.url);
    
    // Get token from query params (from auth redirect) or env var (fallback)
    let token = url.searchParams.get('access_token') || env.GITHUB_TOKEN;
    const provider = url.searchParams.get('provider') || 'github';
    const scope = url.searchParams.get('scope') || 'repo,user';

    if (!token || token === 'undefined') {
        return new Response('Missing token', { status: 500 });
    }

    // Redirect to admin with token in hash — Decap CMS parses this
    const adminHash = '/admin/#/' + 
        '?access_token=' + encodeURIComponent(token) +
        '&token_type=bearer' +
        '&provider=' + encodeURIComponent(provider) +
        '&scope=' + encodeURIComponent(scope);

    return Response.redirect(url.origin + adminHash, 302);
}