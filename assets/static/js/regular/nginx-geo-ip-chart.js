probes.register({
  init: function() {
    this.map_1_obj = new google.visualization.GeoChart(document.getElementById('nginx-geo-ip-div-1'));
    this.map_2_obj = new google.visualization.GeoChart(document.getElementById('nginx-geo-ip-div-2'));
  },
  paint: function() {
    var map_1_obj = this.map_1_obj;
    var map_2_obj = this.map_2_obj;
    $.ajax('/api/nginx_geocache', { dataType: 'json' }).done(function(response) {
      var ip_table = [];   
      /* an empty geochart complains about needing only two columns */
      var ip_list = response.nginx_ips.ips;
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

      if (document.getElementById('nginx-geo-ip-div-1').style.display == "") {
          var paint_on = 'nginx-geo-ip-div-2';
          var old_chart = 'nginx-geo-ip-div-1';
      } else {
          var paint_on = 'nginx-geo-ip-div-1';
          var old_chart = 'nginx-geo-ip-div-2';
      }
     
      if (document.getElementById('nginx-geo-ip-div-1').style.display == "") {
        map_2_obj.draw(chart_data, options);
        setTimeout(function() {
            document.getElementById('nginx-geo-ip-div-1').style.display = "none";
            document.getElementById('nginx-geo-ip-div-2').style.display = "";
        }, 1200);
      } else {
        map_1_obj.draw(chart_data, options);
        setTimeout(function() {
            document.getElementById('nginx-geo-ip-div-2').style.display = "none";
            document.getElementById('nginx-geo-ip-div-1').style.display = "";
        }, 1200);
      }
    });
  }
});