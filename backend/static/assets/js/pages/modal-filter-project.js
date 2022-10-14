const modal = document.querySelector(".modal-dialog");
const modalopen = document.querySelector("#modal-filter");
const modalclose = document.querySelector("#modal-close");
const content = document.querySelector('.pcoded-content');



// 셀럽모델료 범위선택 변수
// const textLeft_cfee = document.getElementById("min_left_cfee");
// const textRight_cfee = document.getElementById("max_right_cfee");
const inputLeft = document.getElementById("input-left_pryear");
const inputRight = document.getElementById("input-right_pryear");
const thumbLeft = document.querySelector(".slider > .thumb_cfee.left_cfee");
const thumbRight = document.querySelector(".slider > .thumb_cfee.right_cfee");
const range = document.querySelector(".slider > .range_cfee");
const inputYear = document.getElementById("pryear");

const nav = document.querySelector('.pcoded-content'); // 네비게이션 바
const filterBar = document.querySelector('#filter-bar'); // 네비게이션 바
const grids = document.getElementsByClassName("list-grid")
const navTop = nav.offsetTop;

const selectTeam = document.getElementById("select_team");
const inputTeam = document.getElementById("team");


function fixNav() {

// console.log('grid 목록 :: ', grids)
if (window.scrollY >= 21) {
  filterBar.classList.add('fixed-nav');
  nav.style.cssText  = 'padding-top: 0px;';

  for (var i = 0; i < grids.length; i++){

    grids[i].style.cssText = "padding-top: 165px;";

  }
} else {
  filterBar.classList.remove('fixed-nav');
  nav.style.cssText  = 'padding-top: 15px;';


  for (var i = 0; i < grids.length; i++){

    grids[i].style.cssText = "padding-top: 0px;";

  }
}
}


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



// 모달창 열고 닫음
function clickmodal(event){


    if (event.cancelable) event.preventDefault();
    event.preventDefault(); //페이지 새로고침 중지
    

    /////////////////////////////////////////////////
    //////// 모달창 open 전에 이전 데이터 불러옴. ///////////

    // 모달창 close
    if(!modal.classList.contains('inactive')){
        modal.classList.add("inactive");

        content.style.cssText  = 'overflow: auto; padding-top:0px;';
        
    }
    // 모달창 open
    else{

        // getChkRecSectionValue();
        content.style.cssText  = 'overflow: hidden; padding-top:0px;';
        modal.classList.remove("inactive");

    }
  }


/////////////////////////////?
// 모달창 -> 취소버튼
function closemodal(event){
  if (event.cancelable) event.preventDefault();
  event.preventDefault(); //페이지 새로고침 중지
  modal.classList.add("inactive");
}// 취소버튼 클릭이벤트 시 inactive 클래스 추가






// // 셀럽 모델료 
// function setLeftValue_() {

//   const _this = inputLeft;
//   const [min, max] = [parseFloat(_this.min), parseFloat(_this.max)];
  
  
//   const percent = ((_this.value - min) / (max - min)) * 100;
//   thumbLeft.style.left = percent + "%";
//   range.style.left = percent + "%";


//   console.log(_this.value)

// };





// 셀럽 모델료 
function setLeftValue_() {
  const _this = inputLeft;
  const [min, max] = [parseFloat(_this.min), parseFloat(_this.max)];
  
  
  // 교차되지 않게, 1을 빼준 건 완전히 겹치기보다는 어느 정도 간격을 남겨두기 위해.
  _this.value = Math.min(parseFloat(_this.value), parseFloat(inputRight.value) - 0.5);
  
  // input, thumb 같이 움직이도록
  const percent = ((_this.value - min) / (max - min)) * 100;
  thumbLeft.style.left = percent + "%";
  range.style.left = percent + "%";


  let x = document.getElementsByClassName("min_value_pryear")[0];
  
  x.innerText= String(_this.value + ' ~ ');
  inputYear.value = _this.value + "%" + inputRight.value;

};

function setRightValue_() {
  const _this = inputRight;
  const [min, max] = [parseFloat(_this.min), parseFloat(_this.max)];
  
  
  
  // 교차되지 않게, 1을 더해준 건 완전히 겹치기보다는 어느 정도 간격을 남겨두기 위해.
  _this.value = Math.max(parseFloat(_this.value), parseFloat(inputLeft.value) + 0.5);
  
  // input, thumb 같이 움직이도록
  const percent = ((_this.value - min) / (max - min)) * 100;
  thumbRight.style.right = 100 - percent + "%";
  range.style.right = 100 - percent + "%";

  let x = document.getElementsByClassName("max_value_pryear")[0];
  
  x.innerText = String(_this.value);
  inputYear.value = inputLeft.value + "%" + _this.value;


};


function setTeam() {

  console.log(selectTeam.value);
  inputTeam.value = selectTeam.value;

}


modalopen.addEventListener("click", clickmodal);
modalclose.addEventListener("click", closemodal);


window.addEventListener('scroll', fixNav);

inputLeft.addEventListener("input", setLeftValue_);
inputRight.addEventListener("input", setRightValue_);
selectTeam.addEventListener("change", setTeam)