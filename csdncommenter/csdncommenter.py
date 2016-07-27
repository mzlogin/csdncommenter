# File   : csdncommenter.py
# Author : Zhuang Ma
# E-mail : chumpma(at)gmail.com
# Website: http://mazhuang.org
# Date   : 2016-07-26
import requests
from BeautifulSoup import BeautifulSoup
import getpass
import time
import random
import re
import urllib
import traceback

class CsdnCommenter():
    """Csdn operator"""
    def __init__(self):
        self.sess = requests.Session()

    def login(self):
        """login and keep session"""
        username = raw_input('username: ')
        password = getpass.getpass('password: ')
        url = 'https://passport.csdn.net/account/login'
        html = self.getUrlContent(self.sess, url)
        if html is None:
            return False
        soup = BeautifulSoup(html)

        lt = self.getElementValue(soup, 'name', 'lt')
        execution = self.getElementValue(soup, 'name', 'execution')
        _eventId = self.getElementValue(soup, 'name', '_eventId')

        data = {
                'username' : username,
                'password' : password,
                'lt' : lt,
                'execution' : execution,
                '_eventId' : _eventId
                }

        response = None
        try:
            response = self.sess.post(url, data)
        except:
#             traceback.print_exc()
            pass

        return self.isLoginSuccess(response)

    def autoComment(self):
        """main handler"""
        if self.getSourceItems() is False:
            print('No source can comment!')
            return

        print('Total %d source(s) wait for comment.' % len(self.sourceitems))

        nhandled = 0
        for sourceid in self.sourceitems.keys():
            left = len(self.sourceitems) - nhandled

            sec = random.randrange(61,71)
            print('Wait %d seconds for start. %s source(s) left.' % (sec, left))
            time.sleep(sec)

            self.comment(sourceid)
            nhandled += 1

        print('Finished!')

    def getSourceItems(self):
        """get (sourceid,username) couples wait for comment"""
        self.sourceitems = dict()
        pagecount = self.getPageCount()
        if pagecount == 0:
            return False

        print('Pagecount is %d.' % pagecount)

        pattern = re.compile(r'/detail/([^/]+)/(\d+)#comment')

        for n in range(1, pagecount + 1):
            if n == 1:
                self.waitUncommentableSourceIfNecessary()
            url = 'http://download.csdn.net/my/downloads/%d' % n
            html = self.getUrlContent(self.sess, url)
            if html is None:
                continue
            soup = BeautifulSoup(html)
            sourcelist = soup.findAll('a', attrs={'class' : 'btn-comment'})
            if sourcelist is None or len(sourcelist) == 0:
                continue
            for source in sourcelist:
                href = source.get('href', None)
                if href is not None:
                    rematch = pattern.match(href)
                    if rematch is not None:
                        self.sourceitems[rematch.group(2)] = rematch.group(1)

        return len(self.sourceitems) > 0

    def waitUncommentableSourceIfNecessary(self):
        """souce cannot comment within 10 minutes after download"""
        url = 'http://download.csdn.net/my/downloads/1'
        maxMinutes = 11
        for i in range(0, maxMinutes):
            html = self.getUrlContent(self.sess, url)
            if html is None:
                break
            soup = BeautifulSoup(html)
            sourcelist = soup.findAll('span', attrs={'class' : 'btn-comment'})
            if sourcelist is None or len(sourcelist) == 0:
                print('None uncommentable source now!')
                break
            print('Waiting for uncommentable source count down %d minutes.' % (maxMinutes-i))
            time.sleep(60)

    def getPageCount(self):
        """get downloaded resources page count"""
        url = 'http://download.csdn.net/my/downloads'
        html = self.getUrlContent(self.sess, url)
        if html is None:
            print('Get pagecount failed')
            return 0
        soup = BeautifulSoup(html)

        pagelist = soup.findAll('a', attrs={'class' : 'pageliststy'})
        if pagelist is None or len(pagelist) == 0:
            return 0

        lasthref = pagelist[len(pagelist) - 1].get('href', None)
        if lasthref is None:
            return 0
        return int(filter(str.isdigit, str(lasthref)))

    def comment(self, sourceid):
        """comment per source"""
        print('sourceid %s commenting...' % sourceid)
        contents = [
                'It just soso, but thank you all the same.',
                'Neither good nor bad.',
                'It is a nice resource, thanks for share.',
                'It is useful for me, thanks.',
                'I have looking this for long, thanks.'
                ]
        rating = self.getSourceRating(sourceid)
        print('current rating is %d.' % rating)
        if rating == 0: # nobody comments
            rating = 3
        content = contents[rating - 1]
        t = '%d' % (time.time() * 1000)

        paramsmap = {
                'sourceid' : sourceid,
                'content' : content,
                'rating' : rating,
                't' : t
                }
        params = urllib.urlencode(paramsmap)
        url = 'http://download.csdn.net/index.php/comment/post_comment?%s' % params
        html = self.getUrlContent(self.sess, url)
        if html is None or html.find('({"succ":1})') == -1:
            print('sourceid %s comment failed! response is %s.' % (sourceid, html))
        else:
            print('sourceid %s comment succeed!' % sourceid)

    def getSourceRating(self, sourceid):
        """get current source rating"""
        rating = 3
        url = 'http://download.csdn.net/detail/%s/%s' % (self.sourceitems[sourceid], sourceid)
        html = self.getUrlContent(self.sess, url)
        if html is None:
            return rating

        soup = BeautifulSoup(html)
        ratingspan = soup.findAll('span', attrs={'class': 'star-yellow'})
        if ratingspan is None or len(ratingspan) == 0:
            return rating

        ratingstyle = ratingspan[0].get('style', None)

        if ratingstyle is None:
            return rating

        rating = int(filter(str.isdigit, str(ratingstyle))) / 15
        return rating


    @staticmethod
    def getElementValue(soup, element_name, element_value):
        element = soup.find(attrs={element_name : element_value})
        if element is None:
            return None
        return element.get('value', None)

    @staticmethod
    def isLoginSuccess(response):
        if response is None or response.status_code != 200:
            return False
        return -1 != response.content.find('lastLoginIP')

    @staticmethod
    def getUrlContent(session, url):
        html = None
        try:
            response = session.get(url)
            if response is not None:
                html = response.text
        except requests.exceptions.ConnectionError as e:
#             traceback.print_exc()
            pass

        return html

def main():
    csdn = CsdnCommenter()
    while csdn.login() is False:
        print('Login failed! Please try again.')
    print('Login succeed!')

    csdn.autoComment()

if __name__ == '__main__':
    main()
