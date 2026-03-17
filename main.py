import os
import shutil
import random
import datetime
import uvicorn
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse

from word_morphy import get_morphological_info
from export_excel import export_to_excel

app = FastAPI()
@app.post("/public/report/export")
async def upload_file(file: UploadFile):
    if file.content_type != "text/plain":
        raise HTTPException(422, {"detail": "Invalid file: send .txt file"})
    
    rand_file = random.randint(1, 1000000)

    path_name = f"files/{rand_file}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    os.makedirs(path_name, exist_ok=True)
    file_path = f"{path_name}/{rand_file}_{file.filename}"

    contents = await file.read()
    text = contents.decode("utf-8")

    export_path = f"{path_name}/morphological_info.xlsx"

    morphological_info = get_morphological_info(text)
    export_to_excel(morphological_info, export_path)

    with open(file_path, "wb+") as file_content:
        shutil.copyfileobj(file.file, file_content)
    
    return FileResponse(
        path=export_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="morphological_info.xlsx",
    )
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)