from app.models import (DocumentPublic, Document, ExtractionStatus, DocumentsPublic, Filter)
from fastapi import UploadFile, Form, APIRouter, HTTPException, Query
from app.api.deps import SessionDep, CurrentUser
from fastapi.responses import FileResponse
from sqlmodel import select, func, col
from app.core.config import settings
from typing import Annotated
from pathlib import Path
import shutil
import uuid
import os


router = APIRouter(prefix="/documents", tags=["documents"])
upload_router = APIRouter(prefix="/uploads", tags=["uploads"])

Filters = Annotated[Filter, Query()]


@router.post("/", response_model=DocumentPublic, status_code=201)
def create_document(
    session: SessionDep, 
    current_user: CurrentUser, 
    file: UploadFile,
    ) -> DocumentPublic:
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    filepath = Path(__file__).parent.parent.parent.parent/f"{settings.UPLOAD_DIR}/{filename}"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with filepath.open("wb") as out:
        shutil.copyfileobj(file.file, out)

    file_url = f"{settings.API_V1_STR}/{settings.UPLOAD_DIR}/{filename}"

    document = Document(file_url=file_url, 
                        user_id=current_user.id,
                        )

    session.add(document)
    session.commit()
    session.refresh(document)
    return document


@router.get("/", response_model=DocumentsPublic)
def read_documents(session: SessionDep, current_user: CurrentUser, filters: Filters) -> DocumentsPublic:
    count = session.exec(select(func.count()).select_from(Document).where(Document.user_id == current_user.id)).one()
    statement = select(Document).order_by(col(Document.uploaded_at).desc()).offset(
         filters.skip).limit(filters.limit).where(Document.user_id == current_user.id)
    document = session.exec(statement=statement).all()
    docs = [DocumentPublic.model_validate(doc) for doc in document]
    documents = DocumentsPublic(data=docs, count=count)

    return documents


@upload_router.get("/{filename}")
def read_document(session: SessionDep, current_user: CurrentUser, filename: str) -> FileResponse:
    upload_dir = (Path(__file__).parent.parent.parent.parent/settings.UPLOAD_DIR).resolve()
    file_path = (upload_dir/filename).resolve()

    if not file_path.is_relative_to(upload_dir):
        raise HTTPException(status_code=404, detail="Invalid file path")
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    file_url = f"{settings.API_V1_STR}/{settings.UPLOAD_DIR}/{filename}"
    file = session.exec(select(Document).where(Document.file_url == file_url
                                               ).where(Document.user_id == current_user.id)).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found on the server")
    return FileResponse(path=file_path)

