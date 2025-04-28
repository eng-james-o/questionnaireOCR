import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

const BACKEND_API = 'http://localhost:8000';

export default function App() {
  console.log('App component rendered');

  const [selectedImages, setSelectedImages] = useState([]);
  const [results, setResults] = useState(null);
  const [processing, setProcessing] = useState(false);

  const handleImageUpload = (event) => {
    const files = Array.from(event.target.files);
    const newImages = [];
    let completedReads = 0;

    files.forEach((file) => {
      const reader = new FileReader();      
      reader.onloadend = () => {        
        newImages.push(reader.result);
        completedReads++;
        if (completedReads === files.length) {
          setSelectedImages(newImages);
        }
      };    
      reader.readAsDataURL(file);    
    });
    }

  const processImage = async () => {
    if (!selectedImages || selectedImages.length === 0) return;

    setProcessing(true);
    try {
      const response = await axios.post(`${BACKEND_API}/process-image/`, {images: selectedImages.map(image => image.split(',')[1]),},
      
      );

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

      <input type="file" accept="image/*" multiple onChange={handleImageUpload} />

      {selectedImages.length > 0 && (
        <div className="images-container">
          {selectedImages.map((image, index) => (
            <img key={index} src={image} alt={`Selected ${index}`} />
          ))}
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
