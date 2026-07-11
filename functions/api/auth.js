export async function onRequest(context) {
    const { env } = context;
    const token = env.GITHUB_TOKEN;

    if (!token || token === 'undefined' || token === '') {
        return new Response('Missing or empty GITHUB_TOKEN', { status: 500 });
    }

    // Clean the token
    const cleanToken = token.trim();

    // For implicit flow, redirect to admin with token in hash
    const redirectUrl = `/admin/#access_token=${encodeURIComponent(cleanToken)}&token_type=bearer`;

    return Response.redirect(redirectUrl, 302);
}