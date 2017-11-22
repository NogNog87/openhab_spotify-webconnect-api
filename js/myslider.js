var app = angular.module('rzSliderDemo', ['rzModule', 'ui.bootstrap']);

app.controller('MainCtrl', function($scope, $rootScope, $timeout) {
             
        $scope.slider_callbacks = {
           
            value: "1",
          
            options: {   
                        floor: 0, 
                        ceil: $scope.itemValue('spotify_current_duration')/1000, 
                        step: 1,                 
                        translate: function(value) {
                            if(value==null || value==0){
                                return value;
                            }
                            var minutes = Math.floor(value/60);
                            var seconds = value - minutes * 60;
                            var out = minutes +":"+ ("0" + seconds).slice(-2);
                            return out;
                        },
                        onStart: function(value) {
                           $scope.stoggle=false;
                        },
                        onChange: function(value) {
                            $scope.stoggle=false;
                        } ,            
                        onEnd: function(value) {
                          $scope.stoggle=true;
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
                        $scope.slider_volume.toggle = false;
                    } ,            
                    onEnd: function(value) {
                      $scope.slider_volume.toggle = true;
                    }
                    
        }
    };   
});