

function printGraph(cluster){
  index = 0
  colors = ['#00FF00', '#79443B', '#531B00', '#E97451	','#CD5700','#7FFFD4', '#FBCEB1', '#E52B50', '#FFBF00','#884DA7','#FC6C85','#808000','#FF6600','#708090','#007FFF','#FFFDD0', '#DF73FF', '#CC9966', '#C2B280','#F400A1','#93C572','#293133','#A98307','#4B0082','#E30B5C']

  var data_list=[]
  $("#label_list").empty();
  for (key in data[cluster]['data']){
    let data_temp = []
    for (elem in data[cluster]['data'][key]){
      data_temp.push({x:data[cluster]['data'][key][elem][0],y:data[cluster]['data'][key][elem][1]})
      let attribute = data[cluster]['data'][key][elem].slice(2)
      $("#label_list").append('<li>');

      for(ke in attribute)
        $("#label_list").append(attribute[ke]);

      $("#label_list").append('</li>');

    }
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

function printGraphNoCluster(datas){
  let index = 0
  colors = ['#00FF00', '#79443B', '#531B00', '#E97451	','#CD5700','#7FFFD4', '#FBCEB1', '#E52B50', '#FFBF00','#884DA7','#FC6C85','#808000','#FF6600','#708090','#007FFF','#FFFDD0', '#DF73FF', '#CC9966', '#C2B280','#F400A1','#93C572','#293133','#A98307','#4B0082','#E30B5C']

  var data_list=[]
  let counter = 0,new_cutted = [4,5,6,8,9,11,12,13,15,20,22,23,24,25,27,28,30,31,32,33,34,35,36,37,39,43,44,45,46,47,48,51,52,53,54,55,57,58,59]
  $("#label_list").empty();

  for (key in datas['full']){
    let data_temp = []
    counter = 0
    for (elem in datas['full'][key]){
      data_temp.push({x:datas['full'][key][elem][0],y:datas['full'][key][elem][1]})
      let attribute = datas["full"][key][elem].slice(2)
      let id = "list_item"+counter+','+index
      $("#label_list").append('<li id="'+id+'">');
      for(ke in attribute){
        string = ""
        for(k in tokenizer[new_cutted[ke]]){
          if (tokenizer[new_cutted[ke]][k] == attribute[ke]){
            $("#label_list").append(k)
          }
        }
      }
      $("#label_list").append('</li>');

      counter++

    }
    var tmp={
      label:datas["label"][index],
      borderColor:"#000000",
      backgroundColor:colors[index],
      data:data_temp
    };
    data_list.push(tmp);
    index++
  }
  console.log("FINITO");
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

  $('#label_list').find("li").each(function() {
    $(this).on('mouseover', function() {
        let id = this.id.replace("list_item","")
        let split = id.split(",")
        let clu = split[1]
        let ind = split[0]
        t(clu,ind)
      }
    );
  })

}
var data = undefined, clusterChart = undefined,tokenizer = {}
$( document ).ready(function() {
    gettokenizer()
});

// $('#a').on('mouseover', function() { t(0); });
// $('#b').on('mouseover', function() { t(1); });
$('#c').on('click', function() { var cluster = $('#lname').val();printGraphNoCluster(data[cluster]) });


$('#d').on('click', function() {
  recluster()
 });
//
function t(cluster,idx) {
  var meta = clusterChart.getDatasetMeta(cluster),
    rect = clusterChart.canvas.getBoundingClientRect(),
    point = meta.data[idx].getCenterPoint(),
    evt = new MouseEvent('mousemove', {
      clientX: rect.left + point.x,
      clientY: rect.top + point.y
    }),
    node = clusterChart.canvas;
  node.dispatchEvent(evt);
}
