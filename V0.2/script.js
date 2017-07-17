
  function onWeioReady() {
    console.log("DOM is loaded, websocket is opened");
    printmychart();
    weioCallbacks["P"] = RecievedHC;
  }

  /*------------------------------------------------------*/
                     /*--- DOUGHNUT ---*/
  /*------------------------------------------------------*/
  
  var myDoughnutChart = null;
  
    function printmychart(){
      Chart.defaults.global.legend.display = false;
      Chart.defaults.global.tooltips.enabled = false;
      Chart.defaults.global.animation.duration = 200;
      Chart.defaults.global.elements.arc.borderWidth = 0;
      var ctx = document.getElementById("myChart");
      myDoughnutChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ["Presence","No"],
          datasets: [
          {
            data: [0, 431],
            backgroundColor: ["#03A9F4","#333333"]
          }]
        },
        options: {
          cutoutPercentage:0,
        }
      });
    }
    
/*------------------------------------------------------*/
                  /*--- RECIEVED HC ---*/
/*------------------------------------------------------*/

  myarray = [];

  function RecievedHC(result) {
    var x = parseInt(result);
    var palier = "";
    var color = "#F44336";
    
    switch(true){
        case (x < 20):
            palier = "En contact";
            color = "#E91E63";
            break;
        case (x > 19 && x < 40):
            palier = "Très proche";
            color = "#9C27B0";
            break;
        case (x > 39 && x < 60):
            palier = "Proche";
            color = "#673AB7";
            break;
        case (x > 59 && x < 80):
            palier = "Normale";
            color = "#3F51B5";
            break;
        case (x > 79 && x < 100):
            palier = "Éloigné";
            color = "#2196F3";
            break;
        case (x > 99 && x < 150):
            palier = "Très éloigné";
            color = "#00BCD4";
            break;
        case (x > 149):
            palier = "Distant";
            color = "#009688";
            break;
    }
    
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1;
    var year = today.getFullYear();
    var hour = today.getHours();
    var min = today.getMinutes();
    var sec = today.getSeconds();
    var milli = today.getMilliseconds();
    
    if(dd<10) { dd='0'+dd } 
    if(mm<10) { mm='0'+mm }
    if(hour<10) { hour='0'+hour } 
    if(min<10) { min='0'+min }
    if(sec<10){ sec='0'+sec }

    var now = dd + "/" + mm + "/" + year + " " + hour + ":" + min + ":" + sec + ":" + milli;

    datas = {"dist" : x , "palier" : palier, "date" : now};
    myarray.push(datas);
    document.getElementById('jsonprint').innerHTML = JSON.stringify(myarray, 'null', 4 );
    
    //print
    $("#titre").text(x + "cm");
    $("#palier").text(palier);
    $("#date").text(dd + "/" + mm + "/" + year + " " + hour + ":" + min + ":" + sec);
    myDoughnutChart.data.datasets[0].backgroundColor[0] = color;
    myDoughnutChart.data.datasets[0].data[0] = result;
    myDoughnutChart.data.datasets[0].data[1] = 431-result;
    myDoughnutChart.update();
}