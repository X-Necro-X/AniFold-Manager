# Necro(ネクロ)
# sidmishra94540@gmail.com

import os, requests, time, webbrowser, PIL.Image, PIL.ImageChops

def anilist(type, data):
    try:
        if type == 'DETAILS':   
            variables = {
                'id': data.get('part')
            }
            query = '''
                query ($id: Int) {
                    Media (id: $id, type: ANIME) {
                        id
                        title {
                            english
                            romaji
                        }
                        coverImage{
                            extraLarge
                        }
                    }
                }
            '''
            response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables}).json()['data']['Media']
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

def isValid(name):
    if name in ['!ndex.txt', '!restrict.txt', 'desktop.ini', '!con.ico', '$RECYCLE.BIN', 'Config.Msi', 'desktop.ini', 'msdownld.tmp', 'System Volume Information']:
        return False
    return True

def create(part, path):
    os.mkdir(path+'/'+part)
    response = anilist('DETAILS', {'part': part})
    if not response:
        print('Anime not found!')
    title = response['title']['english'] if response['title']['english'] else response['title']['romaji']
    title = title.replace('&', 'and').replace('/', '~').replace(':', '~').replace('*', '~').replace('?', '~').replace('"', '~').replace('<', '~').replace('>', '~').replace('|', '~')
    cover = response['coverImage']['extraLarge']
    image = path + '/' + part + '/!con' + os.path.splitext(cover)[1]
    open(image, 'wb').write(requests.get(cover).content)
    icon = PIL.Image.open(image)
    width, height = icon.size
    crop = width if width <= height else height
    icon = icon.crop(((width - crop) // 2, (height - crop) // 2, (width + crop) // 2, (height + crop) // 2)).resize((256,256))
    icon.save(os.path.splitext(image)[0] + '.ico', format = 'ICO', sizes=[(256,256)], quality=95)
    os.remove(image)
    index = open(path + '/' + part + '/!ndex.txt', 'w')
    index.write(part)
    index.close()
    os.system(path[0] + ': & cd ' + path + ' & attrib +s "' + part + '" & cd ' + part + ' & echo [.ShellClassInfo] > desktop.ini & echo IconResource=!con.ico,0 >> desktop.ini & attrib +s +h desktop.ini & attrib +h !con.ico & attrib +h !ndex.txt')
    os.rename(path + '/' + part, path + '/' + title)
    print('Added-', title)
    time.sleep(1)
    return title

def add(path):
    index = open(path + '/!ndex.txt', 'r')
    data = index.read().strip()
    matched = []
    pres = []
    counter = 0
    add, subtract = [], []
    res = open(path + '/!restrict.txt', 'a+')
    res.close()
    restrict = open(path + '/!restrict.txt', 'r')
    restrictions = list(map(int, restrict.read().strip().split(',')[:-1]))
    os.system(path[0] + ': & cd ' + path + ' & attrib +h !restrict.txt')
    restrict.close()
    for part in os.listdir(path):
        if not isValid(part):
            continue
        index = open(path + '/' + part + '/!ndex.txt', 'r')
        newdata = int(index.read().strip())
        index.close()
        pres.append(newdata)
    index.close()
    if int(data) not in pres:
        pres.append(int(data))
        add.append(int(data))
        print('.')
        counter += 1
    matched = [int(data)]
    for current in matched:
        response = anilist('RELATIONS', {'current': current})
        rln = map(lambda x: x['node']['id'], filter(lambda x: x['node']['type']!='MANGA', response))
        for node in rln:
            if node not in matched and node not in restrictions:
                if node in pres:
                    print('.')
                    counter += 1
                    matched.append(node)
                    continue
                webbrowser.open('https://anilist.co/anime/'+str(node), new=2)
                choice = input('Add '+str(node)+'? [Yes(y)/No(n)]')
                if choice in ['n','N']:
                    subtract.append(str(node))                    
                else:
                    add.append(node)
                    print('.')
                    counter += 1
                    matched.append(node)
        time.sleep(1)
    if add:
        for part in add:
            create(str(part), path)
    if subtract:
        os.system(path[0] + ': & cd ' + path + ' & attrib -h !restrict.txt')
        index = open(path + '/' + '!restrict.txt', 'a+')
        restrictions = ','.join(subtract)+','
        index.write(restrictions)
        index.close()
        os.system(path[0] + ': & cd ' + path + ' & attrib +h !restrict.txt')
    print(len(add), '- new anime added!')

def new(path):
    print()
    link = input('Enter link of the anime page (anilist.co): ')
    anime_id = link.split('/')[4]
    title = create(anime_id, path)
    add(path+'/'+title)

def update(path):
    cnt = 1
    for part in os.listdir(path):
        if not isValid(part):
            continue
        print()
        print(str(cnt)+'.', part)
        add(path+'/'+part)
        cnt += 1
    print()
    choice = input('Update folder icons and names too? [Yes(y)/No(n)]')
    if choice in ['n', 'N']:
        return
    for anime in os.listdir(path):
        if not isValid(anime):
            continue
        for part in os.listdir(path+'/'+anime):
            if not isValid(part):
                continue
            index = open(path+'/'+anime+'/'+part+'/!ndex.txt', 'r')
            data = index.read().strip()
            index.close()
            response = anilist('DETAILS', {'part': data})
            if not response:
                print('Anime not found on anilist! Please delete folder', part)
                continue
            title = response['title']['english'] if response['title']['english'] else response['title']['romaji']
            title = title.replace('&', 'and').replace('/', '~').replace(':', '~').replace('*', '~').replace('?', '~').replace('"', '~').replace('<', '~').replace('>', '~').replace('|', '~')
            cover = response['coverImage']['extraLarge']
            image = path + '/' + anime + '/' + part + '/!con' + os.path.splitext(cover)[1]
            os.system(path[0] + ': & cd ' + path + '/' + anime + '/' + part + ' & attrib -h !con.ico')
            open(image, 'wb').write(requests.get(cover).content)
            icon = PIL.Image.open(image)
            width, height = icon.size
            crop = width if width <= height else height
            icon = icon.crop(((width - crop) // 2, (height - crop) // 2, (width + crop) // 2, (height + crop) // 2)).resize((256,256))
            os.remove(path+'/'+anime+'/'+part+'/!con.ico')
            icon.save(os.path .splitext(image)[0] + '.ico', format = 'ICO', sizes=[(256,256)], quality=95)
            os.remove(image)
            os.system(path[0] + ': & cd ' + path + '/' + anime + '/' + part + ' & attrib +h !con.ico')
            os.rename(path + '/' + anime + '/' + part, path + '/' + anime + '/' + title)
            print('Updated-', title)
            time.sleep(1)
    print('If the changes to folder icons are not visible, restart the system.')

def sync(path):
    uid = 599228
    response = anilist('LISTS', {'uid': uid, 'type': 'ANIME'})
    if not response:
        print('User not found!')
    completed = set()
    for list in response:
        if list.get('status') in ['COMPLETED', 'WATCHING']:
            for entry in list.get('entries'):
                completed.add(entry.get('mediaId'))
    unformatted = []
    present = set()
    for anime in os.listdir(path):
        if not isValid(anime):
            continue
        if not os.path.isfile(path+'/'+anime+'/!ndex.txt'):
            unformatted.append(anime)
        try:
            for part in os.listdir(path+'/'+anime):
                if part in ['!ndex.txt', '!restrict.txt', 'desktop.ini', '!con.ico']:
                    continue
                try:
                    index = open(path+'/'+anime+'/'+part+'/!ndex.txt', 'r')
                    data = index.read().strip()
                    present.add(int(data))
                    index.close()
                except:
                    unformatted.append(anime+'/'+part)
        except:
            continue
    comp_not, pres_not = [], []
    for comp in completed:
        if comp not in present:
            comp_not.append(comp)
    for pres in present:
        if pres not in completed:
            pres_not.append(pres)
    while True:
        print()
        print('1. Anime in anilist but not in folder:', len(comp_not))
        print('2. Anime in folder but not in anilist:', len(pres_not))
        print('3. Unformatted folders:', len(unformatted))
        print('4. Exit to Main Menu')
        choice = input('Enter the respective number to view full list: ')
        if choice in ['1', '2']:
            to_be_printed = comp_not if choice=='1' else pres_not
            for part in to_be_printed:
                response = anilist('DETAILS', {'part': part})
                title = response['title']['english'] if response['title']['english'] else response['title']['romaji']
                print(title)
                time.sleep(1)
        elif choice == '3':
            for part in unformatted:
                print(part)
        else:
            return

try:
    if __name__ == '__main__':
        ANIME_PATH = input('Enter Anime Path: ').strip('\\').strip('/')
        while True:
            print()
            print('1. New')
            print('2. Update')
            print('3. Sync')
            print('4. Exit')
            choice = input()
            if choice == '1':
                new(ANIME_PATH)
            elif choice == '2':
                update(ANIME_PATH)
            elif choice == '3':
                sync(ANIME_PATH)
            else:
                break
except Exception as e:
    print(e)