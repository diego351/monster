function drawHeavyProcessTables() {
  /* CPU table first. */ 
  $.ajax('/api/heavy_process_stat', { dataType: 'json' }).done(function(response) {
    var cpu_table = [];
    cpu_table[0] = ['Process', 'CPU usage', 'Tendency'];
    for (var i = 0; i < response.cpuList.length; i++) {
        var cpu_entry = [
            response.cpuList[i].process,
            response.cpuList[i].value,
            response.cpuList[i].tendency
        ];  
        cpu_table.push(cpu_entry);
    }

    /* mem */
    var mem_table = [];
    mem_table[0] = ['Process', 'Memory usage', 'Tendency'];
    for (var i = 0; i < response.memList.length; i++) {
        var mem_entry = [
            response.memList[i].process,
            response.memList[i].value,
            response.memList[i].tendency
        ];
        mem_table.push(mem_entry);
    };

    var options = {
      curveType: 'function',
      legend: 'top',
      fontName: 'maven pro',
      vAxis: {
        maxValue: 3.0,
        minValue: 0.0,
        viewWindow: {
          min: 0.0
        },
        gridlines: {
          count: 16,
          color: '#f6f6f6'
        }
      },
      hAxis: {
        gridlines: {
          color: '#f6f6f6'
        },
        viewWindow: {
          min:0,
          max:29},
        },
        colors: ['#ff2d55', '#5ac8fa', '#4cd964']
    };
    var cpu_chart_data = google.visualization.arrayToDataTable(cpu_table);
    var cpu_chart = new google.visualization.Table(document.getElementById('hps-cpu-chart-div'));
    cpu_chart.draw(cpu_chart_data, options);

    var mem_chart_data = google.visualization.arrayToDataTable(mem_table);
    var mem_chart = new google.visualization.Table(document.getElementById('hps-mem-chart-div'));
    mem_chart.draw(mem_chart_data, options);

    if (!hps_refresh) {
      hps_refresh = setInterval(drawHeavyProcessTables, 2000);
    }
    
  });
};
