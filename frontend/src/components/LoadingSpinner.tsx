import React from 'react';

const LoadingSpinner: React.FC = () => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-8 max-w-sm mx-4 text-center">
        <div className="animate-spin rounded-full h-16 w-16 border-4 border-primary-200 border-t-primary-600 mx-auto mb-4"></div>
        <h3 className="text-lg font-semibold text-secondary-900 mb-2">
          Processing Image
        </h3>
        <p className="text-secondary-600 text-sm">
          Applying face cloaking technology...
        </p>
        <div className="mt-4 text-xs text-secondary-500">
          This may take a few moments depending on image complexity
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;