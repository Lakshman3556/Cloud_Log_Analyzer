# Intelligent Cloud-Based Log Analyzer

A lightweight SIEM-inspired cloud log analysis system built using Flask, AWS, and Machine Learning.

## Architecture Overview
Flask App → Local JSON Logs → Micro-batch Upload → Amazon S3 → AWS Lambda → DynamoDB → ML Anomaly Detection → Alert System → Admin Dashboard

## Technologies Used
- Python (Flask)
- Amazon S3
- AWS Lambda
- DynamoDB
- Scikit-learn (Isolation Forest)
- Gmail SMTP
- Chart.js

## Objective
To design a scalable, cost-effective, intelligent log monitoring system inspired by SIEM principles for academic and small-scale environments.
