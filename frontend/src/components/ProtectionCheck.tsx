import React from 'react';

interface ProtectionResult {
  is_protected: boolean;
  faces_detected: number;
  confidence_scores: number[];
  protection_level: string;
  message: string;
}

interface ProtectionCheckProps {
  originalImage: string;
  cloakedImage: string;
  protectionResult: ProtectionResult | null;
  onCheckProtection: (image: string) => void;
  isProcessing: boolean;
}

const ProtectionCheck: React.FC<ProtectionCheckProps> = ({
  originalImage,
  cloakedImage,
  protectionResult,
  onCheckProtection,
  isProcessing,
}) => {
  const getProtectionLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-secondary-100 text-secondary-600 border-secondary-200';
    }
  };

  const getProtectionIcon = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high':
        return (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
        );
      case 'medium':
        return (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        );
      case 'low':
        return (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm-1-4a1 1 0 112 0 1 1 0 01-2 0zm1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        );
      default:
        return (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
        );
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="text-center mb-6">
        <h3 className="text-2xl font-bold text-secondary-900 mb-2">
          Protection Verification
        </h3>
        <p className="text-secondary-600">
          Test your images against face recognition systems
        </p>
      </div>

      {/* Test Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 mb-8 justify-center">
        <button
          onClick={() => onCheckProtection(originalImage)}
          disabled={isProcessing}
          className={`
            px-6 py-3 rounded-lg font-semibold transition-all duration-200
            ${isProcessing
              ? 'bg-secondary-400 text-white cursor-not-allowed'
              : 'bg-red-600 text-white hover:bg-red-700 hover:shadow-lg'
            }
          `}
        >
          <div className="flex items-center">
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Test Original Image
          </div>
        </button>

        <button
          onClick={() => onCheckProtection(cloakedImage)}
          disabled={isProcessing}
          className={`
            px-6 py-3 rounded-lg font-semibold transition-all duration-200
            ${isProcessing
              ? 'bg-secondary-400 text-white cursor-not-allowed'
              : 'bg-green-600 text-white hover:bg-green-700 hover:shadow-lg'
            }
          `}
        >
          <div className="flex items-center">
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Test Cloaked Image
          </div>
        </button>
      </div>

      {/* Results Display */}
      {protectionResult && (
        <div className="space-y-6 animate-slide-up">
          {/* Protection Level */}
          <div className="text-center">
            <div className={`inline-flex items-center px-4 py-2 rounded-full border ${getProtectionLevelColor(protectionResult.protection_level)}`}>
              {getProtectionIcon(protectionResult.protection_level)}
              <span className="ml-2 font-semibold capitalize">
                {protectionResult.protection_level} Protection
              </span>
            </div>
          </div>

          {/* Detailed Results */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-secondary-50 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-secondary-900 mb-1">
                {protectionResult.faces_detected}
              </div>
              <div className="text-sm text-secondary-600">Faces Detected</div>
            </div>

            <div className="bg-secondary-50 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-secondary-900 mb-1">
                {protectionResult.is_protected ? 'Yes' : 'No'}
              </div>
              <div className="text-sm text-secondary-600">Protected</div>
            </div>

            <div className="bg-secondary-50 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-secondary-900 mb-1">
                {protectionResult.confidence_scores.length > 0 
                  ? `${Math.round(protectionResult.confidence_scores[0] * 100)}%`
                  : 'N/A'
                }
              </div>
              <div className="text-sm text-secondary-600">Confidence Score</div>
            </div>
          </div>

          {/* Message */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex">
              <svg className="w-5 h-5 text-blue-400 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
              <div className="text-sm text-blue-800">
                <p className="font-semibold mb-1">Analysis Result</p>
                <p>{protectionResult.message}</p>
              </div>
            </div>
          </div>

          {/* Confidence Scores Breakdown */}
          {protectionResult.confidence_scores.length > 1 && (
            <div className="bg-white border border-secondary-200 rounded-lg p-4">
              <h4 className="font-semibold text-secondary-900 mb-3">Individual Face Confidence Scores</h4>
              <div className="space-y-2">
                {protectionResult.confidence_scores.map((score, index) => (
                  <div key={index} className="flex items-center">
                    <span className="text-sm text-secondary-600 w-16">Face {index + 1}:</span>
                    <div className="flex-1 bg-secondary-200 rounded-full h-2 mr-3">
                      <div
                        className={`h-2 rounded-full ${
                          score < 0.3 ? 'bg-green-500' : score < 0.6 ? 'bg-yellow-500' : 'bg-red-500'
                        }`}
                        style={{ width: `${score * 100}%` }}
                      ></div>
                    </div>
                    <span className="text-sm font-medium text-secondary-900 w-12">
                      {Math.round(score * 100)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Information Panel */}
      <div className="mt-6 bg-amber-50 border border-amber-200 rounded-lg p-4">
        <div className="flex">
          <svg className="w-5 h-5 text-amber-400 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
          <div className="text-sm text-amber-800">
            <p className="font-semibold mb-1">Understanding Protection Levels</p>
            <ul className="space-y-1 text-xs">
              <li><strong>High:</strong> Excellent protection against facial recognition systems</li>
              <li><strong>Medium:</strong> Good protection, may be vulnerable to advanced systems</li>
              <li><strong>Low:</strong> Limited protection, consider re-cloaking with stronger settings</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProtectionCheck;