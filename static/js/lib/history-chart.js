/* global Chart */

// eslint-disable-next-line no-unused-vars
class HistoryChart {
  constructor() {
    // init color
    this.pieChartBG = [
      '#60acfc',
      '#32d3eb',
      '#5bc49f',
      '#feb64d',
      '#ff7c7c',
      '#9287e7',
      '#27A1EA',
      '#4EBECD',
      '#9CDC82',
      '#FF9F69',
    ];
    this.barChartBG = [
      '#60acfc',
      '#32d3eb',
      '#5bc49f',
      '#feb64d',
      '#ff7c7c',
      '#9287e7',
      '#27A1EA',
      '#4EBECD',
      '#9CDC82',
      '#FF9F69',
      '#E9668E',
      '#747BE1',
      '#39B3EA',
      '#40CEC7',
      '#D4EC59',
      '#FA816D',
      '#D660A8',
      '#6370DE',
      '#35C5EA',
      '#63D5B2',
      '#FFDA43',
      '#FB6E6C',
      '#B55CBD',
      '#668ED6',
      '#9FCDFD',
      '#FF79BC',
      '#FF9797',
      '#CA8EFF',
      '#019858',
      '#C48888',
      '#0080FF',
    ];

    // init all chart
    this.allChart = [];

    // init item bar chart
    const barChart = document.getElementById('item-bar-chart');
    this.allChart.itemBar = this.createBarChart(barChart, '各餐點銷售數量');

    // init gender chart
    const maleChart = document.getElementById('male-pie-chart');
    const femaleChart = document.getElementById('female-pie-chart');
    const genderChart = document.getElementById('gender-pie-chart');
    const ageChart = document.getElementById('age-pie-chart');

    this.allChart.femalePie = this.createPieChart(
      femaleChart,
      '女性各年齡銷售數量',
    );
    this.allChart.malePie = this.createPieChart(
      maleChart,
      '男性各年齡銷售數量',
    );
    this.allChart.genderPie = this.createPieChart(
      genderChart,
      '男女各銷售數量',
      ['女', '男'],
    );
    this.allChart.agePie = this.createPieChart(ageChart, '各年齡層銷售數量');
  }

  updateChart(data) {
    // preprocess to format data
    const itemData = data.itemAnalysis;
    const item = Object.keys(itemData);
    const ageInterval = data.interval;
    const itemNum = Object.values(data.itemAnalysis).map(
      (element) => element.total,
    );
    const femaleNum = Object.values(data.genderAnalysis).map(
      (element) => element.female,
    );
    const maleNum = Object.values(data.genderAnalysis).map(
      (element) => element.male,
    );
    const ageIntervalNum = Object.values(data.genderAnalysis).map(
      (element) => element.total,
    );
    const genderNum = [
      femaleNum.reduce((a, b) => a + b),
      maleNum.reduce((a, b) => a + b),
    ];

    // update female pie
    this.allChart.femalePie.data.labels = ageInterval;
    this.allChart.femalePie.data.datasets[0].data = femaleNum;
    // update male pie
    this.allChart.malePie.data.labels = ageInterval;
    this.allChart.malePie.data.datasets[0].data = maleNum;
    // update gender pie
    this.allChart.genderPie.data.datasets[0].data = genderNum;
    // update age pie
    this.allChart.agePie.data.labels = ageInterval;
    this.allChart.agePie.data.datasets[0].data = ageIntervalNum;
    // update item bar
    this.allChart.itemBar.data.labels = item;
    this.allChart.itemBar.data.datasets[0].data = itemNum;

    // redraw chart
    Object.keys(this.allChart).forEach((key) => {
      this.allChart[key].update();
    });
  }

  createPieChart(ctx, text, labels = []) {
    return new Chart(ctx, {
      type: 'pie',
      data: {
        labels,
        datasets: [
          {
            label: 'Groups',
            backgroundColor: this.pieChartBG,
          },
        ],
      },
      options: {
        title: {
          display: true,
          text,
        },
        legend: {
          labels: {
            fontSize: 0,
          },
        },
      },
    });
  }

  createBarChart(ctx, dataSetLabel) {
    return new Chart(ctx, {
      type: 'bar',
      data: {
        datasets: [
          {
            label: dataSetLabel,
            backgroundColor: this.barChartBG,
          },
        ],
      },
      options: {
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
              },
            },
          ],
        },
      },
    });
  }
}
