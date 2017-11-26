


//start outdated functions -----------------------------------------------------------------------
/*

function checkErrorCodeValidity(errorCode) { //checks if errorCode == 1 duh [deprecated]
	return (errorCode==1)
}

function checkLinkValidity(str) { //check if str contains links [deprecated]
	regex = /(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])?/g;
	let m;

	while ((m = regex.exec(str)) !== null) {
		if (m.index === regex.lastIndex) {
			regex.lastIndex++;
		}

		return (m.lenght>0);
	}
}

function redirectTo(link,response) { //redirects the user to <link> if there's no error [deprecated]
	response = JSON.parse(response);
	if(response['errorCode']=='1'){
		window.location=link;
	}else{
		//alert('An Error occured. Code: ' + response['errorCode']);
	}
}

function redirectToRatedPage(response) {
	response = JSON.parse(response);
	if(response['errorCode']=='1'){
		window.location='/rated';
	}else{
		alert('An Error occured. Code: ' + response['errorCode']);
	}
}

function redirectToPageControl() {
	window.location='/'+document.getElementById("linktextbox").value+'/control';
}
*/
//end outdated functions -------------------------------------------------------------------------


//start outdated function snippets ---------------------------------------------------------------
/*
addlinkrating{if (this.readyState == 4 && this.status == 200 && checkErrorCode(errorCode)) {
			//redirectTo('/rated',this.responseText);
			//alert(String.format('Thank you for rating! (Rated {0}/10.)',desiredRating))
			showOverlay('Rating accepted.',String.format('Thank you for rating! (Rated {0}/10.)',desiredRating));
		}else{
			//alert('An Error occured' + this.responseText['errorCode']);
		}}

getrating{
	if (this.readyState == 4 && this.status == 200) {
			redirectTo('/rating/'+JSON.parse(response)['rating'],this.responseText);
		}else{
			//alert('An Error occured' + this.responseText['errorCode']);
		}
}
*/
