"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Example schemas (retain for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: Optional[str] = Field(None, description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# --------------------------------------------------
# Portfolio app schemas

class Project(BaseModel):
    """
    Portfolio projects
    Collection name: "project"
    """
    title: str
    category: str = Field(..., description="Home | Office | Furniture | Decor")
    description: Optional[str] = None
    images: List[str] = Field(default_factory=list, description="Array of image URLs")
    featured: bool = Field(default=False)

class Testimonial(BaseModel):
    """
    Client testimonials
    Collection name: "testimonial"
    """
    client_name: str
    project_type: str
    quote: str
    avatar: Optional[str] = None
    rating: Optional[int] = Field(default=5, ge=1, le=5)

class Inquiry(BaseModel):
    """
    Contact/consultation inquiries
    Collection name: "inquiry"
    """
    name: str
    email: EmailStr
    phone: Optional[str] = None
    project_type: Optional[str] = None
    message: Optional[str] = None
    source: Optional[str] = Field(default="website")
