import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

const BACKEND_API = 'http://localhost:8000';

export default function App() {
  console.log('App component rendered');

  const [selectedImage, setSelectedImage] = useState(null);
  const [results, setResults] = useState(null);
  const [processing, setProcessing] = useState(false);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const processImage = async () => {
    if (!selectedImage) return;

    setProcessing(true);
    try {
      const response = await axios.post(`${BACKEND_API}/process-image/`, {
        image: selectedImage.split(',')[1], // Remove the base64 prefix
      });

      setResults(response.data);
      alert('Data extracted successfully!');
    } catch (error) {
      console.error('Error processing image:', error);
      alert('Failed to process the image. Please try again.');
    } finally {
      setProcessing(false);
    }
  };

  const exportToExcel = async () => {
    if (!results) return;

    try {
      const response = await axios.post(`${BACKEND_API}/export-excel/`, {
        data: results,
      }, {
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'form_data.xlsx');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);

      alert('Data exported to Excel successfully!');
    } catch (error) {
      console.error('Error exporting to Excel:', error);
      alert('Failed to export data. Please try again.');
    }
  };

  return (
    <div className="App">
      <h1>Questionnaire Scanner</h1>

      <input type="file" accept="image/*" onChange={handleImageUpload} />

      {selectedImage && (
        <div className="image-container">
          <img src={selectedImage} alt="Selected" />
        </div>
      )}

      <button className="button" onClick={processImage} disabled={processing}>
        {processing ? 'Processing...' : 'Process Image'}
      </button>

      {results && (
        <div className="results-container">
          <h2>Extracted Data:</h2>
          <pre>{JSON.stringify(results, null, 2)}</pre>
          <button className="button" onClick={exportToExcel}>Export to Excel</button>
        </div>
      )}
    </div>
  );
}
