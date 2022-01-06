$(document).ready(function(){
	$("button").click(function(){
		$question = $(this).attr("class");
		$cl = "#" + $question;
		$($cl).append("<ol><input type='text' name='" + $question + "'></ol>");});
	$("#submitbutton").click(function(){
		$("#answersid").submit();
	});
});
