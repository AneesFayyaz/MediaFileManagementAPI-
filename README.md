# MediaFileManagementAPI 
## Table of Contents 
1. [Introduction](#introduction) 
2. [Features](#features) 
3. [Installation](#installation) 
4. [File Management](#file-management) 
5. [Project Structure](#project-structure) 
6. [Acknowledgments](#acknowledgments) 
---
## Introduction 
MediaFileManagementAPI is a Django REST API that provides a robust solution for uploading, managing, and tracking metadata of media files. The API includes JWT-based user authentication, detailed change logs for metadata, and secure CRUD operations.
---
## Features 
- **JWT Authentication**: Secure and token-based user authentication. 
- **File Uploads**: Seamless file uploads with metadata tracking. 
- **Change Logs**: Tracks updates to file metadata for auditing purposes. 
- **CRUD Operations**: Full set of operations to create, retrieve, update, and delete files. 
- **Scalable Architecture**: Built using Django REST Framework for high scalability. 
---
## Installation 
### Prerequisites 
- Python 3.x installed on your machine. 
- Git installed for version control. 
- Virtual environment manager (optional but recommended). 
---
### Step 1: Clone the repository 
```bash
git clone https://github.com/your-username/MediaFileManagementAPI.git
cd MediaFileManagementAPI
```
#### Step 2: Create a Virtual Environment 
Create and activate a virtual environment 
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```
#### Step 3: Apply database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
#### Step 4: Run the development server
```bash
python manage.py runserver
```
## File Management
- **Create**: Upload media files via the `/upload/` endpoint.
- **Read**: Retrieve file metadata using `GET /upload/`.
- **Update**: Modify file metadata with `PUT` or `PATCH`. Logs track changes.
- **Delete**: Remove files with `DELETE /upload/<file_id>/`.


## Acknowledgments
- **Django REST Framework** for powering the API.
- **Python** for being the foundation of the project.
- Open-source contributors who inspire and improve the community.

