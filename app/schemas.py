# Import BaseModel to create data model
from pydantic import BaseModel, Field

# Create a Product model to define the structure of product data
class Product(BaseModel):
    # Define fields with validation rules using Field
    ProductID: int = Field(..., gt=0)
    Name: str = Field(..., min_length=1)
    UnitPrice: float = Field(..., gt=0)
    StockQuantity: int = Field(..., ge=0)
    Description: str = Field(..., min_length=1)