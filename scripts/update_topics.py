#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import re
import os
import sys
from datetime import datetime, timezone, timedelta
from urllib.parse import quote
from difflib import SequenceMatcher

DATA_FILE = "data/hot_topics.json"
TIMEOUT = 15
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

SPORTS_KEYWORDS = [
    "湖人","勇士","凯尔特人","尼克斯","雷霆","马刺","骑士","掘金","雄鹿","热火",
    "独行侠","快船","太阳","76人","猛龙","公牛","老鹰","步行者","篮网","灰熊",
    "鹈鹕","爵士","开拓者","国王","森林狼","黄蜂","活塞","魔术","奇才","火箭",
    "詹姆斯","库里","杜兰特","东契奇","约基奇","字母哥","文班亚马","亚历山大",
    "布伦森","唐斯","哈登","米切尔","塔图姆","欧文","伦纳德","保罗","威少",
    "浓眉","戴维斯","爱德华兹","莫兰特","锡安","恩比德","巴特勒",
    "利拉德","乔治","布克","特雷杨","西亚卡姆","戈贝尔","波尔津吉斯",
    "NBA","CBA","总决赛","季后赛","东决","西决","夺冠","MVP","FMVP",
    "选秀","交易","签约","续约","退役","复出","伤病","绝杀","横扫",
    "比分","加时","裁判","犯规","三分","扣篮","盖帽","助攻","篮板",
    "欧冠","世界杯","欧洲杯","英超","西甲","德甲","意甲","法甲","中超",
    "梅西","C罗","姆巴佩","哈兰德","贝林厄姆","维尼修斯","罗德里","亚马尔",
    "皇马","巴萨","曼联","曼城","利物浦","阿森纳","切尔西","拜仁","巴黎",
    "国足","武磊","孙兴慜","三笘薰","金球奖","金靴","红牌","点球","越位",
    "网球","温网","法网","澳网","美网","费德勒","纳达尔","德约","阿尔卡拉斯",
    "F1","赛车","汉密尔顿","舒马赫","勒克莱尔","维斯塔潘",
    "奥运","奥运会","亚运","全红婵","樊振东","孙颖莎","王楚钦","潘展乐",
    "郑钦文","谷爱凌","苏翊鸣","UFC","拳击","泰森","张志磊",
    "乒乓球","羽毛球","跳水","游泳","体操","田径","排球","女排",
    "斯诺克","丁俊晖","奥沙利文","特鲁姆普","希金斯","塞尔比",
    "棒球","橄榄球","高尔夫","老虎伍兹","柯洁","围棋","象棋",
]

