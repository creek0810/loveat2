const APIHistory = {
  rawHistory: '/api/order/history?',
  analysisHistory: '/api/order/analysis-data?',
};

const month = new Map([
  ['Jan', '1'],['Feb', '2'],['Mar', '3'],['Apr', '4'],
  ['May', '5'],['Jun', '6'],['Jul', '7'],['Aug', '8'],
  ['Sep', '9'],['Oct', '10'],['Nov', '11'],['Dec', '12'],
]);

function updateUI(tabActive,result){
	let updateTab = document.getElementById(tabActive+"-tbody");
	let tmp = "";	
	
	result.json().then(function(data){
		console.log(data);
		switch(tabActive){
			case "history":
				for(let index in data){
					let dateTime = data[index]['createdAt'].split(" ");
					dateTime = dateTime[3] + "/" + month.get(dateTime[2]) + "/" + dateTime[1] + "<br>" + dateTime[4].split(":")[0] + ":" + dateTime[4].split(":")[1]; 
					tmp += "<tr><td>" + data[index]['orderID'] + "</td><td>" + dateTime + "</td><td>";
					data[index]['content'].forEach(element=> tmp += element['quantity'] + " * " + element['name'] + "<br>");
					tmp += "</td><td>" + data[index]['notes'] + "</td></tr>";
 				}
				break;
			case "profile":
				for (let key in data['itemAnalysis']){
					tmp += "<tr><td>" + key + "</td><td>" + data['itemAnalysis'][key]['total'] + "</td></tr>";
				}
				break;
			case "contact":
				if ((!document.getElementById("gender-check").checked) && (document.getElementById("age-check").checked)){
					// thead
					tmp = "<tr><th>品項</th>";
					data['interval'].forEach(element=> tmp += "<th>" + element + "</th>");
					tmp += "</tr>";
					document.getElementById("contact-thead").innerHTML = tmp;
					tmp = "";
					//tbody
					for (let key in data['itemAnalysis']){
						tmp += "<tr><td>" + key + "</td>";
						data['itemAnalysis'][key]['sum'].forEach(element=> tmp += "<td>" + element + "</td>");
						tmp += "</tr>";
					}
				}
				else if((document.getElementById("gender-check").checked) && (!document.getElementById("age-check").checked)){
					// thead
					document.getElementById("contact-thead").innerHTML = "<tr><th>品項</th><th align='center'>女</th><th>男</th><th>合計</th></tr>";
					//tbody
					for (let key in data['itemAnalysis']){
						tmp += "<tr><td>" + key + "</td><td>" + data['itemAnalysis'][key]['femaleTotal'] + "</td><td>" + data['itemAnalysis'][key]['maleTotal'] + "</td><td>" + data['itemAnalysis'][key]['total'] +"</tr>";
					}
				}
				else{
					// thead
					tmp = "<tr><th>品項</th><th colspan='" + data['interval'].length + "'>女</th><th colspan='" + data['interval'].length + "'>男</th></tr><tr><th>年齡</th>";
					data['interval'].forEach(element=> tmp += "<th>" + element + "</th>");
					data['interval'].forEach(element=> tmp += "<th>" + element + "</th>");
					tmp += "</tr>";
					document.getElementById("contact-thead").innerHTML = tmp;
					tmp = " ";
					//tbody
					for (let key in data['itemAnalysis']){
						tmp += "<tr><td>" + key + "</td>";
						data['itemAnalysis'][key]['female'].forEach(element=> tmp += "<td>" + element + "</td>");
						data['itemAnalysis'][key]['male'].forEach(element=> tmp += "<td>" + element + "</td>");
						tmp += "</tr>";
					}
				}
				break;
			default:
				break;
		}
		updateTab.innerHTML = tmp;
		tmp = "";
	});
}


async function getData() {
	//const tabActive = document.getElementsByClassName("show")[0].id;	
	const start = document.getElementById('start-time').value;
	const end = document.getElementById('end-time').value;
	
	const rawHistoryResult = await FetchData.get(APIHistory.rawHistory + 'start=' + start + "&end=" + end);	
    if (rawHistoryResult.status === 403){   // show wrong msg
	  console.log("raw_history權限錯誤");
    } 
	else {  
	  updateUI('history',rawHistoryResult);
    }
	
	const analysisHistoryResult = await FetchData.get(APIHistory.analysisHistory + 'start=' + start + "&end=" + end);
	if (analysisHistoryResult.status === 403){   // show wrong msg
	  console.log("analysis權限錯誤");
    } 
	else {  
	  updateUI('profile',analysisHistoryResult.clone());
	  updateUI('contact',analysisHistoryResult.clone()); 
	  drawChart(analysisHistoryResult);
    }
}

function initHistory() {
  //initial page
  getData();
  // add event listener
  document.getElementById('history-time-send').addEventListener('click', getData);
  document.getElementById('gender-check').addEventListener("change",getData);
  document.getElementById('age-check').addEventListener("change",getData);
  document.getElementById('item-analysis-btn').addEventListener("click", toggleItem);
  document.getElementById('gender-analysis-btn').addEventListener("click", toggleGender);
}


window.addEventListener('load', initHistory);

