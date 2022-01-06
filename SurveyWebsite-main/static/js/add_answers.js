$num = 1;

$(document).ready(function(){
	$("button").click(function(){
		var $question = $(this).attr("class");
		console.log($question);
		$cl = "#" + $question;
		$($cl).append("<ol><input type='text' name='" + $question + $num.toString() + "'></ol>");
		$num += 1;});
	$("#submitbutton").click(function(){
		$data = $("form").serialize()
		$.ajax({
			type: 'POST',
			data: $("form").serialize(),
			success: function(){
				console.log($data);
			}

		});
		});
});
