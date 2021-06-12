/*

let c = new Chart($('#myChart'), {
  type: 'bar',
  data: {
    labels: json_from_server['0']['label']
    datasets: [{
      data: json_from_server['0']['data'],
      backgroundColor: ['red', 'blue', 'green', 'orange','pink','purple','yellow','brown','cyan']
    }]
  },
  options: {
    maintainAspectRatio: false
  }
});

json_from_server = {

  '0':{
    'label':[1,2,3,4,5,6,7,8],
    'data':[
      [x1,y1],
      .
      .
      .
      [xn,yn]
    ],
    'full':[
      [x1,y1,attr1,..,attrn,cat1,..,catn],
      .
      .
      .
      [xn,yn,attr1,..,attrn,cat1,..,catn]
    ]
  },
  .
  .
  '8':{
    'label':[1,2,4,3,5,6,8,7....3,2,1,4],
    'data':[
      [x1,y1],
      .
      .
      .
      [xn,yn]
    ],
    'full':[
      [x1,y1,attr1,..,attrn,cat1,..,catn],
      .
      .
      .
      [xn,yn,attr1,..,attrn,cat1,..,catn]
    ]
  },




}



*/


data = undefined
$.ajax({
  url: "http://localhost:3000/get",
  success: function(json_from_server){
    data = json_from_server
    console.log("FIe");
    index = 0
    // while (index < 9){
    //   data = data.replace(index.toString()+': ','"'+index.toString()+'": ')
    //   index++
    // }
    // data = data.replaceAll("'",'"')
    console.log(json_from_server);

    let c = new Chart($('#myChart'), {
      type: 'bar',
      data: {
        labels: json_from_server['0']['label'],
        datasets: [{
          data: json_from_server['0']['data'],
          backgroundColor: ['red', 'blue', 'green', 'orange','pink','purple','yellow','brown','cyan']
        }]
      },
      options: {
        maintainAspectRatio: false
      }
    });

  }
});


// let c = new Chart($('#myChart'), {
//   type: 'bar',
//   data: {
//     labels: ['a', 'b', 'c', 'd'],
//     datasets: [{
//       data: [1, 2, 4, 8],
//       backgroundColor: ['red', 'blue', 'green', 'orange']
//     }]
//   },
//   options: {
//     maintainAspectRatio: false
//   }
// });
// $('#a').on('mouseover', function() { t(0); });
// $('#b').on('mouseover', function() { t(1); });
// $('#c').on('mouseover', function() { t(2); });
$('#d').on('mouseover', function() {

  $.ajax({
    url: "http://localhost:3000/call",
    success: function(json_from_server){
      data = json_from_server
      console.log("FIe");
      index = 0
      // while (index < 9){
      //   data = data.replace(index.toString()+': ','"'+index.toString()+'": ')
      //   index++
      // }
      // data = data.replaceAll("'",'"')
      console.log(data);
      json_from_server = JSON.parse(data);
      console.log(json_from_server);

      let c = new Chart($('#myChart'), {
        type: 'bar',
        data: {
          labels: json_from_server['0']['label'],
          datasets: [{
            data: json_from_server['0']['data'],
            backgroundColor: ['red', 'blue', 'green', 'orange','pink','purple','yellow','brown','cyan']
          }]
        },
        options: {
          maintainAspectRatio: false
        }
      });

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
/*
var ctx = document.getElementById('myChart').getContext('2d');

$.ajax({
  url: "localhost:3000/get",
  success: function(json_from_server){
    console.log(json_from_server);
    console.log(json_from_server[0]['label']);
    console.log(json_from_server[0]['data']);
    console.log(json_from_server[0]['full']);

    let c = new Chart($('#myChart'), {
      type: 'bar',
      data: {
        labels: json_from_server['0']['label']
        datasets: [{
          data: json_from_server['0']['data'],
          backgroundColor: ['red', 'blue', 'green', 'orange','pink','purple','yellow','brown','cyan']
        }]
      },
      options: {
        maintainAspectRatio: false
      }
    });



  }
});
var chart = new Chart(ctx, {
type: 'scatter',
data: {
  labels: ['Jan 01', 'Jan 02', 'Jan 03'],
  datasets: [{
     label: 'Apples Sold',
     data: [3, 5, 1],
     borderColor: 'rgba(255, 99, 132, 0.8)',
     fill: false
  }, {
     label: 'Oranges Sold',
     data: [0, 10, 2],
     borderColor: 'rgba(255, 206, 86, 0.8)',
     fill: false
  }, {
     label: 'Gallons of Milk Sold',
     data: [5, 7, 4],
     borderColor: 'rgba(54, 162, 235, 0.8)',
     fill: false
  }]
},
options: {
  tooltips: {
     mode: 'index',
     intersect: false
  },
  hover: {
     mode: 'index',
     intersect: false
  }
}
});
*/
