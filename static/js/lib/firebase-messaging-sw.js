/* global firebase, clients */
importScripts('https://www.gstatic.com/firebasejs/7.5.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/7.5.0/firebase-messaging.js');
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

messaging.setBackgroundMessageHandler((payload) => {
  if (payload.data.type === 'admin-order-update') {
    const channel = new BroadcastChannel('order-todo');
    channel.postMessage(JSON.parse(payload.data.detail));
  } else {
    const notificationTitle = payload.data.title;
    const notificationOptions = {
      body: payload.data.content,
      icon: 'favicon.ico',
      data: { url: payload.data.url },
      actions: [{ action: 'open_url', title: '立刻查看' }],
    };

    // eslint-disable-next-line no-restricted-globals
    return self.registration.showNotification(
      notificationTitle,
      notificationOptions,
    );
  }
  return undefined;
});

// eslint-disable-next-line no-restricted-globals
self.addEventListener(
  'notificationclick',
  (e) => {
    if (e.action === 'open_url') {
      clients.openWindow(e.notification.data.url);
    }
  },
  false,
);

// eslint-disable-next-line no-restricted-globals
self.addEventListener('message', () => {
  clients.openWindow('/menu');
});
