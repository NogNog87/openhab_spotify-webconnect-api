var module = angular.module('myApp', []);

module.controller('TimeCtrl', function($scope, $interval) {
    var tick = function() {
        $scope.clock = Date.now();
    }
    tick();
    $interval(tick, 1000);
});



function updateClock() {
    var now = new Date(), // current date
        months = ['January', 'February', '...']; // you get the idea
    time = now.getHours() + ':' + now.getMinutes(), // again, you get the idea

        // a cleaner way than string concatenation
        date = [now.getDate(),
            months[now.getMonth()],
            now.getFullYear()
        ].join(' ');

    // set the content of the element with the ID time to the formatted string
    document.getElementById('time').innerHTML = [date, time].join(' / ');

    // call this function again in 1000ms
    setTimeout(updateClock, 1000);
}

updateClock(); // initial call

/*
var myApp = angular.module("myTime", []);

function TimeCtrl($scope, $timeout) {
    $scope.clock = "loading clock..."; // initialise the time variable
    $scope.tickInterval = 1000 //ms

    var tick = function() {
        $scope.clock = Date.now() // get the current time
        $timeout(tick, $scope.tickInterval); // reset the timer
    }

    // Start the timer
    $timeout(tick, $scope.tickInterval);
}

function updateClock() {
    var now = new Date(), // current date
        months = ['January', 'February', '...']; // you get the idea
    time = now.getHours() + ':' + now.getMinutes(), // again, you get the idea

        // a cleaner way than string concatenation
        date = [now.getDate(),
            months[now.getMonth()],
            now.getFullYear()
        ].join(' ');

    // set the content of the element with the ID time to the formatted string
    document.getElementById('mytime').innerHTML = [date, time].join(' / ');

    // call this function again in 1000ms
    setTimeout(updateClock, 1000);
}

updateClock(); // initial call
app.controller('MainCtrl', function($scope, $rootScope, $timeout) {

    var now = Date();
    $scope.time_callbacks = {

        value: "1",
        tvar: "2",
        options: {
            translate: function(value) {
                if (value == null || value == 0) {
                    return value;
                }
                var minutes = Math.floor(value / 60);
                var seconds = value - minutes * 60;
                var out = minutes + ":" + ("0" + seconds).slice(-2);
                return out;
            },
            onStart: function(value) {
                $scope.stoggle = false;
            },
            onChange: function(value) {
                $scope.stoggle = false;
            },
            onEnd: function(value) {
                $scope.stoggle = true;
            },
            startTimer: function(value) {
                updateClock(); // initial call
                $scope.tvar = document.getElementById('mytime').innerHTML;
            },



        }
    };





    myApp.controller("appCtrl", function($scope) {

        $scope.count = 2000;

        var count = $scope.count,
            data = [];

        while (count) {
            data[count] = count--;
        }

        $scope.totalDisplayed = 30;

        $scope.loadMore = function() {
            $scope.totalDisplayed += 35;
        };

        $scope.items = data;

    });
});
*/