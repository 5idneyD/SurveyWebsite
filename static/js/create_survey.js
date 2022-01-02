var question_number = 1;
$(document).ready(function(){
	$("#addquestion").click(function(){
		$("#questions").append("<ol class='question'>" + question_number + "<input type='text'></ol>");
		question_number += 1;});
		
})