overlayActive = false;
culsorState = 'default';

//start api actions --------------------------------------------------------------------------------
function addLinkRating() { //calls the api to rate <link> with rating <rating>
	var desiredLink=document.getElementById("linktextbox").value;
	var desiredRating=document.getElementById("ratingtextbox").value;
	if(desiredLink=='' || desiredLink == null || desiredRating == '' || desiredRating == null){
		showOverlay('Not all fields contain a value','You must enter a valid webpage and a valid rating.');
	}
	var apiLocation='/api/link/'+ desiredLink + '/rate:' + desiredRating;
	// send rate to api
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", apiLocation, true);
	xhttp.setRequestHeader("Content-type", "application/json");
	showOverlayBody();
	xhttp.onreadystatechange = function() {
		responseValidity = checkResponseValidity(this);
		if (responseValidity==1) { //response ok
			showOverlay('Rating accepted.',makeSomeLinks(String.format('Thank you for rating! (Rated {0}/10)',desiredRating)));
		} else if(responseValidity==2) { //some error
			showError(JSON.parse(this.responseText)['errorCode']);
		} else if(responseValidity==3){
			showOverlay('Authenication Error','Denied access to api. Are you logged in?')
		}
	}
	xhttp.send();
}

function calculateRating() { //makes the api calculate the rating for <link>; display confirmation
	var desiredLink=document.getElementById("linktextbox").value;
	var apiLocation='/api/link/'+ desiredLink + '/calculate';

	// calculate with api
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", apiLocation, true);
	xhttp.setRequestHeader("Content-type", "application/json");
	showOverlayBody();
	xhttp.onreadystatechange = function() {
		responseValidity = checkResponseValidity(this);
		if (responseValidity==1) { //ok
			showOverlay('Calculated.',makeSomeLinks(String.format('Calculated ratings for '+ desiredLink+'.')));
		} else if(responseValidity==0) { //error
			showError(JSON.parse(this.responseText)['errorCode']);
		}
	}
	xhttp.send();
}

function getRating() { //get rating for <link> and display in <overlay>
	var desiredLink=document.getElementById("linktextbox").value;
	var apiLocation='/api/link/'+ desiredLink + '/get';

	// calculate with api
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", apiLocation, true);
	xhttp.setRequestHeader("Content-type", "application/json");
	showOverlayBody();
	xhttp.onreadystatechange = function() {
		responseValidity = checkResponseValidity(this);
		if (responseValidity==1) { //response ok
			showOverlay('Average rating.',makeSomeLinks(String.format('On average, '+desiredLink + ' was rated {0}/10.',JSON.parse(this.responseText)['rating'].toFixed(1))));
		} else if(responseValidity==2) { //some error
			showError(JSON.parse(this.responseText)['errorCode']);
		} else if(responseValidity==3){
			showOverlay('Authenication Error','Denied access to api. Are you logged in?')
		}
	}
	xhttp.send();
}

function linktextboxChanged() {
	//generateTopLinkList();
}

function generateTopLinkList() {
		var apiLocation='/api/link/toplinks';
		var xhttp = new XMLHttpRequest();
		xhttp.open("GET", apiLocation, true);
		xhttp.setRequestHeader("Content-type", "application/json");
		//showOverlayBody();
		xhttp.onreadystatechange = function() {
			try {
				responseValidity = checkResponseValidity(this);
				if (responseValidity==1 && this.responseText != '' && this.responseText != null) { //response ok
					//debugger;
					document.getElementsByClassName("toplinks")[0].innerHTML = '';
					for(i=0;i<JSON.parse(this.responseText)['links'].length;i++){
						var parentElement = document.createElement('li');
						var element = document.createElement('a');
						element.innerText = JSON.parse(this.responseText)['links'][i]['link'];
						element.href = JSON.parse(this.responseText)['links'][i]['link'];
						parentElement.appendChild(element);
						document.getElementsByClassName("toplinks")[0].appendChild(parentElement)
					}
				} else if(responseValidity==2) { //some error
					//showError(JSON.parse(this.responseText)['errorCode']);
					throw('test');
				} else if(responseValidity==3){
					//showOverlay('Authenication Error','Denied access to api. Are you logged in?')
					alert('ererere');
				}
			} catch (e) {
				document.getElementById('topLinksLoadingPlaceholder').innerText = 'An error occured while loading the links...'
			}
		}
		xhttp.send();
}
//end api actions ----------------------------------------------------------------------------------


//start tools --------------------------------------------------------------------------------------
function roundTo(n, digits) { //rounds <n> to <digits> digits
	var negative = false;
	if (digits === undefined) {
		digits = 0;
	}
		if( n < 0) {
		negative = true;
	  n = n * -1;
	}
	var multiplicator = Math.pow(10, digits);
	n = parseFloat((n * multiplicator).toFixed(11));
	n = (Math.round(n) / multiplicator).toFixed(2);
	if( negative ) {
		n = (n * -1).toFixed(2);
	}
	return n;
}

function makeSomeLinks(str) { //transform every link in a string into an <a> element
	//returnStr = [];
	regex = /((?:http|ftp|https):\/\/(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])?)/g;
    //matches=str.match(regex);
	//for(i=0;i<matches.length;i++){returnStr.push(matches[i].replace(regex,"<a href='$1'>$1</a>"));}
	return str.replace(regex,"<a href='$1'>$1</a>");
}

if (!String.format) { //replaces the normal String.format function with something closer to python
  String.format = function(format) {
	var args = Array.prototype.slice.call(arguments, 1);
	return format.replace(/{(\d+)}/g, function(match, number) {
	  return typeof args[number] != 'undefined'
		? args[number]
		: match
	  ;
	});
  };
}
//end tools --------------------------------------------------------------------------------------


//start overlay ----------------------------------------------------------------------------------
function showError(errorCode){ //shows an overlay with 'error' and corresponding errorCode
	showOverlay('Error.','An error occured. Code  ' + errorCode)
}

function showOverlayBody() {
	showOverlay('…','…');
}
function showOverlay(title,body){ //shows the overlay with the given title and body
	/*if(overlayActive){
		hideOverlay();
		showOverlay(title,body);
	} else {*/
		document.getElementById('panel-title').innerHTML = '<h3 class="panel-title" id="panel-title">'+title+'</h3>';
		document.getElementById('panel-body').innerHTML = '<p id="panel-body">'+body+'</p>';

		$('.overlay').fadeIn('fast');
		overlayActive = true;
		document.getElementById('closeOverlayButton').focus();
	//}
}

function hideOverlay(){ //hides the overlay
	$('.overlay').fadeOut('fast');
	overlayActive = false;
}
//end overlay ------------------------------------------------------------------------------------


//start checks -----------------------------------------------------------------------------------
function checkResponseValidity(response) { //checks for errors in the http response
	var errorCode = null;
	//console.log(response);
	if(response.readyState == 4 && response.status == 200){ // page ready loaded
		if(JSON.parse(response.responseText)['errorCode']==1){
			errorCode = 1; // reponse errorCode good
		} else {
			errorCode = 2; // response errorCode bad
		}
	} else if(response.readyState == 4 && response.status == 401) {
		errorCode = 3; // page ready but denied access to api
	} else if(! response.readyState == 4) {
		errorCode = 4; // wait for one more 'readyStateChange' -> response not ready
	} else {
		errorCode = 0; // unknown error
	}
	return errorCode;
}
//end checks -------------------------------------------------------------------------------------

if(document.getElementById('topLinksLoadingPlaceholder') != null){generateTopLinkList();}
