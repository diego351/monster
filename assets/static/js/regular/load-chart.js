function getLoadAndPaintShit() {
  $.ajax('/api/load/30', { dataType: 'json' }).done(function(response) {
    var loadTable = [];   
    loadTable[0] = ['Index', '1m', '5m', '15m'];
    for (var i = 0; i < response.load.length; i++) {
      loadEntry = [
        i,
        response.load[i]['1min'],
        response.load[i]['5min'],
        response.load[i]['15min']
      ];
      loadTable.push(loadEntry);
    }

    var options = {
      curveType: 'function',
      fontName: 'maven pro',
      vAxis: {
        maxValue: 3.0,
        minValue: 0.0,
        viewWindow: {
          min: 0.0
        },
        gridlines: {
          count: 16,
          color: '#f6f6f6'
        }
      },
      hAxis: {
        gridlines: {
          color: '#f6f6f6'
        },
        viewWindow: {
          min:0,
          max:29},
        },
        colors: ['#ff2d55', '#5ac8fa', '#4cd964']
    };
    var chartData = google.visualization.arrayToDataTable(loadTable);
    var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
    chart.draw(chartData, options);

    if (!refresh) {
      refresh = setInterval(getLoadAndPaintShit, 2000);
    }
    
  });
};
