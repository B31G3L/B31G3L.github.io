const texttLinkTo = 'Link to screentrackr';
const pickAppAndroid = 'Pick an app';
const title = 'screentrackr';

function copyURLwithParams(){
  let isBrowser = device.platform == 'browser';
  let screentrackrUrl;

  if(isBrowser){
    let hostname =  window.location.hostname;
    let protocol = window.location.protocol;
    screentrackrUrl = protocol + "//" + hostname;
    if(hostname == 'localhost') {
      screentrackrUrl = screentrackrUrl.concat(':8000');
    }
  }else{
    screentrackrUrl = "https://irgendwas.com";
  }


    const urlWithParams = new URL("/", screentrackrUrl);

    urlWithParams.searchParams.append(bgColor, BGColor.value);
    urlWithParams.searchParams.append(markerColor, MarkerColor.value);
    urlWithParams.searchParams.append(markerDensity, MarkerDensity.value);
    urlWithParams.searchParams.append(markerSize, MarkerSize.value);
    urlWithParams.searchParams.append(markerType, MarkerType.value);

    if(isBrowser){
      shareBrowser(urlWithParams)
    }else{
      shareApp(urlWithParams);
    }
  
  }

function shareBrowser(linkToShare){
  var shareData = {
    title: title,
    text: texttLinkTo,
    url: linkToShare
  }
  try {
    navigator.share(shareData)
  } catch(err) {
  }
}

function shareApp(linkToShare){
  var options = {
    subject: texttLinkTo,
    url: linkToShare,
    chooserTitle: pickAppAndroid, 
  };
  window.plugins.socialsharing.shareWithOptions(options);
}