"use strict";

$('#office-id').on('click', () => {

  alert($('#office').val());

  $.get('/news', { id: 'Mpx' }, (res) => {
    const newsPaper = [];
    for(const article of res.articles){
  
      const a = `<a href="${article.link}">${article.title}</a></br>`;
     
      newsPaper.push(a);
    //   $("#article-title").append(`<a href="${article.link}">${article.title}</a>`);
      
    }
    
    $('#article-title').html(newsPaper);
    
  });

  

});

// $.get('/ajax-view', (respones) => {
//       $('#ajax').text(respones);
//   // });

  // $.get('/news', { id: 'Mpx' }, (res) => {
  //   const newsPaper = [];
  //   for(const article of res.articles){
  
  //     const a = `<a href="${article.link}">${article.title}</a></br>`;
     
  //     newsPaper.push(a);
  //   //   $("#article-title").append(`<a href="${article.link}">${article.title}</a>`);
      
  //   }
    
  //   $('#article-title').html(newsPaper);
  //   // $('#ajax').text(newsPaper);
  //   $('#article').html(newsPaper);
    
  // });

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

    $.get('/hourly-forecast', { id: 'Mpx' }, (res) => {
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

$('#news-button').on('click',() => {

  $.get('/news', { id: 'Mpx' }, (res) => {
    const newsPaper = [];
    for(const article of res.articles){
  
      const a = `<a href="${article.link}">${article.title}</a></br>`;
     
      newsPaper.push(a);
    }
  
    $('#article').html(newsPaper);
  });
  
  

});






