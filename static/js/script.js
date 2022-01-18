$(document).ready(function(){
	ranks.forEach(function(e){
		setInterval(here, 500, e);
		console.log(ranks);
		});
});

let ranks = ['#one', '#two', '#three', '#four', '#five', '#six', '#seven']
var animation = "fadeIn 1s forwards"
function here(element){
	const box = document.querySelector(element);
	const rect = box.getBoundingClientRect();
	
	const isInViewport = rect.top >= 0 &&
	rect.left >= 0 &&
	rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
	rect.right <= (window.innerWidth || document.documentElement.clientWidth);
	

	if (isInViewport == true){
	$(element).css(
	{"animation": animation});
}
};



// This will build the example chart on the home page
var ctx = document.getElementById("myChart");
var myChart = new Chart(ctx, {
	type:'bar',
	data: {
		labels: ["Apple", "Pear", "Orange"],
		datasets: [{
			label: "No. of Votes",
			data: [6, 5, 2,0],
			backgroundColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
			],
		}]
	},
});