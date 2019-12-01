/* global FetchData, drawChart */
const APIHistory = {
  rawHistory: '/api/order/history?',
  analysisHistory: '/api/order/analysis-data?',
};

const month = new Map([
  ['Jan', '1'], ['Feb', '2'], ['Mar', '3'], ['Apr', '4'],
  ['May', '5'], ['Jun', '6'], ['Jul', '7'], ['Aug', '8'],
  ['Sep', '9'], ['Oct', '10'], ['Nov', '11'], ['Dec', '12'],
]);

async function updateUI(tabActive, result) {
  const data = await result.json();
  let tmpBody = '';
  let tmpHead = '';

  switch (tabActive) {
    case 'history':
      data.forEach((element) => {
        let dateTime = element.createdAt.split(' ');
        dateTime = `${dateTime[3]}/${month.get(dateTime[2])}/${dateTime[1]}<br>${dateTime[4].split(':')[0]}:${dateTime[4].split(':')[1]}`;
        tmpBody += `<tr><td>${element.orderID}</td><td>${dateTime}</td><td>`;
        element.content.forEach((ele) => {
          tmpBody += `${ele.quantity} * ${ele.name}<br>`;
        });
        tmpBody += `</td><td>${element.notes}</td></tr>`;
      });
      break;
    case 'profile':
      Object.entries(data.itemAnalysis).forEach((element) => {
        tmpBody += `<tr><td>${element[0]}</td><td>${element[1].total}</td></tr>`;
      });
      break;
    case 'contact':
      if ((!document.getElementById('gender-check').checked) && (document.getElementById('age-check').checked)) {
        // thead
        tmpHead = '<tr><th>品項</th>';
        data.interval.forEach((element) => {
          tmpHead += `<th>${element}</th>`;
        });
        tmpHead += '</tr>';
        // tbody
        Object.entries(data.itemAnalysis).forEach((element) => {
          tmpBody += `<tr><td>${element[0]}</td>`;
          element[1].sum.forEach((ele) => {
            tmpBody += `<td>${ele}</td>`;
          });
          tmpBody += '</tr>';
        });
      } else if ((document.getElementById('gender-check').checked) && (!document.getElementById('age-check').checked)) {
        // thead
        document.getElementById('contact-thead').innerHTML = '<tr><th>品項</th><th align="center">女</th><th>男</th><th>合計</th></tr>';
        // tbody
        Object.entries(data.itemAnalysis).forEach((element) => {
          tmpBody += `<tr><td>${element[0]}</td><td>${element[1].femaleTotal}</td><td>${element[1].maleTotal}</td><td>${element[1].total}</tr>`;
        });
      } else {
        // thead
        tmpHead = `<tr><th>品項</th><th colspan="${data.interval.length}">女</th><th colspan="${data.interval.length}">男</th></tr><tr><th>年齡</th>`;
        data.interval.forEach((element) => {
          tmpHead += `<th>${element}</th>`;
        });
        data.interval.forEach((element) => {
          tmpHead += `<th>${element}</th>`;
        });
        tmpHead += '</tr>';
        // tbody
        Object.entries(data.itemAnalysis).forEach((element) => {
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
      document.getElementById('contact-thead').innerHTML = tmpHead;
      tmpHead = '';
      break;
    default:
      break;
  }
  document.getElementById(`${tabActive}-tbody`).innerHTML = tmpBody;
  tmpBody = '';
}


async function getData() {
  // const tabActive = document.getElementsByClassName('show')[0].id;
  const start = document.getElementById('start-time').value;
  const end = document.getElementById('end-time').value;

  const rawHistoryResult = await FetchData.get(`${APIHistory.rawHistory}start=${start}&end=${end}`);
  if (rawHistoryResult.status === 403) { // show wrong msg
    console.log('raw_history權限錯誤');
  } else {
    updateUI('history', rawHistoryResult);
  }

  const analysisHistoryResult = await FetchData.get(`${APIHistory.analysisHistory}start=${start}&end=${end}`);
  if (analysisHistoryResult.status === 403) { // show wrong msg
    console.log('analysis權限錯誤');
  } else {
    updateUI('profile', analysisHistoryResult.clone());
    updateUI('contact', analysisHistoryResult.clone());
    drawChart(analysisHistoryResult);
  }
}
function initHistory() {
  // initial page
  getData();
  // add event listener
  document.getElementById('history-time-send').addEventListener('click', getData);
  document.getElementById('gender-check').addEventListener('change', getData);
  document.getElementById('age-check').addEventListener('change', getData);
}


window.addEventListener('load', initHistory);
