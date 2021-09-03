# Necro(ネクロ)
# sidmishra94540@gmail.com
 
import os, requests, sys, time, webbrowser, PIL.Image
ANIME_PATH = "D:\\"
skip = 0
def createPart(parts, path):
    for partInt in parts:
        try:
            part = str(partInt)
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
        except:
            continue

def check(ANIME_PATH, skip):
    cnt = 1
    tadd = []
    for anime in os.listdir(ANIME_PATH):
        try:
            if cnt <= skip:
                cnt += 1
                continue
            flag = 1
            index = open(ANIME_PATH + anime + '/!ndex.txt', 'r')
            data = index.read().strip()
            matched = []
            pres = []
            counter = 0
            add, subtract = [], []
            res = open(ANIME_PATH + anime + '/!restrict.txt', 'a+')
            res.close()
            restrict = open(ANIME_PATH + anime + '/!restrict.txt', 'r')
            restrictions = list(map(int, restrict.read().strip().split(',')[:-1]))
            os.system(ANIME_PATH[0] + ': & cd ' + ANIME_PATH + anime + ' & attrib +h !restrict.txt')
            restrict.close()
            for part in os.listdir(ANIME_PATH + anime):
                if part == '!ndex.txt' or part == '!restrict.txt' or part == 'desktop.ini' or part == '!con.ico':
                    continue
                index = open(ANIME_PATH + anime + '/' + part + '/!ndex.txt', 'r')
                newdata = int(index.read().strip())
                index.close()
                pres.append(newdata)
            print('--------------------------------------------------')
            print(cnt,anime)
            cnt += 1
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
                        if choice == 'y':
                            add.append(node)
                            print('.')
                            counter += 1
                            matched.append(node)
                        else:
                            subtract.append(str(node))
                time.sleep(1)
            if add:
                createPart(add, ANIME_PATH+anime)
                tadd.extend(add)
            if subtract:
                os.system(ANIME_PATH[0] + ': & cd ' + ANIME_PATH + anime + ' & attrib -h !restrict.txt')
                index = open(ANIME_PATH + anime + '/' + '!restrict.txt', 'a+')
                restrictions = ','.join(subtract)+','
                index.write(restrictions)
                index.close()
                os.system(ANIME_PATH[0] + ': & cd ' + ANIME_PATH + anime + ' & attrib +h !restrict.txt')
            print(len(add), '- new anime added!', '( Total-',counter,')')
        except:
            continue
    print('Anime added: ',tadd)
check(ANIME_PATH, skip)