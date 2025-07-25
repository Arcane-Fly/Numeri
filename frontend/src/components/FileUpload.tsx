import React, { useCallback, useState } from 'react';
import { Upload, File, X } from 'lucide-react';
import { Button } from './ui';
import { documentsApi } from '../lib/api';
import { formatFileSize } from '../lib/utils';
import type { Document as DocumentType } from '../types';

interface FileUploadProps {
  onUploadComplete?: (document: DocumentType) => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onUploadComplete }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      setSelectedFile(files[0]);
    }
  }, []);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      setSelectedFile(files[0]);
    }
  }, []);

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    try {
      // Create FileList from single file
      const fileList = new DataTransfer();
      fileList.items.add(selectedFile);
      const documents = await documentsApi.upload(fileList.files);
      setSelectedFile(null);
      onUploadComplete?.(documents[0]);
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const removeSelectedFile = () => {
    setSelectedFile(null);
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div
        className={`
          border-2 border-dashed rounded-lg p-6 text-center transition-colors
          ${isDragOver ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}
          ${selectedFile ? 'bg-gray-50' : ''}
        `}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {selectedFile ? (
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-white rounded border">
              <div className="flex items-center space-x-2">
                <File size={16} className="text-gray-500" />
                <div className="text-left">
                  <div className="text-sm font-medium">{selectedFile.name}</div>
                  <div className="text-xs text-gray-500">
                    {formatFileSize(selectedFile.size)}
                  </div>
                </div>
              </div>
              <button
                onClick={removeSelectedFile}
                className="text-gray-400 hover:text-gray-600"
              >
                <X size={16} />
              </button>
            </div>
            
            <div className="flex space-x-2">
              <Button
                onClick={handleUpload}
                disabled={uploading}
                className="flex-1"
              >
                {uploading ? 'Uploading...' : 'Upload Document'}
              </Button>
              <Button
                variant="outline"
                onClick={removeSelectedFile}
                disabled={uploading}
              >
                Cancel
              </Button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <Upload size={48} className="mx-auto text-gray-400" />
            <div>
              <h3 className="text-lg font-medium">Upload Tax Documents</h3>
              <p className="text-gray-600">
                Drag and drop your tax documents here, or click to select files
              </p>
              <p className="text-sm text-gray-500 mt-2">
                Supports PDF, PNG, JPG files up to 10MB
              </p>
            </div>
            
            <input
              type="file"
              accept=".pdf,.png,.jpg,.jpeg"
              onChange={handleFileSelect}
              className="hidden"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="cursor-pointer inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 h-10 py-2 px-4">
              Select Files
            </label>
          </div>
        )}
      </div>
    </div>
  );
};