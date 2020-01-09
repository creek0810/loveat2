/* global FetchData, $, lozad */
/* eslint no-underscore-dangle: 0 */
/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "deleteItemOrCombo" }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["eachDescription"] }] */
const ID_TO_NAME = {}; // {"_id1":"name1"}
const TYPE_DATA = {}; // {type1:{"id":[], "category":"item"}}

const menuEditAPI = {
  all: '/api/menu',
  newType: '/api/menu/type/new',
  updateType: '/api/menu/type/update',
  deleteType: '/api/menu/type/delete',
  deleteItem: '/api/menu/item/delete',
  deleteCombo: '/api/menu/combo/delete',
};

const ACTION_NUM = { ADD: 0, UPDATE: 1, DELETE: 2 };
const reNameMsg = [
  '該種類已存在，請重新輸入。',
  '該種類已存在。',
  '該種類已存在。',
];
const successfulMsg = ['成功新增！', '成功修改！', '成功刪除'];
const action = ['add-type-txt', 'update-type-txt', 'delete-type-txt'];

function checkStatus(status, actionNum) {
  if (status === 403) {
    // show wrong msg
    document.getElementById(action[actionNum]).innerText = '權限錯誤。';
  } else if (status === 409) {
    document.getElementById(action[actionNum]).innerText = reNameMsg[actionNum];
  } else {
    // show successful msg
    document.getElementById(action[actionNum]).innerText = successfulMsg[actionNum];
    window.location.reload();
  }
}

/* ---- 點選type 將其他type相關之餐點class設為hidden----*/
function searchByType(event) {
  const tarType = event.target[event.target.selectedIndex].id;
  if (tarType === 'type0') {
    const menuTr = document
      .getElementById('menu-table')
      .getElementsByTagName('tr');
    Array.from(menuTr).forEach((each) => {
      each.setAttribute('class', '');
    });
  } else {
    const tarTypeId = TYPE_DATA[tarType].id;
    tarTypeId.forEach((id) => {
      document.getElementById(id).setAttribute('class', '');
    });
    Object.keys(TYPE_DATA).forEach((type) => {
      if (tarType !== type) {
        TYPE_DATA[type].id.forEach((id) => {
          document.getElementById(id).setAttribute('class', 'hidden');
        });
      }
    });
  }
}

async function deleteItemOrCombo(e) {
  let result;
  if (e.id.match('item')) {
    result = await FetchData.post(menuEditAPI.deleteItem, {
      id: e.id.substring(12),
    });
  } else {
    result = await FetchData.post(menuEditAPI.deleteCombo, {
      id: e.id.substring(13),
    });
  }

  if (result.status === 403) {
    // show wrong msg
    $('#alert-modal').modal('show');
  } else {
    // delete row
    const i = e.parentNode.parentNode.rowIndex;
    document.getElementById('menu-table').deleteRow(i);
  }
}

async function menuInit() {
  const descriptionTrs = document.getElementsByName('description');
  Array.from(descriptionTrs).forEach((eachDescription) => {
    eachDescription.innerHTML = eachDescription.innerHTML.replace(
      /\n/g,
      '<br>',
    );
  });
  const menu = await FetchData.get(menuEditAPI.all).then((res) => res.json());
  menu.forEach((type, idx) => {
    TYPE_DATA[`type${idx + 1}`] = { id: [], category: type.category };
    type.content.forEach((i) => {
      TYPE_DATA[`type${idx + 1}`].id.push(i._id);
      ID_TO_NAME[i._id] = i.name;
    });
  });
}

async function addType() {
  if (document.forms['add-type-form'].reportValidity()) {
    const type = document.getElementById('add-type').value;
    if (type === '未分類(套餐)' || type === '未分類(單品)') {
      checkStatus(409, ACTION_NUM.ADD);
    } else {
      // resolve category's value
      const selection = document.getElementById('item-or-combo-type');
      const category = selection.options[selection.selectedIndex];
      // start post
      const result = await FetchData.post(menuEditAPI.newType, {
        type: document.getElementById('add-type').value,
        category: category.value,
      });
      checkStatus(result.status, ACTION_NUM.ADD);
    }
  }
}

async function updateType() {
  if (document.forms['update-type-form'].reportValidity()) {
    const selection = document.getElementById('update-type-list');
    const index = selection.selectedIndex;
    const result = await FetchData.post(menuEditAPI.updateType, {
      id: selection.options[index].id.substring(12),
      type: document.getElementById('update-type').value,
    });

    checkStatus(result.status, ACTION_NUM.UPDATE);
  }
}

async function deleteType() {
  const selection = document.getElementById('delete-type-list');
  const index = selection.selectedIndex;
  const result = await FetchData.post(menuEditAPI.deleteType, {
    id: selection.options[index].id.substring(12),
  });

  checkStatus(result.status, ACTION_NUM.DELETE);
}
function init() {
  // init lazy load pic
  const observer = lozad(); // lazy load
  observer.observe();
  menuInit();
  document.getElementById('add-type-btn').addEventListener('click', addType);
  document
    .getElementById('update-type-btn')
    .addEventListener('click', updateType);
  document
    .getElementById('delete-type-btn')
    .addEventListener('click', deleteType);
  document.getElementById('type-list').addEventListener('change', searchByType);
}

window.addEventListener('load', init);
