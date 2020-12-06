"use strict";


$('#local-office').on('click', () =>{

  const api_url = 'https://www.weather.gov/';
  const officeId = $('#office-id').val();
  
  window.open(`${api_url}${officeId}`)
  

});



  
  

  // $.get('/hourly-forecast', { id: 'Mpx' }, (res) => {
  //   const hourlyForecast = [];
  //   for(const forecast of res.forecasts){

  //     // alert(forecast.time);
  
  //     const a = `<a href="${forecast.time}">${forecast.temp}</a></br>`;
     
  //     hourlyForecast.push(a);
  //   //   $("#article-title").append(`<a href="${article.link}">${article.title}</a>`);
      
  //   }
    
    
  //   $('#table-forecast').html(hourlyForecast);
    
  // });

  $('#forecast-hourly').on('click', () => {


    const url = $('#hourly-forecast-url').val()
    alert("Scroll Down to See Hourly Forecast Chart")
    $.get('/hourly-forecast', { url: `${url}` }, (res) => {
      const data = [];
      for (const forecast of res.forecasts) {
        data.push({x: forecast.time, y: forecast.temp});
      }
    
      new Chart(
        $('#forecast-chart'),
        {
          type: 'line',
          data: {
            datasets: [
              {
                label: 'Hourly Forecast',
                data: data
              }
            ]
          },
          options: {
            scales: {
              xAxes: [
                {
                  type: 'time',
                  distribution: 'series'
                }
              ]
            }
          }
        }
      );
    });

  });
  

  // $.get('/hourly-forecast', { id: 'Mpx' }, (res) => {
  //   const data = [];
  //   for (const forecast of res.forecasts) {
  //     data.push({x: forecast.time, y: forecast.temp});
  //   }
  
  //   new Chart(
  //     $('#forecast-chart'),
  //     {
  //       type: 'line',
  //       data: {
  //         datasets: [
  //           {
  //             label: 'Hourly Forecast',
  //             data: data
  //           }
  //         ]
  //       },
  //       options: {
  //         scales: {
  //           xAxes: [
  //             {
  //               type: 'time',
  //               distribution: 'series'
  //             }
  //           ]
  //         }
  //       }
  //     }
  //   );
  // });
  
  

$('#news').on('click',() => {

 
  // evt.preventDefault();
  const officeId = $('#office-id').val();
  
  $.get('/news', { id: `${officeId}` }, (res) => {
    const newsPaper = [];
    for(const article of res.articles){
  
      const a = `<a href="${article.link}" target="_blank">${article.title}</a></br>`;
     
      newsPaper.push(a);
    }
  
    $('#article').html(newsPaper);
  });
  
  

});






