var labels = [];
var scores = [];


var create_chart = function (question, labels, scores) {

    var ctx = document.getElementById("myChart");
    console.log(labels);
    console.log(scores);
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: question,
                data: scores,
                backgroundColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                
            }]
        },
    });
    var chart_id = document.getElementById("myChart");
    chart_id.setAttribute("id", "old_chart");
}