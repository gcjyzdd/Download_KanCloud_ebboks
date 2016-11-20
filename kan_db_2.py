#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import sys,os
import json
from kancloud_mth_new import book

class kan_db():

    def __init__(self):
        pass

    def create_table(self,tb_name,**kwargs):
        #connect to database
        try:
            conn=MySQLdb.connect('localhost','testuser','test623','kancloud',charset='utf8')
            print 'connected to database kancloud'
        except:
            print 'connecting to database kancloud failed.'
            sys.exit('EXIT.'.center(60,'*'))

        cursor=conn.cursor()
        conn.set_character_set('utf8')
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')

        # try to delete and create a table
        a=''
        for key,value in kwargs.items():
            a+=key+' '+value+', '
        a=a[0:-2]

        try:
            cursor.execute("DROP TABLE %s" % tb_name )
            print 'Database %s exists. Deleted.' % db_name
        except:
            pass

        print 'CREATE TABLE {0}({1}) '.format( tb_name,a)
        cursor.execute('CREATE TABLE {0}({1}) '.format( tb_name,a))
        #cursor.execute('CREATE TABLE %s(id varchar(8) PRIMARY KEY, name varchar(100), link varchar(200), dlable varchar(5)) ' % tb_name)
        conn.commit()
        cursor.close()

    def fill_table(self,books,tb_name):
        #连接时一定要显式地指定字符编码
        conn=MySQLdb.connect('localhost','testuser','test623','kancloud',charset='utf8',use_unicode=True)
        #conn=MySQLdb.connect('localhost','testuser','test623','kancloud')
        cursor=conn.cursor()

        #cursor.execute('USE TABLE books')

        a='C++编程精髓呵呵呵'
        #a=a.decode('gbk').encode('utf-8')
        for book in books:
            cursor.execute('INSERT INTO %s' %tb_name +' (id,name,link,dlable) values (%s,%s,%s,%s)',
                    [str(book.ID),book.name,book.link,book.downloadable])
        conn.commit()
        cursor.close()
        print 'name'
        print books[0].name,books[1].link,books[1].downloadable,books[2].downloadable,books[3].downloadable


    def load_books(self):
        thefile=open('BOOK_LIST.json','r')
        data=json.load(thefile)
        thefile.close()

        books=[]
        for item in data['Books_info']:
            books.append(book(int(item['ID']),item['link'],item['name'],item['abstract'],item['cover'],item['formats'],item['tags'],item['cover_link'],item['downloadable']))
        return books

    #search name,id

def get_downloadable_links():
    conn=MySQLdb.connect('localhost','testuser','test623','kancloud',charset='utf8')
    cursor=conn.cursor()
    #cursor.execute('SELECT link FROM books WHERE dlable=1 && name like "%C++%"')
    cursor.execute('SELECT link FROM books WHERE dlable="1"')
    r=list(cursor.fetchall())
    conn.commit()
    cursor.close()
    return r

def main():
    a=kan_db()
    a.create_table('books3',id='varchar(8) PRIMARY KEY',name='varchar(100)',link='varchar(200)',dlable='varchar(5)')
    books=a.load_books()
    a.fill_table(books,'books3')

    #cursor.execute('CREATE TABLE %s(id varchar(8) PRIMARY KEY, name varchar(100), link varchar(200), dlable varchar(5)) ' % tb_name)
if __name__=='__main__':
    main()

    sys.exit('EXIT...')
    conn=MySQLdb.connect('localhost','testuser','test623','kancloud',charset='utf8')
    cursor=conn.cursor()
    #cursor.execute('SELECT link FROM books WHERE dlable=1 && name like "%C++%"')
    cursor.execute('SELECT link FROM books WHERE dlable="1"')
    r=list(cursor.fetchall())
    for i in r:
        print i[0]

    #main()

