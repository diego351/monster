probes.register({
  name: 'Nginx',
  init: function() {
    this.pg_chart_obj = new google.visualization.ColumnChart(document.getElementById('postgres_columns'));
  },
  paint: function() {
    var pg_chart_obj = this.pg_chart_obj;
    $.ajax('/api/postgres/10', { dataType: 'json'}).done(function(response) {
      var postgresTable = [];
      postgresTable[0] = ['Index', 'Returned', 'Fetched', 'Inserts', 'Updates', 'Deletes'];
      for (var i = 0; i < response.postgres_stats.length; i++) {
        postgresEntry = [
          i,
          response.postgres_stats[i]['returned'],
          response.postgres_stats[i]['fetched'],
          response.postgres_stats[i]['inserted'],
          response.postgres_stats[i]['updated'],
          response.postgres_stats[i]['deleted']
        ];
        postgresTable.push(postgresEntry);
      }
      var postgresData = new google.visualization.arrayToDataTable(postgresTable);
      var options = { 
        colors: ['#ff2d55', '#5ac8fa', '#4cd964', '#ffcc00'],
        fontName: 'maven pro',
        hAxis: {
          gridlines: {
            color: '#f6f6f6'
          }
        },
        vAxis: {
          gridlines:{color: '#f6f6f6'},
          viewWindow: {
            min: 0.0
          },
        },
        vAxes: [
          {'title': '`returned` count'},
          {'title': 'rows'}
        ],
        series: {
          0: {targetAxisIndex:0},
          1: {targetAxisIndex:1},
          2: {targetAxisIndex:1},
          3: {targetAxisIndex:1},
          4: {targetAxisIndex:1}
        },
      };
      
      pg_chart_obj.draw(postgresData, options);
    });
  } 
});