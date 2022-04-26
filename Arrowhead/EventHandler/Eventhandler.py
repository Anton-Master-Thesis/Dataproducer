from Arrowhead.Orchestration.Orchestration import Orchestrator
from Arrowhead.Orchestration.Services import ServiceManager
from Arrowhead.EventHandler.Events import EventManager
from Arrowhead import SystemConfig

import warnings
import binascii
import urllib3
from requests_pkcs12 import get, post
import requests
import json
from datetime import timezone
import datetime

from Arrowhead.Security import SecurityManager

class EventHandler:
    def __init__(self):
        orch = Orchestrator()
        orch.testConnection()
        orchServices = orch.orchestrate()
        self.ehServices = {}
        for key in ServiceManager.services.keys():
            if key not in orchServices.keys():
                raise Exception("Unable to orchestrate required services")
        
        # Pick the first option for each service
        # More rigorous selection can be implemented
        for service, orchResponse in orchServices.items():
            self.ehServices[service] = orchResponse["response"][0]

    def testConnection(self):
        ehDesc = list(self.ehServices.values())[0]
        security = ehDesc["secure"]
        ehSystem = ehDesc["provider"]

        systemConfig = SystemConfig.loadConfig()
        certConfig = systemConfig["cert"]

        address = ehSystem["address"] + ":" + str(ehSystem["port"]) + "/eventhandler/echo"

        if security.lower() == "certificate":
             # Need to disable warning because AH main cert is not trusted
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            # Need to not verify cert because AH main cert is not trusted (verify=False)
            response = get("https://" + address, pkcs12_filename=certConfig["cloud_cert"], pkcs12_password=certConfig["cert_pass"], verify=False)
            # Reset warnings in case we need to verify other requests
            warnings.resetwarnings()
        elif security.lower() == "not_secure":
            response = get("http://" + address)

        if response.status_code != requests.codes.ok:
            raise Exception(response.status_code, response.text)


    def publish(self, event_type, data):
        ehDesc = list(self.ehServices.values())[0]
        security = ehDesc["secure"]
        ehSystem = ehDesc["provider"]

        systemConfig = SystemConfig.loadConfig()
        certConfig = systemConfig["cert"]

        address = ehSystem["address"] + ":" + str(ehSystem["port"]) + ehDesc["serviceUri"]

        req_body = EventManager.loadEvent(event_type)

        SecurityManager.generateKeys()
        payload = {}
        payload["data"] = data
        message = json.dumps(data).encode("utf-8")
        signature = SecurityManager.getSignature(message)
        payload["signature"] = binascii.hexlify(signature).decode('ascii')

        metadata = req_body["metaData"]
        metadata["systemName"] = systemConfig["system"]["systemName"]

        req_body["payload"] = json.dumps(payload)
        req_body["source"] = systemConfig["system"]
        timestamp = str(datetime.datetime.now(timezone.utc))
        milliIndex = timestamp.find(".")
        timestamp = timestamp.replace(" ", "T")
        req_body["timeStamp"] = timestamp[:]

        if security.lower() == "certificate":
             # Need to disable warning because AH main cert is not trusted
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            # Need to not verify cert because AH main cert is not trusted (verify=False)
            response = post("https://" + address, pkcs12_filename=certConfig["cloud_cert"], pkcs12_password=certConfig["cert_pass"], verify=False, json=req_body)
            # Reset warnings in case we need to verify other requests
            warnings.resetwarnings()
        elif security.lower() == "not_secure":
            response = post("http://" + address, json=req_body)

        if response.status_code != requests.codes.ok:
            raise Exception(response.status_code, response.text)
            