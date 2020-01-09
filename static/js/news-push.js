/* global FetchData, $ */
const NEWS_API = {
  push: '/api/setting/news',
};

async function pushNews() {
  const form = document.getElementById('push-news-form');
  const formData = new FormData(form);
  const jsonData = {};
  formData.forEach((value, key) => {
    jsonData[key] = value;
  });

  // start loading gif
  document.getElementById('loadingDiv').style.display = 'block';
  document.getElementById('loadingImg').style.display = 'block';
  // start push
  const result = await FetchData.post(NEWS_API.push, jsonData);
  if (result.status === 200) {
    $('#push-result-modal').modal('show');
    form.reset();
  }
  // end loading gif
  document.getElementById('loadingDiv').style.display = 'none';
  document.getElementById('loadingImg').style.display = 'none';
}
function init() {
  document.getElementById('push-news-form').addEventListener('submit', () => {
    pushNews();
    return false;
  });
}

window.addEventListener('load', init);
