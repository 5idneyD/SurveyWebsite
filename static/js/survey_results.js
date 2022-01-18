var labels = [];
var scores = [];
var create_chart = function (labels, scores) {

    var ctx = document.getElementById("myChart");
    console.log(labels);
    console.log(scores);
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: scores,
                backgroundColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderColor: "rgba(100, 100, 200, 0.9)"
            }]
        },
    });
    var chart_id = document.getElementById("myChart");
    chart_id.setAttribute("id", "old_chart");
}