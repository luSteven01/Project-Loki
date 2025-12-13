# Project-Loki

A detective mystery game built with Godot 4.5 and powered by AI-driven dialogue. Players investigate the case of Professor Richards by interviewing suspects, collecting evidence, and solving the mystery.

## Prerequisites

- **Godot 4.5** - [Download here](https://godotengine.org/download)
- **Python 3.8+**
- **Git**
- **MongoDB** - For storing game sessions and progress
- **OpenAI API Key** - For AI-powered character dialogue

## Project Structure

```
Project-Loki/
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore rules
├── README.md              # This file
│
├── backend/               # FastAPI backend server
│   ├── main.py           # API server entry point
│   ├── services.py       # Business logic and database
│   ├── characters.py     # Character data and prompts
│   ├── story.py          # Story and narrative data
│   ├── evidence.py       # Evidence system
│   ├── requirements.txt  # Python dependencies
│   ├── Dockerfile        # Docker configuration
│   ├── docker-compose.yml # Docker compose setup
│   └── prompts/          # AI prompt templates
│
├── godot/                # Godot 4.5 game project
│   ├── project.godot     # Godot project file
│   ├── main.gd           # Main game script
│   ├── player.gd         # Player controller
│   ├── game_manager.gd   # Game state manager
│   ├── SceneManager.gd   # Scene management
│   ├── dialogue/         # Dialogue system
│   ├── evidence/         # Evidence UI and logic
│   ├── art/              # Art assets
│   └── Assets/           # Game assets
│
└── venv/                 # Python virtual environment (created during setup)
```

## Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd Project-Loki
```

### 2. MongoDB Setup

Install and start MongoDB on your system:

**macOS (using Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Ubuntu/Debian:**
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**Windows:**
Download and install from [MongoDB Download Center](https://www.mongodb.com/try/download/community)

### 3. Environment Configuration

Create a `.env` file in the **root directory** (Project-Loki/.env):

**Note:** If MongoDB is running on a different host or port, update the `MONGODB_URL` accordingly.

### 3. Backend Setup

#### Option A: Using Python Virtual Environment (Recommended for Development)

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run the backend server
cd backend
python main.py
```

The API server will start at `http://localhost:8000`

#### Option B: Using Docker

```bash
cd backend
docker-compose up --build
```

### 4. Godot Game Setup

1. Open **Godot 4.5**
2. Click **Import**
3. Navigate to `Project-Loki/godot/` and select `project.godot`
4. Click **Import & Edit**

## Running the Game

### Start the Backend

Make sure the backend server is running first:

```bash
# If using virtual environment
cd backend
source ../venv/bin/activate  # On Windows: ..\venv\Scripts\activate
python main.py
```

Or with Docker:

```bash
cd backend
docker-compose up
```

You should see: `Uvicorn running on http://0.0.0.0:8000`

### Run the Game

1. Open the project in Godot 4.5
2. Press **F5** or click the **Play** button
3. The game will connect to the backend at `http://localhost:8000`

## Development Notes

- The `.env` file must be in the **project root directory** (not in backend/)
- The backend API must be running before starting the Godot game
- Backend runs on port **8000** by default
- Game resolution: 1920x1080 (fullscreen mode)

## API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
