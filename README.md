# Resume Tailoring

An AI-powered resume tailoring web app. Paste a job description, and GPT rewrites your resume to match — then generates a clean PDF via LaTeX.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS, shadcn/ui |
| Backend | Python, Flask, OpenAI GPT, Jinja2 |
| PDF Generation | LaTeX (pdflatex / texlive) |
| Deployment | Docker, Nginx, Render |

## Project Structure

```
Resume-Tailoring/
├── my-resume-app/        # React frontend
├── my-resume-backend/    # Flask backend
├── push-frontend.sh      # Deploy frontend to Docker Hub + Render
└── push-backend.sh       # Deploy backend via git subtree to Render
```

## Local Development

### Prerequisites
- Node.js 18+
- Python 3.11+
- LaTeX — [MiKTeX](https://miktex.org/) (Windows) or `texlive-full` (Linux/Mac)

### 1. Clone the repo

```bash
git clone https://github.com/Tristesse02/Resume-Tailoring.git
cd Resume-Tailoring
```

### 2. Set up environment variables

**Frontend** (`my-resume-app/.env`):
```
VITE_API_URL=http://localhost:5000
VITE_DEV_SECRET=your_dev_secret
```

**Backend** (`my-resume-backend/.env`):
```
OPENAI_API_KEY=your_openai_api_key
DEV_SECRET=your_dev_secret
FRONTEND_URL=http://localhost:5173
NETWORK_VISIBILITY=127.0.0.1
LATEX_FONT=pdflatex
```

### 3. Install dependencies

**Frontend:**
```bash
cd my-resume-app
npm install
```

**Backend:**
```bash
cd my-resume-backend
python -m venv venvResumeTailor
source venvResumeTailor/Scripts/activate  # Windows
pip install -r requirements.txt
```

### 4. Run the app

From the `my-resume-app/` directory:
```bash
npm run dev
```
This starts both the frontend (port 5173) and backend (port 5000) concurrently.

## Deployment

The frontend and backend are deployed separately on [Render](https://render.com).

### Frontend

Build the Docker image and push to Docker Hub:

```bash
./push-frontend.sh
```

Then go to your Render dashboard → frontend service → **Manual Deploy**.

### Backend

Push the backend subtree to its GitHub repo (Render auto-deploys on push):

```bash
./push-backend.sh
```

## Environment Variables Reference

| Variable | Location | Description |
|---|---|---|
| `VITE_API_URL` | Frontend | Backend API URL |
| `VITE_DEV_SECRET` | Frontend | Shared secret for dev auth |
| `OPENAI_API_KEY` | Backend | OpenAI API key for GPT |
| `DEV_SECRET` | Backend | Shared secret for dev auth |
| `FRONTEND_URL` | Backend | Frontend URL for CORS |
| `LATEX_FONT` | Backend | LaTeX compiler (`pdflatex`) |
