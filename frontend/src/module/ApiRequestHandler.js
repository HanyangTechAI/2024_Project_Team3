import React, { useState } from "react";
import "../styles/ApiRequestHandler.css"; // 스타일 추가

function ApiRequestHandler({ files }) {
  const [response, setResponse] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [showApiResponse, setShowApiResponse] = useState(false); // API Response 표시 여부
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
      {/* Submit 버튼 */}
      <button className="submit-btn" onClick={handleApiRequest}>
        Submit Files to API
      </button>

      {/* 결과가 있을 때만 카드 표시 */}
      {(imageUrl || response) && (
        <div className="result-card">
          {/* 이미지 결과 */}
          {imageUrl && (
            <div className="result-container">
              <h4 className="result-title">Generated Image</h4>
              <div className="image-card">
                <img src={imageUrl} alt="Generated Result" className="result-image" />
              </div>
            </div>
          )}

          {/* API Response */}
          {response && (
            <div className="api-response-container">
              <button
                className="toggle-btn"
                onClick={() => setShowApiResponse((prev) => !prev)}
              >
                {showApiResponse ? "Hide API Response" : "Show API Response"}
              </button>
              {showApiResponse && (
                <div className="api-response">
                  <pre>{JSON.stringify(response, null, 2)}</pre>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ApiRequestHandler;
