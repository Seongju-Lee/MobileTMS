const modal = document.querySelector(".modal-dialog");
const modalopen = document.querySelector("#modal-filter");
const modalclose = document.querySelector("#modal-close");
const content = document.querySelector('.pcoded-content');


//// 체크박스 관련
// 성별
const gender = document.querySelector("#gender");
const chk_m = document.querySelector("#chk_m");
const chk_w = document.querySelector("#chk_w");


// 연령 범위선택 변수
const textLeft_age = document.getElementById("min_left_age");
const textRight_age = document.getElementById("max_right_age");
const inputLeft_age = document.getElementById("input-left_age");
const inputRight_age = document.getElementById("input-right_age");
const thumbLeft_age = document.querySelector(".slider > .thumb_age.left_age");
const thumbRight_age = document.querySelector(".slider > .thumb_age.right_age");
const range_age = document.querySelector(".slider > .range_age");


// 셀럽모델료 범위선택 변수
const textLeft_cfee = document.getElementById("min_left_cfee");
const textRight_cfee = document.getElementById("max_right_cfee");
const inputLeft = document.getElementById("input-left_cfee");
const inputRight = document.getElementById("input-right_cfee");
const thumbLeft = document.querySelector(".slider > .thumb_cfee.left_cfee");
const thumbRight = document.querySelector(".slider > .thumb_cfee.right_cfee");
const range = document.querySelector(".slider > .range_cfee");


// 셀럽 섹션선택 변수
const buttonSinger = document.getElementById("section_singer");
const buttonActor = document.getElementById("section_actor");
const buttonIdol = document.getElementById("section_idol");
const buttonEntertainment = document.getElementById("section_entertainment");
const buttonBroadcast = document.getElementById("section_broadcast");
const buttonCeleb = document.getElementById("section_celeb");
const buttonYoutube = document.getElementById("section_youtube");


//
const inputPeriodCfee = document.getElementById("period_cfee");
const selectPeriodCfee = document.getElementById("period_");


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
    console.log(params.cfee)
    console.log(params.age)
    console.log(params.section)
    console.log(params.period)
}


