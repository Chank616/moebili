import json
import time

import requests

"""

moebili云签发行版

"""

if __name__ == '__main__':
    configDict = { 
        "cookies": {
            "DedeUserID": "****",
            "SESSDATA": "****",
            "bili_jct": "****"
            }
        }
    # 构造请求头
    headers = {"Cookie": "DedeUserID=" + configDict["cookies"]["DedeUserID"] +
                         "; SESSDATA=" + configDict["cookies"]["SESSDATA"] +
                         "; bili_jct=" + configDict["cookies"]["bili_jct"],
               "Referer": "https://www.bilibili.com/",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, "
                             "like Gecko) Chrome/87.0.4280.67 Safari/537.36"}
    # 尝试获取个人信息来判断cookie是否失效
    myInfoUrl = "https://api.bilibili.com/x/space/myinfo"
    myInfoBody = requests.get(url=myInfoUrl, headers=headers).json()
    # 失效直接退出凹
    if myInfoBody["code"] != 0:
        myInfoMessage = myInfoBody["message"]
        print(f"账号失效！错误信息：{myInfoMessage}")
        input('按任意键退出')
        exit(0)
    # 没失效继续执行
    uid = myInfoBody["data"]["mid"]
    name = myInfoBody["data"]["name"]
    print(f"uid：{uid} - 昵称：{name} - 确认存活，即将开始执行任务")

    # 补全Cookie，视频分享需要buvid3，buvid4
    cookieUrl = "https://api.bilibili.com/x/frontend/finger/spi"
    cookieBody = requests.get(url=cookieUrl, headers=headers).json()
    headers["Cookie"] += f"; buvid3={cookieBody['data']['b_3']}; buvid4={cookieBody['data']['b_4']}"

    # 每日登录
    everyLoginUrl = "https://www.bilibili.com/"
    everyLoginCode = requests.get(url=everyLoginUrl, headers=headers).status_code
    print("[每日登录]完成！") if everyLoginCode == 200 else print(f"[每日登录]访问B站首页出错，HTTP状态码：{everyLoginCode}。")

    # 视频观看 √
    watchUrl = "https://api.bilibili.com/x/v2/history/report"
    watchBody = requests.post(url=watchUrl,
                              data={
                                  "aid": 85763551,
                                  "cid": 146591846,
                                  "progress": 13,
                                  "csrf": configDict["cookies"]["bili_jct"]},
                              headers=headers).json()
    print(f"[视频观看]{watchBody}")

    # 视频分享 √

    # 初始化几个视频信息
    videosUrl = "https://api.bilibili.com/x/web-interface/index/top/rcmd?fresh_type=3"
    videosBody = requests.get(url=videosUrl,
                              headers=headers).json()
    aid = videosBody["data"]["item"][0]["id"]
    videoShareUrl = "https://api.bilibili.com/x/web-interface/share/add"
    videoShareBody = requests.post(url=videoShareUrl,
                                   data={
                                       "aid": aid,
                                       "csrf": configDict["cookies"]["bili_jct"],
                                       "eab_x": "2",
                                       "ramval": "0",
                                       "source": "web_normal",
                                       "ga": "1"},
                                   headers=headers).json()
    print(f"[视频分享]av{aid}，{videoShareBody}")
    # 直播签到
    liveSignUrl = "https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign"
    liveSignBody = requests.get(url=liveSignUrl, headers=headers).json()
    print(f"[直播签到]{liveSignBody}")

    # 银瓜子兑换硬币
    exchangeSilverCoinUrl = "https://api.live.bilibili.com/xlive/revenue/v1/wallet/silver2coin"
    exchangeSilverCoinBody = requests.post(url=exchangeSilverCoinUrl,
                                           data={"csrf": configDict["cookies"]["bili_jct"]},
                                           headers=headers).json()
    print(f"[银瓜子兑换硬币]{exchangeSilverCoinBody}")

    # 漫画签到 √
    mangaSignUrl = "https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn"
    mangaSignBody = requests.post(url=mangaSignUrl,
                                  data={"platform": 'ios'},
                                  headers=headers).json()
    print(f"[漫画签到]{mangaSignBody}")

    # 漫画分享 √
    mangaShareUrl = "https://manga.bilibili.com/twirp/activity.v1.Activity/ShareComic"
    mangaShareBody = requests.post(url=mangaShareUrl,
                                   data={"platform": 'ios'},
                                   headers=headers).json()
    print(f"[漫画分享]{mangaShareBody}")

    """
    大会员的操作
    """
    vipStatus = myInfoBody["data"]["vip"]["status"]
    # 领取B币券给自己充电 √
    if vipStatus:
        biBiQuanUrl = "https://api.bilibili.com/x/vip/privilege/receive"
        biBiQuanBody = requests.post(url=biBiQuanUrl,
                                     data={"csrf": configDict["cookies"]["bili_jct"],
                                           "platform": "web",
                                           "type": "1"}, headers=headers).json()
        if biBiQuanBody["code"] == 0:
            print("[领取B币券]完成！")
            chargeUrl = "https://api.bilibili.com/x/ugcpay/web/v2/trade/elec/pay/quick"
            chargeBody = requests.post(url=chargeUrl,
                                       data={"bp_num": "5", "is_bp_remains_prior": "true",
                                             "up_mid": configDict["cookies"]["DedeUserID"],
                                             "otype": "up",
                                             "oid": configDict["cookies"]["DedeUserID"],
                                             "csrf": configDict["cookies"]["bili_jct"]},
                                       headers=headers).json()
            print(f"[给自己充电]{chargeBody}")
        else:
            print(f"[领取B币券给自己充电]{biBiQuanBody['message']}")

        # 大会员积分并兑换大会员卡
        vipSignUrl = "https://api.bilibili.com/pgc/activity/score/task/sign"
        vipSignBody = requests.post(url=vipSignUrl, headers=headers).json()
        print(f"[会员签到]{vipSignBody}")

        tvTaskUrl = "https://api.bilibili.com/pgc/activity/deliver/task/complete"
        tvTaskBody = requests.post(url=tvTaskUrl,
                                   data={"position": "tv_channel"},
                                   headers=headers).json()
        print(f"[影视浏览]{tvTaskBody}")

        jpTaskUrl = "https://api.bilibili.com/pgc/activity/deliver/task/complete"
        jpTaskBody = requests.post(url=jpTaskUrl,
                                   data={"position": "jp_channel"},
                                   headers=headers).json()
        print(f"[番剧浏览]{jpTaskBody}")

        huiyuangouTaskUrl = "https://show.bilibili.com/api/activity/fire/common/event/dispatch"
        huiyuangouTaskBody = requests.post(url=huiyuangouTaskUrl,
                                           json={"eventId": "hevent_oy4b7h3epeb"},
                                           headers=headers).json()
        print(f"[会员购浏览]{huiyuangouTaskBody}")

        getFilmTaskUrl = "https://api.bilibili.com/pgc/activity/score/task/receive"
        getFilmTaskBody = requests.post(url=getFilmTaskUrl,
                                        json={"aid": "168dc68e2b237b544500d75cf3989803",
                                              "taskCode": "ogvwatch"},
                                        headers=headers).json()
        print(f"[领取观看正片任务]{getFilmTaskBody}")

        filmTaskUrl = "https://api.bilibili.com/x/click-interface/web/heartbeat"
        filmTaskBody = requests.post(url=filmTaskUrl,
                                     data={
                                         "start_ts": int(time.time()),  # 开始播放时间
                                         "aid": "561053721",  # 视频avid
                                         "cid": "846641366",  # 分p编号
                                         "type": "4",
                                         "sub_type": "4",
                                         "dt": "2",
                                         "play_type": "0",
                                         "played_time": "1800",
                                         "realtime": "1800",
                                         "real_played_time": "1800",
                                         "sid": "42384",
                                         "epid": "682241",
                                         "csrf": configDict["cookies"]["bili_jct"],
                                     },
                                     headers=headers).json()
        print(f"[完成观看正片内容]{filmTaskBody}")
        prizesUrl = "https://api.bilibili.com/x/vip_point/sku/list"
        prizesBody = requests.get(url=prizesUrl,
                                  params={
                                      "csrf": configDict["cookies"]["bili_jct"],
                                      "category_id": "1",
                                      "disable_rcmd": "0",
                                      "pn": "1",
                                      "ps": "20",
                                  }, headers=headers).json()
        for prize in prizesBody["data"]["skus"]:
            if "天卡" in prize["title"]:
                exchangeVipUrl = "https://api.bilibili.com/x/vip_point/trade/order/create"
                exchangeVipBody = requests.post(url=exchangeVipUrl,
                                                data={
                                                    "csrf": configDict["cookies"]["bili_jct"],
                                                    "category_id": "1",
                                                    "disable_rcmd": "0",
                                                    "price": prize["price"]["promotion"]["price"],
                                                    "token": prize["token"]},
                                                headers=headers).json()
                print(f"[兑换{prize['title']}]{exchangeVipBody}")
    else:
        print("[领取B币券给自己充电]不是会员！")
        print("[大会员积分]不是会员！")
    input('按任意键退出')
    exit(0)
