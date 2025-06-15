/**
 * Cloudflare Worker for serving React SPA
 * Handles static asset serving and client-side routing
 */

// MIME type mapping for static assets
const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.eot': 'font/eot',
  '.otf': 'font/otf',
  '.webp': 'image/webp',
  '.txt': 'text/plain',
  '.xml': 'application/xml',
  '.pdf': 'application/pdf'
};

function getMimeType(url) {
  const extension = url.substring(url.lastIndexOf('.'));
  return MIME_TYPES[extension] || 'application/octet-stream';
}

function getAssetPath(url) {
  // Remove leading slash and query parameters
  let path = url.pathname.slice(1);
  
  // If no path or path doesn't have extension, serve index.html for SPA routing
  if (!path || !path.includes('.')) {
    return 'index.html';
  }
  
  return path;
}

async function handleRequest(request, env) {
  try {
    const url = new URL(request.url);
    const assetPath = getAssetPath(url);
    
    console.log(`Serving asset: ${assetPath}`);
    
    // Try to get the asset from the binding
    const asset = await env.ASSETS.fetch(`http://placeholder/${assetPath}`);
    
    if (asset.ok) {
      // Create response with appropriate headers
      const response = new Response(asset.body, {
        status: asset.status,
        statusText: asset.statusText,
        headers: {
          'Content-Type': getMimeType(assetPath),
          'Cache-Control': assetPath === 'index.html' 
            ? 'no-cache, no-store, must-revalidate' 
            : 'public, max-age=31536000',
          'X-Content-Type-Options': 'nosniff',
          'X-Frame-Options': 'DENY',
          'X-XSS-Protection': '1; mode=block',
          'Referrer-Policy': 'strict-origin-when-cross-origin'
        }
      });
      
      return response;
    }
    
    // If asset not found and it's not a file request, serve index.html for SPA routing
    if (!assetPath.includes('.')) {
      const indexAsset = await env.ASSETS.fetch('http://placeholder/index.html');
      
      if (indexAsset.ok) {
        return new Response(indexAsset.body, {
          status: 200,
          headers: {
            'Content-Type': 'text/html; charset=utf-8',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'strict-origin-when-cross-origin'
          }
        });
      }
    }
    
    // Return 404 for missing assets
    return new Response('Not Found', { 
      status: 404,
      headers: {
        'Content-Type': 'text/plain'
      }
    });
    
  } catch (error) {
    console.error('Worker error:', error);
    return new Response('Internal Server Error', { 
      status: 500,
      headers: {
        'Content-Type': 'text/plain'
      }
    });
  }
}

// Export the fetch handler
export default {
  async fetch(request, env, ctx) {
    return handleRequest(request, env);
  }
};