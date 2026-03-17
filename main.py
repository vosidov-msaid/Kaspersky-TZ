import uvicorn
from fastapi import FastAPI, Request, status, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.post("/public/report/export")
def upload_file(file: UploadFile):
    if file.content_type != "text/plain":
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content=jsonable_encoder({"detail": "Invalid file: send .txt file"})
        )
    return {"filename": file.filename, "content_type": file.content_type}

    

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)