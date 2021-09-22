from nudenet import NudeDetector
import requests
import uuid
import os

detector = NudeDetector()

def detect(url: str):
    response = requests.get(url)
    
    file_name = "/data/" + str(uuid.uuid1()) + ".gif"
    
    file = open(file_name, "wb")
    file.write(response.content)
    file.close()
    
    result = detector.detect(file_name, mode="fast")
    
    os.remove(file_name)
    
    return result
