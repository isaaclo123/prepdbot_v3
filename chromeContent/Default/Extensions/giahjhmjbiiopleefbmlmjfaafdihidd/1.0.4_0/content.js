var customId = 'fast-catch-KFoi8cNdjb';

if (!document.getElementById(customId)) {
  var iframe = document.createElement('iframe');
  iframe.id = customId;
  iframe.src = chrome.runtime.getURL('index.html');
  iframe.style.position = 'fixed';
  iframe.style.top = 0;
  iframe.style.right = 0;
  iframe.style.bottom = 0;
  iframe.style.left = 0;
  iframe.style.width = '100%';
  iframe.style.height = '100%';
  iframe.style.border = 0;
  iframe.style.zIndex = 2147483647;
  document.body.insertBefore(iframe, document.body.firstChild);
}

chrome.runtime.onMessage.addListener(function(message, _, sendResponse) {
  if (message.from === 'background') {
    if (message.action === 'urlAndContent') {
      sendResponse(getURLAndContent());
    }
    if (message.action === 'dismiss') {
      sendResponse(dismiss());
    }
  }
  return true;
});

function getURLAndContent() {
  var html = document.documentElement.cloneNode(true);
  var scrips = html.getElementsByTagName('script');
  var i = scrips.length;
  while (i--) {
    scrips[i].parentNode.removeChild(scrips[i]);
  }
  return {
    url: window.location.href,
    content: html.innerHTML
  };
}

function dismiss() {
  var iframe = document.getElementById(customId);
  if (iframe && iframe.parentNode) {
    iframe.parentNode.removeChild(iframe);
  }
  return true;
}
