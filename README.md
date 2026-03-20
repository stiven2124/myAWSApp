# AWS Weather API & User Portal

A cloud-native application featuring a custom API key management system, edge-based header transformation, and a serverless weather backend.

## 🏗️ Architecture

The application is structured into three primary layers to handle user management, request routing, and data delivery.

### 1. User Portal (EC2 Instance)
* **Web Server:** Nginx serves as the frontend proxy.
* **App Server:** Gunicorn runs the web application.
* **Flow:** Users register or log in to access a dashboard where their unique **API Key** is generated and displayed.

### 2. Edge Layer (CloudFront)
* **Behaviors:** Routes requests based on path patterns: `/weather`, `/forecast`, and `/apiKeyInfo`.
* **CloudFront Function:** For ease of use, the function intercepts the URL query parameter `?apikey=...` and converts it into a request header (`x-api-key`).
* **Geo-Location:** CloudFront forwards viewer location headers to the backend to provide localized weather data without asking for user coordinates.

### 3. Backend & Security (API Gateway + Lambda + RDS)
* **Custom Authorizer:** A Lambda function triggered by API Gateway. It extracts the `x-api-key` from the headers and validates it against the **RDS** database.
* **Logic:** * **Valid Key:** Request proceeds to the weather/info Lambdas.
    * **Invalid Key:** Returns a `401 Unauthorized` response.
* **Quota Management:** Each user starts with **1,000 API calls**. Every successful request decrements the count in the RDS.

---

## 🛠️ Infrastructure Details

### CloudFront Transformation Function
This function allows the user to simply paste their key into the browser URL while the backend receives it as a secure header.

```javascript
function handler(event) {
    var request = event.request;
    var querystring = request.querystring;

    // Move apikey from URL param to Header
    if (querystring.apikey) {
        request.headers['x-api-key'] = { value: querystring.apikey.value };
    }
    
    return request;
}
