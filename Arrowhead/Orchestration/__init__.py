import os
import json

class OrchestrationConfig:
    orchestrationConfig = {}

    basepath = os.path.abspath(os.path.dirname(__file__))
    # Load the orchestration configuration file which describes which service to connect to and where/how to contact the orchestrator
    @staticmethod
    def loadConfig():
        if not OrchestrationConfig.orchestrationConfig:
            orchConfigpath = os.path.abspath(os.path.join(OrchestrationConfig.basepath, "OrchestrationConfig.json"))
            with open(orchConfigpath, 'r') as f:
                OrchestrationConfig.orchestrationConfig = json.load(f)
        return OrchestrationConfig.orchestrationConfig