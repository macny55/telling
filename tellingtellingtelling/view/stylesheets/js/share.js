function save_session(your_name,other_name,drama_name,drama_image,drama_image_url,result){ 
    var storage = sessionStorage;
    storage.clear();
    storage.setItem("your_name",your_name);
    storage.setItem("other_name", other_name);
    storage.setItem("drama_name",drama_name );
    storage.setItem("drama_image", drama_image);
    storage.setItem("drama_image_url", drama_image_url);
    storage.setItem("result", result);
    // サブミットするフォームを取得
    var f = document.forms['share_content'];
    f.method = 'POST';
    f.action = '/share_result';
    f.submit();
    return 0;
}