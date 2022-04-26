from Arrowhead.Orchestration.Orchestration import Orchestrator
from Arrowhead.Serviceregistry.Serviceregistry import Serviceregistry
from Arrowhead.EventHandler.Eventhandler import EventHandler

if __name__ == "__main__":
    #orch = Orchestrator()
    #orch.testConnection()
    #print(orch.orchestrate())
    sr = Serviceregistry()
    sr.testConnection()
    sr.registerProviders()
    print("Register Done")
    eh = EventHandler()
    eh.testConnection()
    q = False
    while not q:
        inp = input("Continue")
        if inp == "q":
            break
        data = {}
        data["data"] = 20
        eh.publish("temperature", data)
    sr.unregisterProviders()