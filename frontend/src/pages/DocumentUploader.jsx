import React, { useState } from "react";

const API_BASE = import.meta.env.VITE_BACKEND_URL || "http://localhost:5000";

export default function DocumentUploader() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setUploadStatus("");
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const res = await fetch(`${API_BASE}/api/finance/upload-statement`, {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        const result = await res.json();
        setUploadStatus(`✅ Uploaded. ${result.detected_bills?.length || 0} bills detected.`);
      } else {
        setUploadStatus("❌ Upload failed.");
      }
    } catch (err) {
      console.error(err);
      setUploadStatus("❌ Error uploading file.");
    }
  };

  return (
    <div className="p-6 bg-gray-900 text-white space-y-6 rounded-lg shadow">
      <h2 className="text-2xl font-bold">Upload Financial Documents</h2>

      <input
        type="file"
        accept=".pdf,.xlsx,.xls,.csv"
        onChange={handleFileChange}
        className="block bg-gray-800 text-white rounded p-2 w-full"
      />

      <button
        onClick={handleUpload}
        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded font-semibold"
      >
        Upload
      </button>

      {uploadStatus && <div className="mt-3 text-sm">{uploadStatus}</div>}
    </div>
  );
}
