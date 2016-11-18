# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 10:52:23 2016

@author: WaR7
"""

from os.path import expanduser




import xlsxwriter

from os.path import expanduser


home = expanduser("~")




#==============================================================================
# 
# def linkname_to_screenname(blogger,media):
#     filebloggers=sorted([line.lstrip('\\fs48 ').rstrip('\\\n').split(',') for line in open('/Users/War7/Desktop/natappy/bloggers.txt','r') if ',' in line])
#     print (filebloggers)
#     a={'Facebook':1,'Instagram':2,'Twitter':3} 
#     for el in {k:v for k,v in [(lista[a[media]],lista[0]) for lista in filebloggers] }.keys():
#         print (el)
#   #  return {k:v for k,v in [(lista[a[media]],lista[0]) for lista in filebloggers] }[blogger] 
#     
# linkname_to_screenname('theldnchatter','Facebook')
#==============================================================================

def excel():  
    print ('creating excel')
    workbook = xlsxwriter.Workbook('%s/Desktop/bloggers.xlsx' %(home))
    worksheet = workbook.add_worksheet()
    fieldsnames= ('blogger','facebook name','instagram name','twitter name','instagram id','website','visits')
    for col, name in enumerate(fieldsnames):
        worksheet.write(0, col,name)
    posts=sorted([line.lstrip('\\fs48 ').rstrip('\\\n').split(',') for line in open('%s/Desktop/natappy/bloggers.txt' %home,'r') if ',' in line])
    for row ,post in enumerate(posts, 1):
        for col, name in enumerate(post):
            try:
                worksheet.write(row,col,name)
            except:
                pass
    workbook.close()

excel()