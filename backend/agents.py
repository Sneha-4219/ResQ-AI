from backend.shared_knowledge import knowledge_base
from backend.pathfinding import bfs_search
from backend.pathfinding import a_star_search, heuristic

class BaseAgent:
    def __init__(self, name, start_pos):
        self.name = name
        self.pos = start_pos
        self.current_path = []
        self.target = None

class VictimSearchAgent(BaseAgent):
    def scan_environment(self, env_state):
        # In this simulation step, the agent discovers all victims
        for v in env_state.victims:
            if v not in knowledge_base.known_victims and not v['rescued']:
                knowledge_base.known_victims.append(v)
                knowledge_base.log_event(f"Search Agent identified Victim {v['id']} at {v['pos']} ({v['severity']})")

class RoutePlanningAgent:
    def assign_tasks_and_plan(self, env_state, agents, algorithm="A*"):
        active_agent = agents[0]
        
        if active_agent.target and not active_agent.current_path:
            # Replan around fire
            path, nodes = a_star_search(env_state.grid, active_agent.pos, active_agent.target['pos'])
            active_agent.current_path = path
            knowledge_base.log_event(f"Route Agent recalculated new A* path avoiding hazard! (Nodes Explored: {nodes})")
            return

        unassigned_victims = [v for v in knowledge_base.known_victims if not v['rescued'] and v['id'] not in knowledge_base.agent_assignments.values()]
        if not unassigned_victims: return

        # Priority Queue based on severity
        unassigned_victims.sort(key=lambda x: (1 if x['severity'] == 'Critical' else 2, heuristic(active_agent.pos, x['pos'])))
        target_victim = unassigned_victims[0]
        
        active_agent.target = target_victim
        knowledge_base.agent_assignments[active_agent.name] = target_victim['id']
        
        # Choose algorithm based on dropdown
        if algorithm == "BFS":
            path, nodes = bfs_search(env_state.grid, active_agent.pos, target_victim['pos'])
        else:
            path, nodes = a_star_search(env_state.grid, active_agent.pos, target_victim['pos'])
            
        active_agent.current_path = path
        knowledge_base.log_event(f"Calculated {algorithm} path for {active_agent.name} to {target_victim['id']} (Explored {nodes} nodes)")

class SupplyAgent(BaseAgent):
    def prepare_supplies(self, target_victim):
        if target_victim:
            knowledge_base.log_event(f"Supply Agent allocated resources for Victim {target_victim['id']}")