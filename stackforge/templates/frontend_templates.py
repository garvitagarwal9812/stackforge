"""
Frontend source code templates for React 18 + Vite, Next.js 14, Vue 3, and SvelteKit.
"""
from typing import Dict
from stackforge.core.config import StackConfig

def get_frontend_files(config: StackConfig) -> Dict[str, str]:
    files = {}
    frontend = config.frontend
    name = config.project_name
    backend = config.backend

    if frontend == "none":
        return files

    if frontend == "react_vite":
        files["frontend/package.json"] = f"""{{
  "name": "{name}-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx"
  }},
  "dependencies": {{
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "lucide-react": "^0.446.0",
    "axios": "^1.7.7"
  }},
  "devDependencies": {{
    "@types/react": "^18.3.9",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.1",
    "typescript": "^5.6.2",
    "vite": "^5.4.8"
  }}
}}
"""
        files["frontend/vite.config.ts"] = """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true
  }
});
"""
        files["frontend/tsconfig.json"] = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}
"""
        files["frontend/index.html"] = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{name} - StackForge</title>
  </head>
  <body style="margin: 0; background: #0b0f19; color: #f3f4f6; font-family: system-ui, -apple-system, sans-serif;">
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""
        files["frontend/src/main.tsx"] = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './App.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
"""
        files["frontend/src/App.css"] = """
:root {
  --primary: #6366f1;
  --bg-dark: #0b0f19;
  --card-bg: rgba(255, 255, 255, 0.05);
  --border: rgba(255, 255, 255, 0.1);
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 3rem 1.5rem;
}

.hero {
  text-align: center;
  margin-bottom: 3rem;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: rgba(99, 102, 241, 0.2);
  color: #818cf8;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.title {
  font-size: 2.75rem;
  font-weight: 800;
  background: linear-gradient(to right, #818cf8, #c084fc, #38bdf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0.5rem 0;
}

.subtitle {
  color: #9ca3af;
  font-size: 1.125rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  padding: 1.5rem;
  backdrop-filter: blur(8px);
  transition: transform 0.2s ease, border-color 0.2s ease;
}

.card:hover {
  transform: translateY(-4px);
  border-color: #6366f1;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.6rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-healthy {
  background: rgba(34, 197, 94, 0.15);
  color: #4ade80;
}
"""
        files["frontend/src/App.tsx"] = f"""import React, {{ useEffect, useState }} from 'react';

export default function App() {{
  const [health, setHealth] = useState<string>('checking...');
  const [dbStatus, setDbStatus] = useState<string>('{config.database}');

  useEffect(() => {{
    fetch('/health')
      .then(res => res.json())
      .then(data => setHealth(data.status || 'online'))
      .catch(() => setHealth('offline (start backend)'));
  }}, []);

  return (
    <div className="container">
      <div className="hero">
        <div className="badge">🚀 StackForge Architecture</div>
        <h1 className="title">{name}</h1>
        <p className="subtitle">{config.project_description}</p>
        <div style={{{{ marginTop: '1rem' }}}}>
          <span className="status-pill status-healthy">
            ● Backend Status: {{health}}
          </span>
        </div>
      </div>

      <div className="grid">
        <div className="card">
          <h3>⚡ Backend Engine</h3>
          <p style={{{{ color: '#9ca3af' }}}}>{config.backend.upper()} API service configured with healthchecks, CORS & modular routing.</p>
        </div>
        <div className="card">
          <h3>🗄️ Database</h3>
          <p style={{{{ color: '#9ca3af' }}}}>{config.database.upper()} persistent layer with Docker Compose initialization.</p>
        </div>
        <div className="card">
          <h3>🛠️ CI/CD Pipeline</h3>
          <p style={{{{ color: '#9ca3af' }}}}>{config.pipeline.replace('_', ' ').upper()} workflow configured with automated testing and container publishing.</p>
        </div>
        <div className="card">
          <h3>📦 DevOps & K8s</h3>
          <p style={{{{ color: '#9ca3af' }}}}>Multi-stage Dockerfile and Kubernetes manifests ready for cluster deployment.</p>
        </div>
      </div>
    </div>
  );
}}
"""
        files["frontend/Dockerfile"] = """FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""

    elif frontend == "nextjs":
        files["frontend/package.json"] = f"""{{
  "name": "{name}-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {{
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  }},
  "dependencies": {{
    "next": "14.2.13",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "lucide-react": "^0.446.0"
  }},
  "devDependencies": {{
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "typescript": "^5"
  }}
}}
"""
        files["frontend/next.config.js"] = """/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
};

module.exports = nextConfig;
"""
        files["frontend/src/app/layout.tsx"] = """import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Next.js App - StackForge",
  description: "Enterprise fullstack application scaffolded with StackForge",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body style={{ margin: 0, background: "#0b0f19", color: "#f3f4f6", fontFamily: "sans-serif" }}>
        {children}
      </body>
    </html>
  );
}
"""
        files["frontend/src/app/page.tsx"] = f"""export default function Home() {{
  return (
    <main style={{{{ padding: '3rem', maxWidth: '800px', margin: '0 auto', textAlign: 'center' }}}}>
      <h1 style={{{{ fontSize: '2.5rem', color: '#818cf8' }}}}>{name}</h1>
      <p style={{{{ color: '#9ca3af' }}}}>Next.js 14 App Router + Cloud Native DevOps Architecture</p>
      <div style={{{{ marginTop: '2rem', padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}}}>
        <h3>🚀 CI/CD Pipeline: {config.pipeline}</h3>
        <p>Pre-configured with Docker multi-stage builds and automated workflows.</p>
      </div>
    </main>
  );
}}
"""
        files["frontend/Dockerfile"] = """FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
ENV PORT 3000
CMD ["node", "server.js"]
"""

    return files
