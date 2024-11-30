import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import cv2
import numpy as np
import google.generativeai as genai
import base64

app = Flask(__name__)
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = 'AIzaSyD1FAnFY2DDmyaSBPW8nRvCN-2XP02j9g0'  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)
genai_images = []

# Load the YOLO model
model = YOLO("./models/yolo11n.pt")

def send_emergency_email(sender_email, sender_password, recipient_email, emergency_data):
    """
    Send an emergency alert email using Gmail SMTP server.
    
    :param sender_email: Your Gmail address
    :param sender_password: App password for your Gmail account
    :param recipient_email: Email address of the emergency contact
    :param emergency_data: Dictionary containing emergency information
    """
    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Emergency Alert for {emergency_data.get('name', 'Unknown')}"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Create the email body HTML template
    html = f"""
    <p>Hello Emergency Team,</p>
    <p>You got a new alert from {emergency_data.get('name', 'Unknown')}:</p>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px;">
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d0d0; background-color: #f9f9f9;">
          <strong>Emergency Message:</strong>
        </td>
        <td style="padding: 8px; border: 1px solid #d0d0d0;">
          {emergency_data.get('emergencyMessage', 'Automatic emergency detection triggered')}
        </td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d0d0; background-color: #f9f9f9;">
          <strong>Name:</strong>
        </td>
        <td style="padding: 8px; border: 1px solid #d0d0d0;">
          {emergency_data.get('name', 'N/A')}
        </td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d0d0; background-color: #f9f9f9;">
          <strong>Contact Phone:</strong>
        </td>
        <td style="padding: 8px; border: 1px solid #d0d0d0;">
          {emergency_data.get('phone', 'N/A')}
        </td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d0d0; background-color: #f9f9f9;">
          <strong>Emergency Contact Phone:</strong>
        </td>
        <td style="padding: 8px; border: 1px solid #d0d0d0;">
          {emergency_data.get('emergencyPhone', 'N/A')}
        </td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d0d0; background-color: #f9f9f9;">
          <strong>Address:</strong>
        </td>
        <td style="padding: 8px; border: 1px solid #d0d0d0;">
          {emergency_data.get('address', 'N/A')}
        </td>
      </tr>
      <tr>
        <td style="padding: 8px; border: 1px solid #d0d0d0; background-color: #f9f9f9;">
          <strong>Location:</strong>
        </td>
        <td style="padding: 8px; border: 1px solid #d0d0d0;">
          Latitude: {emergency_data.get('latitude', 'N/A')}<br>
          Longitude: {emergency_data.get('longitude', 'N/A')}<br>
          <a href="{emergency_data.get('mapsLink', '#')}" style="color: #1a73e8;">View on Google Maps</a>
        </td>
      </tr>
    </table>
    <p style="color: #666; font-size: 0.9em;">
      Emergency Response System
    </p>
    """

    # Attach HTML content
    msg.attach(MIMEText(html, 'html'))

    try:
        # Setup the SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Enable security
            # Login to the server
            server.login(sender_email, sender_password)
            
            # Send email
            server.sendmail(sender_email, recipient_email, msg.as_string())
        
        print(f"Emergency alert email sent successfully to {recipient_email}")
        return True
    
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

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
    You are a Critical Care AI Safety Monitoring Assistant designed to assess and report on an individual's condition in real-time. Your primary role is to monitor for safety risks, medical emergencies, and signs of distress, providing actionable insights in a structured format.

    Primary Objectives:
    1. Conduct a visual assessment of an individual's physical state.
    2. Identify potential safety risks and emergency scenarios.
    3. Provide concise and actionable observations with situational awareness.

    Critical Detection Areas:

    Mobility and Physical Status:
    - Detect if the person has fallen or is immobilized.
    - Assess body positioning and signs of distress.
    - Identify dangerous or unnatural postures.
    - Detect sudden or prolonged changes in movement or state.

    Physical Condition Indicators:
    - Body and Head Position:
    - Identify unusual or concerning positioning.
    - Detect prolonged motionlessness or unconsciousness.
    - Evaluate for signs of physical distress or discomfort.

    Emergency Markers:
    - Look for:
    - Signs of physical trauma or visible injury.
    - Difficulty breathing or airway obstruction.
    - Sudden collapse or inability to move.
    - Immediate environmental risks or hazards.

    Flags and Definitions:
    The system must raise only one flag per assessment. Use the following format:

    Intensity: <intensity>: <flag>: <explanation>

    - Intensity: A score between 0 and 100 indicating the severity or likelihood of the condition based on the visual input.
    - Flag: The most critical observation related to the individual's condition.
    - Explanation: A two-part explanation:
    1. How: Describes the manner or cause of the incident (e.g., "The individual tripped over an object").  
    2. Impact: Specifies the body parts affected or hurt (e.g., "Impact detected on the head and left arm").

    Flag Definitions:
    - fallen: The individual is on the ground in a manner suggesting a fall.
    - unresponsive: No visible reaction to external stimuli.
    - severe risk: Conditions pose a high probability of harm.
    - potential danger: Nearby factors could harm the individual.
    - motionless: The person has not moved for a concerning duration.
    - disoriented: The individual appears confused or unsteady.
    - restricted movement: Difficulty or inability to move body parts.
    - potential obstruction: Airway may be blocked or compromised.
    - labored breathing: Noticeable difficulty in breathing.
    - seizure-like activity: Repeated involuntary spasms or abnormal movements.
    - visible bleeding: Blood is clearly seen, indicating an injury.
    - hazard nearby: A dangerous object or situation is close to the individual.
    - environmental risk: Unsafe surroundings such as fire, water, or falling objects.
    - sudden collapse: Unexpected falling, suggesting a serious event.
    - no assistance: No immediate signs of risk; the individual appears safe.

    Reporting Guidelines:
    - Output strictly in the format: Intensity: <intensity>: <flag>: <explanation>.
    - Ensure explanations include both "how" the incident occurred and "impact" to body parts.
    - Provide minimal and clear explanations to ensure immediate understanding.
    - Report only one flag per assessment, focusing on the most critical observation.
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
    Analyze these sequential images of a person.
    Provide a brief, concise assessment focusing on safety and potential emergencies.
    Describe observations clearly and succinctly, highlighting any concerning signs or risks.
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

