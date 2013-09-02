function drawNginxColumns() {
  console.log('nginx drawing columns');
  $.ajax('/api/nginx/30', { dataType: 'json'}).done(function(response) {
    var nginxTable = [];
    nginxTable[0] = ['Index', 'Requests', 'Transfer'];
    for (var i = 0; i < response.nginx_stats.length; i++) {
      nginxEntry = [
        i,
        response.nginx_stats[i]['requests'],
        response.nginx_stats[i]['transfer']
      ];
      console.log("nginxEntry " + i + ": " + nginxEntry);
      nginxTable.push(nginxEntry);
    }
    var nginxData = new google.visualization.arrayToDataTable(nginxTable);
    var options = { 
      colors: ['#ff2d55', '#5ac8fa', '#4cd964', '#ffcc00'],
      viewWindow: {
        min: 0.0
      },
      fontName: 'maven pro',
      hAxis: {
        gridlines: {
          color: '#f6f6f6'
        }
      },
      vAxes: [
       {'title': 'requests'},
       {'title': 'transfer'}
      ],
      series: {
        0: {targetAxisIndex:0},
        1:{targetAxisIndex:1}
      },
      vAxis: {
        gridlines:{color: '#f6f6f6'}
      }
    };

    var chart = new google.visualization.ColumnChart(document.getElementById('nginx_columns'));
    chart.draw(nginxData, options);

    if (!nginx_refresh) {
      nginx_refresh = setInterval(drawNginxColumns, 5000);
    }
  });        
}
