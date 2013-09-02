function drawApacheColumns() {
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
        gridlines:{color: '#f6f6f6'}}
    };
    var chart = new google.visualization.ColumnChart(document.getElementById('apache_columns'));
    chart.draw(apacheData, options);

    if (!apache_refresh) {
      apache_refresh = setInterval(drawApacheColumns, 3000);
    }
  });        
}
