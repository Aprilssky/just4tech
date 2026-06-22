# Just4Tech — AI Tool Hub

Full-stack blog and content platform at [just4.tech](https://just4.tech).

## Structure

```
├── frontend/     # Vue 3 SPA (Vite)
│   └── src/
│       ├── views/        # Page components
│       │   ├── Blog.vue
│       │   ├── BlogPost.vue
│       │   ├── Home.vue
│       │   ├── Software.vue (AI Tools)
│       │   ├── Projects.vue
│       │   ├── IndieDevs.vue
│       │   ├── Sites.vue
│       │   ├── Tutorials.vue
│       │   └── admin/    # Admin dashboard
│       ├── components/   # Shared components
│       ├── api/          # API helpers
│       └── utils/        # Meta, SEO utilities
└── backend/     # Python FastAPI (port 8083)
    ├── main.py       # API server
    └── database.py   # SQLite schema + connection
```

## Tech Stack

- **Frontend:** Vue 3, Vue Router, Tailwind CSS, Vite, marked (Markdown), highlight.js
- **Backend:** Python 3, FastAPI, SQLite
- **Server:** Nginx reverse proxy → FastAPI + static SPA
- **CI/CD:** GitHub Actions → auto-deploy on push to `main`

## Deployment

Push to `main` triggers GitHub Actions:
1. **Frontend:** `npm ci` → `npm run build` → rsync to `/var/www/aitoolhub/spa/`
2. **Backend:** rsync `.py` files → `systemctl restart aitoolhub-admin`

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/posts` | Public | List active posts |
| GET | `/api/posts/{id}` | Public | Get post by ID |
| GET | `/api/posts/slug/{slug}` | Public | Get post by slug |
| POST | `/api/posts` | API Key | Create post |
| PUT | `/api/posts/{id}` | API Key | Update post (partial) |
| PUT | `/api/posts/slug/{slug}` | API Key | Update post by slug (partial) |
| DELETE | `/api/posts/{id}` | Session | Delete post |
| GET | `/api/software` | Public | AI Tools list |
| GET | `/api/projects` | Public | Projects list |
| GET | `/rss.xml` | Public | RSS feed |
| POST | `/api/admin/upload` | Session | Upload media |

## Secrets (GitHub Actions)

| Secret | Description |
|--------|-------------|
| `SSH_PRIVATE_KEY` | SSH key for server access |
| `DEPLOY_HOST` | Server IP/hostname |
| `DEPLOY_USER` | Server user (ubuntu) |
