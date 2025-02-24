from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# CORS Middleware (Consider restricting origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific frontend IP/domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Model
class CalculationRequest(BaseModel):
    num1: float
    num2: float
    operation: str

@app.post("/calculate")
async def calculate(request: CalculationRequest):
    """Perform basic arithmetic operations based on user input."""
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
        
        return JSONResponse(content={"result": result}, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
