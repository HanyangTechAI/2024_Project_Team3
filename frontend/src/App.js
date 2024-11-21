import React, { useState } from 'react';
import Header from './module/Header';
import FileUploader from './module/FileUploader';
import StatusMessage from './module/StatusMessage';
import './styles/styles.css';

function App() {
  const [imageUploaded, setImageUploaded] = useState(false);
  const [pdfUploaded, setPdfUploaded] = useState(false);

  // 상태에 따른 메시지 설정
  const getUploadMessage = () => {
    if (!imageUploaded && !pdfUploaded) {
      return "Please upload the image and textbook pdf";
    } else if (imageUploaded && !pdfUploaded) {
      return "Please upload the textbook pdf";
    } else if (!imageUploaded && pdfUploaded) {
      return "Please upload the image";
    } else {
      return "Both image and pdf are uploaded!";
    }
  };

  return (
    <div className="container">
      <Header title="name" />
      <StatusMessage message={getUploadMessage()} />
      <div className="upload-container">
        <FileUploader
          fileType="image"
          label="Upload Image"
          onUpload={() => setImageUploaded(true)}
        />
        <FileUploader
          fileType="pdf"
          label="Upload PDF"
          onUpload={() => setPdfUploaded(true)}
        />
      </div>
    </div>
  );
}

export default App;
