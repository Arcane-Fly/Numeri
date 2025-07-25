from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
import shutil

from ..database.database import get_db
from ..models.models import Document, DocumentStatus
from ..schemas.schemas import DocumentResponse
from ..core.document_processor import DocumentProcessor
from ..config import settings

router = APIRouter()
document_processor = DocumentProcessor()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and process a document"""
    
    # Validate file type
    if not any(file.filename.lower().endswith(ext) for ext in settings.allowed_file_types):
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Supported types: {settings.allowed_file_types}"
        )
    
    # Validate file size
    if file.size and file.size > settings.max_file_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.max_file_size / (1024*1024):.1f}MB"
        )
    
    try:
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.upload_directory, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Create database record
        db_document = Document(
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            content_type=file.content_type or "application/octet-stream",
            status=DocumentStatus.PENDING.value
        )
        
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        # Process document asynchronously (in a real app, this would be a background task)
        try:
            db_document.status = DocumentStatus.PROCESSING.value
            db.commit()
            
            # Process the document
            result = document_processor.process_document(
                file_path=file_path,
                content_type=file.content_type or "application/octet-stream",
                filename=file.filename
            )
            
            if result['success']:
                db_document.status = DocumentStatus.COMPLETED.value
                db_document.ocr_text = result['ocr_text']
                db_document.document_type = result['document_type']
                db_document.extracted_data = result['extracted_data']
            else:
                db_document.status = DocumentStatus.ERROR.value
                
            db.commit()
            db.refresh(db_document)
            
        except Exception as e:
            db_document.status = DocumentStatus.ERROR.value
            db.commit()
            raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
        
        return db_document
        
    except Exception as e:
        # Clean up file if database operation fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all uploaded documents"""
    documents = db.query(Document).offset(skip).limit(limit).all()
    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific document by ID"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Delete a document"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file from filesystem
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    # Delete from database
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}