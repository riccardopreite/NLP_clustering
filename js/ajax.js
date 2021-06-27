var data = {}, statistics = {};
function getFullData(){
  $.ajax({
    url: "http://localhost:3000/getlat_lon",

    success: function(json_from_server){
      data = json_from_server["cluster"]
      statistics = json_from_server["statistics"]
      console.log("RECEIVED");
      console.log(data);
      plotCluster(data["lat_lon_0"],'0')
      drawJsonPercentage(statistics["lat_lon_0"]["categories_0"]["attribute_0"],0)
    }
  });
}

function get_statistics(){
  $.ajax({
    url: "http://localhost:3000/get_stat",

    success: function(statistics_from_server){
      statistics = statistics_from_server
      console.log("RECEIVED stat");
      console.log(statistics);
      drawJsonPercentage(statistics["lat_lon_0"]["categories_0"]["attribute_0"],0)
    }
  });
}

function recluster(){
  $.ajax({
    url: "http://localhost:3000/call",
    success: function(json_from_server){
      data = json_from_server
      plotCluster(data["lat_lon_0"],'0')
    }
  });
}
