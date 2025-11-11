from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import Project, Testimonial, Inquiry

app = FastAPI(title="Designer Portfolio API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
def test():
    # Verify DB connectivity
    try:
        status = "connected" if db is not None else "disconnected"
        collections = []
        if db is not None:
            collections = db.list_collection_names()
        return {"status": "ok", "database": status, "collections": collections}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Seed demo content if DB is available (safe, idempotent-like: read only on GET)
@app.get("/projects", response_model=List[Project])
def list_projects(category: Optional[str] = None, featured: Optional[bool] = None, limit: int = 50):
    if db is None:
        # Fallback demo content (non-persistent)
        demo = [
            Project(title="Warm Minimalist Living Room", category="Home", description="Textured neutrals, soft woods, and diffused light.", images=[
                "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?q=80&w=1600&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1493666438817-866a91353ca9?q=80&w=1600&auto=format&fit=crop"
            ], featured=True),
            Project(title="Contemporary Workspace", category="Office", description="Focus-first layout with acoustic elements.", images=[
                "https://images.unsplash.com/photo-1507209696998-3c532be9b2b3?q=80&w=1600&auto=format&fit=crop"
            ], featured=False),
            Project(title="Handcrafted Oak Dining Table", category="Furniture", description="Bespoke live-edge table in matte oil finish.", images=[
                "https://images.unsplash.com/photo-1600585154526-990dced4db0d?q=80&w=1600&auto=format&fit=crop"
            ], featured=True),
        ]
        return demo

    filter_dict = {}
    if category:
        filter_dict["category"] = category
    if featured is not None:
        filter_dict["featured"] = featured
    docs = get_documents("project", filter_dict, limit)
    # Convert Mongo docs to Pydantic
    projects: List[Project] = []
    for d in docs:
        projects.append(Project(
            title=d.get("title", ""),
            category=d.get("category", "Home"),
            description=d.get("description"),
            images=d.get("images", []),
            featured=d.get("featured", False)
        ))
    return projects


@app.get("/testimonials", response_model=List[Testimonial])
def list_testimonials(limit: int = 20):
    if db is None:
        demo = [
            Testimonial(client_name="Aarav K.", project_type="Home", quote="The space feels like us. Thoughtful, warm, and so well crafted.", rating=5),
            Testimonial(client_name="Meera S.", project_type="Office", quote="Professional process and stunning results.", rating=5),
        ]
        return demo

    docs = get_documents("testimonial", {}, limit)
    items: List[Testimonial] = []
    for d in docs:
        items.append(Testimonial(
            client_name=d.get("client_name", ""),
            project_type=d.get("project_type", ""),
            quote=d.get("quote", ""),
            avatar=d.get("avatar"),
            rating=d.get("rating", 5),
        ))
    return items


@app.post("/inquiry")
def create_inquiry(payload: Inquiry):
    try:
        if db is None:
            # Accept without persistence to keep form functional
            return {"status": "received", "data": payload.model_dump()}
        doc_id = create_document("inquiry", payload)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
