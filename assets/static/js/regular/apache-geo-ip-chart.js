function drawApacheMap() {
  $.ajax('/api/apache_geocache', { dataType: 'json' }).done(function(response) {
    var ip_table = [];   
    /* an empty geochart complains about needing only two columns */
    var ip_list = response.apache_ips.ips;
    console.log(ip_list);
    if (ip_list.length == 0) {
        ip_table[0] = ['Latitude', 'Longitude'];
    } else {
        ip_table[0] = ['Latitude', 'Longitude', 'Requests'];
        for (var i = 0; i < ip_list.length; i++) {
          var ip_entry = [
            ip_list[i].latitude,
            ip_list[i].longitude,
            ip_list[i].number
          ];
          ip_table.push(ip_entry);
        }
        console.log(ip_table);
    }

    var options = {
      legend: 'top',
      fontName: 'maven pro',
      displayMode: 'markers',
      colors: ['#ff2d55', '#5ac8fa', '#4cd964']
    };
    var chart_data = google.visualization.arrayToDataTable(ip_table);

    if (document.getElementById('apache-geo-ip-div-1').style.display == "") {
        var paint_on = 'apache-geo-ip-div-2';
        var old_chart = 'apache-geo-ip-div-1';
    } else {
        var paint_on = 'apache-geo-ip-div-1';
        var old_chart = 'apache-geo-ip-div-2';
    }
    console.log("Painting on " + paint_on);

    var chart = new google.visualization.GeoChart(document.getElementById(paint_on));
    chart.draw(chart_data, options);
    /* I didn't check if charts exposed some onFinishedPainting hook,
     * so I'm doing the stupid thing - giving it 1.5 seconds to paint.
     */
    setTimeout(function() {
        document.getElementById(old_chart).style.display = "none";
        document.getElementById(paint_on).style.display = "";
    }, 1500);

    if (!apache_map_refresh) {
      apache_map_refresh = setInterval(drawApacheMap, 2000);
    }
    
  });
};
