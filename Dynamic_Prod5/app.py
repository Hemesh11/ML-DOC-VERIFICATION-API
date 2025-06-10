from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
import json
import os
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
import elasticapm

apm_config = {
    'SERVICE_NAME': os.environ.get('ES_SERVICE_NAME_BE'),
    'SECRET_TOKEN': os.environ.get('ES_SECRET_TOKEN'),
    'SERVER_URL': os.environ.get('ES_SERVER_URL'),
    'ENVIRONMENT': 'prod'
}
try:
    apm = make_apm_client(apm_config)
    elasticapm.instrument()
    print("APM client started successfully.")
    print(f"APM config: {apm_config}")
except Exception as e:
    print(f"Error initializing Elastic APM: {e}")
    apm = None


# Initialize FastAPI
app = FastAPI(title="Document Verification System", version="1.0", description="Validate documents in regard of a specific service asked")

if apm:
    app.add_middleware(ElasticAPM, client=apm)
    print("ElasticAPM middleware added.")
else:
    print("APM client was not initialized. ElasticAPM middleware not added.")
# Import our validation API
from api.document_validation_api import DocumentValidationAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_server.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("document-validation-api")

# Initialize the validation service
validation_api = DocumentValidationAPI()

# Create the FastAPI app
app = FastAPI(
    title="Document Validation API",
    description="API for validating director and company documents",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input models
class DocumentInfo(BaseModel):
    """Document URL information"""
    url: str = Field(..., description="Document URL for validation")

class DirectorDocuments(BaseModel):
    """Director's documents"""
    aadharCardFront: str = Field(None, description="Aadhar card front URL")
    aadharCardBack: str = Field(None, description="Aadhar card back URL")
    panCard: str = Field(None, description="PAN card URL")
    passportPhoto: str = Field(None, description="Passport photo URL")
    address_proof: str = Field(None, description="Address proof URL")
    signature: str = Field(None, description="Signature URL")
    passport: str = Field(None, description="Passport URL (for foreign directors)")
    drivingLicense: str = Field(None, description="Driving license URL (for foreign directors)")

class Director(BaseModel):
    """Director information"""
    nationality: str = Field(..., description="Director's nationality (Indian/Foreign)")
    authorised: str = Field(..., description="Whether director is authorised (Yes/No)")
    documents: Dict[str, str] = Field(..., description="Director's documents URLs")

class CompanyDocuments(BaseModel):
    """Company documents"""
    address_proof_type: str = Field(None, description="Type of address proof")
    addressProof: str = Field(..., description="Company address proof URL")
    noc: str = Field(None, description="No Objection Certificate URL")

class ValidationRequest(BaseModel):
    """Document validation request"""
    service_id: str = Field("1", description="Service identifier")
    request_id: str = Field(..., description="Unique request identifier")
    preconditions: Optional[Dict[str, Any]] = Field(None, description="Additional preconditions for validation")
    directors: Dict[str, Director] = Field(..., description="Directors information")
    companyDocuments: CompanyDocuments = Field(..., description="Company documents")

# Define error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc)
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Document validation endpoint
@app.post("/validate", response_model=Dict[str, Any])
async def validate_documents(request: ValidationRequest):
    try:
        logger.info(f"Processing validation request: {request.request_id}")
        
        # Convert Pydantic model to dict
        input_data = request.dict()
        
        # Process validation
        api_response, _ = validation_api.validate_document(input_data)
        
        # Log completion
        logger.info(f"Validation completed for request: {request.request_id}")
        
        return api_response
    
    
    except Exception as e:
        logger.error(f"Error processing validation request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Validation processing error: {str(e)}"
        )
    
# Add this after your existing route definitions
@app.get("/")
async def root():
    return {
        "message": "Document Validation API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "validate": "/validate"
        }
    }
# Run the app
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
