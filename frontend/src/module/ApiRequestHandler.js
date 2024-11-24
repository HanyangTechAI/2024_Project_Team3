import React, { useState } from 'react';

function ApiRequestHandler({ files }) {
  const [response, setResponse] = useState(null);

  const handleApiRequest = async () => {
    if (files.length === 0) {
      alert("No files to upload.");
      return;
    }

    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    try {
      const res = await fetch('https://example.com/api/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setResponse(data);
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
    </div>
  );
}

export default ApiRequestHandler;
