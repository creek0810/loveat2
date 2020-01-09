/* global FetchData, $ */
/* eslint no-underscore-dangle: ["error", { "allow": ["_id"] }] */
const PROFILE_UPDATE_API = {
  password: '/api/user/password/update',
  user: '/api/user/update',
};
const PASSWORD = ['oldPassword', 'newPassword', 'comfirmNewPassword'];

/* ----check the fields of the password---- */
function validatePassword() {
  const newPassword = document.getElementById('newPassword');
  const comfirmNewPassword = document.getElementById('comfirmNewPassword');
  /* --validate all password-- */
  PASSWORD.forEach((element) => {
    if (document.getElementById(element).value === '') {
      document.getElementById(element).setCustomValidity('需填寫');
    } else {
      document.getElementById(element).setCustomValidity('');
    }
  });

  if (newPassword.value.length < 7) {
    newPassword.setCustomValidity('密碼需設長度大於等於8個字母長度');
  } else if (newPassword.value !== comfirmNewPassword.value) {
    comfirmNewPassword.setCustomValidity('無法和密碼匹配');
  } else {
    comfirmNewPassword.setCustomValidity('');
  }
}

/* ----update the password---- */
async function updatePassword() {
  validatePassword();
  document.getElementById('update-password-wrong').innerHTML = '';

  if (document.forms['update-password-form'].reportValidity()) {
    const newPassword = document.getElementById('newPassword').value;
    if (newPassword.length >= 8) {
      const result = await FetchData.post(PROFILE_UPDATE_API.password, {
        oldPassword: document.getElementById('oldPassword').value,
        newPassword: document.getElementById('newPassword').value,
      });

      if (result.status === 401) {
        document.getElementById('update-password-wrong').innerHTML = '舊密碼錯誤或是未登入。';
      } else if (result.status === 200) {
        $('#update-password-modal').modal('hide');
        $('#update-success-modal').modal('show');
        PASSWORD.forEach((element) => {
          // clear password field
          document.getElementById(element).value = '';
        });
      }
    }
  }
}

/* ----get and show the photo on the profile---- */
function readURL(input) {
  if (input.files && input.files[0]) {
    const reader = new FileReader();

    reader.onload = function loadPicture(e) {
      document
        .getElementById('picture-show')
        .setAttribute('src', e.target.result);
    };

    reader.readAsDataURL(input.files[0]);
  }
}

/* ----check the fields of the userInfo---- */
function validateUserInfo() {
  const userInfo = ['age', 'gender', 'phone', 'email'];
  const picture = document.getElementById('changePhoto').files[0];

  /* --allow users only use image files-- */
  if (picture) {
    if (picture.type.indexOf('image') === -1) {
      document.getElementById('changePhoto').setCustomValidity('請選取圖片檔');
    } else {
      document.getElementById('changePhoto').setCustomValidity('');
    }
  }
  userInfo.forEach((element) => {
    if (document.getElementById(element).value === '') {
      document.getElementById(element).setCustomValidity('需填寫');
    } else {
      document.getElementById(element).setCustomValidity('');
    }
  });
}

/* ----update the user info---- */
async function updateUserInfo() {
  validateUserInfo();
  if (
    document.forms['user-info-form'].reportValidity()
    && document.forms['user-propic-form'].reportValidity()
  ) {
    const formData = new FormData();
    const gender = document.getElementById('gender');
    formData.append('age', document.getElementById('age').value);
    formData.append('gender', gender.options[gender.selectedIndex].text);
    formData.append('email', document.getElementById('email').value);
    formData.append('phone', document.getElementById('phone').value);
    formData.append('picture', document.getElementById('changePhoto').files[0]);

    const result = await FetchData.postForm(PROFILE_UPDATE_API.user, formData);
    if (result.status === 401) {
      console.log('您沒有該權限喔!');
    } else if (result.status === 200) {
      document.getElementById('exampleModalLabel').innerHTML = '更新個人資料';
      $('#update-success-modal').modal('show');
    }
  }
}

function init() {
  /* ----listener for change photo---- */
  document
    .getElementById('changePhoto')
    .addEventListener('change', function read() {
      readURL(this);
    });
  /* ----listener for password update---- */
  document
    .getElementById('change-password')
    .addEventListener('click', (event) => {
      event.preventDefault();
    });
  document
    .getElementById('updatePassword')
    .addEventListener('click', updatePassword);
  /* ----listener for user info update---- */
  document
    .getElementById('updateUserInfo')
    .addEventListener('click', updateUserInfo);
}

window.addEventListener('load', init);
