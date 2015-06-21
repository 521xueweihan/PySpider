#coding:utf-8
import urllib
######
#爬虫v0.1 利用urlib 和 字符串内建函数
######
'''目标网站：http://bohaishibei.com/post/category/main/
（一个很有趣的网站，一段话配一个图，老有意思了～）
'''
def getHtml(url):
    # 获取网页内容
    page = urllib.urlopen(url)
    html = page.read()
    return html

def content(html):
    # 内容分割的标签
    str = '<article class="article-content">'
    content = html.partition(str)[2]
    str1 = '<div class="article-social">'
    content = content.partition(str1)[0]
    return content # 得到网页的内容
    
def title(content,beg = 0):
    # 匹配title
    # 思路是利用str.index()和序列的切片
    try:
        title_list = []
        while True:   
            num1 = content.index('】',beg)+3
            num2 = content.index('</p>',num1)
            title_list.append(content[num1:num2])
            beg = num2
        
    except ValueError:
         return title_list
         
def get_img(content,beg = 0):
    # 匹配图片的url
    # 思路是利用str.index()和序列的切片
    try:
        img_list = []
        while True:   
            src1 = content.index('http',beg)
            src2 = content.index('/></p>',src1)
            img_list.append(content[src1:src2])
            beg = src2
        
    except ValueError:
         return img_list

def many_img(data,beg = 0):
    #用于匹配多图中的url
    try:
        many_img_str = ''
        while True:
            src1 = data.index('http',beg)
            src2 = data.index(' /><br /> <img src=',src1)
            many_img_str += data[src1:src2]+'|' # 多个图片的url用"|"隔开
            beg = src2
    except ValueError:
        return many_img_str              
         
def data_out(title, img):
    #写入文本
    with open("/home/qq/data.txt", "a+") as fo:
        fo.write('\n')
        for size in range(0, len(title)):
            # 判断img[size]中存在的是不是一个url
            if len(img[size]) > 70: 
                img[size] = many_img(img[size])# 调用many_img()方法
            fo.write(title[size]+'$'+img[size]+'\n')
        
   
#html = getHtml("http://bohaishibei.com/post/10475/")             
#content = content(html)
#title = title(content)
#img = get_img(content)
#data_out(title, img)
# 实现了爬的单个页面的title和img的url并存入文本

def main_content(html):
# 首页内容分割的标签
    str = '<div class="content">'
    content = html.partition(str)[2]
    str1 = '</div>'
    content = content.partition(str1)[0]
    return content # 得到网页的内容
  
#<h2><a href="http://bohaishibei.com/post/10262/" title="[博海拾贝0609期]今天是个好日子 - 博海拾贝">[博海拾贝0609期]今天是个好日子</a></h2>  
def page_url(content, beg = 0):
    try:
        many_img_str = ''
        while True:
            url1 = content.index('<h2><a href="',beg)+13
            url2 = content.index('" ',url1)
            many_img_str += content[url1:url2]+'|' # 多个图片的url用"|"隔开
            beg = url2
    except ValueError:
        return many_img_str   
        
main_html = getHtml("http://bohaishibei.com/post/category/main/")
clean_content = main_content(main_html) 
str = page_url(clean_content)
print str







