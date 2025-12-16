Cloud-Based Microservices Platform

This project is a cloud-native architecture built on AWS, combining EC2-hosted frontend pages,
Dockerized microservices running inside AWS Lambda, RDS for user and API-key management, and
API Gateway fronted by CloudFront. The system provides users with weather data and nearby events
based on their location (retrieved from CloudFront headers).

⸻
Architecture Overview

Frontend (EC2 Instance)
One EC2 instance serves web pages:
	1.	Login / Register Page
	•	Allows users to create accounts and authenticate.
	•	Interacts with RDS for user credentials and profile storage.
	2.	User Dashboard
	•	Displays user' API KEY
	
⸻
Backend (Lambda + Docker on ECR)

All backend microservices are packaged as Docker images, stored in Amazon ECR, and run inside AWS Lambda.

1. Weather Service Lambda
	•	Pulls image from ECR.
	•	Returns weather data based on the user’s location.
	•	Location is extracted from CloudFront-Viewer-Country and similar geolocation headers.

2. Events Service Lambda
	•	Pulls image from ECR.
	•	Returns nearby events again based on user geolocation from CloudFront headers.

3. Authentication Lambda
	•	Provides authentication logic for API Gateway.
	•	Validates user credentials and API keys.
	•	Integrated into API Gateway as a custom Lambda Authorizer.

⸻
CloudFront
	•	Distributes traffic globally.
	•	Passes user geolocation to backend via headers such as:
	•	CloudFront-Viewer-Country
	•	CloudFront-Viewer-City (via geolocation features)

These headers are consumed by the Weather and Events Lambdas.

⸻
API Gateway
	•	Exposes REST endpoints for:
	•	/weather
	•	/events
	•	/auth
	•	Uses the Authentication Lambda as a custom authorizer.
	•	Connects downstream to Weather and Events Lambdas.

⸻
RDS (Relational Database Service)

Stores:
	•	User credentials (email, password hash, API KEY)
	•	User profile details
	•	User API keys

Connected via secure networking (private subnets, SGs, IAM roles).

⸻
Microservice Responsibilities

Weather Service
	•	Input: Location (lat/long and CloudFront city/country headers), API key (query string that gets converted to a header on cloudfront)
	•	Output: JSON weather data
	•	Dependencies: external weather API provider

Events Service (in development)
	•	Input: Same CloudFront geolocation data and api key
	•	Output: List of events near the user
	•	Dependencies: external events API provider

Authentication Service
Handles:
	•	API key validation
	•	Used as Lambda Authorizer in API Gateway

⸻

🔐 Security Overview
	•	All API endpoints sit behind API Gateway with the custom Lambda authorizer.
	•	EC2 instances run behind security groups with limited ingress.
	•	API keys stored inside RDS.
	•	CloudFront enforces HTTPS + geolocation header forwarding.
 (In development)
