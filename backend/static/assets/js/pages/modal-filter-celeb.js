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
const inputLeft_age = document.getElementById("input-left_age");
const inputRight_age = document.getElementById("input-right_age");
const thumbLeft_age = document.querySelector(".slider > .thumb_age.left_age");
const thumbRight_age = document.querySelector(".slider > .thumb_age.right_age");
const range_age = document.querySelector(".slider > .range_age");

console.log(inputLeft_age, inputRight_age)

// 셀럽모델료 범위선택 변수
const inputLeft = document.getElementById("input-left_cfee");
const inputRight = document.getElementById("input-right_cfee");
const thumbLeft = document.querySelector(".slider > .thumb_cfee.left_cfee");
const thumbRight = document.querySelector(".slider > .thumb_cfee.right_cfee");
const range = document.querySelector(".slider > .range_cfee");


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
}

// 모달창 열고 닫음
function clickmodal(event){


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


// ///// 셀럽 모델료 범위 -> 이전 데이터로 선택

// var preRangeMfee = params.mfee.split('%');
    
// let minPreAlpha = preRangeMfee[0];
// let maxPreAlpha = preRangeMfee[1];
// console.log(preRangeMfee, ' ::  셀럽모델료')


// // 왼쪽
// const [minLeftAlpha, maxLeftAlpha] = [parseInt(inputLeft_cfee.min), parseInt(inputLeft_cfee.max)];
// minPreAlpha = Math.min(parseInt(minPreAlpha), parseInt(inputRight_cfee.value) - 1);

// const percentAlphaLeft = ((minPreAlpha - minLeftAlpha) / (maxLeftAlpha - minLeftAlpha)) * 100;
// thumbLeft_cfee.style.left = percentAlphaLeft + "%";
// range_cfee.style.left = percentAlphaLeft + "%";


// let minAlpha = document.getElementsByClassName("min_value_cfee")[0];
// minAlpha.innerText=minPreAlpha;
// inputLeft_cfee.value = minPreAlpha;


// // 오른쪽
// const [minRightAlpha, maxRightAlpha] = [parseInt(inputRight_cfee.min), parseInt(inputRight_cfee.max)];
// maxPreAlpha = Math.max(parseInt(maxPreAlpha), parseInt(inputLeft_cfee.value) - 1);

// const percentAlphaRight = ((maxPreAlpha - minRightAlpha) / (maxRightAlpha - minRightAlpha)) * 100;
// thumbRight_cfee.style.right = 100 - percentAlphaRight + "%";
// range_cfee.style.right = 100 - percentAlphaRight + "%";

// let maxAlpha = document.getElementsByClassName("max_value_cfee")[0];
// maxAlpha.innerText=maxPreAlpha;
// inputRight_cfee.value = maxPreAlpha;

/////



///// 알파모델료 범위 -> 이전 데이터로 선택

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
maxPreAlpha = Math.max(parseFloat(maxPreAlpha), parseFloat(inputLeft.value) - 1);

const percentAlphaRight = ((maxPreAlpha - minRightAlpha) / (maxRightAlpha - minRightAlpha)) * 100;
thumbRight.style.right = 100 - percentAlphaRight + "%";
range.style.right = 100 - percentAlphaRight + "%";

let maxAlpha = document.getElementsByClassName("max_value_cfee")[0];
maxAlpha.innerText=maxPreAlpha;
inputRight.value = maxPreAlpha;

/////






    // 모달창 close
    if(!modal.classList.contains('inactive')){
        modal.classList.add("inactive");

        content.style.cssText  = 'overflow: auto;';
        
    }
    // 모달창 open
    else{

        getChkGenderValue();
        setLeftValue_age();
        setRightValue_age();
        setLeftValue_();
        setRightValue_();
        // getChkRecSectionValue();
        content.style.cssText  = 'overflow: hidden;';
        modal.classList.remove("inactive");

    }
  }


/////////////////////////////?
// 모달창 -> 취소버튼
function closemodal(event){
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

////////////////////////////////
// 모델 추천 점수 섹션 선택 -> 이미지, 호감도, 연기력, 뉴페이스

function getChkRecSectionValue()  {
    // 선택된 목록 가져오기
    const query = 'input[class="chk_section"]:checked';

    const selectedEls = 
        document.querySelectorAll(query);
    

    console.log(selectedEls)
    // 선택된 목록에서 value 찾기
    let result = '';
    selectedEls.forEach((el) => {
      result += el.value + ' ';
      console.log(el.value)
    });
    
    
    console.log('섹션 체크 목록1 :: ' , result)
    result = result.replace(/ /g, '%')

    console.log('섹션 체크 목록2 :: ' , result)
    // document.getElementById("recommendation_section").value = result; 
  
  }


/////////////////////////////////////////////// 주석 체크 진행하기 

function setLeftValue_age() {

    console.log('1222222222222222222222222222222')

    var minAge = inputLeft_age;
    var maxAge = inputRight_age;
    var age = minAge.value + "%" + maxAge.value;
    

    
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

    // $(".min_value").text(_this.value);

};

function setRightValue_age() {
    const _this = inputRight_age;
    const [min, max] = [parseInt(_this.min), parseInt(_this.max)];
    

    var minAge = inputLeft_age;
    var maxAge = inputRight_age;
    
    var age = minAge.value + "%" + maxAge.value;
    
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


function setLeftValue_() {
    const _this = inputLeft;
    const [min, max] = [parseFloat(_this.min), parseFloat(_this.max)];
    

    var mfee = inputLeft.value + "%" + inputRight.value;

    console.log(inputRight.value);

    $('#cfee').val(mfee);


    // 교차되지 않게, 1을 빼준 건 완전히 겹치기보다는 어느 정도 간격을 남겨두기 위해.
    _this.value = Math.min(parseFloat(_this.value), parseFloat(inputRight.value) - 0.1);
    
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
        console.log(_this)
        document.getElementsByClassName("min_value_cfee")[0].innerText = ''
        x.innerText= String(_this.value) + '억'; 
    }else{
        document.getElementsByClassName("min_value_cfee")[0].innerText = String(Math.min(parseFloat(inputLeft.value), parseFloat(inputRight.value) - 0.1)) + '억';
        x.innerText= " - " + String(_this.value) + '억'; 
    }

};

function setRightValue_() {
    const _this = inputRight;
    const [min, max] = [parseFloat(_this.min), parseFloat(_this.max)];
    
    var mfee = inputLeft.value + "%" + inputRight.value;

    console.log(inputRight.value);

    $('#cfee').val(mfee);

    // 교차되지 않게, 1을 더해준 건 완전히 겹치기보다는 어느 정도 간격을 남겨두기 위해.
    _this.value = Math.max(parseFloat(_this.value), parseFloat(inputLeft.value) + 0.1);
    
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
    }
    

};


modalopen.addEventListener("click", clickmodal);
modalclose.addEventListener("click", closemodal);

chk_m.addEventListener("click", getChkGenderValue);
chk_w.addEventListener("click", getChkGenderValue);


// chk_img.addEventListener("click", getChkRecSectionValue);
// chk_fav.addEventListener("click", getChkRecSectionValue);
// chk_act.addEventListener("click", getChkRecSectionValue);
// chk_new.addEventListener("click", getChkRecSectionValue);




///////////////////////////////////////////////////////////////






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

