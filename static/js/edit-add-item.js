/* global FetchData, $ */
/* eslint no-underscore-dangle: 0 */

const newItemAPI = '/api/menu/item/new';
const updateItemAPI = '/api/menu/item/update';
const ADD = 0;
const UPDATE = 1;
let page;

// display on board instantly
function display() {
  const detail = document.getElementById('detail');
  let description = document.getElementById('description').value;
  description = description.replace(/\n/g, '<br />');
  detail.innerHTML = `名稱：${document.getElementById('name').value} <br>
                    價格：${document.getElementById('price').value} <br>
                    說明：${description}`;
}

function clearContent() {
  const idName = ['name', 'price', 'picture', 'description'];
  idName.forEach((id) => {
    document.getElementById(id).value = '';
  });
  document.getElementById('type-list').options[0].selected = true;
  document.getElementById('picture-show').setAttribute('src', '');
  display();
}

function delayURL(url, time) {
  setTimeout(() => {
    window.location.href = `${url}`;
  }, time);
}

const successfulMsg = ['新增', '修改'];
const successfulMsgBody = ['繼續新增下一筆菜單', ''];
function checkStatus(status, actionNum) {
  const statusResult = {
    403: {
      title: '發生錯誤',
      body: '權限錯誤！請登入後再執行。',
    },
    409: {
      title: '發生錯誤',
      body: '此名稱已存在，請更改名字！。',
    },
    200: {
      title: `單品${successfulMsg[actionNum]}成功`,
      body: `單品${successfulMsg[actionNum]}成功！${successfulMsgBody[actionNum]}`,
    },
  };
  document.getElementById('alert-title').innerHTML = statusResult[status].title;
  document.getElementById('alert-body').innerHTML = statusResult[status].body;
  $('#alert-modal').modal('show');
  if (status === 200) {
    if (actionNum === ADD) clearContent();
    else delayURL('/menu/edit', 1800);
  }
}

async function upload() {
  if (document.forms['item-form'].reportValidity()) {
    const selection = document.getElementById('type-list');
    const index = selection.selectedIndex;
    const myForm = document.getElementById('item-form');
    const formData = new FormData(myForm);
    formData.append('type', selection.options[index].id.substring(5));
    if (page === ADD) {
      const result = await FetchData.postForm(newItemAPI, formData);
      checkStatus(result.status, ADD);
    } else {
      formData.append(
        'id',
        document.getElementsByClassName('item-id')[0].id.substring(3),
      );
      const result = await FetchData.postForm(updateItemAPI, formData);
      checkStatus(result.status, UPDATE);
    }
  }
}

// let picture can show instantly
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

function displayInitType() {
  const typeId = document
    .getElementsByClassName('item-type')[0]
    .id.substring(5);
  const typeSection = document.getElementById('type-list');
  const result = [...typeSection.options].find(
    (Eachtype) => Eachtype.id.substring(5) === typeId,
  );
  result.selected = true;
}

function init() {
  if (document.getElementById('name').value !== '') {
    page = UPDATE;
    displayInitType();
  } else page = ADD;
  document.getElementById('clear').addEventListener('click', clearContent);
  document.getElementById('submit').addEventListener('click', upload);
  document.getElementById('name').addEventListener('keyup', display);
  document.getElementById('price').addEventListener('change', display);
  document.getElementById('price').addEventListener('keyup', display);
  document.getElementById('description').addEventListener('keyup', display);
  document
    .getElementById('picture')
    .addEventListener('change', function read() {
      readURL(this);
    });
  display();
}

window.addEventListener('load', init);
