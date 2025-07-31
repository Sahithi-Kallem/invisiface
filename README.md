# InvisiFace: Face Anonymizer and Digital Identity Protection System

InvisiFace is a web-based application that protects individuals from facial recognition technologies and deepfake abuse. It uses adversarial cloaking techniques to modify user images in a way that prevents machine learning models from recognizing the face, without altering it noticeably to humans.

---

## 🌐 Features

- Upload an image directly through the website
- View original and cloaked (protected) versions side by side
- Download the cloaked image
- Check if the cloaked image still triggers recognition using face recognition APIs
- Clean, modern UI built with React and Tailwind CSS
- Fast backend using Flask or FastAPI
- Integrates [Fawkes](https://github.com/Shawn-Shan/fawkes) or similar cloaking tools

---

## ⚙️ Tech Stack

- **Frontend:** React + Tailwind CSS
- **Backend:** Python (Flask or FastAPI)
- **Face Cloaking:** Fawkes (via Python subprocess or direct integration)
- **Face Detection:** face_recognition or DeepFace

---

## 🚀 Getting Started

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd invisiface
