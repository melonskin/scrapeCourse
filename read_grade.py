#!/usr/bin/env python
# -*- coding: utf-8 -*
import os
import re
from collections import defaultdict
import csv
import codecs

def readtxtfile(txtfile):
    txtcontent = txtfile.read().replace('\n', ' ')
    masterDictionary = defaultdict(list)
    while (True):
        foundCourseMatch = re.search("[A-Z]{4}-\d{3}-\d{3} \d+ \d+ \d+ \d+ \d+ \d+ \d.\d+ \d+ \d+ \d+ \d+ \d+ \d+",
                                     txtcontent)
        if foundCourseMatch == None:
            break
        endpoint = foundCourseMatch.span()[1]
        print(foundCourseMatch.group())
        txtcontent = txtcontent[endpoint + 1:]
        currentCourse = foundCourseMatch.group()[:8]
        foundProfessor = re.search("[A-Z]+ [A-Z]", txtcontent[:30])
        if foundProfessor == None:
            foundProfessor = re.search("[A-Z]+-", txtcontent[:30])
        if foundProfessor == None:
            foundProfessor = re.search("[A-Z]+", txtcontent[:30])
        print(foundProfessor.group())
        foundPercent = re.search("\d+.\d+% \d+.\d+% \d+.\d+% \d+.\d+% \d+.\d+% ", txtcontent)
        print(foundPercent.group())
        inspec = foundCourseMatch.group()
        endpoint = foundPercent.span()[1]
        txtcontent = txtcontent[endpoint + 1:]
        masterDictionary[currentCourse].append((foundCourseMatch.group(), foundProfessor.group()))
    return masterDictionary

with open('coursegpa.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', lineterminator='\n')
    spamwriter.writerow(['Department']  + ['NO'] + ['Section'] + ["Instructor"] \
                        +["College"] + ["Semester"] + ["Year"] \
                        + ['A'] + ['B'] + ['C'] + ['D'] \
                        + ['F']  + ["Q"] +['GPA'] + ["NOStudent"])


def percentage(top,bot):
    return str(round(float(top)/float(bot),4)*100)+'%'


def writecsv(dirname, filename, destination):
    College = filename[-6:-4]
    semestern = filename[-7:-6]
    if semestern == '1':
        semester = 'Spring'
    elif semestern == '2':
        semester = 'Summer'
    else:
        semester = 'Fall'
    with open(os.path.join(dirname, filename), 'r',encoding="utf8") as txtfile:
        masterdict = readtxtfile(txtfile)
        for course,classTuple in masterdict.items():
            print(course)
            print(classTuple)
            for tuple in classTuple:
                with open(destination, 'a',encoding='utf8') as csvfile:
                    spamwriter = csv.writer(csvfile, delimiter=',',
                                            quotechar='"', lineterminator='\n')
                    info = tuple[0].split()

                    spamwriter.writerow([info[0][:4]] + [info[0][5:8]] + [info[0][9:12]] +[tuple[1]] \
                                        +[College] + [semester] + [dirname[-4:]] \
                                        + [percentage(info[1],info[6])] + [percentage(info[2],info[6])]+ \
                                        [percentage(info[3],info[6])]+ [percentage(info[4],info[6])] \
                                        + [percentage(info[5],info[6])] + [percentage(info[11],info[6])]+ \
                                        [info[7]]+ [info[6]])


for dirname, dirnames, filenames in os.walk('.'):
    for dirname in dirnames:
        for dirname2, dirnames2, filenames2 in os.walk(os.path.join('.',dirname)):
            for filename in filenames2:
                filename2, file_extension = os.path.splitext(os.path.join('.', dirname, filename))
                if file_extension == '.txt':
                    writecsv(dirname,filename,'coursegpa.csv')



# dirname, filename = '.\Fall2015', "grd20153AG.txt"
# writecsv(dirname, filename, 'coursegpa.csv')


