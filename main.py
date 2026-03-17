import os
import shutil
import random
import datetime
import uvicorn
from fastapi import FastAPI, Request, HTTPException, status, File, UploadFile

app = FastAPI()
@app.post("/public/report/export")
def upload_file(file: UploadFile):
    if file.content_type != "text/plain":
        raise HTTPException(422, {"detail": "Invalid file: send .txt file"})
    
    rand_file = random.randint(1, 1000000)

    path_name = f"files/{rand_file}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    os.makedirs(path_name, exist_ok=True)
    file_path = f"{path_name}/{rand_file}_{file.filename}"
    with open(file_path, "wb+") as file_content:
        shutil.copyfileobj(file.file, file_content)
    return {"filename": file.filename, "content_type": file.content_type, "file_path": file_path}

    

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)