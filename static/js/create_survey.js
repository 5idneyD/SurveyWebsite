var question_number = 1;
$(document).ready(function(){
	$("#addquestion").click(function(){
		$("#questions").append("<ol>Question" + question_number + "<input type='text'>");
		question_number += 1;});
		
})