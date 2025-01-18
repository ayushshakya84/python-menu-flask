[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ayushshakya84_python-menu-flask&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ayushshakya84_python-menu-flask)
# Flask Web Application

## Overview
This is a web-based application built using Flask, providing features such as user authentication, dynamic content rendering, and local/remote system management. The project incorporates a database for user management and integrates security measures such as hashed passwords. Additionally, it is containerized with Docker for seamless deployment.

## Features
- **User Authentication**: Register, login, logout, and user-specific dashboard.
- **User Profile Management**: Update email and personal information.
- **Local Actions**:
  - Create files and folders.
  - Display system date and calendar.
  - Install software.
- **Remote Actions**:
  - Perform similar actions as local but on a remote machine via SSH.
- **Dynamic Menus**: Render different menus for local, remote, and networking actions.

## Technologies Used
- **Backend**: Flask
- **Database**: SQLite (via SQLAlchemy)
- **Frontend**: Jinja2 Templates
- **Authentication**: Flask-Login
- **Security**: Password hashing with Werkzeug
- **Containerization**: Docker
- **Code Quality**: Analyzed with SonarCloud

## Prerequisites
- Python 3.12
- Docker
- SonarCloud account (optional for code analysis)

## Installation and Setup

### Clone the Repository
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### Create a Virtual Environment and Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Initialize the Database
```bash
python
>>> from main import db
>>> db.create_all()
>>> exit()
```

### Run the Application
```bash
python main.py
```
Access the application at `http://localhost:80`.

### Docker Setup
#### Build the Docker Image
```bash
docker build -t flask-web-app .
```

#### Run the Docker Container
```bash
docker run -d -p 80:80 flask-web-app
```

Access the application at `http://localhost`.

## SonarCloud Analysis
To analyze the code quality with SonarCloud:
1. Configure SonarCloud for your repository.
2. Run the analysis using the SonarScanner:
   ```bash
   sonar-scanner \
     -Dsonar.projectKey=your_project_key \
     -Dsonar.organization=your_organization \
     -Dsonar.host.url=https://sonarcloud.io \
     -Dsonar.login=your_sonarcloud_token
   ```

## Project Structure
```
project/
├── main.py            # Application entry point
├── templates/         # HTML templates
├── static/            # Static files (CSS, JS, images)
├── models.py          # Database models
├── requirements.txt   # Python dependencies
├── Dockerfile         # Docker configuration
├── README.md          # Project documentation
└── ...
```

## Environment Variables
- `SECRET_KEY`: The secret key for Flask application security.
- `SQLALCHEMY_DATABASE_URI`: URI for the database connection.
- `PORT`: The port number for the application (default: 80).

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any feature requests, bug fixes, or improvements.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements
- Flask documentation
- SQLAlchemy for ORM
- Docker for containerization
- SonarCloud for code quality analysis

