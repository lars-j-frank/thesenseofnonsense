/**
 * Proxy to GitHub API
 * Adds Authorization header from incoming request to outgoing request
 * Handles CORS
 */

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  // The path after /github/ is the GitHub API path
  // For example, /github/repos/lars-j-frank/thesenseofnonsense/contents/content/series
  // becomes repos/lars-j-frank/thesenseofnonsense/contents/content/series
  const path = url.pathname.split('/github/')[1];
  
  if (!path) {
    return new Response('Missing GitHub API path', { status: 400 });
  }

  // Forward the Authorization header if present
  const authHeader = request.headers.get('Authorization');
  const headers = new Headers();
  if (authHeader) {
    headers.set('Authorization', authHeader);
  }
  // Accept JSON response
  headers.set('Accept', 'application/vnd.github.v3+json');
  // Set user agent to avoid GitHub blocking
  headers.set('User-Agent', 'tson-editor/1.0');

  // Prepare the request to GitHub
  const githubUrl = `https://api.github.com/${path}`;
  
  // Copy query parameters
  url.searchParams.forEach((value, key) => {
    // Skip any internal parameters we might add later
    if (!key.startsWith('_')) {
      url.searchParams.set(key, value);
    }
  });
  
  // Build fetch options
  const fetchOptions = {
    method: request.method,
    headers: headers,
    // Redirect mode: manual to handle redirects ourselves if needed
    redirect: 'follow',
  };

  // For methods with body, we need to pass the body
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    // Clone the request to get its body
    const requestClone = request.clone();
    try {
      // Try to get the body as text, but we'll pass it through as is
      const body = await requestClone.text();
      if (body) {
        fetchOptions.body = body;
      }
    } catch (err) {
      // If we can't read the body, proceed without it (shouldn't happen for valid requests)
      console.warn('Could not read request body:', err);
    }
  }

  // Make the request to GitHub
  let response;
  try {
    response = await fetch(githubUrl, fetchOptions);
  } catch (err) {
    return new Response(`Failed to fetch from GitHub: ${err.message}`, { 
      status: 502,
      headers: { 'Content-Type': 'text/plain' }
    });
  }

  // Prepare response to client
  const responseHeaders = new Headers(response.headers);
  // Set CORS headers
  responseHeaders.set('Access-Control-Allow-Origin', '*');
  responseHeaders.set('Access-Control-Allow-Methods', 'GET,POST,PATCH,PUT,DELETE,OPTIONS');
  responseHeaders.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Handle OPTIONS preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: responseHeaders
    });
  }

  // Return the response from GitHub
  return new Response(response.body, {
    status: response.status,
    headers: responseHeaders
  });
}