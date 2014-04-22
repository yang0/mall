'use strict';

/* Services */

var SERVER = '/';
var STATIC_URL = SERVER + 'static/classic/';
var MEDIA_URL = SERVER + 'static/upload/';
var PARTIAL_URL = STATIC_URL + 'partials/';


angular.module('appService', ['ngResource'])

.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}])

.factory('productService', ['$resource',
  function($resource){
    var categoryService =  $resource('/product/api/categoryProps/:id', {}, {
      categoryProps: {method:'GET', params:{id:0}, isArray:false},
    });


    return angular.extend({}, categoryService);
  }])






.factory('eavService', ['$resource',
  function($resource){
    var eavService =  $resource('/eav/api/enumgroup/:groupId', {}, {
      getEavValues: {method:'GET', params:{groupId:0}, isArray:false},
    });

    return angular.extend({}, eavService);
  }])






.run(function ($rootScope, $window) {
    $rootScope.SERVER = $window.SERVER; //global variable
    $rootScope.STATIC_URL = $window.STATIC_URL;
    $rootScope.MEDIA_URL = $window.MEDIA_URL;
    $rootScope.PARTIAL_URL = $window.PARTIAL_URL;
});
