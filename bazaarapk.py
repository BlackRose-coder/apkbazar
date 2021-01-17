#!/usr/bin/python
import requests as re
import json
import argparse
import sys

def get_details_apk(packageName):
    payload = {"properties":
            {"androidClientInfo":
                {"adId":"","province":"NA","androidId":"702d5128475dc4","city":"NA",
                    "country":"NA","cpu":"x86","device":"","product":"vbox86p","osBuild":"",
                    "hardware":"","model":"Custom Phone","locale":"","manufacturer":"unknown",
                    "mcc":310,"mnc":260,"mobileServiceType":0,"height":1184,"dpi":320,"deviceType":0,
                    "adOptOut":False,"sdkVersion":19,"width":768},"clientID":"LjaphYhASJK1XZBO7J71Lg",
                    "clientVersion":"11.0.1","isKidsEnabled":False,"clientVersionCode":110001,"language":2,
                    "appThemeState":0},"singleRequest":{"appDownloadInfoRequest":{"packageName":packageName,"downloadStatus":1
                }
            }
        }
    response = re.post("https://api.cafebazaar.ir/rest-v1/process/AppDownloadInfoRequest",json=payload).json()
    return response["singleReply"]["appDownloadInfoReply"]["token"]+'.apk'

def apk_download(address,name):
    apk_name = name+'.apk'
    url = "https://appcdn.cafebazaar.ir/apks/{}".format(address)
    with open(apk_name, "wb") as f:
        response = re.get(url,stream=True)
        content_len = int(response.headers.get("content-length"))
        recive_len = 0 
        for data in response.iter_content(chunk_size=4096):
            recive_len += len(data)
            f.write(data)
            done = int(30 * recive_len / content_len)
            sys.stdout.write("\r %s: [%s%s]" % (apk_name,'=' * done, ' ' * (30-done)))
            sys.stdout.flush()
    print("\n") 
    
example_txt = '''
    python bazaarapk.py -p 'xxx.xxxxx' -n 'apkname'
'''
parser = argparse.ArgumentParser(description='Download apk from bazar',epilog=example_txt)
parser.add_argument('-p', type=str, help='packagename', required=True)
parser.add_argument('-n', type=str, help='apk name', required=True)
args = parser.parse_args()
if __name__ == "__main__":
    apk_download(get_details_apk(args.p),args.n)
