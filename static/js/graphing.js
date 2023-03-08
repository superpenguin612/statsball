function drawBoxPlot(array,name,title,color,axis,flipped) {
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'x');
  data.addColumn('number', 'midpoint');
  data.addColumn({id:'max', type:'number', role:'interval'});
  data.addColumn({id:'min', type:'number', role:'interval'});
  data.addColumn({id:'firstQuartile', type:'number', role:'interval'});
  data.addColumn({id:'median', type:'number', role:'interval'});
  data.addColumn({id:'thirdQuartile', type:'number', role:'interval'});

  data.addRows(getBoxPlotValues(array));
  function getBoxPlotValues(array) {
    res = []
    for (var i = 0; i < array.length; i++) {
      var arr = array[i].slice(1).sort(function (a, b) {return a - b;});

      res.push([
        array[i][0],
        arr[Math.floor(arr.length/2)],
        arr[arr.length - 1],
        arr[0],
        arr[Math.floor(arr.length/4)],
        arr[Math.floor(arr.length/2)],
        arr[Math.floor(3*arr.length/4)]
      ])
    }
    return res;
  }

  var options = {
    title:title,
    orientation: (flipped ? 'vertical' : 'horizontal'),
    legend: {position: 'none'},
    hAxis: {
      gridlines: {color: '#fff'}
    },
    vAxis: {
      title: yscale
    },
    lineWidth: 0,
    series: [{'color':color}],//#D3362D
    intervals: {
      barWidth: 1,
      boxWidth: 1,
      lineWidth: 2,
      style: 'boxes'
    },
    interval: {
      max: {
        style: 'bars',
        fillOpacity: 1,
        color: '#777'
      },
      min: {
        style: 'bars',
        fillOpacity: 1,
        color: '#777'
      }
    }
  };
  var chart = new google.visualization.LineChart(document.getElementById(name));
  chart.draw(data, options);
}






function drawStackedBar(array,name,title,flipped) {
  for (let x =1; x <= array.length; x++) {
    var total = 0
    for (let y =1; y <= array[x].length-1; y++) {total = total + array[x][y]}
    for (let y =1; y <= array[x].length-1; y++) {array[x][y] = array[x][y]/total}
  }
  // var data = google.visualization.arrayToDataTable([
  //   ['Genre', 'Fantasy & Sci Fi', 'Romance', 'Mystery/Crime', 'General', 'Western', 'Literature', { role: 'annotation' } ],
  //   ['2010', 10, 24, 20, 32, 18, 5, ''],
  //   ['2020', 16, 22, 23, 30, 16, 9, ''],
  //   ['2030', 28, 19, 29, 30, 12, 13, '']
  // ]);
  var data = google.visualization.arrayToDataTable(array);
  var options = {
    title:title,
    orientation: (flipped ? 'vertical' : 'horizontal'),
    legend: { position: 'top', maxLines: 3 },
    bar: { groupWidth: '75%' },
    isStacked: true,
  };
  var chart = new google.visualization.ColumnChart(document.getElementById(name));
  chart.draw(view, options);
}




function drawScatterPlot(array,name,title,xscale,yscale,showrline) {
  var data = google.visualization.arrayToDataTable(array);
  var options = {
    title:title,
    legend: { position: 'top', maxLines: 3 },
    hAxis: {
      title: xscale
    },
    vAxis: {
      title: yscale
    },
    trendlines: showrline ? {
      0: {
        type: 'linear',
        color: 'green',
        lineWidth: 3,
        opacity: 0.3,
        showR2: true,
        visibleInLegend: true
      }
    } : {}
  };
  var chart = new google.visualization.ScatterChart(document.getElementById(name));
  chart.draw(data, options);
}



