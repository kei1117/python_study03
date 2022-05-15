
function startScraping() {
    let search_keyword = document.getElementById("search_keyword").value;

    if (search_keyword.trim().length == 0) {
        alert('検索ワードを入力してください')
        return;
    }

    document.getElementById("text_box").innerHTML = 'スクレイピングを開始します！';

    // ここでPython側の処理を実行
    eel.main(search_keyword);
}

eel.expose(to_js_process_end);
function to_js_process_end(msg) {
    alert('スクレイピングが完了しました！'+ msg)
}

eel.expose(to_js_process_doing);
function to_js_process_doing(page_count, max_page,max_data) {
    document.getElementById("text_box").innerHTML = 'スクレイピング データ取得中';
    document.getElementById("text_box2").innerHTML = '全'+max_data+'件・'+ max_page +'ページあります';
    document.getElementById("text_box3").innerHTML = page_count +'/'+max_page +'ページ目の処理を開始しています';
}
