class SharedKnowledge:
    def __init__(self):
        self.known_victims = []
        self.known_hazards = []
        self.agent_assignments = {}  # Tracks who is doing what
        self.rescue_log = []         # For the frontend event dashboard

    def log_event(self, message):
        self.rescue_log.append(message)
        print(f"[LOG] {message}")

knowledge_base = SharedKnowledge()