#-*- coding: utf-8 -*-

# version 1.1

# 예상소요시간: 약 70시간

from bs4 import BeautifulSoup
import urllib
import csv
import datetime
import time

class WebCrawler():
    def __init__(self):
        self.data = {}
        self.field_list = [
            'full_name',
            'Commit',
            'Branch',
            'Release',
            'Contributor',
            'License',
            'Topic',
            'Saved_DateTime'
        ]

    # Request HTML
    def Request(self,owner,repository):
        url = 'https://github.com/'+owner+'/'+repository
        print url
        fp = urllib.urlopen(url)
        source = fp.read()
        fp.close()
        self.request = BeautifulSoup(source, 'html.parser')

    # Scrap Summary
    def SummaryScrap(self):

        summary= self.request.findAll('ul', attrs={'class':'numbers-summary'})
        sumelement = summary[0].find_all('a')
        for ele in sumelement:
            parsed = ele.text.replace("\n","").strip().replace(" ","")

            if ',' in parsed:
                parsed = parsed.replace(',','')

            if 'commits' in parsed:
                value = parsed.replace('commits','')

                print 'Commits: ' + value
                self.data['Commit'] = int(value)

            elif 'commit' in parsed:
                value = parsed.replace('commit','')

                print 'Commits: ' + value
                self.data['Commit'] = int(value)

            elif 'branches' in parsed:
                value = parsed.replace('branches','')

                print 'Branches: ' + value
                self.data['Branch'] = int(value)

            elif 'branch' in parsed:
                value = parsed.replace('branch','')

                print 'Branches: ' + value
                self.data['Branch'] = int(value)

            elif 'releases' in parsed:
                value = parsed.replace('releases','')

                print 'Releases: ' + value
                self.data['Release'] = int(value)

            elif 'release' in parsed:
                value = parsed.replace('release','')

                print 'Releases: ' + value
                self.data['Release'] = int(value)

            elif 'contributors' in parsed:
                try:
                    value = parsed.replace('contributors', '')

                    print 'Contributors: ' + value
                    self.data['Contributor'] = int(value)

                except ValueError as e:
                    print 'Fetching Error'

            elif 'contributor' in parsed:
                try:
                    value = parsed.replace('contributor', '')

                    print'Contributors: ' + value
                    self.data['Contributor'] = int(value)

                except ValueError as e:
                    print 'Fetching Error'
            else:
                self.data['License'] = parsed
                print parsed
    # Scrap Topics
    def TopicScrap(self):
        self.data['Topic'] = []
        topic = self.request.findAll('div', attrs={'id':'topics-list-container'})
        if topic:
            topicelement = topic[0].find_all('a')
            print 'Topic: '
            for ele in topicelement:
                parsed = ele.text.replace('\n', '').strip()
                self.data['Topic'].append(parsed)
                print parsed
        else:
            print 'no topic'

    def CSVCreater(self):
        with open('Repository_data.csv', 'a') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=self.field_list)
            writer.writeheader()
    # Save Results

    def CSVWrtier(self):
        print self.data
        with open('Repository_data.csv', 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.field_list)
            self.data['Saved_DateTime'] = str(datetime.datetime.now())
            writer.writerow(self.data)

repositories = WebCrawler()

# Parse Repository owner and name
with open('data/finalRepoDataCol2.csv','r') as csvfile:
    reader = csv.DictReader(csvfile)
    repositories.CSVCreater()
    for row in reader:

        # Crawling Start
        owner,repo = row['full_name'].split('/')
        repositories.data['full_name'] = row['full_name']
        repositories.Request(owner,repo)
        repositories.SummaryScrap()
        repositories.TopicScrap()
        repositories.CSVWrtier()
