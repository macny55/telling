function save_confirm(usr_name,twitter_name,login){ 
    // 「OK」時の処理開始 ＋ 確認ダイアログの表示
    if(login == 0){
	if(window.confirm('保存するためにTwitterでログインしてください')){
	    //location.href = "http://tellingtellingtelling.appspot.com/login";
	    location.href = "http://localhost:9080/login";
	    return 0;
	}else{
	    return 1;
	}
    }else{
    // サブミットするフォームを取得
	var f = document.forms['save_content'];
	f.method = 'POST';
	f.action = '/save_result';
	f.submit();
	return 0;
    }
}