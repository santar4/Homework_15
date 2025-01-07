import os
from datetime import datetime
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException, UploadFile, File, Query, status, BackgroundTasks
import uvicorn

from tools import save_image, optimaze_image

app = FastAPI(docs_url="/",
              title="Santar4 Art Gallery and File Upload API",
              description="API для завантаження, зберігання та обробки художніх творів, а також файлів.",
              )

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
UPLOAD_FILE_DIR = "./upload_files"
Max_file_size = 20 * 1024 * 1024


@app.post("/file/upload")
async def upload_files(file: UploadFile = File(..., description="Upload your files")):
    os.makedirs(UPLOAD_FILE_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_FILE_DIR, file.filename)

    file_content = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(file_content)

    with open(file_path, "a") as buffer:
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        buffer.write(f"file uploaded on: {current_date}")

    return {"file": file, "info": f'{file.filename} uploaded at {current_date}'}


@app.get("/file/download")
def download_file(filename: str = Query(..., description="Enter filename to download him")):
    file_path = os.path.join(UPLOAD_FILE_DIR, filename)
    new_filename = f"santar4{filename}"
    return FileResponse(path=file_path,
                        filename=new_filename,
                        media_type='multipart/form-data')


@app.post("/image/upload")
async def upload_image(background_tasks: BackgroundTasks,
                       files: list[UploadFile] = File(..., description="upload your image")):
    saved_files = []

    for file in files:

        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size > Max_file_size:
            raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File size is too large")

        extension = file.filename.rsplit(".", 1)[-1].lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Unknown file type")

        saved_path = await save_image(file)
        saved_files.append(saved_path)

        background_tasks.add_task(optimaze_image, saved_path)

    return {"detail": "Файли завантажено", "files": saved_files}


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)
