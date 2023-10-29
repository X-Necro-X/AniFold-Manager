# Necro(ネクロ)
# sidmishra94540@gmail.com

import os, requests, time

VISITED_ANIME_IDS = os.getcwd() + '/DO_NOT_REMOVE_Visited_Anime_IDs.txt'
ADDED_LEFTOVERS = os.getcwd() + '/DO_NOT_REMOVE_Added_Leftovers.txt'
OUTPUT = os.getcwd() + '/Leftovers.txt'

def anilist(type: str, data: dict) -> str:
    try:
        if type == 'RELATIONS':
            variables = {
                'id': data.get('current')
            }
            query = '''
                query ($id: Int) {
                    Media (id: $id, type: ANIME) {
                        relations{
                            edges{
                                node{
                                    id
                                    title{
                                        romaji
                                        english
                                    }
                                    type
                                }
                                relationType
                            }
                        }
                    }
                }
            '''
            response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables}).json()['data']['Media']['relations']['edges']
        if type == 'LISTS':
            variables = {
                    'userId': data.get('uid'),
                    'type': data.get('type')
                }
            query = '''
                query ($userId: Int, $type: MediaType){
                    MediaListCollection (userId: $userId, type: $type){
                        lists{
                            name
                            status
                            entries{
                                mediaId
                            }
                        }
                    }
                }
            '''
            response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables}).json()['data']['MediaListCollection']['lists']
    except:
        return None
    return response

def createOrReadFile(path: str) -> str:
    open(path, 'a').close()
    with open(path, 'r') as file:
        return file.read().strip()

def writeToFile(path: str, content: str) -> None:
    with open(path, 'a+') as file:
        file.write(content)

def fetchAnimeList(uid: int) -> str:
    response = anilist('LISTS', {'uid': uid, 'type': 'ANIME'})
    return response

def prepareAddedAnimeList(response: str) -> set[str]:
    addedAnime = set()
    savedAnime = set(createOrReadFile(VISITED_ANIME_IDS).split(','))
    for list in response:
        if list.get('status') in ['COMPLETED', 'WATCHING']:
            for entry in list.get('entries'):
                if str(entry.get('mediaId')) not in savedAnime:
                    addedAnime.add(entry.get('mediaId'))
    return addedAnime

def prepareSavedLeftovers() -> tuple[set[str], set[str]]:
    savedLeftovers = createOrReadFile(ADDED_LEFTOVERS).split('\n')
    if len(savedLeftovers[0]):
        leftoversId = set(map(lambda x: x[:x.find(' ')], savedLeftovers))
        leftoversName = set(map(lambda x: x[x.find(' '):], savedLeftovers))
        return leftoversId, leftoversName
    return set(), set()

def fetchRelationsList(current: str):
    response = anilist('RELATIONS', {'current': current})
    rln = map(lambda x: x['node'], filter(lambda x: x['node']['type']!='MANGA', response))
    return rln

def saveAddedAnime(animeId: str) -> None:
    content = animeId + ','
    writeToFile(VISITED_ANIME_IDS, content)

def saveLeftover(leftoverId: str, leftoverName: str) -> None:
    content = leftoverId + ' ' + leftoverName + '\n'
    writeToFile(ADDED_LEFTOVERS, content)

def saveOutput(leftoversName: set[str]) -> None:
    content = '\n'.join(leftoversName)
    writeToFile(OUTPUT, content)

def leftovers(uid: int) -> None:
    response = fetchAnimeList(uid)
    if not response:
        print('User not found!')
        return
    addedAnime = prepareAddedAnimeList(response)
    counter = 0
    leftoversId, leftoversName = prepareSavedLeftovers()
    for current in addedAnime:
        counter += 1
        print(str(counter) + '/' + str(len(addedAnime)))
        rln = fetchRelationsList(current)
        for node in rln:
            id = node.get('id')
            title = node.get('title').get('english') if node.get('title').get('english') else node.get('title').get('romaji')
            if id not in addedAnime and id not in leftoversId:
                print("    " + title)
                leftoversId.add(id)
                leftoversName.add(title)
                saveLeftover(str(id), title)
        saveAddedAnime(str(current))
        time.sleep(1)
    print('\n' + leftoversName + '\n')
    saveOutput(leftoversName)
    print('Please check file ' + OUTPUT + ' for complete list.')

try:
    if __name__ == '__main__':
        uid = 599228
        leftovers(uid)

except Exception as e:
    print(e)