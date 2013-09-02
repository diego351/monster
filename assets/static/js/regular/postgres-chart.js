function drawPostgresColumns() {
  $.ajax('/api/postgres/10', { dataType: 'json'}).done(function(response) {
    var postgresTable = [];
    postgresTable[0] = ['Index', 'Returned', 'Fetched', 'Inserts', 'Updates', 'Deletes'];
    for (var i = 0; i < response.l; i++) {
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
      viewWindow: {
        min: 0.0
      },
      hAxis: {
        gridlines: {
          color: '#f6f6f6'
        }
      },
      vAxis: {
        gridlines:{color: '#f6f6f6'}
      }
    };
    var chart = new google.visualization.ColumnChart(document.getElementById('postgres_columns'));
    chart.draw(postgresData, options);

    if (!postgres_refresh) {
      postgres_refresh = setInterval(drawPostgresColumns, 3000);
    }
  });        
}
