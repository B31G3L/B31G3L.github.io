

document.getElementById("testClipboard").addEventListener("click", myFunction);

function myFunction(){
    window.cordova.plugins.clipboard.copy({
        type: "text", // default, so not needed for text
        data: "Howdy Partner!"
    }, (res) => {
        console.log(res);
    });

}