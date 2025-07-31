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

def create_test_image():
    """Create a simple test image with a face-like shape"""
    # Create a 200x200 image with a simple face
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple face
    # Head (circle)
    draw.ellipse([50, 50, 150, 150], fill='lightblue', outline='black')
    # Eyes
    draw.ellipse([70, 80, 80, 90], fill='black')
    draw.ellipse([120, 80, 130, 90], fill='black')
    # Nose
    draw.line([100, 95, 100, 110], fill='black', width=2)
    # Mouth
    draw.arc([80, 115, 120, 135], 0, 180, fill='black', width=2)
    
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
        
        # Create test image
        test_image = create_test_image()
        
        # Send to cloak endpoint
        files = {'file': ('test.png', test_image, 'image/png')}
        response = requests.post('http://localhost:8000/api/cloak-image', files=files, timeout=30)
        
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
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Image cloaking test error: {e}")
        return False

def test_protection_check():
    """Test protection checking functionality"""
    try:
        print("🛡️  Testing protection check...")
        
        # Create test image
        test_image = create_test_image()
        
        # Send to protection check endpoint
        files = {'file': ('test.png', test_image, 'image/png')}
        response = requests.post('http://localhost:8000/api/check-protection', files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Protection check test passed")
                print(f"   Faces detected: {data.get('faces_detected', 0)}")
                print(f"   Protection level: {data.get('protection_level', 'unknown')}")
                return True
            else:
                print(f"❌ Protection check failed: {data}")
                return False
        else:
            print(f"❌ Protection check request failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Protection check test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 InvisiFace System Test")
    print("=" * 30)
    
    # Wait for backend to start if needed
    print("⏳ Waiting for backend to start...")
    for i in range(10):
        if test_backend_health():
            break
        time.sleep(2)
        print(f"   Attempt {i+1}/10...")
    else:
        print("❌ Backend failed to start. Please check if it's running on http://localhost:8000")
        sys.exit(1)
    
    # Run tests
    tests_passed = 0
    total_tests = 2
    
    if test_cloak_image():
        tests_passed += 1
    
    if test_protection_check():
        tests_passed += 1
    
    # Results
    print("\n" + "=" * 30)
    print(f"📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! InvisiFace is working correctly.")
        print("\n💡 Next steps:")
        print("   1. Open http://localhost:3000 in your browser")
        print("   2. Upload an image with faces")
        print("   3. Click 'Cloak Image' to protect it")
        print("   4. Use 'Check if Protected' to verify")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()