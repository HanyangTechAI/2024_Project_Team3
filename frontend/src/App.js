import React, { useState } from 'react';
import Header from './module/Header';
import FileUploader from './module/FileUploader';
import StatusMessage from './module/StatusMessage';
import UploadedFiles from './module/UploadedFiles';
import ApiRequestHandler from './module/ApiRequestHandler';
import './styles/styles.css';

function App() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const maxUploads = 3;

  const handleFileUpload = (file) => {
    if (uploadedFiles.length >= maxUploads) {
      alert("You can only upload up to 3 files.");
      return;
    }
    setUploadedFiles((prev) => [...prev, file]);
  };

  const handleFileRemove = (fileName) => {
    setUploadedFiles((prev) => prev.filter((file) => file.name !== fileName));
  };

  return (
    <div className="container">
      <Header title="Welcome" />
      <StatusMessage message="Please upload the image and textbook PDF (Max: 3 files)" />
      <div className="upload-container">
        <FileUploader
          fileType="pdf"
          label="Upload PDF"
          onUpload={handleFileUpload}
        />
        <FileUploader
          fileType="image"
          label="Upload Image"
          onUpload={handleFileUpload}
        />
      </div>
      <UploadedFiles files={uploadedFiles} onRemove={handleFileRemove} />
      <ApiRequestHandler files={uploadedFiles} /> {/* API 요청 컴포넌트 추가 */}
    </div>
  );
}

export default App;
