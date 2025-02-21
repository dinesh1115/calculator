from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific frontend IP in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CalculationRequest(BaseModel):
    num1: float
    num2: float
    operation: str

@app.post("/calculate")  # ✅ MUST be a POST request
async def calculate(request: CalculationRequest):
    if request.operation == "add":
        return {"result": request.num1 + request.num2}
    elif request.operation == "subtract":
        return {"result": request.num1 - request.num2}
    elif request.operation == "multiply":
        return {"result": request.num1 * request.num2}
    elif request.operation == "divide":
        if request.num2 == 0:
            return {"error": "Cannot divide by zero"}
        return {"result": request.num1 / request.num2}
    return {"error": "Invalid operation"}
