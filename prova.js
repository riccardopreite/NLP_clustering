

function printGraph(cluster){
  index = 0
  colors = ['#00FF00', '#79443B', '#531B00', '#E97451	','#CD5700','#7FFFD4', '#FBCEB1', '#E52B50', '#FFBF00','#884DA7','#FC6C85','#808000','#FF6600','#708090','#007FFF','#FFFDD0', '#DF73FF', '#CC9966', '#C2B280','#F400A1','#93C572','#293133','#A98307','#4B0082','#E30B5C']

  var data_list=[]
  for (key in data[cluster]['data']){
    let data_temp = []
    for (elem in data[cluster]['data'][key]){
      data_temp.push({x:data[cluster]['data'][key][elem][0],y:data[cluster]['data'][key][elem][1]})
    }
    console.log(data_temp);
    var tmp={
      label:data[cluster]["label"][index],
      borderColor:"#000000",
      backgroundColor:colors[index],
      data:data_temp
    };
    data_list.push(tmp);
    index++
  }
  if(clusterChart) clusterChart.destroy();

  clusterChart = new Chart($('#myChart'), {
    type: 'scatter',
    data: {
      datasets: data_list
    },
    options: {

      pan: {
        enabled: true,
        mode: 'xy',
      },
      zoom: {
        enabled: true,
        mode: 'xy', // or 'x' for "drag" version
      },
    }
  })
}

// function printGraph(cluster){
//   index = 0
//   colors = ['#00FF00', '#79443B', '#531B00', '#E97451	','#CD5700','#7FFFD4', '#FBCEB1', '#E52B50', '#FFBF00','#884DA7','#FC6C85','#808000','#FF6600','#708090','#007FFF','#FFFDD0', '#DF73FF', '#CC9966', '#C2B280','#F400A1','#93C572','#293133','#A98307','#4B0082','#E30B5C']
//
//   var data_list=[]
//   for (key in data[cluster]['data']){
//     let data_temp = []
//     for (elem in data[cluster]['data']){
//       data_temp.push({x:data[cluster]['data'][elem][0],y:data[cluster]['data'][elem][1]})
//     }
//     console.log(data_temp);
//     var tmp={
//       label:data[cluster]["label"][index],
//       borderColor:"#000000",
//       backgroundColor:colors[index],
//       data:data_temp
//     };
//     data_list.push(tmp);
//     index++
//   }
//   if(clusterChart) clusterChart.destroy();
//
//   clusterChart = new Chart($('#myChart'), {
//     type: 'scatter',
//     data: {
//       datasets: data_list
//     },
//     options: {
//
//       pan: {
//         enabled: true,
//         mode: 'xy',
//       },
//       zoom: {
//         enabled: true,
//         mode: 'xy', // or 'x' for "drag" version
//       },
//     }
//   })
// }
var data = undefined, clusterChart = undefined
$.ajax({
  url: "http://192.168.0.80:3000/get",
  success: function(json_from_server){
    data = json_from_server
    console.log("RECEIVED");
    console.log(data);
    printGraph(0)
  }
});
// $.ajax({
//   url: "http://192.168.0.80:3000/getsingle",
//   success: function(json_from_server){
//     data = json_from_server
//     console.log("RECEIVED");
//     console.log(data);
//     printGraphTemp()
//   }
// });

// $('#a').on('mouseover', function() { t(0); });
// $('#b').on('mouseover', function() { t(1); });
$('#c').on('click', function() { var cluster = $('#lname').val();printGraph(cluster) });


$('#d').on('click', function() {

  $.ajax({
    url: "http://192.168.0.80:3000/call",
    success: function(json_from_server){
      data = json_from_server
      printGraph(0)
    }
  });
 });
//
// function t(idx) {
//   var meta = c.getDatasetMeta(0),
//     rect = c.canvas.getBoundingClientRect(),
//     point = meta.data[idx].getCenterPoint(),
//     evt = new MouseEvent('mousemove', {
//       clientX: rect.left + point.x,
//       clientY: rect.top + point.y
//     }),
//     node = c.canvas;
//   node.dispatchEvent(evt);
// }
