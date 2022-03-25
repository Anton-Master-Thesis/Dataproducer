import os
import json

class SystemConfig:
    system = {}

    basepath = os.path.abspath(os.path.dirname(__file__))
    @staticmethod
    def loadConfig():
        if not SystemConfig.system:
            systemConfigpath = os.path.abspath(os.path.join(SystemConfig.basepath, "SystemConfig.json"))
            with open(systemConfigpath, 'r') as f:
                SystemConfig.system = json.load(f)
        return SystemConfig.system