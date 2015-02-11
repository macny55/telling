$(document).ready( function(){
    var txt = $("#names").text(); // textareaの値
    // ページ読み込み時に実行したい処理
    var your_name = sessionStorage.getItem("your_name"); 
    var other_name = sessionStorage.getItem("other_name"); 
    var drama_name = sessionStorage.getItem("drama_name"); 
    var drama_image = sessionStorage.getItem("drama_image");
    var result = sessionStorage.getItem("result");
    
    txt = txt.replace(/your_name/g, your_name);
    txt = txt.replace(/other_name/g, other_name);
    $("#names").text(txt);
    $("#result").text(result);
    $("#image_def").attr("src","img/drama/"+drama_image);
    $("h2").text("「"+ drama_name +"」");

});