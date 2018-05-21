from lxml.etree import fromstring
import requests

import sys
import unittest, time, re
import csv
import timeit
import urllib2
from bs4 import BeautifulSoup
from sets import Set


validOneWord = Set(['true', 'false', 'yes', 'no'])
f = open("bookmark", "a")

def parsePage(link, popularity):
    print link
    temp = []
    req = urllib2.Request(link, headers={'User-Agent': "Mozilla/5.0"})
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html, 'lxml')
    wrapper = (soup.find(id="center_top"))
    question = wrapper.find(class_="module question_title  jsparams js-question_title").find("h1")
    # print popularity
    # tagsRaw = soup.find(class_="module question_card_categories  jsparams js-question_card_categories")
    # print tagsRaw
    # tagsR = tagsRaw.find_all("a")
    # tag = []
    # for i in tagsR:
    #     tag.append(i.text)
    # print tag
    answer =  wrapper.find(class_= "answer_text")
    if( str(type(answer)) == "<type 'NoneType'>" or str(type(question)) == "<type 'NoneType'>" ):
        print "Question/Answer not found. Skipped"
        return 1
    else:
        answer = answer.text.encode('utf-8')
        question = question.text.encode('utf-8')
    confidence =  wrapper.find("span", class_="confidence_num")
    if str(type(confidence)) == "<type 'NoneType'>":
        print "Confidence not found"
        confidence = "NA"
    else:
        confidence = confidence.text.encode('utf-8')
    temp.append("Science")
    temp.append(popularity)
    temp.append(question)
    temp.append(confidence)
    temp.append(answer)
    return temp

address = 'http://www.answers.com/Q/FAQ/455'
req = urllib2.Request(address + "-187", headers={'User-Agent': "Mozilla/5.0"})
html = urllib2.urlopen(req).read()
soup = BeautifulSoup(html, 'lxml')
for pageNumber in range(188,2807):
    f.write(str(pageNumber) +"\n")
    questionNumber = 0
    start_time_Page = timeit.default_timer()
    wrapperList = soup.find_all(class_='question_slot')
    print "Doing Page number = ",pageNumber-1, " with ",len(wrapperList)," questions"
    final = []
    x = 0
    for crudeQues in wrapperList:
        questionNumber += 1
        start_time = timeit.default_timer()
        print questionNumber
        questionLinks = crudeQues.find("a")
        questionPopularity = crudeQues.find("span", class_="popularity")
        if str(type(questionPopularity)) == "<type 'NoneType'>":
            print "Question popularity not found"
            questionPopularity = 'NA'
        else:
            questionPopularity = questionPopularity.text.encode('utf-8')
        temp = parsePage(questionLinks['href'], questionPopularity)
        if temp == 1:
            continue
        else:
            final.append(temp)
        print "Time taken = ", timeit.default_timer() - start_time
    with open('answers.com1.csv', 'ab') as csvfile:
        print("Finalizing this page")
        spamwriter = csv.writer(csvfile, dialect='excel')
        spamwriter.writerows(final)
    print "Total time taken for this page = ",timeit.default_timer() - start_time_Page
    html = urllib2.urlopen(address + '-' + str(pageNumber) ).read()
    soup = BeautifulSoup(html, 'lxml')
