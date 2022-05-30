cordova.define('cordova/plugin_list', function(require, exports, module) {
module.exports = [
    {
        "file": "plugins/cordova-clipboard/www/clipboard.js",
        "id": "cordova-clipboard.Clipboard",
        "pluginId": "cordova-clipboard",
        "clobbers": [
            "cordova.plugins.clipboard"
        ]
    },
    {
        "file": "plugins/cordova-clipboard-api/www/clipboard.js",
        "id": "cordova-clipboard-api.Clipboard",
        "pluginId": "cordova-clipboard-api",
        "clobbers": [
            "cordova.plugins.clipboard"
        ]
    },
    {
        "file": "plugins/es6-promise-plugin/www/promise.js",
        "id": "es6-promise-plugin.Promise",
        "pluginId": "es6-promise-plugin",
        "runs": true
    },
    {
        "file": "plugins/cordova-plugin-x-socialsharing/www/SocialSharing.js",
        "id": "cordova-plugin-x-socialsharing.SocialSharing",
        "pluginId": "cordova-plugin-x-socialsharing",
        "clobbers": [
            "window.plugins.socialsharing"
        ]
    }
];
module.exports.metadata = 
// TOP OF METADATA
{
    "cordova-clipboard": "1.3.0",
    "cordova-clipboard-api": "1.3.0",
    "es6-promise-plugin": "4.2.2",
    "cordova-plugin-x-socialsharing": "6.0.3"
}
// BOTTOM OF METADATA
});