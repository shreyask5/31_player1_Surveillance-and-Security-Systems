# 31_player1_Surveillance-and-Security-Systems
# Changelog for Emergency Detection System

## **Version 2.1**  
### **Detection Mechanism**  
- Replaced `setInterval()` with `continuousDetection()` using a `while` loop.  
- Added `run` variable to control detection loop.  
- Maintained 200ms delay between capturing 3 frames per cycle.  

### **Performance Monitoring**  
- Integrated `performance.now()` to track server request-response times.  
- Added console logging for precise timing metrics.  

### **Frame Capture Logic**  
- Continues capturing and sending 3 frames per cycle.  
- Stops detection when:
  - Stop button is pressed.  
  - Emergency is detected.  

### **Backend Enhancements**  
- Sends 15 frames every 5 seconds to Gemini API only if a person is detected.  

### **Optimization Highlights**  
- Removed artificial delays, improving loop efficiency.  
- Enhanced server communication stability.  
- Maintained UI consistency and emergency notification system.  

---

## **Version 1.0**  
### **Frontend (HTML/JavaScript)**  
- User registration captures details and validates input.  
- Accesses device camera for frame capture at 3 frames/sec.  
- Sends images to the backend for analysis and displays real-time status.  
- Triggers popup alerts and sends emergency notifications via EmailJS.  

### **Backend (Python Flask)**  
- YOLOv8 detects persons in images.  
- Google Gemini AI analyzes sequences for emergency scenarios.  
- API processes image frames and returns detection status.  

### **Key Features**  
- Detects physical and medical risks like falls, injuries, and breathing issues.  
- Sends emergency emails with user details, location, and Google Maps link.  

### **Supported Emergency Flags**  
- Physical: fallen, motionless, restricted movement.  
- Medical: labored breathing, seizures, injuries.  
- Environmental: obstructions, safety risks.  
