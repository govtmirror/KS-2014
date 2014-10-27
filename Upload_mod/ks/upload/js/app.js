'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', []).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/Awards', {templateUrl: 'partials/awardview.html', controller: PartCtrl});
    $routeProvider.when('/PEBs', {templateUrl: 'partials/pebview.html', controller: PartCtrl});
    $routeProvider.when('/Contracts', {templateUrl: 'partials/contractview.html', controller: PartCtrl});
    $routeProvider.when('/Decisions', {templateUrl: 'partials/decisionview.html', controller: PartCtrl});
    $routeProvider.when('/AnnualReports', {templateUrl: 'partials/annualreportview.html', controller: PartCtrl});
    $routeProvider.when('/Others', {templateUrl: 'partials/otherview.html', controller: PartCtrl});
    $routeProvider.otherwise({redirectTo: '/Awards'});
  }]);
