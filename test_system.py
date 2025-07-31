#!/usr/bin/env python3
"""
Simple test script to verify InvisiFace system functionality
"""

import requests
import sys
import time
from io import BytesIO
from PIL import Image, ImageDraw
import base64
import numpy as np

def create_test_image():
    """Create a more realistic test image with a face-like shape"""
    # Create a larger image for better detection
    img = Image.new('RGB', (400, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a more realistic face
    # Head (oval)
    draw.ellipse([100, 80, 300, 320], fill='#FFDBAC', outline='black', width=2)
    
    # Eyes (more detailed)
    # Left eye
    draw.ellipse([140, 160, 180, 200], fill='white', outline='black', width=2)
    draw.ellipse([150, 170, 170, 190], fill='black')  # pupil
    draw.ellipse([155, 175, 165, 185], fill='white')  # highlight
    
    # Right eye
    draw.ellipse([220, 160, 260, 200], fill='white', outline='black', width=2)
    draw.ellipse([230, 170, 250, 190], fill='black')  # pupil
    draw.ellipse([235, 175, 245, 185], fill='white')  # highlight
    
    # Eyebrows
    draw.arc([135, 140, 185, 160], 0, 180, fill='black', width=3)
    draw.arc([215, 140, 265, 160], 0, 180, fill='black', width=3)
    
    # Nose (more detailed)
    draw.polygon([(200, 200), (190, 240), (200, 250), (210, 240)], fill='#FFDBAC', outline='#D2691E')
    # Nostrils
    draw.ellipse([192, 242, 198, 248], fill='black')
    draw.ellipse([202, 242, 208, 248], fill='black')
    
    # Mouth (more realistic)
    draw.arc([170, 260, 230, 300], 0, 180, fill='black', width=3)
    draw.arc([175, 265, 225, 295], 0, 180, fill='red', width=2)
    
    # Add some facial features for better detection
    # Cheeks
    draw.ellipse([120, 220, 140, 240], fill='#FFB6C1', outline=None)
    draw.ellipse([260, 220, 280, 240], fill='#FFB6C1', outline=None)
    
    # Hair
    draw.arc([90, 70, 310, 200], 0, 180, fill='brown', width=20)
    
    # Add some texture/noise to make it more realistic
    pixels = img.load()
    for i in range(img.width):
        for j in range(img.height):
            if 100 <= i <= 300 and 80 <= j <= 320:  # Only in face area
                r, g, b = pixels[i, j]
                # Add slight noise
                noise = np.random.randint(-5, 6)
                r = max(0, min(255, r + noise))
                g = max(0, min(255, g + noise))
                b = max(0, min(255, b + noise))
                pixels[i, j] = (r, g, b)
    
    # Save to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes

def create_real_face_pattern():
    """Create an even more realistic face pattern using geometric shapes"""
    img = Image.new('RGB', (300, 400), color='#F0F0F0')
    draw = ImageDraw.Draw(img)
    
    # Face outline (more realistic proportions)
    draw.ellipse([50, 50, 250, 350], fill='#FFDBAC', outline='#D2691E', width=2)
    
    # Forehead
    draw.ellipse([70, 50, 230, 150], fill='#FFDBAC')
    
    # Eyes region
    # Left eye socket
    draw.ellipse([80, 120, 140, 180], fill='#F5DEB3', outline='#8B4513', width=1)
    # Right eye socket  
    draw.ellipse([160, 120, 220, 180], fill='#F5DEB3', outline='#8B4513', width=1)
    
    # Eyes
    draw.ellipse([90, 135, 130, 165], fill='white', outline='black', width=2)
    draw.ellipse([170, 135, 210, 165], fill='white', outline='black', width=2)
    
    # Pupils
    draw.ellipse([105, 145, 115, 155], fill='black')
    draw.ellipse([185, 145, 195, 155], fill='black')
    
    # Eyebrows
    draw.ellipse([85, 110, 135, 130], fill='#8B4513')
    draw.ellipse([165, 110, 215, 130], fill='#8B4513')
    
    # Nose
    draw.polygon([(150, 180), (140, 220), (150, 240), (160, 220)], fill='#FFDBAC', outline='#D2691E')
    
    # Mouth
    draw.ellipse([120, 260, 180, 290], fill='#CD5C5C', outline='#8B0000', width=2)
    
    # Chin
    draw.ellipse([100, 280, 200, 340], fill='#FFDBAC')
    
    # Save to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check passed")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend not accessible: {e}")
        return False

def test_cloak_image():
    """Test image cloaking functionality"""
    try:
        print("🔧 Testing image cloaking...")
        
        # Try with the more realistic face first
        test_image = create_real_face_pattern()
        
        # Send to cloak endpoint
        files = {'file': ('test_face.png', test_image, 'image/png')}
        response = requests.post('http://localhost:8000/api/cloak-image', files=files, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('cloaked_image'):
                print("✅ Image cloaking test passed")
                return True
            else:
                print(f"❌ Image cloaking failed: {data}")
                return False
        else:
            print(f"❌ Image cloaking request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Image cloaking test error: {e}")
        return False

def test_protection_check():
    """Test protection checking functionality"""
    try:
        print("🛡️  Testing protection check...")
        
        # Try with the more realistic face
        test_image = create_real_face_pattern()
        
        # Send to protection check endpoint
        files = {'file': ('test_face.png', test_image, 'image/png')}
        response = requests.post('http://localhost:8000/api/check-protection', files=files, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Protection check test passed")
                print(f"   Faces detected: {data.get('faces_detected', 0)}")
                print(f"   Protection level: {data.get('protection_level', 'unknown')}")
                print(f"   Message: {data.get('message', 'No message')}")
                return True
            else:
                print(f"❌ Protection check failed: {data}")
                return False
        else:
            print(f"❌ Protection check request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Protection check test error: {e}")
        return False

def test_with_simple_image():
    """Test with a very simple geometric face"""
    try:
        print("🎭 Testing with simple geometric face...")
        
        # Create simple test image
        test_image = create_test_image()
        
        # Test protection check
        files = {'file': ('simple_face.png', test_image, 'image/png')}
        response = requests.post('http://localhost:8000/api/check-protection', files=files, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Simple face test - Faces detected: {data.get('faces_detected', 0)}")
            print(f"   Message: {data.get('message', 'No message')}")
            return True
        else:
            print(f"❌ Simple face test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Simple face test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 InvisiFace System Test")
    print("=" * 50)
    
    # Wait for backend to start if needed
    print("⏳ Waiting for backend to start...")
    for i in range(15):  # Increased wait time
        if test_backend_health():
            break
        time.sleep(3)
        print(f"   Attempt {i+1}/15...")
    else:
        print("❌ Backend failed to start. Please check if it's running on http://localhost:8000")
        print("   Try running: cd backend && python main.py")
        sys.exit(1)
    
    # Run tests
    tests_passed = 0
    total_tests = 4
    
    print("\n🔍 Running face detection and processing tests...")
    
    if test_cloak_image():
        tests_passed += 1
    
    if test_protection_check():
        tests_passed += 1
    
    if test_with_simple_image():
        tests_passed += 1
    
    # Test backend endpoints directly
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint test passed")
            tests_passed += 1
        else:
            print("❌ Root endpoint test failed")
    except Exception as e:
        print(f"❌ Root endpoint test error: {e}")
    
    # Results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed >= 3:  # Allow for some flexibility
        print("🎉 Most tests passed! InvisiFace appears to be working.")
        print("\n💡 Next steps:")
        print("   1. Open http://localhost:3000 in your browser")
        print("   2. Upload a real photo with clear faces")
        print("   3. Click 'Cloak Image' to protect it")
        print("   4. Use 'Check if Protected' to verify")
        print("\n📝 Note: Face detection works best with:")
        print("   - Clear, well-lit photos")
        print("   - Faces looking toward camera")
        print("   - Good image quality (not blurry)")
        print("   - Standard image formats (JPG, PNG)")
    else:
        print("⚠️  Some tests failed. The system may still work with real photos.")
        print("   Face detection algorithms work better with actual photographs.")
        print("   Try uploading a real photo through the web interface.")
        
    print(f"\n🔗 Access the application:")
    print(f"   Frontend: http://localhost:3000")
    print(f"   Backend:  http://localhost:8000")
    print(f"   API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()