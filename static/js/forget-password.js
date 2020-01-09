/* global FetchData */
const sendEmailAPI = '/api/user/password/forget';

function delayURL(url, time) {
  setTimeout(() => {
    window.location.href = `${url}`;
  }, time);
}

async function sendResetRequest() {
  // validate field and show hint
  if (document.forms['forget-password-form'].reportValidity()) {
    // start post
    document.getElementById('loadingDiv').style.display = 'block';
    document.getElementById('loadingImg').style.display = 'block';
    document.getElementById('txt').innerText = '';
    const result = await FetchData.post(sendEmailAPI, {
      email: document.getElementById('email').value,
      userName: document.getElementById('user-name').value,
    });

    if (result.status === 401) {
      // show wrong msg
      document.getElementById('loadingDiv').style.display = 'none';
      document.getElementById('loadingImg').style.display = 'none';
      document.getElementById('txt').innerText = '信箱或帳號錯誤';
    } else {
      // show successful msg
      document.getElementById('loadingDiv').style.display = 'none';
      document.getElementById('loadingImg').style.display = 'none';
      document.getElementById('forget-password-form').innerHTML = '';
      document.getElementById('txt').innerText = '重設密碼信件已發送，請至信箱查看。';
      delayURL('/menu', 1800);
    }
  }
}

function init() {
  // add event listener
  document
    .getElementById('forget-password-form')
    .addEventListener('submit', () => {
      sendResetRequest();
      return false;
    });
}

window.addEventListener('load', init);
