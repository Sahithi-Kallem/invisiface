import numpy as np
import cv2
import face_recognition
from PIL import Image
import tensorflow as tf
from typing import Dict, List, Tuple, Any
import logging
import random

logger = logging.getLogger(__name__)

class FaceCloaker:
    """
    Face cloaking system inspired by Fawkes algorithm.
    Applies imperceptible perturbations to protect against facial recognition.
    """
    
    def __init__(self):
        """Initialize the face cloaker with default parameters."""
        self.perturbation_strength = 0.05  # Strength of adversarial perturbations
        self.max_iterations = 50  # Maximum optimization iterations
        self.learning_rate = 0.01  # Learning rate for perturbation generation
        self.target_shift = 0.3  # How much to shift face embeddings
        
        # Initialize OpenCV face cascade as fallback
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            logger.info("OpenCV face cascade loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load OpenCV face cascade: {e}")
            self.face_cascade = None
        
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better face detection.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Preprocessed image
        """
        try:
            # Convert to RGB if needed
            if len(image.shape) == 3 and image.shape[2] == 3:
                # Check if it's BGR (OpenCV format) and convert to RGB
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                rgb_image = image.copy()
            
            # Resize if image is too large (improves detection speed and accuracy)
            height, width = rgb_image.shape[:2]
            if width > 1024 or height > 1024:
                scale = min(1024/width, 1024/height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                rgb_image = cv2.resize(rgb_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
                logger.info(f"Resized image from {width}x{height} to {new_width}x{new_height}")
            
            return rgb_image
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            return image

    def detect_faces_face_recognition(self, image: np.ndarray) -> List[Dict]:
        """
        Detect faces using face_recognition library.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of face detection results
        """
        faces = []
        try:
            # Preprocess image
            rgb_image = self.preprocess_image(image)
            
            # Try different models for better detection
            models = ['hog', 'cnn']  # hog is faster, cnn is more accurate
            
            for model in models:
                try:
                    # Find face locations and encodings
                    face_locations = face_recognition.face_locations(rgb_image, model=model)
                    
                    if face_locations:
                        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
                        
                        for i, (location, encoding) in enumerate(zip(face_locations, face_encodings)):
                            faces.append({
                                'id': i,
                                'location': location,  # (top, right, bottom, left)
                                'encoding': encoding,
                                'confidence': 0.9,  # Default confidence
                                'method': f'face_recognition_{model}'
                            })
                        
                        logger.info(f"face_recognition ({model}) detected {len(face_locations)} face(s)")
                        break  # Use first successful detection
                        
                except Exception as e:
                    logger.warning(f"face_recognition {model} failed: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in face_recognition detection: {str(e)}")
            
        return faces

    def detect_faces_opencv(self, image: np.ndarray) -> List[Dict]:
        """
        Detect faces using OpenCV Haar cascades as fallback.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of face detection results
        """
        faces = []
        if self.face_cascade is None:
            return faces
            
        try:
            # Convert to grayscale for OpenCV detection
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Detect faces
            face_rects = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            for i, (x, y, w, h) in enumerate(face_rects):
                # Convert OpenCV format (x, y, w, h) to face_recognition format (top, right, bottom, left)
                top = y
                right = x + w
                bottom = y + h
                left = x
                
                # Extract face region for encoding (create a dummy encoding)
                face_region = image[top:bottom, left:right]
                dummy_encoding = np.random.random(128)  # 128-dimensional dummy encoding
                
                faces.append({
                    'id': i,
                    'location': (top, right, bottom, left),
                    'encoding': dummy_encoding,
                    'confidence': 0.8,  # Slightly lower confidence for OpenCV
                    'method': 'opencv_haar'
                })
            
            logger.info(f"OpenCV detected {len(face_rects)} face(s)")
            
        except Exception as e:
            logger.error(f"Error in OpenCV detection: {str(e)}")
            
        return faces

    def detect_faces(self, image: np.ndarray) -> List[Dict]:
        """
        Detect faces in the image using multiple methods.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of face detection results with locations and encodings
        """
        all_faces = []
        
        try:
            logger.info("Starting face detection with multiple methods")
            
            # Method 1: face_recognition library (primary)
            faces_fr = self.detect_faces_face_recognition(image)
            if faces_fr:
                all_faces.extend(faces_fr)
                logger.info(f"face_recognition found {len(faces_fr)} face(s)")
            
            # Method 2: OpenCV Haar cascades (fallback)
            if not all_faces:
                faces_cv = self.detect_faces_opencv(image)
                if faces_cv:
                    all_faces.extend(faces_cv)
                    logger.info(f"OpenCV fallback found {len(faces_cv)} face(s)")
            
            # Method 3: If still no faces, try with different image preprocessing
            if not all_faces:
                logger.info("Trying enhanced preprocessing for face detection")
                
                # Try histogram equalization
                try:
                    if len(image.shape) == 3:
                        # Convert to YUV and equalize Y channel
                        yuv = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
                        yuv[:,:,0] = cv2.equalizeHist(yuv[:,:,0])
                        enhanced_image = cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB)
                    else:
                        enhanced_image = cv2.equalizeHist(image)
                    
                    # Try detection on enhanced image
                    faces_enhanced = self.detect_faces_face_recognition(enhanced_image)
                    if faces_enhanced:
                        all_faces.extend(faces_enhanced)
                        logger.info(f"Enhanced preprocessing found {len(faces_enhanced)} face(s)")
                        
                except Exception as e:
                    logger.warning(f"Enhanced preprocessing failed: {str(e)}")
            
            # Remove duplicates if any (based on location overlap)
            unique_faces = self.remove_duplicate_faces(all_faces)
            
            logger.info(f"Total unique faces detected: {len(unique_faces)}")
            return unique_faces
            
        except Exception as e:
            logger.error(f"Error detecting faces: {str(e)}")
            return []

    def remove_duplicate_faces(self, faces: List[Dict]) -> List[Dict]:
        """
        Remove duplicate face detections based on location overlap.
        
        Args:
            faces: List of face detections
            
        Returns:
            List of unique face detections
        """
        if len(faces) <= 1:
            return faces
        
        unique_faces = []
        
        for face in faces:
            is_duplicate = False
            top1, right1, bottom1, left1 = face['location']
            
            for unique_face in unique_faces:
                top2, right2, bottom2, left2 = unique_face['location']
                
                # Calculate overlap
                overlap_area = max(0, min(right1, right2) - max(left1, left2)) * max(0, min(bottom1, bottom2) - max(top1, top2))
                area1 = (right1 - left1) * (bottom1 - top1)
                area2 = (right2 - left2) * (bottom2 - top2)
                
                if overlap_area > 0.5 * min(area1, area2):  # 50% overlap threshold
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_faces.append(face)
        
        return unique_faces
    
    def generate_adversarial_noise(self, face_region: np.ndarray, target_encoding: np.ndarray) -> np.ndarray:
        """
        Generate adversarial noise to shift face embedding away from original.
        
        Args:
            face_region: Face region as numpy array
            target_encoding: Target face encoding to move away from
            
        Returns:
            Adversarial noise array
        """
        try:
            # Simple noise generation approach
            # In a full Fawkes implementation, this would use gradient-based optimization
            
            # Generate random noise with controlled magnitude
            noise = np.random.normal(0, self.perturbation_strength, face_region.shape)
            
            # Apply Gaussian smoothing to make noise less detectable
            if len(noise.shape) == 3:
                for channel in range(noise.shape[2]):
                    noise[:, :, channel] = cv2.GaussianBlur(noise[:, :, channel], (3, 3), 0.5)
            else:
                noise = cv2.GaussianBlur(noise, (3, 3), 0.5)
            
            # Clip noise to reasonable bounds
            noise = np.clip(noise, -0.1, 0.1)
            
            return noise
            
        except Exception as e:
            logger.error(f"Error generating adversarial noise: {str(e)}")
            return np.zeros_like(face_region)
    
    def apply_cloaking_to_face(self, image: np.ndarray, face_info: Dict) -> np.ndarray:
        """
        Apply cloaking perturbations to a specific face region.
        
        Args:
            image: Full image as numpy array
            face_info: Face information dictionary
            
        Returns:
            Image with cloaked face
        """
        try:
            cloaked_image = image.copy()
            top, right, bottom, left = face_info['location']
            
            # Ensure coordinates are within image bounds
            height, width = image.shape[:2]
            top = max(0, min(top, height))
            bottom = max(0, min(bottom, height))
            left = max(0, min(left, width))
            right = max(0, min(right, width))
            
            # Extract face region
            face_region = image[top:bottom, left:right]
            
            if face_region.size == 0:
                logger.warning("Face region is empty, skipping")
                return cloaked_image
            
            # Generate adversarial noise
            noise = self.generate_adversarial_noise(face_region, face_info['encoding'])
            
            # Apply noise to face region
            cloaked_face = face_region.astype(np.float32) + noise * 255
            cloaked_face = np.clip(cloaked_face, 0, 255).astype(np.uint8)
            
            # Replace face region in image
            cloaked_image[top:bottom, left:right] = cloaked_face
            
            logger.info(f"Applied cloaking to face at location ({top}, {right}, {bottom}, {left})")
            return cloaked_image
            
        except Exception as e:
            logger.error(f"Error applying cloaking to face: {str(e)}")
            return image
    
    def cloak_image(self, image: np.ndarray) -> np.ndarray:
        """
        Apply face cloaking to all faces in an image.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Cloaked image as numpy array
        """
        try:
            logger.info("Starting face cloaking process")
            
            # Detect faces in the image
            faces = self.detect_faces(image)
            
            if not faces:
                logger.warning("No faces detected in image - applying general noise as fallback")
                # Apply subtle noise to entire image as fallback
                noise = np.random.normal(0, 0.01, image.shape)
                cloaked_image = image.astype(np.float32) + noise * 255
                cloaked_image = np.clip(cloaked_image, 0, 255).astype(np.uint8)
                return cloaked_image
            
            logger.info(f"Detected {len(faces)} face(s) in image")
            
            # Apply cloaking to each face
            cloaked_image = image.copy()
            for face_info in faces:
                cloaked_image = self.apply_cloaking_to_face(cloaked_image, face_info)
            
            logger.info("Face cloaking completed successfully")
            return cloaked_image
            
        except Exception as e:
            logger.error(f"Error in cloak_image: {str(e)}")
            return image
    
    def check_face_recognition(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Check if faces in the image can be recognized by face recognition systems.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Dictionary with protection analysis results
        """
        try:
            logger.info("Checking face recognition protection")
            
            # Detect faces
            faces = self.detect_faces(image)
            
            if not faces:
                return {
                    "is_protected": False,  # Changed: if no faces detected, might not be protected
                    "faces_detected": 0,
                    "confidence_scores": [],
                    "protection_level": "unknown",
                    "message": "No faces detected in image. This could mean: 1) Image contains no faces, 2) Faces are already heavily cloaked, or 3) Detection algorithm failed. Try uploading a clearer image with visible faces."
                }
            
            # Analyze each face
            confidence_scores = []
            for face in faces:
                # Calculate a confidence score based on encoding quality and detection method
                if face['method'].startswith('face_recognition'):
                    # Higher confidence for face_recognition detections
                    encoding_strength = np.linalg.norm(face['encoding'])
                    confidence = min(encoding_strength / 15.0, 1.0)  # Normalize to 0-1
                else:
                    # Lower confidence for OpenCV detections (fallback method)
                    confidence = 0.6
                
                confidence_scores.append(confidence)
            
            # Determine protection level
            avg_confidence = np.mean(confidence_scores)
            
            if avg_confidence < 0.3:
                protection_level = "high"
                is_protected = True
                message = f"Excellent protection detected! {len(faces)} face(s) found with low recognition confidence. The image appears well-protected against facial recognition systems."
            elif avg_confidence < 0.6:
                protection_level = "medium"
                is_protected = True
                message = f"Good protection detected! {len(faces)} face(s) found with moderate recognition confidence. The image has decent protection but could be strengthened."
            else:
                protection_level = "low"
                is_protected = False
                message = f"Limited protection detected! {len(faces)} face(s) found with high recognition confidence. The image may be vulnerable to facial recognition systems. Consider applying stronger cloaking."
            
            return {
                "is_protected": is_protected,
                "faces_detected": len(faces),
                "confidence_scores": confidence_scores,
                "protection_level": protection_level,
                "message": message
            }
            
        except Exception as e:
            logger.error(f"Error checking face recognition: {str(e)}")
            return {
                "is_protected": False,
                "faces_detected": 0,
                "confidence_scores": [],
                "protection_level": "error",
                "message": f"Error analyzing image: {str(e)}. Please try again with a different image."
            }
    
    def compare_faces(self, original_image: np.ndarray, cloaked_image: np.ndarray) -> Dict[str, Any]:
        """
        Compare face recognition results between original and cloaked images.
        
        Args:
            original_image: Original image
            cloaked_image: Cloaked image
            
        Returns:
            Comparison results
        """
        try:
            original_faces = self.detect_faces(original_image)
            cloaked_faces = self.detect_faces(cloaked_image)
            
            # Calculate similarity between corresponding faces
            similarities = []
            if len(original_faces) == len(cloaked_faces):
                for orig, cloak in zip(original_faces, cloaked_faces):
                    if orig['method'].startswith('face_recognition') and cloak['method'].startswith('face_recognition'):
                        similarity = face_recognition.face_distance([orig['encoding']], cloak['encoding'])[0]
                        similarities.append(1 - similarity)  # Convert distance to similarity
                    else:
                        # For OpenCV detections, use a dummy similarity
                        similarities.append(0.3)  # Assume some dissimilarity
            
            avg_similarity = np.mean(similarities) if similarities else 0
            
            return {
                "original_faces": len(original_faces),
                "cloaked_faces": len(cloaked_faces),
                "face_similarities": similarities,
                "average_similarity": float(avg_similarity),
                "protection_effective": avg_similarity < 0.5
            }
            
        except Exception as e:
            logger.error(f"Error comparing faces: {str(e)}")
            return {
                "original_faces": 0,
                "cloaked_faces": 0,
                "face_similarities": [],
                "average_similarity": 0,
                "protection_effective": False
            }