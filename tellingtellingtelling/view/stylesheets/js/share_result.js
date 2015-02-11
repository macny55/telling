$(document).ready( function(){
 //  if($("*[name=get_flag]").val()==1){
	// ページ読み込み時に実行したい処理
	var txt = $("*[name=tweet]").val(); // textareaの値
	var drama_name = sessionStorage.getItem("drama_name"); 
	var drama_image = sessionStorage.getItem("drama_image"); 
	var drama_image_url = sessionStorage.getItem("drama_image_url"); 
	txt = txt.replace(/「」/g, "「" + drama_name + "」");
	$("*[name=tweet]").val(txt);
	$("*[name=drama_image]").val(drama_image);
    	$("*[name=drama_image_url]").val(drama_image_url);
 //   }
});