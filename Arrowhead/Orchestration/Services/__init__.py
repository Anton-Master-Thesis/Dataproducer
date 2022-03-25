from pathlib import Path
import json
import os
import glob

class ServiceManager:
    services = {}

    @staticmethod
    def loadServices():
        path = basepath = os.path.abspath(os.path.dirname(__file__))
        servicespath = glob.glob(path + "/*.json")
        cleanServicesPath = []
        for sub in servicespath:
            if ".schema." not in sub:
                cleanServicesPath.append(sub)
        for sub in cleanServicesPath:
            with open(sub, 'r') as f:
                ServiceManager.services[Path(sub).stem] = (json.load(f))