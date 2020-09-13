import requests
from bs4 import BeautifulSoup

URL = 'https://wallpaperscraft.ru/catalog/minimalism'
URL_IMG = 'https://images.wallpaperscraft.ru/image'
DEF_SIZE = ('2560×1440', '1920x1080', '1600x900', '1280x720')

class Parser():

    def __init__(self, url = 'https://wallpaperscraft.ru', source = 'https://images.wallpaperscraft.ru/image', tag_source = 'wallpapers__link', size = ('2560×1440', '1920x1080', '1600x900', '1280x720')):
        self.URL = url
        self.URL_SOURCE = source #URL источника, для сайтов, где картинки располагаются по другому пути
        self.IMG_SIZE = size
        self.TAG_SOURCE = tag_source #HTML тэг, по которой ищется ссылка на картинку

    def checkLink(self, link): #Проверка ссылки на существоввание
        r = requests.get(link)
        if r.status_code == 200: return True
        else: return False

    def createLink(self, img_name): #Создает массив ссылок на картинки по имени картинки
        all_size_link = []
        start_link = '/'.join([self.URL_SOURCE, img_name])
        for size in self.IMG_SIZE:
            end_link = '.'.join(map(str, [size, 'jpg']))
            link = '_'.join([start_link, end_link])
            if self.checkLink(link): all_size_link.append(link) #ЗДЕСЬ ИСПРАВИЛ УСЛОВИЕ ПО ВРЕМЯ ПЕРЕДЕЛКИ В ООП
        return all_size_link

    def parsePage(self, page): # return None if image does't exist, else return list with links
        img_links = page.find_all('a', {'class': self.TAG_SOURCE})
        if not img_links: return None
        img_data = {}
        for link in img_links:
            link = link.get('href')
            link_parts = link.split('/')
            name = link_parts[-1]
            all_size_img = self.createLink(name)
            img_data.update({name:all_size_img})
        return img_data

    def parse(self, start=0, duration=100): #return dict with {name:[source}}
        images_source = {}
        for page_counter in range(duration):
            page_url = '/'.join([self.URL, 'page%s'%(page_counter+start)])
            page_request = requests.get(page_url)
            if page_request.status_code != 200: break
            page = BeautifulSoup(page_request.text, 'html.parser')
            #parsePage
            img_links = page.find_all('a', {'class': self.TAG_SOURCE})
            if not img_links: break
            for link in img_links:
                link = link.get('href')

                link_parts = link.split('/')
                name = link_parts[-1]
                all_size_link = {}
                #createLink
                start_link = '/'.join([self.URL_SOURCE, name])
                for size in self.IMG_SIZE:
                    end_link = '.'.join(map(str, [size, 'jpg']))
                    link = '_'.join([start_link, end_link])
                    # if self.checkLink(link):  Черезчур замедляет процесс парсинга
                    print({link:size})
                    all_size_link.update({link:size})
                images_source.update({name:all_size_link})
        return images_source


if __name__=='__main__':
    p = Parser(url='https://wallpaperscraft.ru/catalog/anime')
    print(p.parse(duration=3))
