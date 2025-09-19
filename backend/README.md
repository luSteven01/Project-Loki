# Project Loki Backend

## Prerequisites

- Python 3.8+
- Git
- OpenAI API Key
- MongoDB Atlas account (or local MongoDB) - Open network access 0.0.0.0

## Quick Setup

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd Project-Loki
```

### 2. Environment Configuration
Create `.env` file in the **root directory** (not in backend folder):
```
OPENAI_API_KEY=sk-your-openai-key-here
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/AI_game?retryWrites=true&w=majority
DATABASE_NAME=AI_game
```

### 3. MongoDB Atlas Setup (Required)
1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Set up database with network access 0.0.0.0/0

## Running with Virtual Environment

### 1. Create and Activate Virtual Environment
```bash
# From project root directory
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 2. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Run the Application
```bash
# Make sure you're in the backend directory
uvicorn main:app --reload
Or 
python main.py
```

### 4. Access the Application
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Test Interface: http://localhost:8000/static/index.html

### 5. Deactivate Virtual Environment (when done)
```bash
deactivate
```

## Alternative: Running with Docker (Recommended)

### Start Services
```bash
cd backend
docker-compose up --build
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f detective-api
```

## Project Structure
```
Project-Loki/
├── .env                    # Environment variables
├── .gitignore             # Git ignore rules
├── venv/                  # Virtual environment
└── backend/
    ├── main.py            # FastAPI application
    ├── requirements.txt   # Python dependencies
    ├── services.py        # Business logic
    ├── story.py           # Story management
    ├── prompt.py          # AI prompts
    ├── Dockerfile         # Docker configuration
    ├── docker-compose.yml # Container orchestration
    └── static/
        └── index.html     # Test web interface
```

## Development Notes

- Make sure your `.env` file is in the project root directory
- The virtual environment approach is recommended for development
- Use Docker for production deployment
- API will be available at http://localhost:8000 when running