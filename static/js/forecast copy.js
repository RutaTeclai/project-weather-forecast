"use strict";


function hourlyForecast(){

    // alert('hello');
    // alert($('#forecast-office').text());
    alert($('#office-id').val());
}


// $('#hourly-forecast-link').on('click', () =>{

//     // const url = $('#office-id').val();
//     const url = {lnk: 'top'}
//     $.get('/hourly-forecast.json',url, (res) =>{
//         $('#hourly-forecast').html(res);
//         alert(res)
//     });

//     // alert(url.forecast_hourly)
//     // alert($('#office-id').val());
//     // alert(url['forecast_hourly'])
// });

$('#dani').on('click', () => {
    // Our GET request URL will look like this:
    //       /status?order=123
    $.get('/ajax-view', (res) => {
      $('#ajax').html(res);
      $('#ajax').text(res);
    });
  });

// $.get('/ajax-view', (respones) => {
//     $('#ajax').text(respones);
// });


$('#hourly-forecast-link').on('click', () =>{

    // $.get('/ajax-view', (res) => {
    //     $('#ajax').text(res);
    //     alert(res);
    // });
    alert("message");

});

$.get('https://api.weather.gov/offices/top/headlines', (res) => {
  
  for (const headline of res.graph) {

    // const div = `<div ${letter}"></div>`;
    const article = `<a href="${headline.link}">${headline.title}</a>`;
    $("#article").append(article);
    alert(headline.link);
    alert(headline.title);
  }
});

// // https://api.weather.gov/offices/top/headlines


$('#office-id').on('click', () => {
    // 
    
    alert('what happened')
    // const officeId = $('#office').val();
    // // alert(officeId)
    // $.get('/news', { id: `'${officeId}'` }, (res) => {
    //   const newsPaper = [];
    //   for(const article of res.articles){
  
    //     const a = `<a href="${article.link}">${article.title}</a></br>`;
       
    //     newsPaper.push(a);
    //     $("#article-title").append(`<a href="${article.link}">${article.title}</a>`);
        
    //   }
      
    //   $('#article-title').html(newsPaper);
      
    // });
  });