@app.route('/projects/api3/analyze', methods=['POST'])
def analyze_images():
    global genai_images
    
    # Extract email configuration from request JSON
    email_config = request.form.get('email_config')
    if email_config:
        try:
            email_config = json.loads(email_config)
        except json.JSONDecodeError:
            email_config = {}
    else:
        email_config = {}
    
    # Default response in case no analysis occurs
    default_response = {
        "message": "No Person detected",
        "emergency": False
    }

    person_seen_response = {
        "message": "Person detected: Generating Response...",
        "emergency": False
    }
    
    for i in range(3):  # Collect 3 images
        file = request.files.get(f'image{i}')
        if file:
            # Read the image
            image = np.frombuffer(file.read(), np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            genai_images.append(image)
    
    # Check if person is detected
    if not any(detect_person(img) for img in genai_images):
        genai_images = genai_images[:-3]  # Remove last 3 images
        return jsonify(default_response)
        
    # Analyze images when we have collected enough
    if len(genai_images) == 15:
        try:
            images = genai_images
            genai_images = []
            full_analysis = analyze_situation(images)
            
            # Determine emergency based on Gemini's analysis
            emergency_keywords = [
                "fallen:", 
                "unresponsive:", 
                "severe risk:", 
                "potential danger:", 
                "motionless:", 
                "disoriented:", 
                "restricted movement:", 
                "potential obstruction:", 
                "labored breathing:", 
                "seizure-like activity:", 
                "visible bleeding:", 
                "hazard nearby:", 
                "environmental risk:", 
                "sudden collapse:"
            ]
            is_emergency = any(keyword in full_analysis.lower() for keyword in emergency_keywords)
            
            # Send emergency email if configured and emergency detected
            if is_emergency and email_config:
                try:
                    send_emergency_email(
                        sender_email='emergencyresponsesystem1@gmail.com',
                        sender_password='qsdu vnit fbpt okjw',
                        recipient_email=email_config.get('emergencyResponseEmail', 'shreyasksh6@gmail.com'),
                        emergency_data={
                            'name': email_config.get('name', 'Unknown'),
                            'emergencyMessage': full_analysis,
                            'phone': email_config.get('phone', 'N/A'),
                            'emergencyPhone': email_config.get('emergency_phone', 'N/A'),
                            'address': email_config.get('address', 'N/A'),
                            'latitude': email_config.get('latitude', 'N/A'),
                            'longitude': email_config.get('longitude', 'N/A'),
                            'mapsLink': email_config.get('maps_link', '#')
                        }
                    )
                except Exception as e:
                    print(f"Error sending emergency email: {e}")
            
            return jsonify({
                "message": full_analysis,
                "emergency": is_emergency
            })
        except Exception as e:
            print(f"Error in analysis: {e}")
            return jsonify(default_response)
    
    # If not enough images collected, return default response
    return jsonify(person_seen_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)