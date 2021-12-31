$(document).ready(function(){
	ranks.forEach(function(e){
		setInterval(here, 1000, e);
		console.log(ranks);
		});
});

let ranks = ['#one', '#two', '#three', '#four', '#five', '#six', '#seven']

function here(element){
	const box = document.querySelector(element);
	const rect = box.getBoundingClientRect();
	
	const isInViewport = rect.top >= 0 &&
	rect.left >= 0 &&
	rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
	rect.right <= (window.innerWidth || document.documentElement.clientWidth);
	

	if (isInViewport == true){
	$(element).css(
	{"opacity": "1"});
	var ind = ranks.indexOf(element);
	ranks = ranks.splice(ind, 1);
}
};