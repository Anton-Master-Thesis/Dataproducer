from atexit import unregister
from requests_pkcs12 import post, get, delete
from Arrowhead import SystemConfig
from Arrowhead.Serviceregistry import ServiceregistryConfig
from Arrowhead.Serviceregistry.Services import ServiceManager
import urllib3
import warnings
import requests
import json
import os

class Serviceregistry:

    def __init__(self):
        pass

    def testConnection(self):
        config = ServiceregistryConfig.loadConfig()

        cloudConfig = config["serviceregistryConfig"]
        systemConfig = SystemConfig.loadConfig()
        certConfig = systemConfig["cert"]

        adress = cloudConfig["ip"] + ":" + str(cloudConfig["port"]) + "/serviceregistry/echo"
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

    def registerProviders(self):
        config = ServiceregistryConfig.loadConfig()
        cloudConfig = config["serviceregistryConfig"]
        systemConfig = SystemConfig.loadConfig()
        certConfig = systemConfig["cert"]

        adress = cloudConfig["ip"] + ":" + str(cloudConfig["port"]) + "/serviceregistry/register"

        services = ServiceManager.loadServices()
        for service, serviceRequest in services.items():
            payload = serviceRequest

            payload["providerSystem"] = systemConfig["system"]

            if cloudConfig["secure"]:
                # Need to disable warning because AH main cert is not trusted
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                # Need to not verify cert because AH main cert is not trusted (verify=False)
                response = post("https://" + adress, pkcs12_filename=certConfig["cloud_cert"], pkcs12_password=certConfig["cert_pass"], verify=False, json=payload)
                # Reset warnings in case we need to verify other requests
                warnings.resetwarnings()
            else:
                response = post("http://" + adress, json=payload)

            if response.status_code != requests.codes.created:
                print("Unable to orchestrate service ", service, response.status_code, response.json())
                print("Trying to re-register service", service)
                self.unregisterProvider(service)
                self.registerProvider(service)
                #raise Exception("Unable to register service")

    def registerProvider(self, service):
        config = ServiceregistryConfig.loadConfig()
        cloudConfig = config["serviceregistryConfig"]
        systemConfig = SystemConfig.loadConfig()
        certConfig = systemConfig["cert"]

        adress = cloudConfig["ip"] + ":" + str(cloudConfig["port"]) + "/serviceregistry/register"

        services = ServiceManager.loadServices()

        serviceRequest = services[service]

        payload = serviceRequest

        payload["providerSystem"] = systemConfig["system"]

        if cloudConfig["secure"]:
            # Need to disable warning because AH main cert is not trusted
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            # Need to not verify cert because AH main cert is not trusted (verify=False)
            response = post("https://" + adress, pkcs12_filename=certConfig["cloud_cert"], pkcs12_password=certConfig["cert_pass"], verify=False, json=payload)
            # Reset warnings in case we need to verify other requests
            warnings.resetwarnings()
        else:
            response = post("http://" + adress, json=payload)


    def unregisterProviders():
        config = ServiceregistryConfig.loadConfig()
        cloudConfig = config["serviceregistryConfig"]
        systemConfig = SystemConfig.loadConfig()
        
        certConfig = systemConfig["cert"]

        baseadress = cloudConfig["ip"] + ":" + str(cloudConfig["port"]) + "/serviceregistry/deregister"

        services = ServiceManager.loadServices()
        for service, serviceRequest in services.items():
            address = baseadress + "?serviceDefinition=" + serviceRequest["serviceDefinition"]
            address += "&address=" + systemConfig["system"]["address"]
            address += "&port=" + systemConfig["system"]["port"]
            address += "&system_name=" + systemConfig["system"]["systemName"]
            if cloudConfig["secure"]:
                # Need to disable warning because AH main cert is not trusted
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                # Need to not verify cert because AH main cert is not trusted (verify=False)
                response = delete("https://" + address, pkcs12_filename=certConfig["cloud_cert"], pkcs12_password=certConfig["cert_pass"], verify=False)
                # Reset warnings in case we need to verify other requests
                warnings.resetwarnings()
            else:
                response = delete("http://" + address)

    def unregisterProvider(self, service):
        config = ServiceregistryConfig.loadConfig()
        cloudConfig = config["serviceregistryConfig"]
        systemConfig = SystemConfig.loadConfig()
        
        certConfig = systemConfig["cert"]

        baseadress = cloudConfig["ip"] + ":" + str(cloudConfig["port"]) + "/serviceregistry/deregister"

        services = ServiceManager.loadServices()

        serviceRequest = services[service]

        address = baseadress + "?serviceDefinition=" + serviceRequest["serviceDefinition"]
        address += "&address=" + systemConfig["system"]["address"]
        address += "&port=" + str(systemConfig["system"]["port"])
        address += "&system_name=" + systemConfig["system"]["systemName"]

        if cloudConfig["secure"]:
            # Need to disable warning because AH main cert is not trusted
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            # Need to not verify cert because AH main cert is not trusted (verify=False)
            response = delete("https://" + address, pkcs12_filename=certConfig["cloud_cert"], pkcs12_password=certConfig["cert_pass"], verify=False)
            # Reset warnings in case we need to verify other requests
            warnings.resetwarnings()
        else:
            response = delete("http://" + address)


