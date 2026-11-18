from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.environment import env_state
from backend.shared_knowledge import knowledge_base
from backend.agents import BaseAgent, VictimSearchAgent, RoutePlanningAgent, SupplyAgent

app = FastAPI(title="ResQ AI Simulation Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Multi-Agent System
rescue_unit = BaseAgent("RescueUnit-1", (0, 0))
search_agent = VictimSearchAgent("SearchAgent-1", (0, 0))
route_agent = RoutePlanningAgent()
supply_agent = SupplyAgent("SupplyAgent-1", (0, 0))
agents_list = [rescue_unit]

@app.get("/")
def read_root():
    return {"status": "ResQ AI Backend is running"}

@app.get("/api/environment")
def get_environment():
    state = env_state.get_state()
    state["agents"] = [{"name": a.name, "pos": a.pos} for a in agents_list]
    state["logs"] = knowledge_base.rescue_log
    return state

@app.post("/api/step")
def step_simulation(algo: str = "A*"):
    search_agent.scan_environment(env_state)
    
    if not rescue_unit.current_path and not rescue_unit.target:
        route_agent.assign_tasks_and_plan(env_state, agents_list, algorithm=algo)
        if rescue_unit.target:
            supply_agent.prepare_supplies(rescue_unit.target)
            
    if rescue_unit.current_path:
        next_step = rescue_unit.current_path[0]
        
        if env_state.grid[next_step[0]][next_step[1]] == 'F':
            knowledge_base.log_event(f"⚠️ HAZARD DETECTED at {next_step}! Replanning route...")
            rescue_unit.current_path = []
            route_agent.assign_tasks_and_plan(env_state, agents_list, algorithm=algo) 
            return get_environment()

        next_step = rescue_unit.current_path.pop(0)
        rescue_unit.pos = next_step
        knowledge_base.log_event(f"{rescue_unit.name} moved to {next_step}")
        
        if rescue_unit.target and rescue_unit.pos == rescue_unit.target['pos']:
            knowledge_base.log_event(f"✅ Victim {rescue_unit.target['id']} successfully RESCUED!")
            for v in env_state.victims:
                if v['id'] == rescue_unit.target['id']:
                    v['rescued'] = True
                    env_state.grid[v['pos'][0]][v['pos'][1]] = '.' 
            rescue_unit.target = None
            rescue_unit.current_path = [] 
            
    return get_environment()

@app.post("/api/spawn_hazard")
def spawn_hazard():
    if rescue_unit.current_path and len(rescue_unit.current_path) > 2:
        # Drop fire exactly 2 steps ahead to guarantee the agent sees it
        target_cell = rescue_unit.current_path[1]
        env_state.grid[target_cell[0]][target_cell[1]] = 'F'
        env_state.hazards.append(target_cell)
        knowledge_base.log_event(f"🔥 *** SUDDEN FIRE SPAWNED at {target_cell} ***")
    return {"status": "Hazard spawned"}