# InvisiFace: Face Anonymizer and Digital Identity Protection System

## 🎯 Project Overview

InvisiFace is a comprehensive web-based application that provides face anonymization and digital identity protection using advanced cloaking algorithms inspired by the Fawkes research project. The system adds imperceptible perturbations to images that fool facial recognition systems while maintaining visual quality for humans.

## 🏗️ Architecture

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **Features**: 
  - Drag & drop image upload
  - Side-by-side image comparison
  - Real-time protection verification
  - Image download functionality
  - Responsive modern UI

### Backend
- **Framework**: FastAPI (Python)
- **Core Technology**: Face cloaking using Fawkes-inspired algorithms
- **Libraries**: 
  - OpenCV for image processing
  - face_recognition for face detection
  - TensorFlow for adversarial perturbations
  - PIL for image manipulation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ with pip
- Node.js 16+ with npm
- Git

### Installation & Running

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd invisiface
   ```

2. **Start the application**
   ```bash
   ./start.sh
   ```

   This will automatically:
   - Set up Python virtual environment
   - Install backend dependencies
   - Start FastAPI server on http://localhost:8000
   - Install frontend dependencies
   - Start React app on http://localhost:3000

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Setup

If you prefer to run services separately:

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 📖 How to Use

1. **Upload Image**: Drag and drop or click to upload an image containing faces
2. **Generate Cloaked Version**: Click "Cloak Image" to apply protection
3. **Compare Results**: View original and cloaked images side-by-side
4. **Verify Protection**: Use "Check if Protected" to test against face recognition
5. **Download**: Save the cloaked image for personal use

## 🔧 API Endpoints

### POST /api/cloak-image
Apply face cloaking to uploaded image
- **Input**: Multipart form data with image file
- **Output**: Base64 encoded cloaked image

### POST /api/check-protection
Verify face recognition protection level
- **Input**: Multipart form data with image file
- **Output**: Protection analysis results

### POST /api/download-cloaked
Generate downloadable cloaked image
- **Input**: Multipart form data with image file
- **Output**: PNG file download

## 🛡️ Privacy & Security

- **Local Processing**: All image processing happens locally
- **No Cloud Storage**: Images are never stored or transmitted to external services
- **No Data Retention**: Images are processed in memory and discarded
- **Open Source**: Full transparency in protection algorithms

## 🎨 Features

### Core Functionality
- ✅ Face detection and isolation
- ✅ Adversarial perturbation generation
- ✅ Imperceptible noise application
- ✅ Protection level verification
- ✅ Multi-face support

### User Interface
- ✅ Modern, responsive design
- ✅ Drag & drop file upload
- ✅ Real-time processing feedback
- ✅ Side-by-side comparison
- ✅ Download functionality
- ✅ Protection verification tools

### Technical Features
- ✅ RESTful API architecture
- ✅ TypeScript for type safety
- ✅ Comprehensive error handling
- ✅ Loading states and feedback
- ✅ Cross-browser compatibility

## 🔬 Technology Details

### Face Cloaking Algorithm
The system implements a simplified version of the Fawkes algorithm:

1. **Face Detection**: Uses face_recognition library to locate faces
2. **Feature Extraction**: Generates face encodings
3. **Adversarial Noise**: Creates targeted perturbations
4. **Noise Application**: Applies imperceptible changes to face regions
5. **Quality Preservation**: Maintains visual fidelity

### Protection Verification
- Analyzes face recognition confidence scores
- Provides protection level assessment (High/Medium/Low)
- Tests against standard face recognition models
- Offers detailed confidence breakdowns

## 📁 Project Structure

```
invisiface/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── face_cloaker.py      # Core cloaking algorithms
│   ├── requirements.txt     # Python dependencies
│   └── start.sh            # Backend startup script
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.tsx         # Main application
│   │   └── index.css       # Tailwind styles
│   ├── package.json        # Node dependencies
│   └── start.sh           # Frontend startup script
├── start.sh               # Main startup script
├── README.md             # Project overview
└── PROJECT_SETUP.md      # This file
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill processes on ports 3000 and 8000
   lsof -ti:3000 | xargs kill -9
   lsof -ti:8000 | xargs kill -9
   ```

2. **Python Dependencies**
   ```bash
   # Update pip and reinstall
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

3. **Node Dependencies**
   ```bash
   # Clear cache and reinstall
   npm cache clean --force
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Face Recognition Issues**
   - Ensure image contains clear, visible faces
   - Try different image formats (JPG, PNG)
   - Check image file size (max 10MB recommended)

### Performance Optimization

- **CPU Processing**: Face cloaking takes ~30-60 seconds per image on CPU
- **Memory Usage**: Large images may require more RAM
- **Browser Compatibility**: Modern browsers recommended for optimal performance

## 🔮 Future Enhancements

- [ ] GPU acceleration support
- [ ] Batch image processing
- [ ] Advanced cloaking algorithms
- [ ] Mobile app version
- [ ] Integration with cloud storage
- [ ] Real-time video cloaking
- [ ] Custom protection levels
- [ ] Face recognition model testing

## 📄 License

MIT License - See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review API documentation at http://localhost:8000/docs

---

**Note**: This system is designed for educational and privacy protection purposes. While effective against many facial recognition systems, it should not be considered a complete security solution.