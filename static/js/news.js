"use strict";

$('#office-id').on('click', () => {
    
    // const office_id = $('#dani').val();
    // alert(office_id);

    // $.get('/news', { id: `'${officeId}'` }, (res) => {
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