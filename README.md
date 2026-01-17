# Human-Centric Biometric Verification System for XR Environments

## Project Overview

This project is a **high-security automated identity verification system** designed with **Extended Reality (XR)** and **Biometric Security** standards in mind.  
It utilizes **Computer Vision–based facial recognition** and integrates **Liveness Detection (Blink Analysis)** to prevent spoofing attacks (e.g., using photographs instead of real users).

---

## Key Features

### 1. Liveness Detection (Anti-Spoofing)

Unlike standard face recognition systems, this solution requires an **intentional eye blink** to verify identity and log attendance.

- Uses **Eye Aspect Ratio (EAR)** algorithm  
- EAR is computed from **68 facial landmarks**
- Prevents spoofing using static images

---

### 2. Identity Rejection (Unknown Handling)

The system implements **Euclidean Distance Thresholding** to reject unauthorized users.

- Face embeddings compared using distance metrics  
- If the confidence score exceeds the threshold, access is denied  

**Condition:**
  Distance < 0.45
  
Any face failing this condition is flagged as:

> **"Unknown Identity"**

---

### 3. Temporal Filtering (Blink Debouncing)

To ensure data integrity, a **Blink Cooldown (Temporal Filter)** is implemented.

- Prevents multiple triggers from a single blink  
- Adds a frame-based delay after successful verification  
- Ensures one blink = one verification entry  

---

### 4. Automated Status Logic

The system automatically determines attendance status:

- **Present** → If verified before `FIXED_TIME`
- **Late** → If verified after `FIXED_TIME`

This is done by comparing the **real-time system clock** with a predefined threshold.

---

## Technical Stack

### Language
- **Python 3.x**

### Core Libraries
- **OpenCV** – Image processing & real-time visualization  
- **Dlib / face_recognition** –  
  - HOG-based face detection  
  - 128D facial embeddings  
- **NumPy** – Mathematical operations for EAR calculation  
- **Datetime** – Temporal logic for attendance records  

---

## Project Structure

```plaintext
Project_Folder/
├── known_faces/              # Store authorized user photos (e.g., Aliza.jpg)
├── Attendance.csv            # Automated log file (generated on first run)
├── AttendanceManagement.py   # Main Python script
└── README.md                 # Project documentation
```

## Implementation Logic

### 1. Face Localization
* **Optimization:** Input frames are dynamically resized to $0.25\times$ scale.
* **Impact:** Ensures low-latency processing and high FPS, crucial for real-time XR pipelines.

### 2. Landmark Extraction
* **Core Engine:** Utilizes Dlib’s HOG-based detector to identify **68 specific facial landmarks**.
* **Mapping:** Precision mapping of ocular regions to monitor micro-movements of the eyelids.

### 3. EAR Calculation
The **Eye Aspect Ratio (EAR)** is computed to quantify the state of the eye (open/closed). It is calculated using the Euclidean distance between vertical and horizontal eye coordinates:

$$EAR = \frac{||p_2 - p_6|| + ||p_3 - p_5||}{2||p_1 - p_4||}$$

### 4. Verification Rule
* **Threshold:** If $EAR < 0.21$, an intentional blink is registered.
* **Logging:** Identity is verified and written to a secure CSV ledger including:
    * **Identity Name**
    * **Timestamp (ISO Format)**
    * **Attendance Status** (Categorized via temporal thresholds)

---
### 🖼️ System Output Demo
<img width="648" height="589" alt="Screenshot 2026-01-18 001728" src="https://github.com/user-attachments/assets/e1619f94-7f21-4db7-b5f5-2bf26bb0e1e4" />
*Figure 1: Real-time verification showing identity recognition and blink-triggered authentication.*

## 📊 Business Logic Visual Indicators

| Indicator | Frame Color | Meaning |
| :--- | :--- | :--- |
| ✅ **Verified** | 🟢 Green | Identity verified within the permitted time threshold. |
| ⏰ **Late** | 🔴 Red | Identity verified but timestamp exceeds the cut-off. |
| ⚠️ **Unknown** | 🟠 Orange | Unknown user or failed identification (Distance $> 0.45$). |

---

## Future Enhancements
* **Advanced Tracking:** Integration with **MediaPipe Face Mesh** for sub-millimeter ocular precision.
* **Concurrency:** Support for multi-user simultaneous verification.
* **XR Integration:** Porting the authentication pipeline for standalone **AR/VR headsets** (Meta Quest/HoloLens).

---

## 👤 Author
**Aliza Memon** 📧 **Email:** [alizanisar11@gmail.com](mailto:alizanisar11@gmail.com)  
🌐 **Portfolio:** [portfolioaliza.netlify.app](https://portfolioaliza.netlify.app)
