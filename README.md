![image](https://github.com/user-attachments/assets/a9a653fe-59a6-48f5-81d2-5f0b20eca8ec)# Emergency Detection System: Surveillance and Security Application

## **Try Emergency Detection System Live**: [https://shreyask.in/projects/emergency-detection](https://shreyask.in/projects/emergency-detection)

This project was developed during the 24-hour Gradient AI Hackathon, where it secured **second place 🥈** for its innovative approach to safety monitoring.  

This project is an advanced web application designed to provide real-time safety monitoring and emergency detection using computer vision and artificial intelligence technologies. The system utilizes machine learning models and AI analysis to identify potential emergency situations, offering immediate response mechanisms for personal safety.

The core functionality involves continuous video monitoring, detecting potential physical risks or medical emergencies through advanced image analysis. By leveraging YOLOv8 for object detection and Google Gemini AI for sophisticated scenario interpretation, the application provides a comprehensive safety monitoring solution.

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

## Demo Video

https://my-portfolio-website-s3-bucket.s3.ap-south-1.amazonaws.com/assets/Emergency_Response_System_Demo.mp4

## Features and Functionalities

- **Intelligent Emergency Detection**: 
  - Real-time video analysis using YOLOv8 and Google Gemini AI
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
  - YOLOv8 (Object Detection)
  - Google Gemini AI
- **Communication**:
  - RESTful API
  - FormData for image transmission
- **Deployment**:
  - Hosted on cloud infrastructure
- **Version Control**: Git

## Changelog

### **Version 2.2**  
- **Communication Architecture**  
  - Replaced EmailJS with direct server-side email handling
  - Integrated user details transmission within image analysis requests
  - Removed client-side email sending dependency

- **User Notification Enhancements**  
  - Emergency popup now includes detailed analysis and email confirmation
  - Improved transparency in emergency communication

- **Data Transmission**  
  - `FormData` updated to include comprehensive user configuration
  - Centralized email handling on the server for enhanced security

- **Security and Privacy**  
  - Reduced sensitive user information exposure
  - Improved server-side email dispatch mechanism

### **Version 2.1**  
- **Detection Mechanism**  
  - Replaced `setInterval()` with `continuousDetection()` using a `while` loop
  - Added `run` variable to control detection loop
  - Maintained 200ms delay between capturing 3 frames per cycle

- **Performance Monitoring**  
  - Integrated `performance.now()` to track server request-response times
  - Added console logging for precise timing metrics

- **Frame Capture Logic**  
  - Continues capturing and sending 3 frames per cycle
  - Stops detection when stop button is pressed or emergency is detected

### **Version 1.0**  
- **Initial Implementation**  
  - User registration with detail validation  
  - Device camera frame capture  
  - Backend image analysis  
  - Emergency notification via EmailJS  

## Conclusion

The Emergency Detection System represents an innovative approach to personal safety, leveraging cutting-edge AI and computer vision technologies. By providing real-time monitoring and intelligent emergency detection, the application offers users an additional layer of security and rapid response capabilities.

## References

- **[YOLOv8 Documentation](https://docs.ultralytics.com/)**
- **[Google Gemini AI Documentation](https://ai.google.dev/tutorials)**
- **[Flask Documentation](https://flask.palletsprojects.com/)**
- **[WebRTC MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API)**
- **[Computer Vision Research Papers](https://arxiv.org/list/cs.CV/recent)**
