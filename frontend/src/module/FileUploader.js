import React from 'react';

function FileUploader({ fileType, label, onUpload }) {
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onUpload();
    }
  };

  return (
    <div className="file-uploader">
      <label className="file-label">
        <img
          src={
            fileType === "image"
              ? "https://cdn-icons-png.flaticon.com/512/2948/2948035.png"
              : "https://cdn-icons-png.flaticon.com/512/3342/3342137.png"
          }
          alt={label}
          className="file-icon"
        />
        <input
          type="file"
          accept={fileType === "image" ? "image/*" : ".pdf"}
          onChange={handleFileChange}
          className="file-input"
        />
      </label>
    </div>
  );
}

export default FileUploader;
