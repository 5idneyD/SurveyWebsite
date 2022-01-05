var question_number = 1;
$(document).ready(function(){
	$("#addquestion").click(function(){
	    $n = question_number.toString();
		$("#questions").append("<ol class='new_questions'>Question" + question_number + "<input type='text' class='" + $n + "'>");
		question_number += 1;});
});