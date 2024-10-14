import io
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, logger
from fastapi.responses import JSONResponse
import pandas as pd
from app.services.detection_service import detect_equipment_events
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
from app.auth.jwt_handler import verify_token

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):

    try:
        if not verify_token(token):
            return JSONResponse(content={"error": "Invalid token"}, status_code=401)
    except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return JSONResponse(content={"error": "Internal server error"}, status_code=500)
    
    
    # Validate the file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    # Read the contents of the file
    contents = await file.read()
    
    # Try reading the CSV into a DataFrame
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Error parsing the CSV file.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Process the DataFrame to detect equipment events
    result_df = detect_equipment_events(df)
    
    # Return the result as a list of dictionaries
    return {"events": result_df.to_dict(orient='records')}
