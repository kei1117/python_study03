import time
import datetime
import math
import eel

import pandas as pd

from chrome_driver import *

EXP_CSV_PATH = "results/exp_list_{search_keyword}_{datetime}.csv"
PAGE_URL = "https://tenshoku.mynavi.jp/list/kw{search_keyword}/pg{page_count}/?jobsearchType=14&searchType=18"


@eel.expose
def main(search_keyword):
    
    # driverを起動
    chrome_driver = ChromeDriver()
    chrome_driver.open_url(PAGE_URL.format(search_keyword = search_keyword, page_count = 1))
    
    time.sleep(5)
    
    chrome_driver.log(f"処理開始")
    chrome_driver.log("検索キーワード:{}".format(search_keyword))

    # ポップアップを閉じる
    chrome_driver.close_modal()
    time.sleep(5)
    chrome_driver.close_modal()
    
    # 最大件数取得
    max_data = chrome_driver.get_text("result__num")
    max_data = int(max_data.replace('件',''))
    
    # 最大ページ数を計算
    max_page = math.ceil(max_data/50)
    print(f'全{max_data}件,{max_page}ページあります')
    
    
    data = []
    page_count = 1

    while page_count <= max_page:
        print(f'{page_count}ページ目です！')
        
        # jsへ情報を渡す
        eel.to_js_process_doing(page_count, max_page, max_data) # type: ignore
        
        chrome_driver.open_url(PAGE_URL.format(search_keyword = search_keyword, page_count = page_count))
        time.sleep(3)
        result = chrome_driver.get_data(page_count)
        data.extend(result)
        page_count += 1
        
    chrome_driver.log("処理終了")
        
    # # DataFrame作成
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    df = pd.DataFrame(data)    
    chrome_driver.makedir_for_filepath(EXP_CSV_PATH)
    df.to_csv(EXP_CSV_PATH.format(search_keyword=search_keyword, datetime=now), header=False, index=False, encoding='utf_8_sig')
    
    msg = f"csv書き込み処理完了 成功件数: {chrome_driver.success} 件 / 失敗件数: {chrome_driver.fail} 件"
    chrome_driver.log(msg)

    # jsへ情報を渡す
    eel.to_js_process_end(msg)  # type: ignore

# ウエブコンテンツを持つフォルダー
eel.init("web")

# 最初に表示するhtmlページ
eel.start("index.html", size=(750,600))