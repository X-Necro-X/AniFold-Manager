import os, requests, sys, time, webbrowser
ANIME_PATH = "D:\\"
skip = 7
def setIcon(ANIME_PATH, skip):
    cnt = 1
    for anime in os.listdir(ANIME_PATH):
        if anime[0]=='!' or anime=='$RECYCLE.BIN':
            continue
        try:
            if cnt <= skip:
                cnt += 1
                continue
            flag = 1
            index = open(ANIME_PATH + anime + '/!ndex.txt', 'r')
            data = index.read()
            matched = []
            pres = []
            add, subtract = [], []
            res = open(ANIME_PATH + anime + '/!restrict.txt', 'a+')
            res.close()
            restrict = open(ANIME_PATH + anime + '/!restrict.txt', 'r')
            restrictions = list(map(int, restrict.read().split(',')[:-1]))
            os.system(ANIME_PATH[0] + ': & cd ' + ANIME_PATH + anime + ' & attrib +h !restrict.txt')
            restrict.close()
            for part in os.listdir(ANIME_PATH + anime):
                if part == '!ndex.txt' or part == '!restrict.txt' or part == 'desktop.ini' or part == '!con.ico':
                    continue
                index = open(ANIME_PATH + anime + '/' + part + '/!ndex.txt', 'r')
                data = int(index.read())
                index.close()
                pres.append(data)
            if flag:
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
                matched = [int(data)]
                for current in matched:
                    variables = {
                        'id': current
                    }
                    response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables}).json()['data']['Media']['relations']['edges']
                    rln = map(lambda x: x['node']['id'], filter(lambda x: x['node']['type']!='MANGA', response))
                    for node in rln:
                        if node in pres:
                            matched.append(node)
                            continue
                        if node not in matched and node not in restrictions:
                            webbrowser.open('https://anilist.co/anime/'+str(node), new=2)
                            choice = input('Add '+str(node)+'? [Yes(y)/No(n)]')
                            if choice == 'y':
                                add.append(node)
                                matched.append(node)
                            else:
                                subtract.append(str(node))
                    time.sleep(1)
            if add:
                print('   -Anime to be added:', add)
            if subtract:
                os.system(ANIME_PATH[0] + ': & cd ' + ANIME_PATH + anime + ' & attrib -h !restrict.txt')
                index = open(ANIME_PATH + anime + '/' + '!restrict.txt', 'a+')
                restrictions = ','.join(subtract)+','
                index.write(restrictions)
                index.close()
                os.system(ANIME_PATH[0] + ': & cd ' + ANIME_PATH + anime + ' & attrib +h !restrict.txt')
        except Exception as e:
            print(e)
            continue
setIcon(ANIME_PATH, skip)