import React, { useEffect, useState } from 'react';
import { FileText, Trash2, Eye } from 'lucide-react';
import { Button, Card, CardContent, CardHeader, CardTitle } from './ui';
import { documentsApi } from '../lib/api';
import { formatFileSize, getStatusColor, getDocumentTypeLabel } from '../lib/utils';
import type { Document } from '../types';

export const DocumentList: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const docs = await documentsApi.list();
      setDocuments(docs);
    } catch (error) {
      console.error('Failed to load documents:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this document?')) {
      return;
    }

    try {
      await documentsApi.delete(id.toString());
      setDocuments(docs => docs.filter(doc => doc.id !== id));
    } catch (error) {
      console.error('Failed to delete document:', error);
      alert('Failed to delete document. Please try again.');
    }
  };

  if (loading) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="text-center text-gray-500">Loading documents...</div>
        </CardContent>
      </Card>
    );
  }

  if (documents.length === 0) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="text-center text-gray-500">
            No documents uploaded yet. Upload your first tax document to get started.
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Uploaded Documents</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {documents.map((document) => (
            <div
              key={document.id}
              className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
            >
              <div className="flex items-center space-x-3">
                <FileText size={20} className="text-gray-500" />
                <div>
                  <div className="font-medium">{document.original_filename}</div>
                  <div className="text-sm text-gray-500">
                    {formatFileSize(document.file_size)} • {' '}
                    {document.document_type && getDocumentTypeLabel(document.document_type)}
                  </div>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <span
                  className={`px-2 py-1 text-xs rounded-full ${getStatusColor(document.status)}`}
                >
                  {document.status.charAt(0).toUpperCase() + document.status.slice(1)}
                </span>
                
                <div className="flex space-x-1">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => {
                      // In a real app, this would open a modal with document details
                      alert(`Document: ${document.original_filename}\nStatus: ${document.status}\nType: ${document.document_type || 'Unknown'}`);
                    }}
                  >
                    <Eye size={16} />
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDelete(document.id)}
                    className="text-red-600 hover:text-red-700"
                  >
                    <Trash2 size={16} />
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};