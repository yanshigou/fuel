import requests
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool
url = 'https://www.autohome.com.cn/grade/carhtml/{}.html'


def year(endurl, ent3, ent1):
    endresu = []
    res = requests.get(endurl)
    soup = BeautifulSoup(res.text, 'html.parser')
    f = open('CarInfo.txt', "a+", encoding='utf-8')
    for ant0 in soup.select('#divSeries'):
        for ant1 in ant0.select('.interval01'):
            for ant2 in ant1.select('.interval01-list'):
                for ant3 in ant2.select('li'):
                    resu2 = {}
                    resu2['车系'] = ent3.select('h4 a')[0].text.replace("·", "")
                    resu2['品牌'] = ent1.select('dt div a')[0].text.replace("·", "")
                    resu2['年款'] = ant3.select('.interval01-list-cars p a')[0].text.replace("·", "")
                    if ant2.select('.interval01-list-guidance div'):
                        resu2['价格'] = ant3.select('.interval01-list-guidance div')[0].text
                    else:
                        resu2['价格'] = '暂无报价'
                    print(resu2)
                    f.write(ent1.select('dt div a')[0].text.replace("·", "")+" "+ent3.select('h4 a')[0].text.replace("·", "")+" "+ant3.select('.interval01-list-cars p a')[0].text.replace("·", "")+"\n")
                    endresu.append(resu2)
    f.close()
    return endresu


def fn(carurl):
    endresult1 = []
    res = requests.get(carurl)
    soup = BeautifulSoup(res.text, 'html.parser')
    for ent1 in soup.select('dl'):
        # print(ent1)
        for ent2 in ent1.select('.rank-list-ul'):
            # print(ent2)
            for ent3 in ent2.select('li'):
                # print(ent3)
                if ent3.select('h4'):
                    m = re.search('<a href="//car.autohome.com.cn/price(.*)">报价', str(ent3))
                    if m:
                        ypnum = m.group(1)
                        endresult1.extend(year("https://car.autohome.com.cn/price" + ypnum, ent3, ent1))
    return endresult1


if __name__ == '__main__':
    endresult = []
    # res=[]

    # 多线程(快)（适用于网络密集型请求）
    # for i in range(97, 123):
    #     p = MyThread(chr(i).upper())
    #     # res.append(p)
    #     p.start()

    # 多进程(还可以)(cpu密集型，io密集型，网络密集型都适用，但相对占用CPU资源)
    # for i in range(97,123):
    #     p=MyProcess(chr(i).upper())
    #     p.start()

    # 进程池(慢)
    p = Pool(4)
    for i in range(97, 123):
        newurl=url.format(chr(i).upper())
    # newurl = url.format(chr(97).upper())
        res = p.apply(fn, args=(newurl,))
        endresult.extend(res)
        # p.close()
        # p.join()
        print(endresult.__len__())
    # newurl = url.format(chr(97).upper())
    # fn(newurl)

    # for x in res:
    #     x.join()
    #     endresult.extend(x.get_result())
    # df = pandas.DataFrame(endresult)
    # print(df)
    # df.to_excel('car18.xlsx')

    # f = open('CarInfo.txt', encoding='utf-8')
    # for i in f:
    #     print(i)

# IO密集型代码(文件处理、网络爬虫等)，
# 多线程能够有效提升效率(单线程下有IO操作会进行IO等待，造成不必要的时间浪费，
# 而开启多线程能在线程A等待时，自动切换到线程B，可以不浪费CPU的资源，从而能提升程序执行效率)。
# 所以python的多线程对IO密集型代码比较友好。

