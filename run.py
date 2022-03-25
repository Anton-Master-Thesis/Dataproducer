from Arrowhead.Orchestration.Orchestration import Orchestrator


if __name__ == "__main__":
    orch = Orchestrator()
    orch.testConnection()
    print(orch.orchestrate())