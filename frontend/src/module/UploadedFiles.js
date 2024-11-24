import React from 'react';

function UploadedFiles({ files, onRemove }) {
  return (
    <div className="uploaded-files">
      <ul>
        {files.map((file, index) => (
          <li key={index} className="uploaded-file-item">
            <span>{file.name}</span>
            <button onClick={() => onRemove(file.name)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UploadedFiles;
