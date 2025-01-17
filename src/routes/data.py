from fastapi import APIRouter, FastAPI, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controller import DataController, ProjectController
import os 
import aiofiles
from models import ResponseSignal
import logging

logger = logging.getLogger('uvicorn.error')


data_router = APIRouter(
    prefix='/api/v1/data',
    tags=['api_v1', 'data']
)

@data_router.post('/upload/{project_id}')
async def upload_data(
    project_id: str,
    file: UploadFile,
    app_settings: Settings = Depends(get_settings)
):
    data_controller = DataController()
    # validate the uploaded file
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal': result_signal
            }
        )
    # print('uploading file')
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    # print(f'project file created: {project_dir_path}')
    file_path, file_id = data_controller.generate_unique_filepath(
        org_filename=file.filename,
        project_id=project_id
    )

    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk:= await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE): 
                await f.write(chunk)
    except Exception as e:
        logger.error(f'Error while uploading file: {e}')
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ResponseSignal.FILE_UPLOAD_FAILED.value
        )

    return JSONResponse(
        content={
            'signal': ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            'file_id': file_id
        }
    )