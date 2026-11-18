const API_URL = "http://127.0.0.1:8000";
let simulationInterval = null;

async function fetchEnvironment() {
    try {
        const response = await fetch(`${API_URL}/api/environment`);
        const data = await response.json();
        renderGrid(data);
    } catch (error) {
        console.error("Error fetching environment:", error);
    }
}

async function stepSimulation() {
    try {
        const algo = document.getElementById("algo-select").value;
        const response = await fetch(`${API_URL}/api/step?algo=${algo}`, { method: "POST" });
        const data = await response.json();
        renderGrid(data);
    } catch (error) {
        console.error("Error stepping simulation:", error);
    }
}

function renderGrid(data) {
    const { grid, size, agents, logs } = data;
    const gridContainer = document.getElementById("grid-container");
    gridContainer.innerHTML = "";
    
    gridContainer.style.gridTemplateColumns = `repeat(${size}, 30px)`;
    gridContainer.style.gridTemplateRows = `repeat(${size}, 30px)`;

    for (let r = 0; r < size; r++) {
        for (let c = 0; c < size; c++) {
            const cellElement = document.createElement("div");
            cellElement.classList.add("cell");
            
            // 1. Check if an agent is currently on this tile
            const agentHere = agents.find(a => a.pos[0] === r && a.pos[1] === c);
            const cellValue = grid[r][c];

            if (agentHere) {
                cellElement.classList.add("cell-agent");
                cellElement.textContent = "A";
            } 
            // 2. Otherwise render the environment
            else if (cellValue === ".") cellElement.classList.add("cell-safe");
            else if (cellValue === "#") cellElement.classList.add("cell-obs");
            else if (cellValue === "F") {
                cellElement.classList.add("cell-F");
                cellElement.textContent = "F";
            }
            else if (cellValue === "V") {
                cellElement.classList.add("cell-V");
                cellElement.textContent = "V";
            }
            else if (cellValue === "R") {
                cellElement.classList.add("cell-R");
                cellElement.textContent = "R";
            }

            gridContainer.appendChild(cellElement);
        }
    }
    
    updateLogs(logs);
}

function updateLogs(logs) {
    const logList = document.getElementById("log-list");
    logList.innerHTML = "";
    logs.forEach(log => {
        const li = document.createElement("li");
        li.textContent = log;
        logList.appendChild(li);
    });
    
    // UI FIX: Wait for DOM to render, then force scroll to absolute bottom
    const logContainer = document.querySelector(".log-area");
    setTimeout(() => {
        logContainer.scrollTo({
            top: logContainer.scrollHeight,
            behavior: 'smooth'
        });
    }, 10);
}

// Attach event listener to Start button
document.getElementById("start-btn").addEventListener("click", () => {
    if (!simulationInterval) {
        simulationInterval = setInterval(stepSimulation, 500); // Step every 500ms
        document.getElementById("start-btn").textContent = "Simulation Running...";
        document.getElementById("start-btn").disabled = true;
    }
});

window.onload = fetchEnvironment;
// Attach event listener to Spawn Hazard button
document.getElementById("hazard-btn").addEventListener("click", async () => {
    try {
        await fetch(`${API_URL}/api/spawn_hazard`, { method: "POST" });
    } catch (error) {
        console.error("Error spawning hazard:", error);
    }
});