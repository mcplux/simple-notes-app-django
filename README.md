# Simple Notes App Django

## 🧱 Tech Stack

- [**🐍 Python**](https://www.python.org/) – The language that keeps things readable, powerful, and actually enjoyable to work with.
- [**🌿 Django**](https://www.djangoproject.com/) – Batteries-included backend framework handling auth, ORM, business logic, and all the serious stuff.
- [**⚡ HTMX**](https://htmx.org/) – Server-driven interactivity. Dynamic UI using minimal JS.
- [**🏔 Alpine.js**](https://alpinejs.dev/) – Lightweight frontend reactivity for the small bits of state HTMX doesn’t cover.
- [**🎨 TailwindCSS**](https://tailwindcss.com/) – Utility-first styling without fighting CSS.
- [**🔍 Lucide**](https://lucide.dev/) – Clean, consistent SVG icons.
- [**⚙️ Pydantic Settings**](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) - Type-safe environment configuration.
- [**🐘 PostgreSQL**](https://www.postgresql.org/) – Reliable, production-grade database.
- [**🐳 Docker**](https://docs.docker.com/) - Containerized everything.
- [**📦 Docker Compose**](https://docs.docker.com/compose/) - Orchestrates all services.
- [**🗄 Adminer**](https://www.adminer.org/) – Lightweight database UI for quickly inspecting and managing PostgreSQL without extra setup.

## 🚀 Development Setup

Follow these steps to run the project locally in development mode

1. **Clone Repository**
   ```bash
   git clone git@github.com:mcplux/simple-notes-app-django.git
   cd simple-notes-app-django
   ```
2. **Create your environment file**

   Duplicate the example environment file and update the variables as needed:

   ```bash
   cp .env.example .env
   ```

3. **Start required services (database & adminer)**
   ```bash
   docker compose up db adminer -d
   ```
   This will start:
   - `db`: PostgreSQL database.
   - `adminer`: Database UI Web.
4. **Build the web container**
   ```bash
   docker compose build web
   ```
5. **Apply database migrations**
   ```bash
   docker compose run --rm web ./manage.py migrate
   ```
6. **(Optional, but recommended) Create a superuser**
   ```bash
   docker compose run --rm web ./manage.py createsuperuser
   ```
   And follow instruction, then you will have access to Django admin panel.
7. **Run development server in watch mode**
   ```bash
   docker compose up web --watch
   ```
   Now the application should be running and have useful links (default):
   - **Web application**: http://localhost:8000/
   - **Admin panel**: http://localhost:8000/admin/
   - **Adminer**: http://localhost:8080
8. **You can work in you machine**
   ```bash
   uv sync
   ```

### 🗒️ Useful commands

- **Raise all containers**

  ```bash
  docker compose up -d
  docker compose up --watch web
  ```

- **Stop all containers**
  ```bash
  docker compose down
  ```
- **Rebuild from scratch (if things get weird)**
  ```bash
  docker compose down -v
  docker compose build web --no-cache
  ```
- **Install a new dependency**

  In your host

  ```bash
  uv add <dependency>
  ```
