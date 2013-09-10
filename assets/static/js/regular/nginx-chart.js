probes.register({
  name: 'Nginx',
  init: function() {
	console.log("INIT");
    this.nginx_chart_obj = new google.visualization.ColumnChart(document.getElementById('nginx_columns'));
  },
  paint: function() {
    var nginx_chart_obj = this.nginx_chart_obj;
	console.log("Painting.");
    $.ajax('/api/nginx/30', { dataType: 'json'}).done(function(response) {
      var nginxTable = [];
      nginxTable[0] = ['Index', 'Requests', 'Transfer'];
      for (var i = 0; i < response.nginx_stats.length; i++) {
        nginxEntry = [
          i,
          response.nginx_stats[i]['requests'],
          response.nginx_stats[i]['transfer']
        ];
        nginxTable.push(nginxEntry);
      }
      var nginxData = new google.visualization.arrayToDataTable(nginxTable);
      var options = { 
        colors: ['#ff2d55', '#5ac8fa', '#4cd964', '#ffcc00'],
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
          gridlines:{color: '#f6f6f6'},
          viewWindow: {
            min: 0.0
          }
        }
      };
      nginx_chart_obj.draw(nginxData, options);
    });
  }
});