MOVIE_KEYWORDS = [
    "电影","票房","上映","首映","点映","排片","观影","影评","烂片","神作",
    "豆瓣","评分","IMDb","奥斯卡","戛纳","柏林","威尼斯","金像奖","金马奖",
    "好莱坞","宝莱坞","流媒体","Netflix","Disney","HBO","Hulu","Apple TV",
    "剧集","电视剧","网剧","台剧","港剧","韩剧","日剧","美剧","英剧",
    "综艺","真人秀","选秀","纪录片","动漫","动画","番剧","国漫","日漫",
    "导演","编剧","制片人","监制","杀青","开机","定档","撤档","改档",
    "预告片","海报","剧照","路透","番位","撕番","换角","选角","试镜",
    "票房破","票房冠军","票房纪录","首日票房","累计票房","分账票房",
    "口碑","评分","烂番茄","爆米花","豆瓣分","开分","涨分","跌分",
    "爆款","神剧","烂尾","高开低走","低开高走","续集","前传","外传",
    "翻拍","改编","原著","小说改","漫改","游戏改","真人版","影版","剧版",
    "院线","流媒体上线","全网独播","同步播出","超前点播","大结局","收官",
    "金鹰奖","白玉兰","飞天奖","百花奖","华表奖","金鸡奖","金马奖","金像奖",
    "艾美奖","金球奖","格莱美","托尼奖","威尼斯","柏林","戛纳","圣丹斯",
    "北影节","上影节","FIRST","平遥","釜山","东京电影节",
    "贺岁档","春节档","暑期档","国庆档","五一档","情人节档","清明档",
    "视帝","视后","影帝","影后","最佳男配","最佳女配","最佳导演",
    "提名","入围","获奖","大满贯","双黄蛋","爆冷","陪跑",
    "宫崎骏","诺兰","昆汀","斯皮尔伯格","卡梅隆","维伦纽瓦","奉俊昊",
    "是枝裕和","北野武","李安","王家卫","张艺谋","陈凯歌","冯小刚",
    "贾樟柯","王小帅","娄烨","宁浩","姜文","管虎","陈思诚","郭帆",
    "饺子","田晓鹏","追光","彩条屋","皮克斯","迪士尼","梦工厂",
    "漫威","DC","蜘蛛侠","钢铁侠","蝙蝠侠","超人","金刚狼","死侍",
    "星球大战","星际迷航","哈利波特","指环王","霍比特人","沙丘",
    "阿凡达","泰坦尼克号","盗梦空间","星际穿越","黑暗骑士","教父",
    "肖申克","楚门","阿甘","辛德勒","美丽人生","千与千寻","龙猫",
    "霸王别姬","活着","无间道","大话西游","功夫","让子弹飞","药神",
    "流浪地球","哪吒","战狼","红海","长津湖","满江红","封神","热辣滚烫",
    "第二十条","飞驰人生","熊出没","喜羊羊","猪猪侠","柯南","哆啦A梦",
    "蜡笔小新","海贼王","火影","死神","鬼灭","咒术","间谍过家家",
    "三体","流浪地球","狂飙","漫长的季节","隐秘的角落","沉默的真相",
    "庆余年","赘婿","雪中悍刀行","斗罗大陆","斗破苍穹","完美世界",
    "凡人修仙传","吞噬星空","神印王座","一念永恒","仙逆",
    "长相思","莲花楼","苍兰诀","星汉灿烂","梦华录","卿卿日常",
    "开端","人世间","觉醒年代","山海情","大江大河","繁花",
    "我的阿勒泰","春色寄情人","承欢记","与凤行","玫瑰的故事",
    "歌手","浪姐","披哥","声生不息","时光音乐会","你好星期六",
    "奔跑吧","极限挑战","五哈","向往的生活","桃花坞","五十公里",
    "密室大逃脱","明星大侦探","大侦探","萌探","开始推理吧",
    "脱口秀","吐槽大会","喜剧大赛","一年一度","喜人奇妙夜",
    "脱口秀大会","怎么办","脱口秀","谐星","相声","德云社",
    "赵本山","沈腾","马丽","贾玲","张小斐","周星驰","成龙","李连杰",
    "吴京","黄渤","徐峥","王宝强","雷佳音","张译","于和伟","胡歌",
    "刘亦菲","赵丽颖","杨幂","迪丽热巴","杨紫","周冬雨","章子怡",
    "巩俐","张曼玉","林青霞","王祖贤","周迅","汤唯","倪妮",
    "朱一龙","王一博","肖战","易烊千玺","王俊凯","王源","李现",
    "成毅","檀健次","邓为","张凌赫","王鹤棣","吴磊","刘昊然",
    "白敬亭","魏大勋","范丞丞","蔡徐坤","华晨宇","薛之谦","张杰",
    "周深","毛不易","李荣浩","邓紫棋","蔡依林","王心凌","杨丞琳",
    "周杰伦","林俊杰","五月天","陈奕迅","张学友","刘德华","黎明",
    "郭富城","张国荣","梅艳芳","Beyond","崔健","窦唯","朴树",
    "许巍","李志","宋冬野","赵雷","毛不易","李健","张杰",
]

