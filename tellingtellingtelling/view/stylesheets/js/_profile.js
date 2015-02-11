$(function() {
    $("form").submit(function(){
	if($("input[name='your-name']").val().length == 0 || $("input[name='other-name']").val().length == 0){	
	    $("button[class='judge-button']").before("<span>名前が未入力です</span>");
	    $("span").css({
		"color":"red",
		"font-weight":"bold"
	    });
	    return false;
	}
	else if($("input[name='your-sex']").is(':checked') == false || $("input[name='other-sex']").is(':checked') == false){	
	    $("button[class='judge-button']").before("<span>性別が未入力です</span>");
	    $("span").css({
		"color":"red",
		"font-weight":"bold"
	    });
	    return false;
	}
    });
});

//if($("input[name='your-name']").val().length == 0 || $("input[name='other-name']").val().length == 0 || $("input[name='your-sex']").prop('checked') == false || $("input[name='other-sex']").prop('checked') == false){	