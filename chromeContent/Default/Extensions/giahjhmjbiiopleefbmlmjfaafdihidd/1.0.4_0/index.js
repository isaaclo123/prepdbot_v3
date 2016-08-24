(function() {
  var onPostDismissMessage = function() {
    chrome.runtime.sendMessage({from: 'app', action: 'dismiss'});
  };
  var dismiss = document.getElementById('fast-catch-button-icon');
  dismiss.addEventListener('click', onPostDismissMessage, false);
})();