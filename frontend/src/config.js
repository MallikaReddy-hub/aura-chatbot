/**
 * Central API configuration
 * In development, Vite proxies '/api' to 'http://127.0.0.1:8000'
 * In production, when served by FastAPI or reverse proxy, relative '/api' is used by default.
 * If frontend is deployed separately (e.g., Vercel), VITE_API_BASE_URL can be set to the backend URL.
 */
export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/+$/, '');
