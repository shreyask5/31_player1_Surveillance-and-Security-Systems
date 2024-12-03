# Emergency Detection System: Surveillance and Security Application

## **Try Emergency Detection System Live**: [https://shreyask.in/projects/emergency-response-system/demo](https://shreyask.in/projects/emergency-detection/demo)
## **Watch Emergency Response System Demo**: [Watch Demo Here](https://shreyask.in/projects/emergency-response-system/#demo)

This project was developed during the **24-hour Gradient AI Hackathon** conducted at B. M. S. College of Engineering, where it secured **second place 🥈** out of **60 teams** for its innovative approach to safety monitoring.  

This project is an advanced web application designed to provide real-time safety monitoring and emergency detection using computer vision and artificial intelligence technologies. The system utilizes machine learning models and AI analysis to identify potential emergency situations, offering immediate response mechanisms for personal safety.

The core functionality involves continuous video monitoring, detecting potential physical risks or medical emergencies through advanced image analysis. By leveraging YOLOv11 for object detection and Google Gemini AI for sophisticated scenario interpretation, the application provides a comprehensive safety monitoring solution.

## Table of Contents

- [Introduction](#introduction)
- [Project Overview](#project-overview)
- [Features and Functionalities](#features-and-functionalities)
- [Technology Stack](#technology-stack)
- [Changelog](#changelog)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

The Emergency Detection System aims to enhance personal safety through intelligent, real-time monitoring. By combining computer vision, machine learning, and AI-driven analysis, the application can detect potential emergencies and trigger immediate response mechanisms.

## Project Overview

The system continuously monitors a user's environment, analyzing video frames to identify potential safety risks, medical emergencies, or unusual situations. When a critical scenario is detected, it automatically sends detailed emergency notifications to designated contacts.

## Features and Functionalities

- **Intelligent Emergency Detection**: 
  - Real-time video analysis using YOLOv11 and Google Gemini AI
  - Detects physical risks, medical emergencies, and environmental hazards
- **Comprehensive Scenario Analysis**:
  - Identifies falls, immobility, breathing difficulties
  - Recognizes seizures, injuries, and potential obstructions
- **Automated Notification System**:
  - Sends detailed emergency emails with user location
  - Generates Google Maps links for precise location tracking
- **User-Friendly Interface**:
  - Simple registration process
  - Real-time status updates
  - Emergency popup notifications
- **Flexible Detection Mechanism**:
  - Configurable detection intervals
  - Continuous monitoring with controllable start/stop functionality

## Technology Stack

- **Frontend**: 
  - HTML5
  - Vanilla JavaScript
  - WebRTC for camera access
- **Backend**:
  - Python Flask
  - YOLOv11 (Object Detection)
  - Google Gemini AI
- **Communication**:
  - RESTful API
  - FormData for image transmission
- **Deployment**:
  - Hosted on shreyask.in website hosted on AWS EC2 and Emergency Response System flask server hosted on Google Cloud N2
- **Version Control**: Git

## Changelog

## **Version 2.2**  
### **Communication Updates**  
- Replaced EmailJS with server-side email handling.  
- Integrated user details into image analysis requests.  
- Removed client-side email dependency.  

### **Enhanced Notifications**  
- Emergency popup includes detailed analysis and email confirmation.  
- Improved transparency in emergency communication.  

### **Data Handling**  
- Added comprehensive user data (details, location, emergency contact) to `FormData`.  
- Centralized email dispatch to reduce client-side exposure of sensitive information.  

### **Technical Improvements**  
- Streamlined detection workflow and backend communication.  
- Eliminated external email service dependencies for better reliability.  

### **User Experience**  
- Maintained core functionality with smoother backend integration.  

---

## **Version 2.1**  
### **Detection Mechanism**  
- Replaced `setInterval()` with `continuousDetection()` using a `while` loop.  
- Added `run` variable for detection control.  
- Maintained 200ms delay between frame captures.  

### **Performance Monitoring**  
- Integrated `performance.now()` for precise request-response timing.  
- Added console logs for server communication tracking.  

### **Backend Enhancements**  
- Sends 15 frames every 5 seconds to Gemini API only if a person is detected.  

### **Optimization**  
- Improved loop efficiency and communication stability.  
- Removed artificial delays, enhancing performance.  

---

## **Version 1.0**  
### **Frontend**  
- User registration captures details and validates input.  
- Captures 3 frames/sec via device camera for analysis.  
- Displays real-time status and triggers emergency alerts.  

### **Backend**  
- YOLOv11 for person detection.  
- Google Gemini AI for emergency scenario analysis.  
- API processes image frames and returns detection status.  

### **Key Features**  
- Detects physical risks (falls, injuries) and medical issues (breathin# Emergency Detection System: Surveillance and Security Application problems, seizures).  
- Sends emergency emails with user details and location link.  

### **Supported Emergency Flags**  
- Physical: fallen, motionless, restricted movement.  
- Medical: labored breathing, seizures, injuries.  
- Environmental: obstructions, safety risks.  

## Conclusion

The Emergency Detection System represents an innovative approach to personal safety, leveraging cutting-edge AI and computer vision technologies. By providing real-time monitoring and intelligent emergency detection, the application offers users an additional layer of security and rapid response capabilities.

## References

- **[YOLOv11 Documentation](https://docs.ultralytics.com/)**
- **[Google Gemini AI Documentation](https://ai.google.dev/tutorials)**
- **[Flask Documentation](https://flask.palletsprojects.com/)**
- **[WebRTC MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API)**
