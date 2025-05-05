# FastAPI Task Manager

A simple, production-ready FastAPI application that can be deployed to DigitalOcean's App Platform with no coding or infrastructure knowledge required, using Docker for reliable deployments.

## 📝 About

This project demonstrates how to build and deploy a FastAPI application to DigitalOcean App Platform in minutes using a no-code approach with Docker. It features:

- A RESTful API for managing tasks (create, read, update, delete)
- Interactive API documentation with Swagger UI
- Docker-based deployment for consistent environments
- Health check endpoint for monitoring

## 🚀 No-Code Docker Deployment

Deploy this application to DigitalOcean App Platform in just 3 simple steps:

1. Fork this repository to your GitHub account
2. Sign up for DigitalOcean using my [referral link](https://m.do.co/c/eddc62174250) to get $200 in credits
3. Use DigitalOcean's point-and-click interface to deploy:
   - Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
   - Click "Create App" → Select GitHub → Choose this repository
   - DigitalOcean will automatically detect the Dockerfile
   - Follow the simple on-screen instructions (all defaults work perfectly!)

No infrastructure management, no command line, no complex configuration!

## 📦 Project Structure

```
├── main.py             # FastAPI application
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration for deployment
└── README.md           # Project documentation
```

## ⚙️ Why Docker Deployment?

Using Docker for deployment offers several advantages:

- **Environment Consistency**: Same environment in development and production
- **No Configuration Needed**: DigitalOcean automatically detects and uses your Dockerfile
- **Security**: The container runs as a non-root user
- **Dependency Management**: All dependencies defined in one place
- **Portability**: The same container can run anywhere Docker is supported

## 🛠️ Local Development

### Prerequisites

- Python 3.8+ or Docker

### Setup with Python

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/fastapi-task-manager.git
   cd fastapi-task-manager
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

### Setup with Docker

1. Clone this repository
2. Build and run the Docker container:
   ```bash
   docker build -t fastapi-task-manager .
   docker run -p 8000:8000 fastapi-task-manager
   ```

3. Access the API at http://localhost:8000 and the docs at http://localhost:8000/docs

## 📚 API Documentation

Once deployed, your API documentation will be available at:
- Swagger UI: `https://your-app-url/docs`
- ReDoc: `https://your-app-url/redoc`

## 🔍 Task Manager API Features

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create a new task |
| GET | `/tasks/{task_id}` | Get a specific task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |
| GET | `/health` | Health check endpoint |

### Example Task Object

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Complete project",
  "description": "Finish the FastAPI project deployment",
  "is_completed": false,
  "created_at": "2025-05-05T12:00:00.000Z",
  "updated_at": "2025-05-05T12:00:00.000Z"
}
```

## 💻 Why DigitalOcean App Platform?

- **Dockerfile Detection**: Automatically recognizes and builds your Docker container
- **Truly No-Code Deployment**: Point, click, deploy - no infrastructure knowledge required
- **Automatic HTTPS**: Secure by default with free SSL certificates
- **GitHub Integration**: Changes to your code are automatically deployed
- **Scaling**: Easily scale up when you need more resources
- **Affordable**: Starting at just $5/month for hobby projects
- **Free Trial**: $200 in credits for 60 days with my referral link

## 🌟 Support the Developer

If you find this project helpful, please consider:

1. Signing up for DigitalOcean using my [referral link](https://m.do.co/c/eddc62174250)
2. Starring this repository on GitHub
3. Sharing it with others who might benefit

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
