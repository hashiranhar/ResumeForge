# ResumeForge 🔨

Professional CV builder with Markdown editor, real-time PDF preview, and AI-powered editing assistant.

## 🚀 Quick Overview

ResumeForge is a modern web application that lets users create professional CVs using Markdown. It features real-time PDF preview, AI assistance, and professional customization options.

**Live Demo**: Try the editor without registration at `/editor?demo=true`

## ✨ Key Features

### Core CV Building
- **Markdown Editor** with syntax highlighting and special formatting (`[CENTER]`, `[DATE: content]`)
- **Real-time PDF Preview** with professional styling
- **Professional Templates** for different industries
- **Export Options** (PDF/Markdown) with custom styling

### AI-Powered Tools
- **Chat Assistant** - Get conversational advice about your CV
- **Inline Editor** - Make instant AI-powered improvements
- **ATS Score Analysis** - Optimize for Applicant Tracking Systems

### Customization
- Multiple fonts, themes, and sizing options
- Dark/light mode support
- Responsive design with resizable panels
- Professional color schemes

## 🛠️ Tech Stack

**Backend**: FastAPI + PostgreSQL + JWT Auth + WeasyPrint + Hugging Face AI  
**Frontend**: SvelteKit + TypeScript + Tailwind CSS + Vite  
**AI**: DeepSeek-V3 model via Hugging Face API

## 📁 Project Structure

```
ResumeForge/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── core/      # Config & security
│   │   ├── models/    # Database models
│   │   ├── routers/   # API endpoints
│   │   └── services/  # Business logic
│   └── alembic/       # DB migrations
├── frontend/          # SvelteKit application
│   └── src/
│       ├── lib/       # Components & stores
│       └── routes/    # Pages
└── requirements.txt   # Dependencies
```

## 🚀 Quick Start

### 1. Backend Setup
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r ../requirements.txt

# Create .env file
echo "DATABASE_URL=postgresql://user:pass@localhost/resumeforge
SECRET_KEY=your-secret-key
HUGGINGFACE_API_KEY=your-api-key" > ../.env

# Setup database
alembic upgrade head
python scripts/seed_templates.py

# Start server
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

**Access**: http://localhost:3000 (Frontend) | http://localhost:8000/docs (API)

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### CV Management
- `GET /api/cvs/` - List CVs
- `POST /api/cvs/` - Create CV
- `PUT /api/cvs/{id}` - Update CV
- `GET /api/cvs/{id}/pdf` - Download PDF

### AI Features
- `POST /api/llm/chat` - Chat about CV
- `POST /api/llm/inline-edit` - AI editing
- `POST /api/llm/ats-score` - ATS analysis

## 📝 Special Markdown Features

```markdown
# John Doe
**Software Engineer** [CENTER]

📧 email@example.com [CENTER]

## Experience
### Senior Developer | Company [DATE: 2022 - Present]
- Led team of 5 developers
- Improved performance by 40%
```

## 🔧 Development

```bash
# Run migrations
alembic revision --autogenerate -m "description"
alembic upgrade head

# Frontend linting
npm run lint && npm run format

# Tests
npm run test
```

## 🌟 Production Setup

### Required Environment Variables
```env
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=production-secret-key
HUGGINGFACE_API_KEY=your-api-key
ENVIRONMENT=production
```

### Security Features
- JWT authentication with bcrypt password hashing
- SQL injection protection via SQLAlchemy ORM
- XSS protection with DOMPurify sanitization
- CORS configuration for secure cross-origin requests

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**ResumeForge** - Building careers, one CV at a time. 🚀
