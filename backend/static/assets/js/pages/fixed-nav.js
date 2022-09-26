
const content = document.querySelector('.pcoded-content');


function scriptQuery(){
    var script = document.getElementsByTagName('script');


    script = script[script.length-1].src
    .replace(/^[^\?]+\?/, '')
    .replace(/#.+$/, '')
    .split('&');
    
    var queries = {} , query;
    
    while(script.length){
        query = script.shift().split('=');
        console.log(query);

        queries[query[0]] = query[1];
    }
    
    return queries;
}

const params = scriptQuery();
if (params.gender){
    console.log(params.gender.split('%').length)
    console.log(params.mfee)
    console.log(params.age)
    console.log(params.alpha)
    console.log(params.recommendation_section)
}




const nav = document.querySelector('.pcoded-content'); // 네비게이션 바
const filterBar = document.querySelector('#filter-bar'); // 네비게이션 바
// const grid = document.querySelector('.list-grid');
const grids = document.getElementsByClassName("list-grid")

const navTop = nav.offsetTop;


function fixNav() {

// console.log('grid 목록 :: ', window.scrollY)
if (window.scrollY >= 21) {
  filterBar.classList.add('fixed-nav');
  nav.style.cssText  = 'padding-top: 0px;';

  for (var i = 0; i < grids.length; i++){

    grids[i].style.cssText = "padding-top: 190px; ";

  }
} else {
  filterBar.classList.remove('fixed-nav');
  nav.style.cssText  = 'padding-top: 15px;';


  for (var i = 0; i < grids.length; i++){

    grids[i].style.cssText = "padding-top: 0px;";

  }
}
}

window.addEventListener('scroll', fixNav);


