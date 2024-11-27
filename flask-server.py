import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import cv2
import numpy as np
import google.generativeai as genai
import time
import base64

app = Flask(__name__)
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = 'AIzaSyD1FAnFY2DDmyaSBPW8nRvCN-2XP02j9g0'  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)
genai_images = []

# Load the YOLO model
model = YOLO("./models/yolo11n.pt")

def encode_image(image):
    """Encode image to base64 for Gemini API"""
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')

def analyze_situation(images):
    """
    Analyze images using Gemini to detect potential emergency situations
    """
    # System instructions for the AI assistant
    system_instructions = """
    Role: You are a critical care AI safety monitoring assistant.

    Primary Objectives:
    1. Conduct a comprehensive visual assessment of an individual's condition
    2. Identify potential safety risks and emergency scenarios
    3. Provide precise, actionable observations with high situational awareness

    Critical Detection Areas:
    - Mobility and Physical Status:
      * Determine if the person has fallen or is immobilized
      * Assess body positioning and potential physical distress
      * Detect unnatural or dangerous body postures
      * Identify sudden changes in physical state

    Physical Condition Indicators:
    - Body and Head Position:
      * Check for unusual positioning
      * Detect prolonged motionlessness
      * Identify signs of potential unconsciousness or medical event
      * Assess overall body language and potential signs of distress

    Emergency Markers:
    - Look for signs of:
      * Physical trauma or injury
      * Medical emergencies
      * Inability to move or respond
      * Signs of immediate danger or risk

    Reporting Guidelines:
    - Provide clear, concise, and objective observations
    - Highlight specific visual evidence
    - Indicate potential severity of the situation
    - Recommend immediate actions if necessary

    Confidentiality and Sensitivity:
    - Maintain utmost respect for individual's privacy
    - Focus on critical safety assessment
    - Provide objective, non-invasive analysis
    """

    # Initialize the generation config
    generation_config = {
        "temperature": 0.2,
        "top_p": 1,
        "top_k": 32,
        "max_output_tokens": 4096,
    }

    # Create the model with system instructions
    model_vision = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        system_instruction=system_instructions,
        generation_config=generation_config,
    )

    # Prepare images for Gemini
    image_parts = [{"mime_type": "image/jpeg", "data": encode_image(img)} for img in images]

    # Prompt for analysis
    prompt = """
    Carefully analyze these sequential images of a person.
    Provide a comprehensive assessment focusing on safety and potential emergency scenarios.
    Describe your observations in detail, highlighting any concerning signs or potential risks.
    """

    try:
        # Send images to Gemini for analysis
        response = model_vision.generate_content([prompt] + image_parts)
        return response.text
    except Exception as e:
        return f"Analysis error: {str(e)}"

def detect_person(image):
    """Detect if a person is present in the image"""
    results = model(image)
    class_ids = results[0].boxes.cls.cpu().tolist()
    return "person" in [results[0].names[int(cls)] for cls in class_ids]

@app.route('/analyze', methods=['POST'])
def analyze_images():
    global genai_images
    
    # Default response in case no analysis occurs
    default_response = {
        "message": "No critical situation detected",
        "emergency": False
    }
    
    images = []
    for i in range(3):  # Collect 3 images
        file = request.files.get(f'image{i}')
        if file:
            # Read the image
            image = np.frombuffer(file.read(), np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            images.append(image)
            genai_images.append(image)
    
    # Check if person is detected
    if not images or not any(detect_person(img) for img in images):
        genai_images = genai_images[:-3]  # Remove last 3 images
        return jsonify(default_response)
    
    # Analyze images when we have collected enough
    if len(genai_images) >= 15:
        try:
            full_analysis = analyze_situation(genai_images[-15:])
            print(full_analysis)
            
            # Determine emergency based on Gemini's analysis
            is_emergency = any(keyword in full_analysis.lower() for keyword in [
                "fallen", "unresponsive", "emergency", "medical attention", 
                "needs help", "potential danger", "motionless", 
                "critical condition", "urgent", "severe risk"
            ])
            
            return jsonify({
                "message": full_analysis,
                "emergency": is_emergency
            })
        except Exception as e:
            print(f"Error in analysis: {e}")
            return jsonify(default_response)
    
    # If not enough images collected, return default response
    return jsonify(default_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)