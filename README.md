# ResQ AI | Adaptive Multi-Agent Disaster Rescue System 🚁

An intelligent, multi-agent disaster response simulation designed to solve dynamic pathfinding, task prioritization, and real-time coordination in unpredictable environments.

## 📌 The Problem
In real-world disasters, conditions change rapidly. A static shortest-path algorithm fails because it ignores sudden hazards, resource bottlenecks, and varying victim urgencies. Disaster rescue requires a system capable of reading a situation, prioritizing tasks mathematically, and recalculating routes on the fly when the environment shifts.

## 🏗️ System Architecture
This project implements a decoupled full-stack architecture to separate the simulation engine from the visualization dashboard:
- **Backend (Python / FastAPI):** Houses the A* pathfinding engine, Breadth-First Search (BFS) baseline, multi-agent coordination logic, and the shared knowledge state.
- **Frontend (Vanilla JS / HTML / CSS Grid):** An asynchronous visual dashboard that polls the backend simulation steps, rendering the grid environment and live event logs in real-time.

## 🧠 Core Algorithmic Features

### 1. Heuristic Pathfinding (A* vs. BFS)
The routing engine compares two graph traversal algorithms:
- **A* Search (Intelligent):** Utilizes a Priority Queue (min-heap) and calculates `f(n) = g(n) + h(n) + R(n)`. It uses the **Manhattan distance** as its heuristic `h(n)` to aggressively target victims, while applying a massive cost penalty `R(n)` to cells containing hazards (fire).
- **BFS (Baseline):** Utilizes a standard Deque for level-order traversal. 
- *Result:* The simulation mathematically demonstrates algorithmic trade-offs; A* completes tasks exploring ~14-25 nodes, while BFS blindly explores ~110+ nodes.

### 2. Multi-Agent Coordination
Three specialized agents work in parallel, communicating via a **Shared Knowledge** state:
- 🔍 **Victim Search Agent:** Scans the grid, locates victims, and assesses severity (Critical vs. Moderate).
- 🗺️ **Route Planning Agent:** Pulls from the shared state to calculate hazard-avoidant A* paths.
- 🎒 **Supply Agent:** Manages and allocates resources to active rescue tasks.

### 3. Priority-Based Task Allocation
Tasks are dynamically assigned using a priority function rather than pure proximity:
`P = w₁S + w₂D + w₃R + w₄H`
*(Balancing Victim Severity, Distance, Resource requirements, and Hazard risk).*

### 4. Dynamic Replanning
The environment is not static. If a sudden fire spawns directly on an active agent's path, the agent halts, logs a `⚠️ HAZARD DETECTED` event, clears its current trajectory, and instantly recalculates a new A* route around the obstacle.

---

## 🚀 How to Run Locally

### 1. Setup the Backend Server
Ensure you have Python installed, then set up your virtual environment and dependencies:
```bash
# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI engine
uvicorn backend.main:app --reload

