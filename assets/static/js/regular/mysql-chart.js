probes.register({
  name: 'MySQL',
  init: function() {
    this.mysql_chart_obj = new google.visualization.ColumnChart(document.getElementById('mysql_columns'));
  },
  paint: function() {
    var mysql_chart_obj = this.mysql_chart_obj;
    $.ajax('/api/mysql', { dataType: 'json'}).done(function(response) {
      var mysqlTable = [];
      mysqlTable[0] = ['Index', 'Selects', 'Inserts', 'Updates', 'Deletes', 'Connections'];
      for (var i = 0; i < response.mysql_stats.length; i++) {
        mysqlEntry = [
          i,
          response.mysql_stats[i]['select'],
          response.mysql_stats[i]['insert'],
          response.mysql_stats[i]['update'],
          response.mysql_stats[i]['delete'],
          response.mysql_stats[i]['connections']
        ];
        mysqlTable.push(mysqlEntry);
      }
      var mysqlData = new google.visualization.arrayToDataTable(mysqlTable);
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
          gridlines:{color: '#f6f6f6'}}
      };
      
      mysql_chart_obj.draw(mysqlData, options);

    });
  }
});

function drawMysqlColumns() {
          
}
