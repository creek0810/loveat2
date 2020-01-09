/* global FetchData, HistoryChart */
const APIHistory = {
  rawHistory: '/api/order/history?',
  analysisHistory: '/api/order/analysis-data?',
};

const month = new Map([
  ['Jan', '1'],
  ['Feb', '2'],
  ['Mar', '3'],
  ['Apr', '4'],
  ['May', '5'],
  ['Jun', '6'],
  ['Jul', '7'],
  ['Aug', '8'],
  ['Sep', '9'],
  ['Oct', '10'],
  ['Nov', '11'],
  ['Dec', '12'],
]);

let result = '';
let chart = '';
let tableItem = true;
let tableGender = true;

function toggleItem() {
  if (tableItem) {
    document.getElementById('item-analysis-btn').innerHTML = '切換詳細資料';
    document.getElementById('item-analysis-table').classList.add('hidden');
    document.getElementById('item-analysis-chart').classList.remove('hidden');
  } else {
    document.getElementById('item-analysis-btn').innerHTML = '切換圖表';
    document.getElementById('item-analysis-table').classList.remove('hidden');
    document.getElementById('item-analysis-chart').classList.add('hidden');
  }
  tableItem = !tableItem;
}

function toggleGender() {
  if (tableGender) {
    document.getElementById('gender-analysis-btn').innerHTML = '切換詳細資料';
    document.getElementById('gender-analysis-table').classList.add('hidden');
    document.getElementById('gender-analysis-chart').classList.remove('hidden');
  } else {
    document.getElementById('gender-analysis-btn').innerHTML = '切換圖表';
    document.getElementById('gender-analysis-table').classList.remove('hidden');
    document.getElementById('gender-analysis-chart').classList.add('hidden');
  }
  tableGender = !tableGender;
}

function updateHistoryUI() {
  let tmpBody = '';

  result.forEach((element) => {
    let dateTime = element.createdAt.split(' ');
    dateTime = `${dateTime[3]}/${month.get(dateTime[2])}/${dateTime[1]}<br>${
      dateTime[4].split(':')[0]
    }:${dateTime[4].split(':')[1]}`;
    tmpBody += `<tr><td>${element.orderID}</td><td>${dateTime}</td><td>`;
    element.content.forEach((ele) => {
      tmpBody += `${ele.quantity} * ${ele.name}<br>`;
    });
    tmpBody += `</td><td>${element.notes}</td></tr>`;
  });

  document.getElementById('history-tbody').innerHTML = tmpBody;
}

function updateProfileUI() {
  let tmpBody = '';

  Object.entries(result.itemAnalysis).forEach((element) => {
    tmpBody += `<tr><td>${element[0]}</td><td>${element[1].total}</td></tr>`;
  });
  document.getElementById('profile-tbody').innerHTML = tmpBody;
}

function updateContactUI() {
  let tmpHead = '';
  let tmpBody = '';
  const gender = document.getElementById('gender-check').checked;
  const age = document.getElementById('age-check').checked;

  if (!gender && age) {
    // thead
    tmpHead = '<tr><th>品項</th>';
    result.interval.forEach((element) => {
      tmpHead += `<th>${element}</th>`;
    });
    tmpHead += '</tr>';
    // tbody
    Object.entries(result.itemAnalysis).forEach((element) => {
      tmpBody += `<tr><td>${element[0]}</td>`;
      element[1].sum.forEach((ele) => {
        tmpBody += `<td>${ele}</td>`;
      });
      tmpBody += '</tr>';
    });
  } else if (gender && !age) {
    // thead
    tmpHead = '<tr><th>品項</th><th>女</th><th>男</th><th>合計</th></tr>';
    // tbody
    Object.entries(result.itemAnalysis).forEach((element) => {
      tmpBody += `<tr><td>${element[0]}</td><td>${element[1].femaleTotal}</td><td>${element[1].maleTotal}</td><td>${element[1].total}</tr>`;
    });
  } else {
    // thead
    tmpHead = `<tr><th>品項</th><th colspan="${result.interval.length}">女</th><th colspan="${result.interval.length}">男</th></tr><tr><th>年齡</th>`;
    result.interval.forEach((element) => {
      tmpHead += `<th>${element}</th>`;
    });
    result.interval.forEach((element) => {
      tmpHead += `<th>${element}</th>`;
    });
    tmpHead += '</tr>';
    // tbody
    Object.entries(result.itemAnalysis).forEach((element) => {
      tmpBody += `<tr><td>${element[0]}</td>`;
      element[1].female.forEach((ele) => {
        tmpBody += `<td>${ele}</td>`;
      });
      element[1].male.forEach((ele) => {
        tmpBody += `<td>${ele}</td>`;
      });
      tmpBody += '</tr>';
    });
  }
  tmpBody = tmpBody.replace(/<td>0/g, '<td>-');
  document.getElementById('contact-thead').innerHTML = tmpHead;
  document.getElementById('contact-tbody').innerHTML = tmpBody;
}

async function getData() {
  const start = document.getElementById('start-time').value;
  const end = document.getElementById('end-time').value;

  const rawHistoryResult = await FetchData.get(
    `${APIHistory.rawHistory}start=${start}&end=${end}`,
  );
  result = await rawHistoryResult.json();
  if (rawHistoryResult.status === 403) {
    // show wrong msg
    console.log('raw_history權限錯誤');
  } else {
    updateHistoryUI();
  }

  const analysisHistoryResult = await FetchData.get(
    `${APIHistory.analysisHistory}start=${start}&end=${end}`,
  );
  result = await analysisHistoryResult.json();
  if (analysisHistoryResult.status === 403) {
    // show wrong msg
    console.log('analysis權限錯誤');
  } else {
    updateProfileUI();
    updateContactUI();
    chart.updateChart(result);
  }
}

function initHistory() {
  // init all chart
  chart = new HistoryChart();
  // initial page
  getData();
  // add event listener
  document
    .getElementById('history-time-send')
    .addEventListener('click', getData);
  document
    .getElementById('gender-check')
    .addEventListener('change', updateContactUI);
  document
    .getElementById('age-check')
    .addEventListener('change', updateContactUI);
  document
    .getElementById('item-analysis-btn')
    .addEventListener('click', toggleItem);
  document
    .getElementById('gender-analysis-btn')
    .addEventListener('click', toggleGender);
}

window.addEventListener('load', initHistory);
