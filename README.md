
# ResQ AI | Adaptive Multi-Agent Disaster Rescue System 🚁

An intelligent, multi-agent disaster response simulation designed to solve dynamic pathfinding, task prioritization, and real-time coordination in unpredictable environments.

## 📌 The Problem

In real-world disasters, conditions change rapidly. A static shortest-path algorithm fails because it ignores sudden hazards, resource bottlenecks, and varying victim urgencies.

Disaster rescue requires a system capable of understanding the situation, prioritizing tasks mathematically, and recalculating routes dynamically when the environment changes.

## 🏗️ System Architecture

This project implements a decoupled full-stack architecture that separates the simulation engine from the visualization dashboard.

- **Backend (Python / FastAPI):** Houses the A* pathfinding engine, Breadth-First Search (BFS) baseline, multi-agent coordination logic, and shared knowledge state.
- **Frontend (Vanilla JavaScript / HTML / CSS Grid):** An asynchronous visual dashboard that polls the backend for simulation steps, rendering the grid environment and live event logs in real time.

## 🧠 Core Algorithmic Features

### 1. Heuristic Pathfinding (A* vs. BFS)

The routing engine compares two graph traversal algorithms:

- **A* Search (Intelligent):** Utilizes a Priority Queue (min-heap) and calculates:

  `f(n) = g(n) + h(n) + R(n)`

  It uses **Manhattan distance** as its heuristic `h(n)` to efficiently target victims while applying a significant cost penalty `R(n)` to cells containing hazards (such as fire).

- **BFS (Baseline):** Utilizes a standard Deque for level-order traversal without heuristic guidance.

- **Result:** The simulation demonstrates the algorithmic trade-offs. A* completes tasks while exploring approximately **14–25 nodes**, whereas BFS explores approximately **110+ nodes**.

### 2. Multi-Agent Coordination

Three specialized agents work in parallel, communicating through a **Shared Knowledge State**:

- 🔍 **Victim Search Agent:** Scans the grid, locates victims, and assesses their severity (Critical vs. Moderate).
- 🗺️ **Route Planning Agent:** Retrieves information from the shared state to calculate hazard-avoiding A* paths.
- 🎒 **Supply Agent:** Manages and allocates resources to active rescue tasks.

### 3. Priority-Based Task Allocation

Tasks are dynamically assigned using a priority function rather than relying solely on proximity:

`P = w₁S + w₂D + w₃R + w₄H`

This function balances:

- **S:** Victim severity
- **D:** Distance
- **R:** Resource requirements
- **H:** Hazard risk

The weights (`w₁`, `w₂`, `w₃`, and `w₄`) determine the relative importance of each factor.

### 4. Dynamic Replanning

The environment is not static. If a sudden fire appears directly on an active agent's path:

1. The agent detects the newly introduced hazard.
2. The agent halts its current movement.
3. A `⚠️ HAZARD DETECTED` event is logged.
4. The current trajectory is cleared.
5. The A* algorithm recalculates a new, hazard-avoiding route.

This enables the system to adapt to unexpected environmental changes in real time.

---

## 🚀 How to Run Locally

### 1. Set Up the Backend Server

Ensure Python is installed, then create and activate a virtual environment.

**Create a virtual environment:**

```bash
python -m venv venv
```

**Activate the virtual environment:**

Windows:
```bash
.\venv\Scripts\activate
```

macOS / Linux:
```bash
source venv/bin/activate
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

**Start the FastAPI engine:**

```bash
uvicorn backend.main:app --reload
```

The backend server will run at:

`http://127.0.0.1:8000`

### 2. Launch the Dashboard

1. Open the project in VS Code.
2. Navigate to the `frontend` directory.
3. Right-click `index.html` and select **Open with Live Server**.
4. Select your preferred algorithm (A* or BFS).
5. Click **Start Simulation**.
6. Use the **Spawn Sudden Fire** button to test dynamic replanning.

---

## 🎯 Project Objective

ResQ AI demonstrates how intelligent pathfinding, multi-agent coordination, mathematical task prioritization, and dynamic replanning can work together to simulate an adaptive disaster rescue system.
