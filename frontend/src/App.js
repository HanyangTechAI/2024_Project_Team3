import React, { useState } from 'react';
import './App.css';

function App() {
  const [imageSrc, setImageSrc] = useState(null);

  const handleUpload = async (type) => {
    const url = type === 'material' ? '/upload-material' : '/upload-pdf';

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (response.ok) {
        const data = await response.json();
        setImageSrc(data.imageUrl);
      } else {
        console.error('Failed to upload');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="app-container">
      <div className="button-container">
        <button className="upload-button" onClick={() => handleUpload('material')}>교재 업로드</button>
        <button className="upload-button" onClick={() => handleUpload('pdf')}>수업자료 업로드</button>
      </div>
      <div className="image-container">
        {imageSrc ? (
          <img src={imageSrc} alt="Uploaded from server" className="uploaded-image" />
        ) : (
          <p className="placeholder-text">교재와 수업자료 pdf 를 업로드 해주세요</p>
        )}
      </div>
    </div>
  );
}

export default App;
