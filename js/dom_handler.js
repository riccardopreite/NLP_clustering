
var start = 0, end = 10;
var start_attribute = 0, end_attribute = 10;
let colors = ['#CD5700', '#79443B', '#7FFFD4', '#884DA7	','#708090', '#531B00','#E97451	','#00FF00','#FBCEB1','#E52B50','#FFBF00','#FC6C85','#808000','#FF6600','#007FFF','#FFFDD0','#DF73FF','#CC9966','#C2B280','#F400A1','#93C572','#293133','#A98307','#4B0082','#E30B5C']

function drawJsonPercentage(myObj,index){
  //ricevo l'oggetto con attribute_0 già scelto

  let text = "<table border='1' style='table-layout:fixed;width: 485px;'><col width='20px' /> <col width='5px' />"
  counter = 0
  for (let x in myObj) {
    tex = myObj[x].toString().slice(0, 6) + "%"
    key = x.replace("{","")
    key = key.replace("}","")
    if(counter >= start_attribute && counter<=end_attribute)
      text += "<tr><td style='overflow: hidden;'><font color='"+ colors[index]+"'>" + key + "</font></td>"+"<td><font color='"+ colors[index]+"'>" + tex + "</font></td>"+"</tr>";
    counter++
  }
  text += "</table>"
  document.getElementById("demo").innerHTML = text;
}

function changeAttributepercentage(element,index){
  var lat_cluster = $('#latlon').val();
  let lat_lab = 'lat_lon_'+lat_cluster;
  var cat_cluster = "categories_" + $('#lcat').val();
  start_attribute = 0, end_attribute = 10;

  drawJsonPercentage(statistics[lat_lab][cat_cluster][element],index)
}



function plotCluster(datas,categories){
  let index = 0
  let cat_lab = "categories_"+categories
  var data_list=[]
  let counter = 0;
  start = 0, end = 10;
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
  if(clusterChart) clusterChart.destroy();

  clusterChart = new Chart($('#myChart'), {
    type: 'scatter',
    data: {
      datasets: data_list
    },
    options: {
      maintainAspectRatio: false,
      pan: {
        enabled: true,
        mode: 'xy',
      },
      zoom: {
        enabled: true,
        mode: 'xy',
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

function nextAttributePerc(){
  let select = document.getElementById("attribute")
  var lat_cluster = $('#latlon').val();
  let lat_lab = 'lat_lon_'+lat_cluster;
  var cat_cluster = "categories_" + $('#lcat').val();
  let attr = select.options[select.selectedIndex].value
  let index = select.selectedIndex
  let len = Object.keys(statistics[lat_lab][cat_cluster][attr]).length;
  if(end_attribute + 10 < len){
    start_attribute = start_attribute + 10
    end_attribute = end_attribute + 10
  }
  else{
    end_attribute = len - 1
    start_attribute = end_attribute - 10
  }

  drawJsonPercentage(statistics[lat_lab][cat_cluster][attr],index)
}

function prevAttributePerc(){
  let select = document.getElementById("attribute")
  var lat_cluster = $('#latlon').val();
  let lat_lab = 'lat_lon_'+lat_cluster;
  var cat_cluster = "categories_" + $('#lcat').val();
  let attr = select.options[select.selectedIndex].value
  let index = select.selectedIndex

  if(start_attribute - 10 < 0){
    start_attribute = 0
    end_attribute = 10
  }
  else {
    start_attribute = start_attribute - 10
    end_attribute = end_attribute - 10
  }

  drawJsonPercentage(statistics[lat_lab][cat_cluster][attr],index)
}


var data = undefined, clusterChart = undefined,tokenizer = {}
$( document ).ready(function() {
    getFullData()
});

$('#redraw').on('click', function() {
  var lat_cluster = $('#latlon').val();
  let lat_lab = 'lat_lon_'+lat_cluster;
  var cat_cluster = $('#lcat').val();
  let select = document.getElementById("attribute")
  var cat_cluster_lab = "categories_" + $('#lcat').val();
  let attr = select.options[select.selectedIndex].value
  let index = select.selectedIndex
  start = 0;
  end = 10;
  start_attribute = 0, end_attribute = 10;
  plotCluster(data[lat_lab],cat_cluster)
  drawJsonPercentage(statistics[lat_lab][cat_cluster_lab][attr],index)
});
$('#getcluster').on('click', function() {
  getFullData()
});


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
