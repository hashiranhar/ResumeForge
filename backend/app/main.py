from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, cvs, templates, llm, pdf, subscription

app = FastAPI(
    title="ResumeForge API",
    description="Professional CV builder with Markdown editor and AI assistance",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Whatever Svelte dev server will be 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(cvs.router)
app.include_router(templates.router)
app.include_router(llm.router)
app.include_router(pdf.router)
app.include_router(subscription.router)  

@app.get("/")
def root():
    return {"message": "ResumeForge API is running"}