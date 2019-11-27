/* global FetchData, $ */
const API = {
  login: 'https://loveat2.appspot.com/api/user/login',
  register: 'https://loveat2.appspot.com/api/user/register',
};
function validatePassword() {
  const confirmPassword = document.getElementById('register-confirm-password').value;
  const password = document.getElementById('register-password').value;
  if (confirmPassword !== password) {
    document.getElementById('register-confirm-password').setCustomValidity('無法和密碼匹配');
  } else {
    document.getElementById('register-confirm-password').setCustomValidity('');
  }
}
async function login() {
  // validate field and show hint
  if (document.forms['login-form'].reportValidity()) {
    // start post
    const result = await FetchData.post(API.login, {
      userName: document.getElementById('login-user-name').value,
      password: document.getElementById('login-password').value,
    });
    if (result.status === 401) {
      // show wrong msg
      document.getElementById('login-wrong').innerText = 'Wrong user name or password.';
    } else {
      // refresh page
      window.location.reload();
    }
  }
}

async function register() {
  // clear register-wrong content
  document.getElementById('register-wrong').innerText = '　';
  // validate filed and show hint
  if (document.forms['register-form'].reportValidity()) {
    // get input value
    const result = await FetchData.post(API.register, {
      userName: document.getElementById('register-user-name').value,
      password: document.getElementById('register-password').value,
      age: parseInt(document.getElementById('register-age').value, 10),
      gender: document.getElementById('register-gender').value,
      phone: document.getElementById('register-phone').value,
      email: document.getElementById('register-email').value,
    });
    if (result.status === 409) {
      document.getElementById('register-wrong').innerText = '此帳號已經有人使用';
    } else if (result.status === 200) {
      $('#register-modal').modal('hide');
      $('#register-success-modal').modal('show');
    }
  }
}
function init() {
  // add event listener
  document.getElementById('login').addEventListener('click', login);
  document.getElementById('register').addEventListener('click', register);
  // validate password when password or confirm password change
  document.getElementById('register-password').addEventListener('keyup', validatePassword);
  document.getElementById('register-confirm-password').addEventListener('keyup', validatePassword);
}

window.addEventListener('load', init);
