'use strict';

/* App Module */

angular.module('app', [
  'appService',
  'appDerectives',
  'ngSanitize'
])



.controller('productItemCtrl', ['$scope', '$window', 'productService', 
  function($scope, $window, productService) {

  	$scope.keyProp={}
  	$scope.keyProp.prop_type=1;
  	$scope.normalProp={}
  	$scope.normalProp.prop_type=2;
  	$scope.sellProp={};
  	$scope.sellProp.prop_type=3;

    $scope.initCategory = function(){
      $scope.categories = $window.categories;
      $scope.productItem = {};
      $scope.productItem.product_category = $scope.categories[0];
    }

    $scope.changeCategory = function(){
    	$scope.categoryProps = undefined;
    	productService.categoryProps({'id':$scope.productItem.product_category.id}, function(categoryDetail){
          	$scope.categoryProps = categoryDetail.props;
          	console.log($scope.categoryProps[0].name);
      	});
    }

    $scope.initCategory();

}]);

