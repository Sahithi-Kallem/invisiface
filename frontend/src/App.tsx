import React, { useState, useCallback } from 'react';
import axios from 'axios';
import ImageUpload from './components/ImageUpload';
import ImageComparison from './components/ImageComparison';
import ProtectionCheck from './components/ProtectionCheck';
import LoadingSpinner from './components/LoadingSpinner';
import './App.css';

interface ProtectionResult {
  is_protected: boolean;
  faces_detected: number;
  confidence_scores: number[];
  protection_level: string;
  message: string;
}

function App() {
  const [originalImage, setOriginalImage] = useState<string | null>(null);
  const [cloakedImage, setCloakedImage] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [protectionResult, setProtectionResult] = useState<ProtectionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const handleImageUpload = useCallback((file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      if (e.target?.result) {
        setOriginalImage(e.target.result as string);
        setCloakedImage(null);
        setProtectionResult(null);
        setError(null);
      }
    };
    reader.readAsDataURL(file);
  }, []);

  const handleCloakImage = async () => {
    if (!originalImage) return;

    setIsProcessing(true);
    setError(null);

    try {
      // Convert base64 to blob
      const response = await fetch(originalImage);
      const blob = await response.blob();
      
      // Create form data
      const formData = new FormData();
      formData.append('file', blob, 'image.png');

      // Send to backend
      const cloakResponse = await axios.post(
        `${API_BASE_URL}/api/cloak-image`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      if (cloakResponse.data.success) {
        setCloakedImage(cloakResponse.data.cloaked_image);
      } else {
        setError('Failed to cloak image');
      }
    } catch (err) {
      console.error('Error cloaking image:', err);
      setError('Error processing image. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleCheckProtection = async (imageToCheck: string) => {
    setIsProcessing(true);
    setError(null);

    try {
      // Convert base64 to blob
      const response = await fetch(imageToCheck);
      const blob = await response.blob();
      
      // Create form data
      const formData = new FormData();
      formData.append('file', blob, 'image.png');

      // Send to backend
      const checkResponse = await axios.post(
        `${API_BASE_URL}/api/check-protection`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      if (checkResponse.data.success) {
        setProtectionResult(checkResponse.data);
      } else {
        setError('Failed to check protection');
      }
    } catch (err) {
      console.error('Error checking protection:', err);
      setError('Error checking protection. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownloadCloaked = async () => {
    if (!cloakedImage) return;

    try {
      // Convert base64 to blob
      const response = await fetch(cloakedImage);
      const blob = await response.blob();
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'cloaked_image.png';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error downloading image:', err);
      setError('Error downloading image. Please try again.');
    }
  };

  const resetApp = () => {
    setOriginalImage(null);
    setCloakedImage(null);
    setProtectionResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-secondary-50 to-primary-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-secondary-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center mr-3">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-secondary-900">InvisiFace</h1>
                <p className="text-sm text-secondary-600">Face Anonymizer & Digital Identity Protection</p>
              </div>
            </div>
            <button
              onClick={resetApp}
              className="px-4 py-2 text-secondary-600 hover:text-secondary-800 transition-colors"
            >
              Reset
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            <div className="flex">
              <svg className="w-5 h-5 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              {error}
            </div>
          </div>
        )}

        {/* Step 1: Upload Image */}
        {!originalImage && (
          <div className="animate-fade-in">
            <ImageUpload onImageUpload={handleImageUpload} />
          </div>
        )}

        {/* Step 2: Image Processing and Comparison */}
        {originalImage && (
          <div className="space-y-8 animate-slide-up">
            <ImageComparison
              originalImage={originalImage}
              cloakedImage={cloakedImage}
              onCloakImage={handleCloakImage}
              onDownloadCloaked={handleDownloadCloaked}
              isProcessing={isProcessing}
            />

            {/* Step 3: Protection Check */}
            {cloakedImage && (
              <ProtectionCheck
                originalImage={originalImage}
                cloakedImage={cloakedImage}
                protectionResult={protectionResult}
                onCheckProtection={handleCheckProtection}
                isProcessing={isProcessing}
              />
            )}
          </div>
        )}

        {/* Loading Overlay */}
        {isProcessing && <LoadingSpinner />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-secondary-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-secondary-600">
            <p className="text-sm">
              InvisiFace protects your privacy by adding imperceptible perturbations to images
              that fool facial recognition systems while maintaining visual quality.
            </p>
            <p className="text-xs mt-2">
              All processing is done locally. Your images are not stored or transmitted to external services.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
