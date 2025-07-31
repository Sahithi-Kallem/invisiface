# InvisiFace: Face Anonymizer and Digital Identity Protection System

A comprehensive web-based application that provides face anonymization and digital identity protection using advanced cloaking algorithms.

## Features

- **Face Cloaking**: Upload images and apply invisible perturbations to protect against facial recognition
- **Side-by-Side Comparison**: View original and cloaked images simultaneously
- **Protection Verification**: Check if images are protected against face recognition systems
- **Download Cloaked Images**: Save anonymized images for personal use
- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS

## Technology Stack

### Frontend
- React 18
- Tailwind CSS
- Axios for API communication
- File upload with drag & drop

### Backend
- FastAPI (Python)
- Face cloaking using Fawkes-inspired algorithms
- Face recognition verification
- Image processing with OpenCV and PIL

## Installation

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## Usage

1. Upload an image containing faces
2. Click "Cloak Image" to apply protection
3. Compare original and cloaked versions side-by-side
4. Use "Check if Protected" to verify anonymization effectiveness
5. Download the cloaked image for use

## Privacy & Security

InvisiFace processes all images locally and does not store or transmit personal data to external services. The cloaking algorithms add imperceptible perturbations that fool facial recognition systems while maintaining image quality.

## License

MIT License - See LICENSE file for details
