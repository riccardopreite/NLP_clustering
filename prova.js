
var start = 0, end = 10;
function plotCluster(datas,categories){
  let index = 0
  let cat_lab = "categories_"+categories
  // colors = ['#00FF00', '#79443B', '#531B00', '#E97451	','#CD5700','#7FFFD4', '#FBCEB1', '#E52B50', '#FFBF00','#884DA7','#FC6C85','#808000','#FF6600','#708090','#007FFF','#FFFDD0', '#DF73FF', '#CC9966', '#C2B280','#F400A1','#93C572','#293133','#A98307','#4B0082','#E30B5C']
  let colors = ['#00FF00', '#79443B', '#7FFFD4', '#884DA7	','#708090']
  var data_list=[]
  let counter = 0;
  $("#label_list").empty();

  for (attr in datas[cat_lab]){
    let data_temp = []

    for (vect in datas[cat_lab][attr]){
        counter = 0
        for(elem in datas[cat_lab][attr][vect]){
          data_temp.push({x:datas[cat_lab][attr][vect][elem][0],y:datas[cat_lab][attr][vect][elem][1]})
          let attribute = datas[cat_lab][attr][vect][elem].slice(2)
          let id = "list_item"+counter+','+index
          $("#label_list").append('<li id="'+id+'"></li>');
          document.getElementById(id).innerHTML = '<div style="width:1800px;height:auto;word-wrap: break-word; "><p>'+attribute+'</p></div>'
          counter++
        }

    }
    var tmp={
      label:attr,
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
  /*aggiungere freccette avanti e indietro*/
  showRightlabel(start,end)
}

function showRightlabel(start,end){
  let ul = document.getElementById("label_list")
  if (!ul.childNodes || ul.childNodes.length == 0) return;

  for (var itemi=0;itemi<ul.childNodes.length;itemi++) {
    var item = ul.childNodes[itemi];
    if (item.nodeName == "LI") {
      if(itemi >= start && itemi<=end)
        item.style.display = ""
      else
        item.style.display = "none"
    }
  }

}

function nextAttribute(){
  let ul = document.getElementById("label_list")
  if (!ul.childNodes || ul.childNodes.length == 0) return;
  let len = ul.childNodes.length
  if(end + 10 < len){
    start = start + 10
    end = end + 10
  }
  else{
    end = ul.childNodes.length - 1
    start = end - 10
  }
  showRightlabel(start,end)
}

function prevAttribute(){
  if(start - 10 < 0){
    start = 0
    end = 10
  }
  else {
    start = start - 10
    end = end - 10
  }
  showRightlabel(start,end)
}


var data = undefined, clusterChart = undefined,tokenizer = {}
$( document ).ready(function() {
    // gettokenizer()
    // getFullData()
    // getsingle()
});

$('#redraw').on('click', function() {
  var lat_cluster = $('#latlon').val();
  let lat_lab = 'lat_lon_'+lat_cluster;
  if(lat_cluster == 8) lat_lab = 'lat_lon_0';
  var cat_cluster = $('#lcat').val();

  plotCluster(data[lat_lab],cat_cluster)
});
$('#getcluster').on('click', function() { getFullData() });


$('#recluster').on('click', function() {
  recluster()
 });


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