// 모달창 열고 닫음
function clickmodal(event){


    if (event.cancelable) event.preventDefault();
    // window.scrollTo(0,0);
    event.preventDefault(); //페이지 새로고침 중지
    

    /////////////////////////////////////////////////
    //////// 모달창 open 전에 이전 데이터 불러옴. ///////////






///// 성별 이전 선택 데이터로 설정.
    var preSelectGender = params.gender.split('%'); //이전에 선택한 성별 체크박스
    
    for(var i=0; i<preSelectGender.length; i++){

        if(!preSelectGender[i] | !(preSelectGender[i] == 'm' | preSelectGender[i] == 'w')){
            break;
        }
        else{
            var preId = 'chk_' + preSelectGender[i];
            document.getElementById(preId).checked = true;

        }
    }
/////

    



///// 연령 범위 -> 이전 데이터로 선택

    var preRangeAge = params.age.split('%');

    let minPreAge = preRangeAge[0];
    let maxPreAge = preRangeAge[1];
    console.log(preRangeAge)

    // 왼쪽
    const [minLeftAge, maxLeftAge] = [parseInt(inputLeft_age.min), parseInt(inputLeft_age.max)];
    minPreAge = Math.min(parseInt(minPreAge), parseInt(inputRight_age.value) - 1);
    
    const percentLeftAge = ((minPreAge - minLeftAge) / (maxLeftAge - minLeftAge)) * 100;
    thumbLeft_age.style.left = percentLeftAge + "%";
    range_age.style.left = percentLeftAge + "%";

    let minAge = document.getElementsByClassName("min_value_age")[0];
    minAge.innerText=minPreAge;
    inputLeft_age.value = minPreAge;



    // 오른쪽
    const [minRightAge, maxRightAge] = [parseInt(inputRight_age.min), parseInt(inputRight_age.max)];
    maxPreAge = Math.max(parseInt(maxPreAge), parseInt(inputLeft_age.value) + 1);
    
    const percentRightAge = ((maxPreAge - minRightAge) / (maxRightAge - minRightAge)) * 100;
    thumbRight_age.style.right = 100 - percentRightAge + "%";
    range_age.style.right = 100 - percentRightAge + "%";

    let maxAge = document.getElementsByClassName("max_value_age")[0];
    maxAge.innerText=maxPreAge; 
    inputRight_age.value = maxPreAge;


/////

///// 셀럽모델료 범위 -> 이전 데이터로 선택

    var preRangeMfee = params.cfee.split('%');
        
    let minPreAlpha = preRangeMfee[0];
    let maxPreAlpha = preRangeMfee[1];
    console.log(preRangeMfee, ' :: 셀럽모델료')


    // 왼쪽
    const [minLeftAlpha, maxLeftAlpha] = [parseFloat(inputLeft.min), parseFloat(inputLeft.max)];
    minPreAlpha = Math.min(parseFloat(minPreAlpha), parseFloat(inputRight.value) - 1);

    const percentAlphaLeft = ((minPreAlpha - minLeftAlpha) / (maxLeftAlpha - minLeftAlpha)) * 100;
    thumbLeft.style.left = percentAlphaLeft + "%";
    range.style.left = percentAlphaLeft + "%";


    let minAlpha = document.getElementsByClassName("min_value_cfee")[0];
    minAlpha.innerText=minPreAlpha;
    inputLeft.value = minPreAlpha;


    // 오른쪽
    const [minRightAlpha, maxRightAlpha] = [parseFloat(inputRight.min), parseFloat(inputRight.max)];
    maxPreAlpha = Math.max(parseFloat(maxPreAlpha), parseFloat(inputLeft.value) + 1);

    const percentAlphaRight = ((maxPreAlpha - minRightAlpha) / (maxRightAlpha - minRightAlpha)) * 100;
    thumbRight.style.right = 100 - percentAlphaRight + "%";
    range.style.right = 100 - percentAlphaRight + "%";

    let maxAlpha = document.getElementsByClassName("max_value_cfee")[0];
    maxAlpha.innerText=maxPreAlpha;
    inputRight.value = maxPreAlpha;

    /////

    ///// 셀럽섹션 이전 선택 데이터로 설정.
    console.log(params.section)
    var preSelectSection = params.section.split('%'); //이전에 선택한 성별 체크박스
        
    for(var i=0; i<preSelectSection.length -1; i++){


        var preId = 'section_' + preSelectSection[i];
        console.log(preId);
        document.getElementById(preId).checked = true;

    }
/////


///// 셀럽 모델료 기간 이전 데이터로 설정

    console.log(params.period);
    inputPeriodCfee.value = params.period;

    for (let i=0; i<selectPeriodCfee.options.length; i++){  
        //select box의 option value가 입력 받은 value의 값과 일치할 경우 selected
      if(selectPeriodCfee.options[i].value == params.period){
        selectPeriodCfee.options[i].selected = true;
      }
    }  
    // selectPeriodCfee.selected = true;

/////

    // 모달창 close
    if(!modal.classList.contains('inactive')){
        modal.classList.add("inactive");

        content.style.cssText  = 'overflow: auto; padding-top:0px;';
        
    }
    // 모달창 open
    else{

        setLeftValue_age();
        setRightValue_age();
        setLeftValue_();
        setRightValue_();
        setCelebSection();
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



//////////////////////////////
// 성별 체크박스 남자, 여자 선택 값 -> gender input에 추가
function getChkGenderValue()  {

    const query = 'input[class="chk_gender"]:checked';
    const selectedEls = 
        document.querySelectorAll(query);
    
    let result = '';
    selectedEls.forEach((el) => {
      result += el.value + ' ';
    });
    
    
    result = result.replace(' ', '%')

    document.getElementById("gender").value = result; 
    
  }


inputLeft_age.addEventListener("input", setLeftValue_age);
inputRight_age.addEventListener("input", setRightValue_age);


inputLeft.addEventListener("input", setLeftValue_);
inputRight.addEventListener("input", setRightValue_);



/////////////////////////////////////////////// 주석 체크 진행하기 

function setLeftValue_age() {


    var age = textLeft_age.innerText + "%" + textRight_age.innerText;
    
    console.log(age);
    $('#age').val(age);


    const _this = inputLeft_age;
    const [min, max] = [parseInt(_this.min), parseInt(_this.max)];
    
    // 교차되지 않게, 1을 빼준 건 완전히 겹치기보다는 어느 정도 간격을 남겨두기 위해.
    _this.value = Math.min(parseInt(_this.value), parseInt(inputRight_age.value) - 1);
    
    // input, thumb 같이 움직이도록
    const percent = ((_this.value - min) / (max - min)) * 100;
    
    thumbLeft_age.style.left = percent + "%";
    range_age.style.left = percent + "%";


    let x = document.getElementsByClassName("min_value_age")[0];
    x.innerText=_this.value; 


};

function setRightValue_age() {
    const _this = inputRight_age;
    const [min, max] = [parseInt(_this.min), parseInt(_this.max)];
    

    var age = textLeft_age.innerText + "%" + textRight_age.innerText;
    
    console.log(age);
    $('#age').val(age);


    // 교차되지 않게, 1을 더해준 건 완전히 겹치기보다는 어느 정도 간격을 남겨두기 위해.
    _this.value = Math.max(parseInt(_this.value), parseInt(inputLeft_age.value) + 1);
    
    // input, thumb 같이 움직이도록
    const percent = ((_this.value - min) / (max - min)) * 100;
    thumbRight_age.style.right = 100 - percent + "%";
    range_age.style.right = 100 - percent + "%";

    let x = document.getElementsByClassName("max_value_age")[0];
    x.innerText=_this.value; 

    // console.log(_this.value)
};




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


    let x = document.getElementsByClassName("min_value_cfee")[0];
    
    x.innerText= String(_this.value) + '억'; 


    if(inputLeft.value == 0 && _this.value == 0){
        document.getElementsByClassName("min_value_cfee")[0].innerText =  'X';
        x.innerText= " ";
    }else if(inputLeft.value == _this.value){
        document.getElementsByClassName("min_value_cfee")[0].innerText = ''
        x.innerText= String(_this.value) + '억'; 
    }else{
        document.getElementsByClassName("min_value_cfee")[0].innerText = String(Math.min(parseFloat(inputLeft.value), parseFloat(inputRight.value) - 0.1)) + '억';
        x.innerText= " - " + String(_this.value) + '억'; 
    }

    var cfee = textLeft_cfee.innerText.split('억')[0] + "%" + textRight_cfee.innerText.split('억')[0].substring(2, textRight_cfee.innerText.lastIndexOf('억'));

    $('#cfee').val(cfee);
    console.log(cfee);

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

    let x = document.getElementsByClassName("max_value_cfee")[0];
    

    if(inputLeft.value == 0 && _this.value == 0){
        document.getElementsByClassName("min_value_cfee")[0].innerText =  'X';
        x.innerText= " ";
    }else if(inputLeft.value == _this.value){
        console.log(_this)
        document.getElementsByClassName("min_value_cfee")[0].innerText = ''
        x.innerText= String(_this.value) + '억'; 
    }else{
        document.getElementsByClassName("min_value_cfee")[0].innerText = String(Math.min(parseFloat(inputLeft.value), parseFloat(inputRight.value) - 0.1)) + '억';
        x.innerText= " - " + String(_this.value) + '억'; 

        console.log('LEFT :: ', String(Math.min(parseFloat(inputLeft.value), parseFloat(inputRight.value) - 0.1)))
        console.log('RIGHT :: ', String(_this.value))
    }
    
    var cfee = textLeft_cfee.innerText.split('억')[0] + "%" + textRight_cfee.innerText.split('억')[0].substring(2, textRight_cfee.innerText.lastIndexOf('억'));

    $('#cfee').val(cfee);
    console.log(textRight_cfee.innerText)

};


modalopen.addEventListener("click", clickmodal);
modalclose.addEventListener("click", closemodal);

chk_m.addEventListener("click", getChkGenderValue);
chk_w.addEventListener("click", getChkGenderValue);



///////////////////////////////////////////////////////////////



// 셀럽 섹션 선택
function setCelebSection() {
    
    
    const query = 'input[class="model_section"]:checked';
    const selectedEls = 
        document.querySelectorAll(query);
    
    let result = '';
    selectedEls.forEach((el) => {
      result += el.value + ' ';
    });
    
    
    result = result.replace(/ /g, '%')

    console.log('셀럽 섹션 확인 :: ', result)
    document.getElementById("section").value = result; 
    

};

buttonSinger.addEventListener("click", setCelebSection);
buttonActor.addEventListener("click", setCelebSection);
buttonIdol.addEventListener("click", setCelebSection);
buttonEntertainment.addEventListener("click", setCelebSection);
buttonBroadcast.addEventListener("click", setCelebSection);
buttonCeleb.addEventListener("click", setCelebSection);
buttonYoutube.addEventListener("click", setCelebSection);







///////////////////////////////////////////////////////////////

const nav = document.querySelector('.pcoded-content'); // 네비게이션 바
const filterBar = document.querySelector('#filter-bar'); // 네비게이션 바
// const grid = document.querySelector('.list-grid');
const grids = document.getElementsByClassName("list-grid")

const navTop = nav.offsetTop;


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


window.addEventListener('scroll', fixNav);



const alignThiry = document.querySelector('#pills-contact-tab'); 
const alignMovchoi = document.querySelector('#pills-profile-tab'); 
const alignProcount = document.querySelector('#pills-home-tab'); 
var loc = document.querySelector(".tab-content").offsetTop;

function scrollToTop(){

window.scrollTo(0, 0)
// $(window).scrollTop(0);

}; 

alignThiry.addEventListener('click', scrollToTop);
alignMovchoi.addEventListener('click', scrollToTop);
alignProcount.addEventListener('click', scrollToTop);



document.querySelector(".mob-toggler").addEventListener('click', function () {
    console.log("FFF")
    document.querySelector('.pcoded-header > .collapse,.pcoded-header > .container > .collapse').classList.toggle('d-flex');
  });
  
  
  
  
  // search-bar
  document.querySelector(".pop-search").addEventListener('click', function () {
    slideDown(document.querySelector(".search-bar"), 200);
    document.querySelector(".search-bar input").focus();
  });
  document.querySelector(".search-bar .btn-close").addEventListener('click', function () {
    slideUp(document.querySelector(".search-bar"), 200);
  });
  if (document.querySelector('.pcoded-navbar').classList.contains('theme-horizontal')) {
    rmactive();
    horizontalmenu();
  }