function drawNginxMap() {
  $.ajax('/api/nginx_geocache', { dataType: 'json' }).done(function(response) {
    var ip_table = [];   
    ip_table[0] = ['Latitude', 'Longitude', 'Requests'];
    var ip_list = response.nginx_ips.ips;
    for (var i = 0; i < ip_list.length; i++) {
      var ip_entry = [
        ip_list[i].latitude,
        ip_list[i].longitude,
        ip_list[i].number
      ];
      ip_table.push(ip_entry);
    }
    console.log(ip_table);

    var options = {
      legend: 'top',
      fontName: 'maven pro',
      displayMode: 'markers',
//      colors: ['#ff2d55', '#5ac8fa', '#4cd964']
    };
    var chart_data = google.visualization.arrayToDataTable(ip_table);
    var chart = new google.visualization.GeoChart(document.getElementById('nginx-geo-ip-div'));
    chart.draw(chart_data, options);

    if (!nginx_map_refresh) {
      nginx_map_refresh = setInterval(drawNginxMap, 2000);
    }
    
  });
};
