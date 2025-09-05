## Prerequisites

- Docker Desktop
- Git
- OpenAI API Key
- MongoDB Atlas account (or local MongoDB)

## Quick Setup

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd detective-game/backend
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
2. I'll add you to mongodb altas




## Project Structure
```
detective-game/
├── .env                    # Environment variables
├── .gitignore             # Git ignore rules
└── backend/
    ├── main.py            # FastAPI application
    ├── requirements.txt   # Python dependencies
    ├── Dockerfile         # Docker configuration
    ├── docker-compose.yml # Container orchestration
    └── static/
        └── index.html     # Test web interface
```

## Development Commands

### Start Services
```bash
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

### Rebuild After Changes
```bash
docker-compose down
docker-compose up --build
```