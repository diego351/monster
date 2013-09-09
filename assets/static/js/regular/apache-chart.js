probes.register({
  name: 'Apache2',
  init: function() {
    this.apache_chart_obj = new google.visualization.ColumnChart(document.getElementById('apache_columns'));
  },
  paint: function() {
    var apache_chart_obj = this.apache_chart_obj;
    $.ajax('/api/apache', { dataType: 'json'}).done(function(response) {
      var apacheTable = [];
      apacheTable[0] = ['Index', 'Requests', 'Transfer'];
      for (var i = 0; i < response.apache_activity.length; i++) {
        apacheEntry = [
          i,
          response.apache_activity[i]['requests'],
          response.apache_activity[i]['transfer']
        ];
        apacheTable.push(apacheEntry);
      }
      var apacheData = new google.visualization.arrayToDataTable(apacheTable);
      var options = { 
        colors: ['#ff2d55', '#5ac8fa', '#4cd964', '#ffcc00'],
        fontName: 'maven pro',
        hAxis: {
          gridlines: {
            color: '#f6f6f6'
          }
        },
        viewWindow: {
          min: 0.0
        },
        vAxis: {
          gridlines:{color: '#f6f6f6'},
          viewWindow: {
            min: 0.0
          }
        },
        vAxes: [
          {'title': 'transfer'},
          {'title': 'requests'}
        ],
        series: {
          0: {targetAxisIndex:1},
          1: {targetAxisIndex:0}
        }
      };

      apache_chart_obj.draw(apacheData, options);
    });
  }
});