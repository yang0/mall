'use strict';

/* Directives */


angular.module('appDerectives', ['ngResource', 'appService'])


.directive('sellFields', ['eavService', function(eavService) {
    return {
      restrict: 'E',
      scope: {},
      transclude: true,
      controller: function($scope) {
	      	var eavEnumVals = $scope.eavEnumVals = {};

	  		this.addEnumGroup = function(groupId, enumVals){
	  			eavEnumVals[groupId] = enumVals;


	  			var skuArray=[];
	  			var log = [];
	  			angular.forEach(eavEnumVals, function(val, key){
	  				
	  				var oldArray = [].concat(skuArray);
	  				var step = 0;
	  				angular.forEach(val, function(vName, vId){

	  					if(vName != "false"){
	  						//生成sku组合
	  						step++;
	  						if(oldArray.length==0){
	  							
		  						var v = {}
		  						var enumValPair = {}
		  						enumValPair[vId] = vName
		  						v[key] = enumValPair;
		  						skuArray.push(v)
		  					}else{
		  						if(step == 1){
		  							
		  							for(var i =0; i < skuArray.length; i++){
		  								var v = skuArray[i];
		  								var enumValPair = {}
				  						enumValPair[vId] = vName
				  						v[key] = enumValPair;
		  							}
		  						}else{
		  							
		  							for(var i=0; i< oldArray.length; i++){
		  								console.log(skuArray[0]["3"]);

		  								var v = angular.extend({}, oldArray[i]);
		  								var enumValPair = {}
				  						enumValPair[vId] = vName
				  						v[key] = enumValPair;
		  								skuArray.push(v);
		  							}

		  						}
		  					}
	  					}

	  					
	  					
	  				})
	  				
	  			}, log)

				$scope.skuArray = skuArray;

	  		};
       },
      templateUrl: PARTIAL_URL + 'eav/sell_fields.html'
    };
 }])


.directive('sellField', ['eavService', function(eavService) {
    return {
      require: '^sellFields',
      restrict: 'E',
      scope: {
        prop: '=prop'
      },
      link: function(scope, element, attrs, sellCtrl) {
      		var dataType = scope.prop.datatype;
      		getEavVal(scope.prop.eav_group);
      		console.log(scope.prop.eav_group);

      		scope.selectVal = function(){
      			console.log("aaaaaaabbbbb");
      			sellCtrl.addEnumGroup(scope.prop.id, scope.eavEnumVals[scope.prop.id]);
      		};


      		function getEavVal(groupId){
      			scope.eavEnumVals={};
      			scope.eavEnumVals[scope.prop.id]={};


      			eavService.getEavValues({'groupId':groupId}, function(eavEnumGroup){
		          	scope.eavEnumGroup = eavEnumGroup;
		      	});
      		}
      		
       },
      templateUrl: PARTIAL_URL + 'eav/sell_field.html'
    };
  }])



.directive('eavField', ['eavService', function(eavService) {
    return {
      restrict: 'E',
      scope: {
        prop: '=prop'
      },
      link: function(scope, element, attrs) {
      		var dataType = scope.prop.datatype;
      		if(dataType <= 1){
      			scope.contentUrl = PARTIAL_URL + 'eav/field_number.html';
      		}else if(dataType == 3){
      			scope.contentUrl = PARTIAL_URL + 'eav/field_date.html';
      		}else if(dataType == 4){
      			scope.contentUrl = PARTIAL_URL + 'eav/field_bool.html';
      		}else if(dataType == 5){
      			getEavVal(scope.prop.eav_group);
      			scope.contentUrl = PARTIAL_URL + 'eav/field_enum.html';
      		}else{
      			scope.contentUrl = PARTIAL_URL + 'eav/field_text.html';
      		} 


      		function getEavVal(groupId){
      			scope.eavEnumVals={};
      			scope.eavEnumVals[groupId]={};

      			eavService.getEavValues({'groupId':groupId}, function(eavEnumGroup){
		          	scope.eavEnumGroup = eavEnumGroup;
		      	});
      		}
       },
      template: '<div ng-include="contentUrl"></div>'
    };
  }])
