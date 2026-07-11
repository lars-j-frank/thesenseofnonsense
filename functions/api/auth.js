export async function onRequest(context) {
    const { env } = context;
    const token = env.GITHUB_TOKEN;

    if (!token || token === 'undefined' || token === '') {
        return new Response(JSON.stringify({ error: 'Missing or empty GITHUB_TOKEN' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }

    // Return the token in the format expected by Decap CMS
    return new Response(JSON.stringify({
        access_token: token.trim(),
        token_type: 'bearer'
    }), {
        headers: { 'Content-Type': 'application/json' }
    });
}