def now_beijing():
    return datetime.now(timezone(timedelta(hours=8)))

def safe_request(url, headers=None, timeout=TIMEOUT):
    try:
        resp = requests.get(url, headers=headers or HEADERS, timeout=timeout)
        if resp.status_code == 200:
            return resp
    except Exception as e:
        print(f"  [ERROR] Request failed: {url} -> {e}")
    return None

def classify_topic(title):
    # 强制排除 - 这些标题无论命中什么关键词都不算影视/体育
    FORCE_EXCLUDE = ["武契奇", "火影手游"]
    if any(kw in title for kw in FORCE_EXCLUDE):
        return None

    is_sports = any(kw in title for kw in SPORTS_KEYWORDS)
    is_movie = any(kw in title for kw in MOVIE_KEYWORDS)
    if is_sports and is_movie:
        return "综合"
    elif is_sports:
        return "体育"
    elif is_movie:
        return "影视"
    else:
        return None

def normalize_title(title):
    t = title.strip()
    t = re.sub(r"^#+|#+$", "", t)
    t = re.sub(r"\s+", "", t)
    t = re.sub(r"[【】\[\]()]", "", t)
    return t

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def merge_topics(all_items):
    merged = []
    for item in all_items:
        norm = normalize_title(item["title"])
        found = False
        for m in merged:
            if similarity(norm, normalize_title(m["title"])) > 0.65 or norm in m["title"] or m["title"] in norm:
                m["sources"].append(item["source"])
                m["hot_value"] += item.get("hot_value", 0)
                if item.get("url"):
                    m["urls"][item["source"]] = item["url"]
                found = True
                break
        if not found:
            merged.append({
                "title": item["title"],
                "category": item["category"],
                "sources": [item["source"]],
                "hot_value": item.get("hot_value", 0),
                "urls": {item["source"]: item.get("url", "")} if item.get("url") else {},
                "raw_titles": [item["title"]]
            })
    return merged

def fetch_weibo():
    items = []
    try:
        url = "https://weibo.com/ajax/side/hotSearch"
        resp = safe_request(url, headers={
            **HEADERS,
            "Referer": "https://weibo.com/"
        })
        if resp:
            data = resp.json()
            if data.get("ok") == 1 and data.get("data") and data["data"].get("realtime"):
                for d in data["data"]["realtime"]:
                    title = d.get("word", "")
                    if not title:
                        continue
                    cat = classify_topic(title)
                    if cat:
                        hot = d.get("num", 0)
                        if not hot:
                            hot = (51 - d.get("realpos", 50)) * 10000
                        items.append({
                            "title": title,
                            "source": "微博",
                            "category": cat,
                            "hot_value": hot,
                            "url": f"https://s.weibo.com/weibo?q={quote(title)}"
                        })
    except Exception as e:
        print(f"  [WARN] Weibo fetch error: {e}")
    return items

def fetch_baidu():
    items = []
    try:
        url = "https://top.baidu.com/api/board?platform=wise&tab=realtime"
        resp = safe_request(url)
        if resp:
            data = resp.json()
            if data.get("success") and data.get("data") and data["data"].get("cards"):
                cards = data["data"]["cards"]
                for card in cards:
                    if card.get("component") == "tabTextList":
                        for content in card.get("content", []):
                            for item in content.get("content", []):
                                title = item.get("word", "")
                                if not title:
                                    continue
                                cat = classify_topic(title)
                                if cat:
                                    idx = item.get("index", 50)
                                    hot = (51 - idx) * 9000
                                    items.append({
                                        "title": title,
                                        "source": "百度",
                                        "category": cat,
                                        "hot_value": hot,
                                        "url": item.get("url", "")
                                    })
    except Exception as e:
        print(f"  [WARN] Baidu fetch error: {e}")
    return items

