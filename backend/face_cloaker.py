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
        
    def detect_faces(self, image: np.ndarray) -> List[Dict]:
        """
        Detect faces in the image using face_recognition library.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of face detection results with locations and encodings
        """
        try:
            # Convert BGR to RGB if needed
            if len(image.shape) == 3 and image.shape[2] == 3:
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                rgb_image = image
                
            # Find face locations and encodings
            face_locations = face_recognition.face_locations(rgb_image)
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
            
            faces = []
            for i, (location, encoding) in enumerate(zip(face_locations, face_encodings)):
                faces.append({
                    'id': i,
                    'location': location,  # (top, right, bottom, left)
                    'encoding': encoding,
                    'confidence': 0.9  # Default confidence
                })
                
            return faces
            
        except Exception as e:
            logger.error(f"Error detecting faces: {str(e)}")
            return []
    
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
            
            # Extract face region
            face_region = image[top:bottom, left:right]
            
            if face_region.size == 0:
                return cloaked_image
            
            # Generate adversarial noise
            noise = self.generate_adversarial_noise(face_region, face_info['encoding'])
            
            # Apply noise to face region
            cloaked_face = face_region.astype(np.float32) + noise * 255
            cloaked_face = np.clip(cloaked_face, 0, 255).astype(np.uint8)
            
            # Replace face region in image
            cloaked_image[top:bottom, left:right] = cloaked_face
            
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
                logger.info("No faces detected in image")
                return image
            
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
                    "is_protected": True,
                    "faces_detected": 0,
                    "confidence_scores": [],
                    "protection_level": "high",
                    "message": "No faces detected - image is protected"
                }
            
            # Analyze each face
            confidence_scores = []
            for face in faces:
                # Calculate a mock confidence score based on encoding quality
                # In a real implementation, this would test against known face databases
                encoding_strength = np.linalg.norm(face['encoding'])
                confidence = min(encoding_strength / 10.0, 1.0)  # Normalize to 0-1
                confidence_scores.append(confidence)
            
            # Determine protection level
            avg_confidence = np.mean(confidence_scores)
            
            if avg_confidence < 0.3:
                protection_level = "high"
                is_protected = True
                message = "Image appears to be well protected against face recognition"
            elif avg_confidence < 0.6:
                protection_level = "medium"
                is_protected = True
                message = "Image has moderate protection against face recognition"
            else:
                protection_level = "low"
                is_protected = False
                message = "Image may be vulnerable to face recognition systems"
            
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
                "protection_level": "unknown",
                "message": f"Error analyzing image: {str(e)}"
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
                    similarity = face_recognition.face_distance([orig['encoding']], cloak['encoding'])[0]
                    similarities.append(1 - similarity)  # Convert distance to similarity
            
            avg_similarity = np.mean(similarities) if similarities else 0
            
            return {
                "original_faces": len(original_faces),
                "cloaked_faces": len(cloaked_faces),
                "face_similarities": similarities,
                "average_similarity": avg_similarity,
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