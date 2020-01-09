/* eslint-disable no-unused-vars */
/* global Cart, $, FetchData, lozad */
/* eslint no-underscore-dangle: ["error", { "allow": ["_id"] }] */

const ID_TO_NAME = {}; // {"_id1":"name1"}
const TYPE_DATA = {}; // {type1:{"id":[], "category":"item"}}
let myCart = null;

/* ---- show the nothing message to users ---- */
function showNothing(mode) {
  // mode: true or false
  const showNothingDiv = document.getElementById('show-nothing');
  if (mode === true) {
    showNothingDiv.innerHTML = '找不到東西~<br>可能是關鍵字錯誤或是老闆還沒有新增東西喔~';
    showNothingDiv.classList.remove('hidden');
  } else {
    showNothingDiv.classList.add('hidden');
  }
}

/* ---- 點選type 將其他type相關之餐點class設為hidden----*/
function searchByType(event) {
  const tarType = event.target.id;
  const tarTypeId = TYPE_DATA[tarType].id;
  const showNothingFlag = tarTypeId.length === 0; // true : display show nothing
  showNothing(showNothingFlag);
  tarTypeId.forEach((id) => {
    document.getElementById(id).classList.remove('hidden');
  });
  Object.keys(TYPE_DATA).forEach((type) => {
    if (tarType !== type) {
      TYPE_DATA[type].id.forEach((id) => {
        document.getElementById(id).classList.add('hidden');
      });
    }
  });
}

/* ---- search by name ---- */
function searchByName(event) {
  let showNothingFlag = true; // true : display show nothing
  if (event.which === 13) {
    // enter key
    const itemName = document.getElementById('search').value;
    Object.keys(ID_TO_NAME).forEach((id) => {
      if (ID_TO_NAME[id].includes(itemName)) {
        document.getElementById(id).classList.remove('hidden');
        showNothingFlag = false;
      } else {
        document.getElementById(id).classList.add('hidden');
      }
    });
    showNothing(showNothingFlag);
  }
}

/* ---- user add item into local storage ----*/
function addContent(event) {
  const itemId = event.target.id.replace('submit_', '');
  const itemQuantity = parseInt(
    document.getElementById(`input_${itemId}`).value,
    10,
  );
  const orderHintModal = document.getElementById('orderHintContent');
  let itemCategory = '';

  Object.keys(TYPE_DATA).forEach((type) => {
    if (TYPE_DATA[type].id.includes(itemId)) {
      itemCategory = TYPE_DATA[type].category;
    }
  });

  const data = {
    _id: itemId,
    category: itemCategory,
    quantity: itemQuantity,
  };

  if (data.quantity >= 1 && data.quantity <= 99) {
    const addResult = myCart.add(data);
    if (addResult) {
      orderHintModal.innerHTML = `新增成功~<br>祝您吃的開心~<br>此商品目前總數為${
        myCart.get()[data._id].quantity
      }`;
    } else {
      orderHintModal.innerHTML = `單品總數量最高上限99<br>此商品目前總數為${
        myCart.get()[data._id].quantity
      }`;
    }
  } else {
    orderHintModal.innerHTML = '新增失敗~<br>請再確認一次訂單資訊喔~';
  }
  $('#orderHintModal').modal('show');
  document.getElementById(`input_${itemId}`).value = 1; // clear the input field value to 1
}

async function init() {
  // init lazy load pic
  const observer = lozad();
  observer.observe();
  // init cart
  myCart = await new Cart();
  /* ---- fetch menu data ----- */
  const res = await FetchData.get('/api/menu');
  const menu = await res.json();
  let totalType = 0;
  menu.forEach((type, idx) => {
    TYPE_DATA[`type${idx + 1}`] = { id: [], category: type.category };
    type.content.forEach((i) => {
      TYPE_DATA[`type${idx + 1}`].id.push(i._id);
      ID_TO_NAME[i._id] = i.name;
    });
    totalType = idx + 1;
  });

  /* -- listener for type --*/
  for (let i = 0; i < totalType; i += 1) {
    document
      .getElementById(`type${i + 1}`)
      .addEventListener('click', searchByType);
  }
  /* -- listener for search --*/
  document.getElementById('search').addEventListener('keypress', searchByName);

  /* -- listener for add item --*/
  Object.keys(ID_TO_NAME).forEach((i) => {
    document
      .getElementById(`submit_${i}`)
      .addEventListener('click', addContent);
  });
}

window.addEventListener('load', init);
