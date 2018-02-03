var app = angular.module('spotifySlider', ['rzModule', 'ui.bootstrap']);

app.controller('MainCtrl', function($scope, $rootScope, $timeout) {

    $scope.slider_callbacks = {

        value: "1",
        offVal: new Date(Date.now() - Date.parse($scope.itemValue('spotify_current_update_time'))),

        options: {
            floor: 0,
            ceil: $scope.itemValue('spotify_current_duration'),
            step: 1,
            translate: function(value) {
                if (value == null || value == 0) {
                    return value;
                }
                offVal = new Date(Date.now() - Date.parse($scope.itemValue('spotify_current_update_time')));
                var modVal = new Date(value + Date.now() - Date.parse($scope.itemValue('spotify_current_update_time')));

                if ($scope.itemValue('spotify_current_playing') == 'OFF') {
                    modVal = new Date(parseInt(value));
                    console.log('Paused value:' + value + 'and modVal' + modVal + 'for state' + $scope.itemValue('spotify_current_playing.state'));

                }
                if (value === $scope.itemValue('spotify_current_duration')) {
                    console.log('Translate ceil value:' + value);
                    modVal = new Date(parseInt(value));
                    console.log('Translate ceil value:' + value + 'and modVal' + modVal);
                }
                //console.log('value :' + value + 'now:' + Date.now() + 'offset diff' + (Date.now() - Date.parse($scope.itemValue('spotify_current_update_time'))) + 'offVal: ' + Date.parse($scope.itemValue('spotify_current_update_time')));

                var minutes = Math.floor(modVal / 60000);
                var seconds = modVal.getSeconds(); //(value / 10000) % 60;
                var out = minutes + ":" + ("0" + seconds).slice(-2);
                //console.log('value:' + value + 'seconds' + seconds);
                console.log('Time log value:' + out);
                return out;
            },
            onStart: function(value) {
                $scope.stoggle = false;
                $scope.offsetTime = Date.now();
                offVal = Date.now();
            },
            onChange: function(value) {
                $scope.stoggle = false;
                offVal = Date.now();
            },
            onEnd: function(value) {
                $scope.stoggle = true;
            },
            getTime: function() {
                $scope.offsetTime = Date.now();
                offVal = Date.now();
                return Date.now();
            }

        }
    };


    $scope.slider_volume = {

        value: $scope.itemValue('spotify_current_volume'),
        toggle: true,
        options: {
            floor: 0,
            ceil: 100,
            step: 1,


            onStart: function(value) {
                $scope.slider_volume.toggle = false;
            },
            onChange: function(value) {
                $scope.slider_volume.toggle = true;
            },
            onEnd: function(value) {
                $scope.slider_volume.toggle = true;
            }

        }
    };




});