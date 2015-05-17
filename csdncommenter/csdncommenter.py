# File   : CsdnCommenter.py
# Author : Zhuang Ma
# E-mail : ChumpMa(at)gmail.com
# Website: http://www.mazhuang.org
# Date   : 2015-05-17
import requests
from BeautifulSoup import BeautifulSoup
import getpass
import time
import random
import re
import urllib

class CsdnCommenter():
    """Csdn operator"""
    def __init__(self):
        self.sess = requests.Session()

    def login(self):
        """login and keep session"""
        username = raw_input('username: ')
        password = getpass.getpass('password: ')
        url = 'https://passport.csdn.net/account/login'
        html = self.sess.get(url).text
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

        response = self.sess.post(url, data)

        return self.isLoginSuccess(response)

    def autoComment(self):
        """main handler"""
        if self.getSourceIds() is False:
            print 'No source can comment!'
            return

        print 'Total %d source(s) wait for comment.' % len(self.sourceids)

        nhandled = 0
        for sourceid in self.sourceids:
            left = len(self.sourceids) - nhandled

            sec = random.randrange(61,71)
            print 'Wait %d seconds for start. %s source(s) left.' % (sec, left)
            time.sleep(sec)

            self.comment(sourceid)
            nhandled += 1

        print 'Finished!'

    def getSourceIds(self):
        """get source ids wait for comment"""
        self.sourceids = set()
        pagecount = self.getPageCount()
        if pagecount == 0:
            return False

        print 'Pagecount is %d.' % pagecount

        pattern = re.compile(r'.+/(\d+)#comment')

        for n in range(1, pagecount + 1):
            url = 'http://download.csdn.net/my/downloads/%d' % n
            html = self.sess.get(url).text
            soup = BeautifulSoup(html)
            sourcelist = soup.findAll('a', attrs={'class' : 'btn-comment'})
            if sourcelist is None:
                continue
            for source in sourcelist:
                href = source.get('href', None)
                if href is not None:
                    rematch = pattern.match(href)
                    if rematch is not None:
                        self.sourceids.add(rematch.group(1))

        return len(self.sourceids) > 0

    def getPageCount(self):
        """get downloaded resources page count"""
        url = 'http://download.csdn.net/my/downloads'
        html = self.sess.get(url).text
        soup = BeautifulSoup(html)

        pagelist = soup.findAll('a', attrs={'class' : 'pageliststy'})
        if pagelist is None:
            return 0

        lasthref = pagelist[len(pagelist) - 1].get('href', None)
        if lasthref is None:
            return 0
        return int(filter(str.isdigit, str(lasthref)))

    def comment(self, sourceid):
        """comment per source"""
        print 'sourceid %s commenting...' % sourceid
        contents = [
                'It just soso, but thank you all the same.',
                'Neither good nor bad.',
                'It is a nice resource, thanks for share.',
                'It is useful for me, thanks.',
                'I have looking this for long, thanks.'
                ]
        rating = random.randrange(1,6)
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
        html = self.sess.get(url).text
        if html.find('({"succ":1})') != -1:
            print 'sourceid %s comment succeed!' % sourceid
        else:
            print 'sourceid %s comment failed! response is %s.' % (sourceid, html)

    @staticmethod
    def getElementValue(soup, element_name, element_value):
        element = soup.find(attrs={element_name : element_value})
        if element is None:
            return None
        return element.get('value', None)

    @staticmethod
    def isLoginSuccess(response):
        if response.status_code != 200:
            return False
        return -1 != response.content.find('lastLoginIP')

def main():
    csdn = CsdnCommenter()
    while csdn.login() is False:
        print 'Login failed! Please try again.'
    print 'Login succeed!'

    csdn.autoComment()

if __name__ == '__main__':
    main()
