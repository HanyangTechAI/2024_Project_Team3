import React from "react";
import "../styles/UploadedFiles.css";

function UploadedFiles({ files, onRemove }) {
  // files 배열이 비어있으면 렌더링하지 않음
  if (!files || files.length === 0) {
    return null;
  }

  return (
    <div className="uploaded-files">
      <h3>Uploaded Files</h3>
      <div className="file-list">
        {files.map((file, index) => (
          <div key={index} className="file-card">
            <span className="file-name">{file.name}</span>
            <button className="remove-btn" onClick={() => onRemove(file.name)}>
              ✖
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default UploadedFiles;
