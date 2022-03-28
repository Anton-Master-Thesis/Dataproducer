import os
import json

class ServiceregistryConfig:
    serviceregistryConfig = {}

    basepath = os.path.abspath(os.path.dirname(__file__))
    # Load the orchestration configuration file which describes which service to connect to and where/how to contact the orchestrator
    @staticmethod
    def loadConfig():
        if not ServiceregistryConfig.serviceregistryConfig:
            srConfigpath = os.path.abspath(os.path.join(ServiceregistryConfig.basepath, "ServiceregistryConfig.json"))
            with open(srConfigpath, 'r') as f:
                ServiceregistryConfig.serviceregistryConfig = json.load(f)
        return ServiceregistryConfig.serviceregistryConfig