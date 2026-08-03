from fastapi import UploadFile, Form, APIRouter
from app.api.deps import SessionDep, CurrentUser
from app.models import DocumentPublic, Document, ExtractionStatus
from app.core.config import settings
from pathlib import Path
import os
import shutil
import uuid


router = APIRouter(prefix="/documents", tags=["documents"])


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


