chrome.browserAction.onClicked.addListener(function browserActionOnClick(tab) {
  chrome.tabs.executeScript(tab.id, {
    file: 'content.js'
  });
});

chrome.runtime.onMessage.addListener(function runtimeOnMessage(message, _, sendResponse) {
  if (message.from === 'app') {
    getContent(message, sendResponse);
  }
  return true;
});

function getContent(message, sendResponse) {
  chrome.tabs.query({active: true, currentWindow: true}, function tabsQuery(tabs) {
    chrome.tabs.sendMessage(getFirstTabId(tabs), {from: 'background', action: message.action}, function(response) {
      sendResponse(response);
    });
  });
}

function getFirstTabId(tabs) {
  return tabs[0].id;
}
