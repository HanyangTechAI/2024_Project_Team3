import React, { useState } from "react";

function ApiRequestHandler({ files }) {
  const [response, setResponse] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const flaskBackendUrl = "http://localhost:5000"; // Flask 백엔드 URL

  const handleApiRequest = async () => {
    if (files.length === 0) {
      alert("No files to upload.");
      return;
    }

    const formData = new FormData();
    files.forEach((file) => {
      formData.append("files", file);
    });

    try {
      const res = await fetch(`${flaskBackendUrl}/api/upload`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResponse(data);

      // PDF의 첫 번째 파일에서 result_image URL 추출
      const pdfResult = data.find((result) => result.type === "pdf" && result.success);
      if (pdfResult && pdfResult.result_image) {
        setImageUrl(pdfResult.result_image); // 이미지 URL 설정
      }
    } catch (error) {
      console.error("API request failed:", error);
      alert("Failed to send files to the server.");
    }
  };

  return (
    <div className="api-request-handler">
      <button onClick={handleApiRequest}>Submit Files to API</button>
      {response && (
        <div className="api-response">
          <h4>API Response:</h4>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
      {imageUrl && (
        <div className="result-image">
          <h4>Generated Image:</h4>
          <img src={imageUrl} alt="Generated Result" style={{ maxWidth: "100%" }} />
        </div>
      )}
    </div>
  );
}

export default ApiRequestHandler;
