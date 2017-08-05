import sys
import requests
import html2text
import re
from waverly.models import Podcast
from bs4 import BeautifulSoup # might be removed based on polly results


class Mercury():

    # sending the article to Mercury ==> getting a json to self.article
    def __init__(self, pod_id):

        print ('\n🙎  [mercury] received podcast id:', pod_id)

        podcast = Podcast.objects.get(id=pod_id)
        self.url = podcast.url_article

        url = "https://mercury.postlight.com/parser?url=" + self.url
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': 'YoDQXgWfZIhqb3XiX8lbuz8Kmv0N8rwZhFtzd986' # :)
            }

        try:
            this_article = requests.get(url, headers=headers)
            self.article = this_article.json()
        except:
            print ('\n🤦‍♀️  ❗️  [mercury] there was a problem downloading the article: ~WHERE:', sys._getframe().f_code.co_name, '\n')


    # a function that parses the article data from the Mercury json file (stored in self.article)
    def process(self):

        # getting content (raw html) and generating: self.text1, self.text2, and self.status
        try:
            self.content = self.article['content']
        except Exception as e:
            self.content = '[ could not get content ]'
            self.text1 = '[ could not get content ]'
            self.text2 = '[ could not get content ]'
            self.title = '[ could not get content ]'
            self.authors = '[ could not get content ]'
            self.image = ''
            self.dek = '[ could not get content ]'
            self.summary = '[ could not get content ]'
            self.pages = -1
            self.domain = '[ could not get content ]'
            self.status = -1
            print ('\n🤦‍♀️  ❗️  [mercury] could not get any content from the page. ~ERR:', str(e), '~WHERE:', sys._getframe().f_code.co_name, '\n')
            pass

        if not (self.content == '[ could not get content ]'):

            try:
                html = self.content
                html = re.sub(r'<figure.*?\/figure>', '', html, re.IGNORECASE|re.MULTILINE)
                html = re.sub(r'<img.*?\/img>', '', html, re.IGNORECASE|re.MULTILINE)
                html = re.sub(r'<picture.*?\/picture>', '', html, re.IGNORECASE|re.MULTILINE)
                html = re.sub(r'<source.*?\/source>', '', html, re.IGNORECASE|re.MULTILINE)
                html = re.sub(r'<figcaption.*?\/figcaption>', '', html, re.IGNORECASE|re.MULTILINE)
                html = re.sub(r'class="caption".*?</', '', html, re.IGNORECASE|re.MULTILINE)
                html = re.sub(r"class='caption'.*?</", "", html, re.IGNORECASE|re.MULTILINE)
                html = re.sub(r'class="attribution".*?</', '', html, re.IGNORECASE|re.MULTILINE)
                html = re.sub(r"class='attribution'.*?</", "", html, re.IGNORECASE|re.MULTILINE)
                html = re.sub(r'class="credit".*?</', '', html, re.IGNORECASE|re.MULTILINE)
                html = re.sub(r"class='credit'.*?</", "", html, re.IGNORECASE|re.MULTILINE)
                html = re.sub(r'.source:.*?</', '', html, re.IGNORECASE|re.MULTILINE)
                html = re.sub(r'.Source:.*?</', '', html, re.IGNORECASE|re.MULTILINE)
                text_maker = html2text.HTML2Text()
                text_maker.ignore_links = True
                text_maker.ignore_images = True
                text_maker.ignore_emphasis = True
                text_maker.body_width = 0
                text = text_maker.handle(html)
                text = re.sub(r'#+\s', '', text, re.IGNORECASE|re.MULTILINE)
                self.text1 = text

                self.text2 = (BeautifulSoup(html, 'html.parser')).get_text()

                if (self.text1 == "") or (self.text2 == ""):
                    self.status = -1
                else:
                    self.status = 0

            except Exception as e:
                self.text1 = '[ could not find content ]'
                self.text2 = '[ could not find content ]'
                self.status = -1
                print ('\n🤦‍♀️  ❗️  [mercury] there was a problem processing the article. ~ERR:', str(e), '~WHERE:', sys._getframe().f_code.co_name, '\n')
                pass

            try:
                self.title = self.article['title']
            except Exception as e:
                self.title = '[ could not find title ]'
                print ('\n🤦‍♀️  ❗️  [mercury] there was a problem processing the article. ~ERR:', str(e), '~WHERE:', sys._getframe().f_code.co_name, '\n')
                pass

            try:
                self.authors = self.article['author']
            except Exception as e:
                self.authors = '[ could not find author ]'
                print ('\n🤦‍♀️  ❗️  [mercury] there was a problem processing the article. ~ERR:', str(e), '~WHERE:', sys._getframe().f_code.co_name, '\n')
                pass

            try:
                self.image = self.article['lead_image_url']
            except Exception as e:
                self.image = '[ could not find image ]'
                print ('\n🤦‍♀️  ❗️  [mercury] there was a problem processing the article. ~ERR:', str(e), '~WHERE:', sys._getframe().f_code.co_name, '\n')
                pass

            try:
                self.dek = self.article['dek']
            except Exception as e:
                self.dek = '[ could not find dek ]'
                print ('\n🤦‍♀️  ❗️  [mercury] there was a problem processing the article. ~ERR:', str(e), '~WHERE:', sys._getframe().f_code.co_name, '\n')
                pass

            try:
                self.summary = self.article['excerpt']
            except Exception as e:
                self.summary = '[ could not find summary ]'
                print ('\n🤦‍♀️  ❗️  [mercury] there was a problem processing the article. ~ERR:', str(e), '~WHERE:', sys._getframe().f_code.co_name, '\n')
                pass

            try:
                self.pages = self.article['total_pages']
            except Exception as e:
                self.pages = -1
                print ('\n🤦‍♀️  ❗️  [mercury] there was a problem processing the article. ~ERR:', str(e), '~WHERE:', sys._getframe().f_code.co_name, '\n')
                pass

            try:
                self.domain = self.article['domain']
            except Exception as e:
                self.domain = '[ could not find number of pages ]'
                print ('\n🤦‍♀️  ❗️  [mercury] there was a problem processing the article. ~ERR:', str(e), '~WHERE:', sys._getframe().f_code.co_name, '\n')
                pass

            try:
                self.date_published = self.article['date_published']
            except Exception as e:
                self.title = '[ could not find publication date ]'
                print ('\n🤦‍♀️  ❗️  [mercury] there was a problem processing the article. ~ERR:', str(e), '~WHERE:', sys._getframe().f_code.co_name, '\n')
                pass

    def export(self):
        try:
            filename = 'mercury' + '_' + str(article_bank.index(self.url)) + '.txt'
            file = open(filename, 'w')

            file.write('===== STATUS =====\n')
            file.write(str(self.status))
            file.write('\n\n')

            file.write('===== URL =====\n')
            file.write(str(self.url))
            file.write('\n\n')

            file.write('===== DOMAIN =====\n')
            file.write(str(self.domain))
            file.write('\n\n')

            file.write('===== PAGES =====\n')
            file.write(str(self.pages))
            file.write('\n\n')

            file.write('===== DATE PUBLISHED =====\n')
            file.write(str(self.date_published))
            file.write('\n\n')

            file.write('===== AUTHORS =====\n')
            file.write(str(self.authors))
            file.write('\n\n')

            file.write('===== IMAGE =====\n')
            file.write(str(self.image))
            file.write('\n\n')

            file.write('===== TITLE =====\n')
            file.write(str(self.title))
            file.write('\n\n')

            file.write('===== DEK =====\n')
            file.write(str(self.dek))
            file.write('\n\n')

            file.write('===== SUMMARY =====\n')
            file.write(str(self.summary))
            file.write('\n\n')

            file.write('===== CONTENT =====\n')
            file.write(str(self.content))
            file.write('\n\n')

            file.write('===== TEXT1 html2text =====\n')
            file.write(str(self.text1))
            file.write('\n\n')

            file.write('===== TEXT2 BeautifulSoup =====\n')
            file.write(str(self.text2))
            file.write('\n\n')

            file.close()
            print ('\n🙎  [mercury] article was exported:', filename, '\n')

        except Exception as e:
            print ('\n🤦‍♀️  ❗️  [mercury] there was a problem exporting the article. ~ERR:', str(e), '~WHERE:', sys._getframe().f_code.co_name, '\n')
            pass
