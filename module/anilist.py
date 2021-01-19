from argparse import MetavarTypeHelpFormatter
from structure import baseModule
import requests

class NatsumeAniList(baseModule.BaseModule):
    def __init__(self):
        super().__init__()
        self.url = 'https://graphql.anilist.co'
        self.animeSearch = """
        query ($search: String, $type: MediaType, $isAdult: Boolean) {
            anime: Page (perPage: 10) {
                result: media (type: $type, isAdult: $isAdult, search: $search) {
                    id
                    title {
                        english
                        romaji
                    }
                }
            }
        }
        """

        self.mangaSearch = """
        query ($search: String, $type: MediaType, $isAdult: Boolean) {
            manga: Page (perPage: 10) {
                result: media (type: $type, isAdult: $isAdult, search: $search) {
                    id
                    title {
                        english
                        romaji
                    }
                }
            }
        }
        """
        
        
        self.animeResult = '''\
            query media($id: Int, $type: MediaType) {
                Media(id: $id, type: $type) {
                    id
                    title {
                        english
                        romaji
                    }
                    coverImage {
                        large
                        medium
                    }
                    startDate { year }
                    description(asHtml: false)
                    season
                    type
                    siteUrl
                    status
                    episodes
                    isAdult
                    meanScore
                    averageScore
                    genres
                }
                
            }'''
        
        self.mangaResult = '''\
            query media($id: Int, $type: MediaType) {
                Media(id: $id, type: $type) {
                    id
                    title {
                        english
                        romaji
                    }
                    coverImage {
                        large
                        medium
                    }
                    startDate { year }
                    description(asHtml: false)
                    type
                    siteUrl
                    status
                    isAdult
                    meanScore
                    averageScore
                    genres
                    chapters
                }
            }
            '''

    def parser(self, title: str, mode: str):
        title = " ".join(title)
        id = self.getMediaID(title, mode)
        if ('anime' in mode): self.getAnime(id)
        if ('manga' in mode): self.getManga(id)
    
    def getAnime(self, id: str):
        animeMetadata = requests.post(self.url, json={
            'query': self.animeResult,
            'variables': {
                'id': id,
                'type': 'ANIME'
            }
        }).json()
        animeMeta = animeMetadata['data']['Media']
        print("{0}[{1}{2}{0}]{3}".format(self.CXMAGENTA, self.CCYAN, animeMeta['title']['romaji'], self.CRESET))
        self.utils.printInfo("Description", "\n" + animeMeta['description'].replace("<br>", ""))
        self.utils.printInfo("Season", animeMeta['season'])
        self.utils.printInfo("Status", animeMeta['status'])
        self.utils.printInfo("Episodes", str(animeMeta['episodes']))
        self.utils.printInfo("Avg. Score", str(animeMeta['averageScore']))
        self.utils.printInfo("Genres", ", ".join(animeMeta['genres']))
    
    def getManga(self, id: int):
        mangaMetadata = requests.post(self.url, json={
            'query': self.mangaResult,
            'variables': {
                'id': id,
                'type': 'MANGA'
            }
        }).json()
        mangaMeta = mangaMetadata['data']['Media']
        print("{0}[{1}{2}{0}]{3}".format(self.CXMAGENTA, self.CCYAN, mangaMeta['title']['romaji'], self.CRESET))
        self.utils.printInfo("Status", mangaMeta['status'])
        self.utils.printInfo('Chapters', str(mangaMeta['chapters']))
        self.utils.printInfo("Avg. Score", str(mangaMeta['averageScore']))
        self.utils.printInfo("Genres", ", ".join(mangaMeta['genres']))

    def getMediaID(self, title: str, mode: str) -> int:
        if ('anime' in mode.lower()): 
            mode = 'ANIME'
        elif ('manga' in mode.lower()):
            mode = 'MANGA'
        else:
            self.utils.graceExit()

        metaResponse = requests.post(self.url, json={
            'query': self.animeSearch if mode == 'ANIME' else self.mangaSearch,
            'variables': {
                'search': title,
                'type': mode
            }
        }).json()
        metaID = metaResponse['data']["{}".format(mode.lower())]['result'][0]['id']
        return metaID
