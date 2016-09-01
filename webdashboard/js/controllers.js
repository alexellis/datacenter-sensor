var app = angular.module('dashboard', []);

app.controller('SensorsController', function($scope, $http) {
  var refresh = 500;
  var chartRefresh = 1000;
  var totalLines =0;
  var lines = [];
  var colours = [
    {r:255, g:0, b:0},
    {r:0, g:255, b:0},
    {r:0, g:0, b:255},
    {r:100, g:255, b:100}
  ];

  var getStyle = function getStyle(index) {
    return { 
      strokeStyle: 'rgba(' +colours[index]['r'] + ', '+ colours[index]['g'] + ', ' + colours[index]['b'] + ', 1)', 
      fillStyle: 'rgba(' +colours[index]['r'] + ', '+ colours[index]['g'] + ', ' + colours[index]['b'] + ', 0.2)', 
      lineWidth:3 
    };
  };

  var smoothie = new SmoothieChart();
  smoothie.streamTo(document.getElementById("sensorCanvas"), chartRefresh /*delay*/); 

  var interval = setInterval(function() {

    $http.get("/json").then(function(response) {
      $scope.sensors = response.data["sensors"];
      var currentLines = $scope.sensors.length;
      if(!totalLines) {
        totalLines = currentLines;
        for(var j = 0; j < totalLines; j++) {
          var line = new TimeSeries();
          smoothie.addTimeSeries(line, getStyle(j));
          lines.push(line);
        }
      }
      if(lines.length) {
        for(var i = 0; i < $scope.sensors.length; i++) {
          var temp = $scope.sensors[i]["temp"];
          lines[i].append(new Date().getTime(), temp);
        }
      }
    }).catch(function() {
      $scope.error = "Unable to reach stats API";
    });
  }, refresh);

});
