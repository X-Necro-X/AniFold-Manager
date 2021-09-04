# Necro(ネクロ)
# sidmishra94540@gmail.com
 
# icon, name update
# https://anilist.co/anime/101280/That-Time-I-Got-Reincarnated-as-a-Slime/

import os, requests, time, webbrowser, PIL.Image

def create(part, path):
    os.mkdir(path+'/'+part)
    variables = {
    'id': part
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
    os.system(ANIME_PATH[0] + ': & cd ' + path + ' & attrib +s "' + part + '" & cd ' + part + ' & echo [.ShellClassInfo] > desktop.ini & echo IconResource=!con.ico,0 >> desktop.ini & attrib +s +h desktop.ini & attrib +h !con.ico & attrib +h !ndex.txt')
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
        if part in ['!ndex.txt', '!restrict.txt', 'desktop.ini', '!con.ico']:
            continue
        index = open(path + '/' + part + '/!ndex.txt', 'r')
        newdata = int(index.read().strip())
        index.close()
        pres.append(newdata)
    print('--------------------------------------------------')
    index.close()
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
    if int(data) not in pres:
        pres.append(int(data))
        add.append(int(data))
        print('.')
        counter += 1
    matched = [int(data)]
    for current in matched:
        variables = {
            'id': current
        }
        response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables}).json()['data']['Media']['relations']['edges']
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
    link = input('Enter link of the anime page (anilist.co): ')
    anime_id = link.split('/')[4]
    title = create(anime_id, path)
    add(path+'/'+title)

def update(path):
    cnt = 1
    for part in os.listdir(path):
        print(str(cnt)+'.', part)
        add(path+'/'+part)
        cnt += 1

def sync(path):
    pass

if __name__ == '__main__':
    print('----------------------------------------------------------------------------------------------------')
    print('------------------------------------------ANIFOLD  SAMURAI------------------------------------------')
    print('----------------------------------------------------------------------------------------------------')
    # ANIME_PATH = input('Enter Anime Path: ').strip('\\').strip('/')
    ANIME_PATH = 'E:\Important\Projects\Anifold Samurai\Test'.strip('\\').strip('/')
    while True:
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
    print('----------------------------------------------------------------------------------------------------')
    print('---------------------------------------------THANK  YOU---------------------------------------------')
    print('----------------------------------------------------------------------------------------------------')