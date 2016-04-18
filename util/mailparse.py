# -*-coding:utf-8 -*-
"""
   ********************************************************
   * Author: zhang baoqing                                *
   *                                                      *
   * Mail :  zhangbaoqing@xiaomi.com                      *
   *                                                      *
   * Create Time: 2015-12-21 09:49                        *
   *                                                      *
   * Filename: recevie_mail.py
   *                                                      *
   ********************************************************
    说明：
        请打开163邮箱的imap服务
"""

import imaplib
import email

class MailParse():
    __host = "imap.163.com" # "pop.mail_serv.com"
    __username = "" # xxx.163.com
    __password = ""  # 登录密码
    __port = 993
    try:
        serv = imaplib.IMAP4_SSL(__host, __port)
    except Exception, e:
        serv = imaplib.IMAP4(__host, __port)

    @classmethod
    def parseHeader(cls, message):
        """ 解析邮件首部 """
        subject = message.get('subject')   
        h = email.Header.Header(subject)
        dh = email.Header.decode_header(h)
       # print "dh00: %s, dh01: %s" % (dh[0][0], dh[0][1])
        if not dh[0][1]:
            charset = "utf-8"
        else:
            charset = dh[0][1]
        subject = unicode(dh[0][0], charset).encode('utf-8')
        # 主题
        #print subject
        #print '</br>'
        # 发件人
        #print 'From:', email.utils.parseaddr(message.get('from'))[1]
        #print '</br>'
        # 收件人
        #print 'To:', email.utils.parseaddr(message.get('to'))[1]
        #print '</br>'
        # 抄送人
        #print 'Cc:',email.utils.parseaddr(message.get_all('cc'))[1]
        return email.utils.parseaddr(message.get('from'))[1]

    @classmethod
    def parseBody(cls, message):
        """ 解析邮件/信体 """
        # 循环信件中的每一个mime的数据块
        for part in message.walk():
            # 这里要判断是否是multipart，是的话，里面的数据是一个message 列表
            if not part.is_multipart(): 
                charset = part.get_charset()
               # print 'charset: ', charset
                contenttype = part.get_content_type()
                #print 'content-type', contenttype
                name = part.get_param("name") #如果是附件，这里就会取出附件的文件名
                if name:
                    # 有附件
                    # 下面的三行代码只是为了解码象=?gbk?Q?=CF=E0=C6=AC.rar?=这样的文件名
                    fh = email.Header.Header(name)
                    fdh = email.Header.decode_header(fh)
                    fname = dh[0][0]
                    #print '附件名:', fname
                    # attach_data = par.get_payload(decode=True) #　解码出附件数据，然后存储到文件中
         
                    # try:
                    #     f = open(fname, 'wb') #注意一定要用wb来打开文件，因为附件一般都是二进制文件
                    # except:
                    #     print '附件名有非法字符，自动换一个'
                    #     f = open('aaaa', 'wb')
                    # f.write(attach_data)
                    # f.close()
                else:
                    #不是附件，是文本内容
                    body = part.get_payload(decode=True) # 解码出文本内容，直接输出来就可以了。
                    if body:
                        return body
                    # pass
                # print '+'*60 # 用来区别各个部分的输出

    @classmethod
    def getMail(cls):
       
        cls.serv.login(cls.__username, cls.__password)
        cls.serv.select("mywork") #选取所要获取邮件的文件夹
        # 搜索邮件内容
        typ, data = cls.serv.search(None, 'ALL') 

        count = 1
        pcount = 1
        from_ = u""
        body = u""
        for num in data[0].split()[::-1]:
            typ, data = cls.serv.fetch(num, '(RFC822)')
            text = data[0][1]
            message = email.message_from_string(text)   # 转换为email.message对象
            from_ = cls.parseHeader(message)
            #print '</br>'
            body = cls.parseBody(message)    
            pcount += 1
            cls.serv.store(num, '+FLAGS', '\\Deleted') #读完邮件后，删除邮件，保证cront每次获取的是最新邮件
            if pcount > count:
                break

        cls.serv.expunge()
        cls.serv.close()
        cls.serv.logout()
        return from_, body

    @classmethod
    def deletemail(cls):
        pass




if __name__ == "__main__":
    from_, body =MailParse.getMail()
    print "from: %s\n"% from_
    print "body: %s\n"% body
