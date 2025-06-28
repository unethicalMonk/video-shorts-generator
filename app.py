import os
import uuid
from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from clipper import generate_clips
import zipfile

app = FastAPI()

# Serve the static frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_form():
    with open("static/index.html") as f:
        return f.read()


@app.post("/upload/")
async def upload_video(
    file: UploadFile,
    num_clips: int = Form(...),
    min_dur: float = Form(...),
    max_dur: float = Form(...)
):
    # Save uploaded video
    input_filename = f"uploads/{uuid.uuid4()}.mp4"
    with open(input_filename, "wb") as f:
        f.write(await file.read())

    # Create unique output directory
    clip_folder = f"clips/{uuid.uuid4().hex}"
    os.makedirs(clip_folder, exist_ok=True)

    # Generate clips
    clip_paths = generate_clips(input_filename, num_clips, min_dur, max_dur, clip_folder)

    # Create zip file
    zip_path = f"{clip_folder}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for clip in clip_paths:
            zipf.write(clip, os.path.basename(clip))

    return FileResponse(zip_path, media_type="application/zip", filename="clips.zip")
