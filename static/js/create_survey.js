var question_number = 2;
$(document).ready(function(){
	$("#addquestion").click(function(){
		$("#questions").append("<ol>" + question_number + "<input type='text'></ol>");
		question_number += 1;})
})