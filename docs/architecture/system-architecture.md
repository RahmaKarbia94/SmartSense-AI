# SmartSense AI — System Architecture

## 1. Overview

SmartSense AI is an IoT platform designed for real-time environmental
monitoring, data storage, visualization, and AI-powered analysis.

## 2. System Components

### Virtual IoT Device
Generates environmental sensor data.

### MQTT Broker
Handles communication between IoT devices and the backend.

### Backend
Receives, validates, and processes telemetry data.

### Database
Stores sensor measurements and historical data.

### Dashboard
Provides real-time and historical visualization.

### AI Module
Analyzes collected data for anomaly detection and prediction.

## 3. Data Flow

Virtual Sensor
→ MQTT Broker
→ Backend
→ Database
→ Dashboard

Backend
→ AI Module