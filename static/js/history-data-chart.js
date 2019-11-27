let tableItem = true;
let tableGender = true;

function toggleItem() {
  if(tableItem) {
    document.getElementById('item-analysis-table').classList.add("hidden");
    document.getElementById('item-analysis-chart').classList.remove("hidden");
  } else {
    document.getElementById('item-analysis-table').classList.remove("hidden");
    document.getElementById('item-analysis-chart').classList.add("hidden");
  }
  tableItem = !tableItem;
}

function toggleGender() {
  if(tableGender) {
    document.getElementById('gender-analysis-table').classList.add("hidden");
    document.getElementById('gender-analysis-chart').classList.remove("hidden");
  } else {
    document.getElementById('gender-analysis-table').classList.remove("hidden");
    document.getElementById('gender-analysis-chart').classList.add("hidden");
  }
  tableGender = !tableGender;
}

function drawChart(result){
	result.json().then(function(data){
		let item = [];
		let itemNum = [];
		let ageInterval = data['interval'];
		let femaleNum = [];
		let maleNum = [];
		let ageIntervalNum = [];
		let genderNum = [0,0];
	
		for (let key in data['itemAnalysis']){
			item.push(key);
			itemNum.push(data['itemAnalysis'][key]['total']);
		}
		for (let key in data['genderAnalysis']){
			femaleNum.push(data['genderAnalysis'][key]['female']);
			maleNum.push(data['genderAnalysis'][key]['male']);
			ageIntervalNum.push(data['genderAnalysis'][key]['total']);
		}
		
		for(let index in ageInterval){
			genderNum[0] += femaleNum[index];
			genderNum[1] += maleNum[index];
		}
		
		drawItem(item,itemNum);
		drawGender(ageInterval,femaleNum,maleNum,ageIntervalNum,genderNum);
	});
}

function drawItem(item,itemNum) {
  const barChart = document.getElementById('item-bar-chart');
  const pieChart = document.getElementById('item-pie-chart');
  let myBarChart = new Chart(barChart, {
    type: 'bar',
    data: {
      labels: item,
      datasets: [{
        label: '',
        data: itemNum,
        backgroundColor: [
          "#60acfc", "#32d3eb", "#5bc49f", "#feb64d", "#ff7c7c",
          "#9287e7", "#27A1EA", "#4EBECD", "#9CDC82", "#FF9F69",
          "#E9668E", "#747BE1", "#39B3EA", "#40CEC7", "#D4EC59",
          "#FA816D", "#D660A8", "#6370DE", "#35C5EA", "#63D5B2",
          "#FFDA43", "#FB6E6C", "#B55CBD", "#668ED6", "#9FCDFD",
		  "#FF79BC", "#FF9797", "#CA8EFF", "#019858", "#C48888",
		  "#0080FF",
        ]
      }]
    }
  });
  let myPieChart = new Chart(pieChart, {
    type: 'pie',
    data: {
      labels: item,
      datasets: [{
        label: 'Groups',
        data: itemNum,
        backgroundColor: [
          "#60acfc", "#32d3eb", "#5bc49f", "#feb64d", "#ff7c7c",
          "#9287e7", "#27A1EA", "#4EBECD", "#9CDC82", "#FF9F69",
          "#E9668E", "#747BE1", "#39B3EA", "#40CEC7", "#D4EC59",
          "#FA816D", "#D660A8", "#6370DE", "#35C5EA", "#63D5B2",
          "#FFDA43", "#FB6E6C", "#B55CBD", "#668ED6", "#9FCDFD",
		  "#FF79BC", "#FF9797", "#CA8EFF", "#019858", "#C48888",
		  "#0080FF",
        ]
      }]
    }
  });
}

function drawGender(ageInterval,femaleNum,maleNum,ageIntervalNum,genderNum) {
  const maleChart = document.getElementById('male-pie-chart');
  const femaleChart = document.getElementById('female-pie-chart');
  const genderChart = document.getElementById('gender-pie-chart');
  const ageChart = document.getElementById('age-pie-chart');
  femaleNum = [100,23,34,52,12,32,41];
  maleNum = [12,23,43,12,34,23,12];
  let myFemaleChart = new Chart(femaleChart, {
    type: 'pie',
    data: {
      labels: ageInterval,
      datasets: [{
        label: 'Groups',
        data: femaleNum,
        backgroundColor: [
          "#60acfc", "#32d3eb", "#5bc49f", "#feb64d", "#ff7c7c",
          "#9287e7", "#27A1EA", "#4EBECD", "#9CDC82", "#FF9F69",
          "#E9668E", "#747BE1", "#39B3EA", "#40CEC7", "#D4EC59",
          "#FA816D", "#D660A8", "#6370DE", "#35C5EA", "#63D5B2",
          "#FFDA43", "#FB6E6C", "#B55CBD", "#668ED6", "#9FCDFD"
        ]
      }]
    }
  });
  let myMaleChart= new Chart(maleChart, {
    type: 'pie',
    data: {
      labels: ageInterval,
      datasets: [{
        label: 'Groups',
        data: maleNum,
        backgroundColor: [
          "#60acfc", "#32d3eb", "#5bc49f", "#feb64d", "#ff7c7c",
          "#9287e7", "#27A1EA", "#4EBECD", "#9CDC82", "#FF9F69",
          "#E9668E", "#747BE1", "#39B3EA", "#40CEC7", "#D4EC59",
          "#FA816D", "#D660A8", "#6370DE", "#35C5EA", "#63D5B2",
          "#FFDA43", "#FB6E6C", "#B55CBD", "#668ED6", "#9FCDFD"
        ]
      }]
    }
  });
  let myGenderChart = new Chart(genderChart, {  //男女比
    type: 'pie',
    data: {
      labels: ["女","男"],
      datasets: [{
        label: 'Groups',
        data: genderNum,
        backgroundColor: [
          "#60acfc", "#32d3eb", "#5bc49f", "#feb64d", "#ff7c7c",
          "#9287e7", "#27A1EA", "#4EBECD", "#9CDC82", "#FF9F69",
        ]
      }]
    }
  });
  let myAgeChart = new Chart(ageChart, {  //年齡比
    type: 'pie',
    data: {
      labels: ageInterval,
      datasets: [{
        label: 'Groups',
        data: ageIntervalNum,
        backgroundColor: [
          "#60acfc", "#32d3eb", "#5bc49f", "#feb64d", "#ff7c7c",
          "#9287e7", "#27A1EA", "#4EBECD", "#9CDC82", "#FF9F69",
        ]
      }]
    }
  });
}
