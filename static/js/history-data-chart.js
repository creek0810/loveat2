/* global Chart */
let tableItem = true;
let tableGender = true;

function toggleItem() {
  if (tableItem) {
    document.getElementById('item-analysis-table').classList.add('hidden');
    document.getElementById('item-analysis-chart').classList.remove('hidden');
  } else {
    document.getElementById('item-analysis-table').classList.remove('hidden');
    document.getElementById('item-analysis-chart').classList.add('hidden');
  }
  tableItem = !tableItem;
}

function toggleGender() {
  if (tableGender) {
    document.getElementById('gender-analysis-table').classList.add('hidden');
    document.getElementById('gender-analysis-chart').classList.remove('hidden');
  } else {
    document.getElementById('gender-analysis-table').classList.remove('hidden');
    document.getElementById('gender-analysis-chart').classList.add('hidden');
  }
  tableGender = !tableGender;
}

function drawItem(item, itemNum) {
  const barChart = document.getElementById('item-bar-chart');
  const pieChart = document.getElementById('item-pie-chart');

  // eslint-disable-next-line no-unused-vars
  const myItemBar = new Chart(barChart, {
    type: 'bar',
    data: {
      labels: item,
      datasets: [{
        label: '各餐點銷售數量',
        data: itemNum,
        backgroundColor: [
          '#60acfc', '#32d3eb', '#5bc49f', '#feb64d', '#ff7c7c',
          '#9287e7', '#27A1EA', '#4EBECD', '#9CDC82', '#FF9F69',
          '#E9668E', '#747BE1', '#39B3EA', '#40CEC7', '#D4EC59',
          '#FA816D', '#D660A8', '#6370DE', '#35C5EA', '#63D5B2',
          '#FFDA43', '#FB6E6C', '#B55CBD', '#668ED6', '#9FCDFD',
          '#FF79BC', '#FF9797', '#CA8EFF', '#019858', '#C48888',
          '#0080FF',
        ],
      }],
    },
  });
  // eslint-disable-next-line no-unused-vars
  const myItemPie = new Chart(pieChart, {
    type: 'pie',
    data: {
      labels: item,
      datasets: [{
        label: 'Groups',
        data: itemNum,
        backgroundColor: [
          '#60acfc', '#32d3eb', '#5bc49f', '#feb64d', '#ff7c7c',
          '#9287e7', '#27A1EA', '#4EBECD', '#9CDC82', '#FF9F69',
          '#E9668E', '#747BE1', '#39B3EA', '#40CEC7', '#D4EC59',
          '#FA816D', '#D660A8', '#6370DE', '#35C5EA', '#63D5B2',
          '#FFDA43', '#FB6E6C', '#B55CBD', '#668ED6', '#9FCDFD',
          '#FF79BC', '#FF9797', '#CA8EFF', '#019858', '#C48888',
          '#0080FF',
        ],
      }],
    },
    options: {
      title: {
        display: true,
        text: '各餐點銷售數量',
      },
    },
  });
}

function drawGender(ageInterval, femaleNum, maleNum, ageIntervalNum, genderNum) {
  const maleChart = document.getElementById('male-pie-chart');
  const femaleChart = document.getElementById('female-pie-chart');
  const genderChart = document.getElementById('gender-pie-chart');
  const ageChart = document.getElementById('age-pie-chart');

  // eslint-disable-next-line no-unused-vars
  const myFemaleChart = new Chart(femaleChart, {
    type: 'pie',
    data: {
      labels: ageInterval,
      datasets: [{
        label: 'Groups',
        data: femaleNum,
        backgroundColor: [
          '#60acfc', '#32d3eb', '#5bc49f', '#feb64d', '#ff7c7c',
          '#9287e7', '#27A1EA', '#4EBECD', '#9CDC82', '#FF9F69',
          '#E9668E', '#747BE1', '#39B3EA', '#40CEC7', '#D4EC59',
          '#FA816D', '#D660A8', '#6370DE', '#35C5EA', '#63D5B2',
          '#FFDA43', '#FB6E6C', '#B55CBD', '#668ED6', '#9FCDFD',
        ],
      }],
    },
    options: {
      title: {
        display: true,
        text: '女性各年齡銷售數量',
      },
    },
  });
  // eslint-disable-next-line no-unused-vars
  const myMaleChart = new Chart(maleChart, {
    type: 'pie',
    data: {
      labels: ageInterval,
      datasets: [{
        label: 'Groups',
        data: maleNum,
        backgroundColor: [
          '#60acfc', '#32d3eb', '#5bc49f', '#feb64d', '#ff7c7c',
          '#9287e7', '#27A1EA', '#4EBECD', '#9CDC82', '#FF9F69',
          '#E9668E', '#747BE1', '#39B3EA', '#40CEC7', '#D4EC59',
          '#FA816D', '#D660A8', '#6370DE', '#35C5EA', '#63D5B2',
          '#FFDA43', '#FB6E6C', '#B55CBD', '#668ED6', '#9FCDFD',
        ],
      }],
    },
    options: {
      title: {
        display: true,
        text: '男性各年齡銷售數量',
      },
    },
  });
  // eslint-disable-next-line no-unused-vars
  const myGenderChart = new Chart(genderChart, { // 男女比
    type: 'pie',
    data: {
      labels: ['女', '男'],
      datasets: [{
        label: 'Groups',
        data: genderNum,
        backgroundColor: [
          '#60acfc', '#32d3eb', '#5bc49f', '#feb64d', '#ff7c7c',
          '#9287e7', '#27A1EA', '#4EBECD', '#9CDC82', '#FF9F69',
        ],
      }],
    },
    options: {
      title: {
        display: true,
        text: '男女各銷售數量',
      },
    },
  });
  // eslint-disable-next-line no-unused-vars
  const myAgeChart = new Chart(ageChart, { // 年齡比
    type: 'pie',
    data: {
      labels: ageInterval,
      datasets: [{
        label: 'Groups',
        data: ageIntervalNum,
        backgroundColor: [
          '#60acfc', '#32d3eb', '#5bc49f', '#feb64d', '#ff7c7c',
          '#9287e7', '#27A1EA', '#4EBECD', '#9CDC82', '#FF9F69',
        ],
      }],
    },
    options: {
      title: {
        display: true,
        text: '各年齡層銷售數量',
      },
    },
  });
}

// eslint-disable-next-line no-unused-vars
async function drawChart(res) {
  const data = await res.json();
  const itemData = data.itemAnalysis;
  const item = Object.keys(itemData);
  const ageInterval = data.interval;
  const itemNum = [];
  const femaleNum = [];
  const maleNum = [];
  const ageIntervalNum = [];
  const genderNum = [0, 0];

  Object.values(data.itemAnalysis).forEach((element) => {
    itemNum.push(element.total);
  });
  Object.values(data.genderAnalysis).forEach((element) => {
    femaleNum.push(element.female);
    genderNum[0] += element.female;
    maleNum.push(element.male);
    genderNum[1] += element.male;
    ageIntervalNum.push(element.total);
  });
  drawItem(item, itemNum);
  drawGender(ageInterval, femaleNum, maleNum, ageIntervalNum, genderNum);
}

function initChart() {
  document.getElementById('item-analysis-btn').addEventListener('click', toggleItem);
  document.getElementById('gender-analysis-btn').addEventListener('click', toggleGender);
}

window.addEventListener('load', initChart);
