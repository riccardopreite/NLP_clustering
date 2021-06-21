
function gettokenizer(){
  $.ajax({
    url: "http://192.168.0.80:3000/gettokenizer",
    success: function(token){
      tokenizer = token
      console.log("RECEIVED token dict");
      console.log(tokenizer);
      getsingle()
    }
  });
}
function getsingle(){
  $.ajax({
    url: "http://192.168.0.80:3000/getsingle",
    success: function(json_from_server){
      data = json_from_server
      console.log("RECEIVED");
      console.log(data);
      printGraphNoCluster(json_from_server)
    }
  });
}

function oldgetFullData(){
  $.ajax({
    url: "http://192.168.0.80:3000/get",
    success: function(json_from_server){
      data = json_from_server
      console.log("RECEIVED");
      console.log(data);
      // printGraph(0)
      printGraphNoCluster(data[0])
    }
  });
}

function getFullData(){
  $.ajax({
    // url: "http://192.168.0.137:3000/getlat_lon",
    url: "http://192.168.0.80:3000/getlat_lon",

    success: function(json_from_server){
      data = json_from_server
      console.log("RECEIVED");
      console.log(data);
      plotCluster(data["lat_lon_0"],'0')
    }
  });
}

function recluster(){
  $.ajax({
    url: "http://192.168.0.80:3000/call",
    success: function(json_from_server){
      data = json_from_server
      printGraph(0)
    }
  });
}