def fetch_douyin():
    items = []
    try:
        url = "https://aweme.snssdk.com/aweme/v1/hot/search/list/"
        resp = safe_request(url, headers={
            **HEADERS,
            "Referer": "https://www.douyin.com/"
        })
        if resp:
            data = resp.json()
            if data.get("status_code") == 0 and data.get("data") and data["data"].get("word_list"):
                for d in data["data"]["word_list"]:
                    title = d.get("word", "")
                    if not title:
                        continue
                    cat = classify_topic(title)
                    if cat:
                        items.append({
                            "title": title,
                            "source": "抖音",
                            "category": cat,
                            "hot_value": d.get("hot_value", 0) or (51 - d.get("position", 50)) * 8000,
                            "url": f"https://www.douyin.com/search/{quote(title)}"
                        })
    except Exception as e:
        print(f"  [WARN] Douyin fetch error: {e}")
    return items

def fetch_bilibili():
    items = []
    try:
        url = "https://api.bilibili.com/x/web-interface/search/square?limit=50"
        resp = safe_request(url, headers={
            **HEADERS,
            "Referer": "https://search.bilibili.com/"
        })
        if resp:
            data = resp.json()
            if data.get("code") == 0 and data.get("data") and data["data"].get("trending"):
                for d in data["data"]["trending"].get("list", []):
                    title = d.get("keyword", "")
                    if not title:
                        continue
                    cat = classify_topic(title)
                    if cat:
                        items.append({
                            "title": title,
                            "source": "哔哩哔哩",
                            "category": cat,
                            "hot_value": d.get("heat_score", 0) or 50000,
                            "url": f"https://search.bilibili.com/all?keyword={quote(title)}"
                        })
    except Exception as e:
        print(f"  [WARN] Bilibili fetch error: {e}")
    return items

def fetch_hupu():
    items = []
    try:
        url = "https://bbs.hupu.com/all-nba"
        resp = safe_request(url, headers={
            **HEADERS,
            "Referer": "https://bbs.hupu.com/"
        })
        if resp:
            html = resp.text
            pattern = r'<a[^>]*class="[^"]*truetit[^"]*"[^>]*href="(/[^"]+)"[^>]*>(.*?)</a>'
            matches = re.findall(pattern, html)
            for i, (href, title_raw) in enumerate(matches[:30]):
                title = re.sub(r"<[^>]+>", "", title_raw).strip()
                if not title:
                    continue
                cat = classify_topic(title) or "体育"
                items.append({
                    "title": title,
                    "source": "虎扑",
                    "category": cat,
                    "hot_value": (30 - min(i, 29)) * 5000,
                    "url": f"https://bbs.hupu.com{href}"
                })
    except Exception as e:
        print(f"  [WARN] Hupu fetch error: {e}")
    return items

def fetch_douban_movie():
    items = []
    try:
        url = "https://movie.douban.com/chart"
        resp = safe_request(url, headers={
            **HEADERS,
            "Referer": "https://movie.douban.com/"
        })
        if resp:
            html = resp.text
            pattern = r'<div class="pl2">.*?<<a[^>]*>(.*?)</a>.*?<<span class="rating_nums">([\d.]+)</span>.*?<<span class="pl">\((\d+)人评价\)</span>'
            matches = re.findall(pattern, html, re.DOTALL)
            for i, (title_raw, rating, people) in enumerate(matches[:15]):
                title = re.sub(r"<[^>]+>", "", title_raw).strip().split("/")[0].strip()
                if not title:
                    continue
                hot = float(rating) * 10000 + int(people) * 0.1
                items.append({
                    "title": f"豆瓣热门电影：{title}",
                    "source": "豆瓣电影",
                    "category": "影视",
                    "hot_value": hot,
                    "url": f"https://movie.douban.com/subject_search?search_text={quote(title)}"
                })
    except Exception as e:
        print(f"  [WARN] Douban movie fetch error: {e}")
    return items

