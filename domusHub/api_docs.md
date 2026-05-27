# DomusHub API Documentation

This document explains the available API endpoints for DomusHub, what parameters they accept, and how to authenticate.

---

## Base URL
*   **Local Development:** `http://127.0.0.1:8000`
*   **Production Deployment:** `https://domushub.onrender.com`

---

## Authentication Methods

The API accepts two types of authentication depending on how you configure your client app:

1.  **JWT (JSON Web Tokens):** Pass the access token in the request header like this:
    ```text
    Authorization: Bearer <your_access_token>
    ```
2.  **Standard Token Authentication:** Pass your persistent DRF auth token like this:
    ```text
    Authorization: Token <your_auth_token>
    ```

---

## Endpoints List

### 1. Generate JWT Access Tokens
*   **URL Path:** `/api/token/`
*   **HTTP Method:** `POST`
*   **Authentication Required:** No
*   **Request Body (JSON):**
    ```json
    {
      "username": "agent_michael",
      "password": "Password123!"
    }
    ```
*   **Success Response (`200 OK`):**
    ```json
    {
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

### 2. Refresh Expired JWT Token
*   **URL Path:** `/api/token/refresh/`
*   **HTTP Method:** `POST`
*   **Authentication Required:** No
*   **Request Body (JSON):**
    ```json
    {
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```
*   **Success Response (`200 OK`):**
    ```json
    {
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

### 3. Get All Properties (Paginated)
*   **URL Path:** `/api/properties/`
*   **HTTP Method:** `GET`
*   **Authentication Required:** No
*   **Query Parameters (Optional):**
    *   `page`: The page number to fetch (Default is 1).
    *   `search`: Filter properties by title, address, or category name.
    *   `ordering`: Order by fields like `price`, `-price`, `created_at`, or `-created_at`.
    *   `category__slug`: Filter specifically by a category's URL slug (e.g., `duplex`).
*   **Success Response (`200 OK`):**
    ```json
    {
      "count": 14,
      "next": "https://domushub.onrender.com/api/properties/?page=2",
      "previous": null,
      "results": [
        {
          "id": 5,
          "title": "Modern 3 Bedroom Flat",
          "property_address": "Plot 9 lekki ajah road",
          "description": "Newly built flat with running water and 24/7 security.",
          "price": "4500000.00",
          "status": "AVAILABLE",
          "image": "https://cloudinary.com",
          "created_at": "2026-05-27T14:09:47Z",
          "category": 1,
          "owner": 2
        }
      ]
    }
    ```

### 4. Create a Property Listing
*   **URL Path:** `/api/properties/`
*   **HTTP Method:** `POST`
*   **Authentication Required:** Yes (JWT Bearer or DRF Token)
*   **Request Content-Type:** `multipart/form-data` (Required because you are uploading an image file).
*   **Form Data Fields:**
    *   `title` (String, Required)
    *   `property_address` (String, Required)
    *   `description` (String, Optional)
    *   `price` (Decimal, Required)
    *   `category` (Integer ID, Required)
    *   `status` (String: `AVAILABLE`, `PENDING`, `UNDER_OFFER`, or `SOLD`)
    *   `image` (File binary, Optional)
*   **Success Response (`201 Created`):**
    ```json
    {
      "id": 6,
      "title": "Modern 3 Bedroom Flat",
      "property_address": "Plot 9 lekki ajah road",
      "description": "Newly built flat with running water and 24/7 security.",
      "price": "4500000.00",
      "status": "AVAILABLE",
      "image": "https://cloudinary.com",
      "created_at": "2026-05-27T14:15:22Z",
      "category": 1,
      "owner": 2
    }
    ```

---

## Common Error Codes

*   **`400 Bad Request`:** Missing required form data fields or invalid numeric inputs (e.g., passing text instead of a number for `price`).
*   **`401 Unauthorized`:** Missing, expired, or malformed authentication header.
*   **`403 Forbidden`:** The token is valid, but the logged-in user account doesn't have permissions to perform the action.
