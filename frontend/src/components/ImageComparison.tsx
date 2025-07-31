import React from 'react';

interface ImageComparisonProps {
  originalImage: string;
  cloakedImage: string | null;
  onCloakImage: () => void;
  onDownloadCloaked: () => void;
  isProcessing: boolean;
}

const ImageComparison: React.FC<ImageComparisonProps> = ({
  originalImage,
  cloakedImage,
  onCloakImage,
  onDownloadCloaked,
  isProcessing,
}) => {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="text-center mb-6">
        <h3 className="text-2xl font-bold text-secondary-900 mb-2">
          Image Comparison
        </h3>
        <p className="text-secondary-600">
          Compare your original image with the cloaked version
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Original Image */}
        <div className="space-y-4">
          <div className="text-center">
            <h4 className="text-lg font-semibold text-secondary-900 mb-2">
              Original Image
            </h4>
            <div className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-red-100 text-red-800">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              Vulnerable to Recognition
            </div>
          </div>
          <div className="relative bg-secondary-50 rounded-lg overflow-hidden">
            <img
              src={originalImage}
              alt="Original"
              className="w-full h-auto max-h-96 object-contain mx-auto"
            />
          </div>
        </div>

        {/* Cloaked Image */}
        <div className="space-y-4">
          <div className="text-center">
            <h4 className="text-lg font-semibold text-secondary-900 mb-2">
              Cloaked Image
            </h4>
            {cloakedImage ? (
              <div className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-green-100 text-green-800">
                <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Protected Against Recognition
              </div>
            ) : (
              <div className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-secondary-100 text-secondary-600">
                <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                </svg>
                Waiting for Processing
              </div>
            )}
          </div>
          
          <div className="relative bg-secondary-50 rounded-lg overflow-hidden min-h-[200px] flex items-center justify-center">
            {cloakedImage ? (
              <img
                src={cloakedImage}
                alt="Cloaked"
                className="w-full h-auto max-h-96 object-contain mx-auto"
              />
            ) : (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-secondary-200 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </div>
                <p className="text-secondary-500">Click "Cloak Image" to generate protected version</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 mt-8 justify-center">
        <button
          onClick={onCloakImage}
          disabled={isProcessing}
          className={`
            px-6 py-3 rounded-lg font-semibold text-white transition-all duration-200
            ${isProcessing
              ? 'bg-secondary-400 cursor-not-allowed'
              : 'bg-primary-600 hover:bg-primary-700 hover:shadow-lg'
            }
          `}
        >
          {isProcessing ? (
            <div className="flex items-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Processing...
            </div>
          ) : (
            <div className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {cloakedImage ? 'Cloak Again' : 'Cloak Image'}
            </div>
          )}
        </button>

        {cloakedImage && (
          <button
            onClick={onDownloadCloaked}
            disabled={isProcessing}
            className="px-6 py-3 rounded-lg font-semibold text-primary-700 bg-primary-50 border border-primary-200 hover:bg-primary-100 transition-all duration-200"
          >
            <div className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Download Cloaked Image
            </div>
          </button>
        )}
      </div>

      {/* Information Panel */}
      <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex">
          <svg className="w-5 h-5 text-blue-400 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
          <div className="text-sm text-blue-800">
            <p className="font-semibold mb-1">How Face Cloaking Works</p>
            <p>
              Our system adds imperceptible perturbations to your image that fool facial recognition algorithms 
              while keeping the image visually identical to humans. The changes are mathematically designed to 
              disrupt machine learning models without affecting image quality.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImageComparison;