from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI()

# CORS Middleware (Modify for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client.calculator  # Database name
history_collection = db.history  # Collection name

# Request Model
class CalculationRequest(BaseModel):
    num1: float
    num2: float
    operation: str

@app.post("/calculate")
async def calculate(request: CalculationRequest):
    """Perform basic arithmetic and save history to MongoDB."""
    try:
        if request.operation == "add":
            result = request.num1 + request.num2
        elif request.operation == "subtract":
            result = request.num1 - request.num2
        elif request.operation == "multiply":
            result = request.num1 * request.num2
        elif request.operation == "divide":
            if request.num2 == 0:
                raise HTTPException(status_code=400, detail="Cannot divide by zero")
            result = request.num1 / request.num2
        else:
            raise HTTPException(status_code=400, detail="Invalid operation")
        
        # Save to MongoDB
        calculation_data = {
            "num1": request.num1,
            "num2": request.num2,
            "operation": request.operation,
            "result": result
        }
        await history_collection.insert_one(calculation_data)

        return JSONResponse(content={"result": result}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/history")
async def get_history():
    """Retrieve calculation history from MongoDB."""
    history = await history_collection.find().to_list(100)  # Get last 100 records
    return {"history": history}
