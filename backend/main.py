import json
inputReceived = input()
value = json.loads(inputReceived)['key']
myJson = {
    'bey': value
}
print(json.dumps(myJson))
