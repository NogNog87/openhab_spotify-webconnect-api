var myApp = angular.module("myApp", []);

myApp.directive("whenScrolled", function() {
    return function(scope, elm, attr) {
        var raw = elm[0];
        elm.bind("scroll", function() {
            if (raw.scrollTop + raw.offsetHeight >= raw.scrollHeight) {
                scope.$apply(attr.whenScrolled);
            }
        });
    };
});

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