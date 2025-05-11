# 📸 PhotoHire - Photographer Booking App

PhotoHire is an Android-based application that lets users hire professional photographers in cities like Dehradun, Rishikesh, Chandigarh, and Delhi. The app provides an Uber-like experience for booking, locating, and communicating with photographers.

---

## ✨ Features

### Customer Features
- Google Sign-In
- Search & book photographers
- View portfolios
- Live chat with photographers
- Booking tracking

### Photographer Features
- Register profile & portfolio
- Share live location
- Receive and manage bookings
- Communicate with customers

### Developer Backend (Python)
- REST APIs
- User authentication
- Booking management
- Chat & location services

---

## 🛠️ Tech Stack

| Layer        | Tech                              |
|--------------|-----------------------------------|
| Frontend     | Kotlin (Android)                  |
| Backend      | Python (FastAPI / Django)         |
| Auth         | Google OAuth2, JWT                |
| Database     | PostgreSQL / Firebase             |
| Messaging    | Firebase Cloud Messaging / Socket.IO |
| Live Location| Google Maps API / LocationManager |

---

## 📷 Screenshots

### 1. Customer Home Screen
![Customer Home](screenshots/customer_home.png)

### 2. Photographer Profile & Portfolio
![Photographer Profile](screenshots/photographer_profile.png)

### 3. Chat Interface
![Chat Screen](screenshots/chat_screen.png)

### 4. Photographer Registration
![Photographer Registration](screenshots/photographer_register.png)

---

## 🚀 Getting Started

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload