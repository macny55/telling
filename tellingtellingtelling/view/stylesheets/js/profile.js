$(function() {
    if($("input[name='your-name']").val().length == 0 || $("input[name='other-name']").val().length == 0 || $("input[name='your-sex']").is(':checked') == false){
		$('.judge-button').prop('disabled', true);
	}

/*ラジオボタンが必ず異性になるように制御   
    $("input[name='your-sex']").click(function() {
	if($('#your-male').is(':checked')){
	    $("input[name='other-sex']").attr('checked',false);
	    $('#other-female').attr('checked','checked');
	}else if($('your-female').is(':checked')){
	    $("input[name='other-sex']").attr('checked',false);
	    $('#other-male').attr('checked','checked');
	}
    });   
    $("input[name='other-sex']").click(function() {
	if($("input[name='other-sex']").val() == 'male'){
	    $("input[name='your-sex']").attr('checked',false);
	    $('#your-female').attr('checked','checked');
	}else if($("input[name='other-sex']").val() == 'female'){
	    $("input[name='your-sex']").attr('checked',false);
	    $('#your-male').attr('checked','checked');
	}
    });
*/

//全ての項目値が入力されれば次の画面に進めるボタンが有効化なるように制御
    $("input[name='other-sex']").click(function() {
	if($("input[name='your-name']").val().length == 0 || $("input[name='other-name']").val().length == 0 || $("input[name='your-sex']").is(':checked') == false){
	    $('.judge-button').prop('disabled', true);
	} else {
	    $('.judge-button').prop('disabled', false);
	    $("#judge").attr("src","img/judge.png");
	}
    });
    $("input[name='your-sex']").click(function() {
	if($("input[name='your-name']").val().length == 0 || $("input[name='other-name']").val().length == 0 || $("input[name='your-sex']").is(':checked') == false){
	    $('.judge-button').prop('disabled', true);
	} else {
	    $('.judge-button').prop('disabled', false);
	    $("#judge").attr("src","img/judge.png");
	}
    });
    $("input[name='your-name']").focusout(function() {
	if($("input[name='your-name']").val().length == 0 || $("input[name='other-name']").val().length == 0 || $("input[name='your-sex']").is(':checked') == false){
	    $('.judge-button').prop('disabled', true);
	} else {
	    $('.judge-button').prop('disabled', false);
	    $("#judge").attr("src","img/judge.png");
	}
    });
    $("input[name='other-name']").focusout(function() {
	if($("input[name='your-name']").val().length == 0 || $("input[name='other-name']").val().length == 0 || $("input[name='your-sex']").is(':checked') == false){
	    $('.judge-button').prop('disabled', true);
	} else {
	    $('.judge-button').prop('disabled', false);
	    $("#judge").attr("src","img/judge.png");
	}
    });
    $("input[name='your-birthday']").focusout(function() {
	if($("input[name='your-name']").val().length == 0 || $("input[name='other-name']").val().length == 0 || $("input[name='your-sex']").is(':checked') == false){
	    $('.judge-button').prop('disabled', true);
	} else {
	    $('.judge-button').prop('disabled', false);
	    $("#judge").attr("src","img/judge.png");
	}
    });
    $("input[name='other-birthday']").focusout(function() {
	if($("input[name='your-name']").val().length == 0 || $("input[name='other-name']").val().length == 0 || $("input[name='your-sex']").is(':checked') == false){
	    $('.judge-button').prop('disabled', true);
	} else {
	    $('.judge-button').prop('disabled', false);
	    $("#judge").attr("src","img/judge.png");
	}
    });
});

//if($("input[name='your-name']").val().length == 0 || $("input[name='other-name']").val().length == 0 || $("input[name='your-sex']").prop('checked') == false || $("input[name='other-sex']").prop('checked') == false){