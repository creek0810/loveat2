/* eslint-disable no-unused-vars */
/* global Cart, $, FetchData */
/* eslint no-underscore-dangle: ["error", {"allow":["_id"]}] */

let myCart = null;

function orderTotal() {
  let total = 0;
  const dataSet = myCart.get();
  Object.keys(dataSet).forEach((key) => {
    total += dataSet[key].quantity * dataSet[key].price;
  });
  document.getElementById('total').innerHTML = total;
}

function deleteItem(e) {
  const itemId = e.target.id.substr(7);
  const key = e.target.parentNode.parentNode.rowIndex;
  myCart.delete(itemId);
  document.getElementById('cart-table').deleteRow(key);
  orderTotal();
}

function updateSum(id) {
  const order = myCart.get();
  document.getElementById(`item-sum-${id}`).innerHTML = order[id].price * order[id].quantity;
}

function changeQuantity(e) {
  let newQuantity = parseInt(e.target.value, 10);
  const id = e.target.id.substr(9);
  const originQuantity = myCart.get()[id].quantity;

  if (newQuantity <= 0 || newQuantity > 99 || Number.isNaN(newQuantity)) {
    document.getElementById('hint-content').innerHTML = '輸入錯誤';
    document.getElementById('bussiness_data').style.display = 'none';
    $('#order-send-hint-modal').modal('show');
    newQuantity = originQuantity;
    e.target.value = newQuantity;
  }

  myCart.updateQuantity(id, newQuantity);
  updateSum(id);
  orderTotal();
}

function orderDescription() {
  const description = [];
  const dataSet = myCart.get();
  Object.keys(dataSet).forEach((key) => {
    const text = dataSet[key].description;
    if (text !== '') {
      description.push(`${dataSet[key].name}: ${text}`);
    }
  });
  return description.join(';');
}

function orderContent() {
  const dataSet = myCart.get();
  const postOrder = Object.keys(dataSet).reduce((acc, key) => {
    acc.push({
      id: key,
      category: dataSet[key].category,
      quantity: dataSet[key].quantity,
    });
    return acc;
  }, []);
  return postOrder;
}

function clearOrder() {
  myCart.clear();
  document.getElementById('item-table').innerHTML = '';
  document.getElementById('total').innerHTML = 0;
}

function toState() {
  window.location = '/order/state';
}

function checkStatus(status) {
  const order = myCart.get();
  if (status === 200) {
    document.getElementById('close-modal').addEventListener('click', toState);
    document.getElementById('hint-content').innerHTML = '下單成功';
    document.getElementById('bussiness_data').style.display = 'none';
    clearOrder();
  } else if (status === 401) {
    document.getElementById('hint-content').innerHTML = '您尚未登入';
    document.getElementById('bussiness_data').style.display = 'none';
  } else if (status === 403) {
    document.getElementById('hint-content').innerHTML = '您的帳號已被凍結，無法下單';
  } else {
    document.getElementById('hint-content').innerHTML = '訂單錯誤或預定取餐時間未營業';
  }
  $('#order-send-hint-modal').modal('show');
}

async function sendOrder() {
  const detailTime = $('#order-take-time')
    .data('DateTimePicker')
    .date();
  const takenTime = detailTime.format('YYYY-MM-DDTHH:mm');
  if (takenTime === null || Date.parse(takenTime).valueOf() < Date.now()) {
    document.getElementById('hint-content').innerHTML = '訂單錯誤或預定取餐時間未營業';
    $('#order-send-hint-modal').modal('show');
  } else {
    const total = document.getElementById('total').innerHTML;
    const order = {
      takenAt: takenTime,
      notes: orderDescription(),
      total: parseInt(total, 10),
      content: orderContent(),
    };
    const response = await FetchData.post('/api/order/new', order);
    checkStatus(response.status);
  }
}

function setDiscription(e) {
  const description = e.target.value;
  const data = myCart.get();
  const desId = e.target.id.substr(12);
  if (desId in data) {
    data[desId].description = description;
  }
  myCart.updateLocalStorage();
}

function drawItem(data) {
  const result = Object.keys(data).reduce(
    (acc, key) => `${acc} <tr id="${key}">
              <td data-th="名稱 : ">${data[key].name}</td>
              <td data-th="數量 : ">
                <input type="number" id="quantity-${key}" min="1" value="${
  data[key].quantity
}" class="quantity-input form-control">
              </td>
              <td data-th="價格 : ">${data[key].price}</td>
              <td data-th="備註 : ">
                <input id="description-${key}" class="form-control description-input" type="text" value="${
  data[key].description
}">
              </td>
              <td data-th="總共 : " id="item-sum-${key}" >${data[key].price
      * data[key].quantity}</td>
              <td>
                <button id="delete-${key}" class="btn btn-primary delete-item" type="button">Delete</button>
              </td>
            </tr>`,
    '',
  );
  // draw it
  document.querySelector('#cart-table tbody').innerHTML = result;
  // add event listener
  const quantityInput = document.getElementsByClassName('quantity-input');
  [...quantityInput].forEach((cur) => {
    cur.addEventListener('change', changeQuantity);
  });

  const deleteBtn = document.getElementsByClassName('delete-item');
  [...deleteBtn].forEach((cur) => {
    cur.addEventListener('click', deleteItem);
  });

  const descriptionTxt = document.getElementsByClassName('description-input');
  [...descriptionTxt].forEach((cur) => {
    cur.addEventListener('change', setDiscription);
  });
}

async function init() {
  myCart = await new Cart();
  orderTotal();
  drawItem(myCart.get());
  document.getElementById('clear-order').addEventListener('click', clearOrder);
  document.getElementById('send-order').addEventListener('click', sendOrder);
  $('#order-take-time').datetimepicker({
    showTodayButton: true,
    format: 'YYYY/M/D H:mm',
    dayViewHeaderFormat: 'YYYY/M/D H:mm',
  });
}

window.addEventListener('load', init);