def fetch_douban_tv():
    items = []
    try:
        url = "https://movie.douban.com/tv/"
        resp = safe_request(url, headers={
            **HEADERS,
            "Referer": "https://movie.douban.com/"
        })
        if resp:
            html = resp.text
            pattern = r'<em>(.*?)</em>.*?<<span class="rating_nums">([\d.]+)</span>'
            matches = re.findall(pattern, html, re.DOTALL)
            for i, (title_raw, rating) in enumerate(matches[:15]):
                title = re.sub(r"<[^>]+>", "", title_raw).strip()
                if not title or len(title) > 50:
                    continue
                items.append({
                    "title": f"豆瓣热门剧集：{title}",
                    "source": "豆瓣剧集",
                    "category": "影视",
                    "hot_value": float(rating) * 10000 if rating else 50000 - i*2000,
                    "url": f"https://movie.douban.com/subject_search?search_text={quote(title)}"
                })
    except Exception as e:
        print(f"  [WARN] Douban TV fetch error: {e}")
    return items

def main():
    print(f"[{now_beijing().strftime('%Y-%m-%d %H:%M:%S')}] 开始抓取影视+体育话题...")
    
    all_items = []
    sources = [
        ("微博", fetch_weibo),
        ("百度", fetch_baidu),
        ("抖音", fetch_douyin),
        ("哔哩哔哩", fetch_bilibili),
        ("虎扑", fetch_hupu),
        ("豆瓣电影", fetch_douban_movie),
        ("豆瓣剧集", fetch_douban_tv),
    ]
    
    for name, func in sources:
        try:
            items = func()
            print(f"  [{name}] 抓取到 {len(items)} 条相关话题")
            all_items.extend(items)
        except Exception as e:
            print(f"  [{name}] 抓取失败: {e}")
    
    if not all_items:
        print("[ERROR] 所有数据源均失败，保留旧数据")
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f2:
                old = json.load(f2)
            old["note"] = f"本次更新失败，数据为上次有效更新：{old.get('update_time', 'unknown')}"
            old["update_time"] = now_beijing().strftime("%Y-%m-%d %H:%M:%S")
            with open(DATA_FILE, 'w', encoding='utf-8') as f2:
                json.dump(old, f2, ensure_ascii=False, indent=2)
        return
    
    merged = merge_topics(all_items)
    merged.sort(key=lambda x: x["hot_value"], reverse=True)
    
    for i, m in enumerate(merged, 1):
        m["rank"] = i
    
    # 体育榜
    sports = [m for m in merged if m["category"] in ("体育", "综合")]
    
    # 影视榜 - 过滤特定内容和豆瓣来源
    EXCLUDED_MOVIE_KEYWORDS = ["火影手游", "武契奇"]
    EXCLUDED_MOVIE_SOURCES = ["豆瓣电影", "豆瓣剧集"]
    
    movies = []
    for m in merged:
        if m["category"] in ("影视", "综合"):
            # 排除特定关键词
            if any(kw in m["title"] for kw in EXCLUDED_MOVIE_KEYWORDS):
                continue
            # 排除豆瓣来源
            if any(src in m.get("sources", []) for src in EXCLUDED_MOVIE_SOURCES):
                continue
            movies.append(m)
    
    for i, m in enumerate(sports, 1):
        m["sports_rank"] = i
    for i, m in enumerate(movies, 1):
        m["movie_rank"] = i
    
    result = {
        "update_time": now_beijing().strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(merged),
        "sports_count": len(sports),
        "movie_count": len(movies),
        "all": merged[:100],
        "sports": sports[:50],
        "movies": movies[:50],
    }
    
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f2:
        json.dump(result, f2, ensure_ascii=False, indent=2)
    
    print(f"[{now_beijing().strftime('%Y-%m-%d %H:%M:%S')}] 更新完成：综合榜 {len(merged)} 条 | 体育榜 {len(sports)} 条 | 影视榜 {len(movies)} 条")

if __name__ == "__main__":
    main()
