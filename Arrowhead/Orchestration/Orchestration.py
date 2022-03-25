from requests_pkcs12 import post, get
from Arrowhead import SystemConfig
from Arrowhead.Orchestration import OrchestrationConfig
from Arrowhead.Orchestration.Services import ServiceManager
import urllib3
import warnings
import requests
import json
import os


class Orchestrator:

    def __init__(self):
        pass

    # Starts the orchestration process
    # Raises Exception if the http resonse code from the orchestrator is not 2xx or 3xx
    def orchestrate(self):
        config = OrchestrationConfig.loadConfig()
        cloudConfig = config["orchestrationConfig"]
        systemConfig = SystemConfig.loadConfig()
        certConfig = systemConfig["cert"]

        ServiceManager.loadServices()
        
        serviceDescriptions = {}

        # build the adress to request
        adress = cloudConfig["ip"] + ":" + str(cloudConfig["port"]) + "/orchestrator/orchestration"
        for service, orchRequest in ServiceManager.services.items():
            # build the orchestration request payload
            payload = {}
            payload["requesterSystem"] = systemConfig["system"]
            payload["requestedService"] = orchRequest["requestedService"]
            payload["orchestrationFlags"] = orchRequest["orchestrationFlags"]

            # check if we need to use http or https
            if cloudConfig["secure"]:
                # Need to disable warning because AH main cert is not trusted
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                # Need to not verify cert because AH main cert is not trusted (verify=False)
                response = post("https://" + adress, pkcs12_filename=certConfig["cloud_cert"], pkcs12_password=certConfig["cert_pass"], verify=False, json=payload)
                # Reset warnings in case we need to verify other requests
                warnings.resetwarnings()
            else :
                response = post("http://" + adress, json=payload)

            # Check if request was successful
            if response.status_code != requests.codes.ok:
                print("Unable to orchestrate service", service, response.status_code, response.json())
                continue

            serviceDescriptions[service] = response.json()
        return serviceDescriptions

    # Tests the connection via the /echo endpoint of the orchestrator
    # Raises exception if connection could not be established
    def testConnection(self):
        config = OrchestrationConfig.loadConfig()

        cloudConfig = config["orchestrationConfig"]
        systemConfig = SystemConfig.loadConfig()
        certConfig = systemConfig["cert"]

        adress = cloudConfig["ip"] + ":" + str(cloudConfig["port"]) + "/orchestrator/echo"
        if cloudConfig["secure"]:
            # Need to disable warning because AH main cert is not trusted
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            # Need to not verify cert because AH main cert is not trusted (verify=False)
            response = get("https://" + adress, pkcs12_filename=certConfig["cloud_cert"], pkcs12_password=certConfig["cert_pass"], verify=False)
            # Reset warnings in case we need to verify other requests
            warnings.resetwarnings()
        else:
            response = get("http://" + adress)

        # Check if request was successful
        if response.status_code != requests.codes.ok:
            raise Exception(response.status_code, "Unable to connect to the orchestrator")
