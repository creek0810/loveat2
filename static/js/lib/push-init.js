/* global firebase, FetchData */

const pushAPI = {
  updateToken: '/api/user/token',
};

// init firebase
firebase.initializeApp({
  apiKey: 'AIzaSyBzQFgi_cijoRqGwUtkWYGg7NZeqcjDTOY',
  authDomain: 'loveat2.firebaseapp.com',
  databaseURL: 'https://loveat2.firebaseio.com',
  projectId: 'loveat2',
  storageBucket: 'loveat2.appspot.com',
  messagingSenderId: '1010525619811',
  appId: '1:1010525619811:web:25889ad1dfc18545b05a56',
});
const messaging = firebase.messaging();
messaging.usePublicVapidKey(
  'BMSp_k2JZITgK0Q7D2o3cnWsD_9bOqR8LYQTM4tTGWQXg_P_DZ5OGb3YWC-JmjuRkK1FrjpnGbH3BnSP17rtiXo',
);

function getTokenAndSend() {
  messaging.getToken().then((token) => {
    if (token) {
      FetchData.post(pushAPI.updateToken, {
        token,
      });
    }
  });
}

function requestPermission() {
  const nav = document.getElementById('settingDropDown');
  // check if user login
  if (nav != null) {
    if (
      Notification.permission === 'default'
      || Notification.permission === 'undefined'
    ) {
      Notification.requestPermission().then((permission) => {
        if (permission === 'granted') {
          getTokenAndSend();
        }
      });
    } else {
      getTokenAndSend();
    }
  }
}

window.addEventListener('load', requestPermission);
