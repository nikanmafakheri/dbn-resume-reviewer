import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 3000,
    // Dev proxy: the frontend calls a relative `/api/v1` (same-origin, like
    // prod on Vercel where vercel.json rewrites `/api/*` to the backend).
    // During local dev, forward those calls to the FastAPI backend on 8000 so
    // the browser never needs CORS or a hardcoded absolute URL.
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
  css: {
    postcss: {},
  },
})
