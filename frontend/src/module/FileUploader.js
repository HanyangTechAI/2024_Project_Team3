import React from "react";
import "../styles/FileUploader.css"; // 스타일 파일 추가

function FileUploader({ fileType, label, onUpload }) {
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      onUpload(file);
    }
  };

  return (
    <div className="file-uploader">
      <label className="file-label">
        <div className={`file-button ${fileType}`}>
          <img
            src={
              fileType === "image"
                ? "https://cdn-icons-png.flaticon.com/512/3342/3342137.png"
                : "https://cdn-icons-png.flaticon.com/512/136/136440.png"
            }
            alt={label}
            className="file-icon"
          />
          <span className="file-label-text">{label}</span>
        </div>
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
