const modal = document.querySelector(".modal-dialog");
const modalopen = document.querySelector("#modal-filter");
const modalclose = document.querySelector("#modal-close");
const content = document.querySelector('.pcoded-content');

const gender = document.querySelector("#gender");
const chk_m = document.querySelector("#chk_m");
const chk_w = document.querySelector("#chk_w");


const alpha = document.querySelector("#alpha");
const chk_alpha = document.querySelector("#chk_auto");
const chk_0100 = document.querySelector("#chk_0100");


// 연령 범위선택 변수
const inputLeft_age = document.getElementById("input-left_age");
const inputRight_age = document.getElementById("input-right_age");
const thumbLeft_age = document.querySelector(".slider > .thumb_age.left_age");
const thumbRight_age = document.querySelector(".slider > .thumb_age.right_age");
const range_age = document.querySelector(".slider > .range_age");

// 알파모델료 범위선택 변수
const inputLeft = document.getElementById("input-left");
const inputRight = document.getElementById("input-right");
const thumbLeft = document.querySelector(".slider > .thumb.left");
const thumbRight = document.querySelector(".slider > .thumb.right");
const range = document.querySelector(".slider > .range");


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
console.log(params.gender.split('%').length)
console.log(params.mfee)
console.log(params.age)
console.log(params.alpha)


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

    
    ///// 알파모델료(상훈페이, 레디자동) 이전 선택 데이터로 설정.
    var preSelectAlpha = params.alpha.split('%'); //이전에 선택한 성별 체크박스

    for(var i=0; i<preSelectAlpha.length; i++){

        if(!preSelectAlpha[i] | !(preSelectAlpha[i] == '0100' | preSelectAlpha[i] == 'auto')){
            break;
        }
        else{
            var preId = 'chk_' + preSelectAlpha[i];
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


///// 알파모델료 범위 -> 이전 데이터로 선택

    var preRangeMfee = params.mfee.split('%');
    
    let minPreAlpha = preRangeMfee[0];
    let maxPreAlpha = preRangeMfee[1];
    console.log(preRangeMfee, ' ::  알파모델료')


    // 왼쪽
    const [minLeftAlpha, maxLeftAlpha] = [parseInt(inputLeft.min), parseInt(inputLeft.max)];
    minPreAlpha = Math.min(parseInt(minPreAlpha), parseInt(inputRight.value) - 1);
    
    const percentAlphaLeft = ((minPreAlpha - minLeftAlpha) / (maxLeftAlpha - minLeftAlpha)) * 100;
    thumbLeft.style.left = percentAlphaLeft + "%";
    range.style.left = percentAlphaLeft + "%";


    let minAlpha = document.getElementsByClassName("min_value")[0];
    minAlpha.innerText=minPreAlpha;
    inputLeft.value = minPreAlpha;


    // 오른쪽
    const [minRightAlpha, maxRightAlpha] = [parseInt(inputRight.min), parseInt(inputRight.max)];
    maxPreAlpha = Math.max(parseInt(maxPreAlpha), parseInt(inputLeft.value) - 1);
    
    const percentAlphaRight = ((maxPreAlpha - minRightAlpha) / (maxRightAlpha - minRightAlpha)) * 100;
    thumbRight.style.right = 100 - percentAlphaRight + "%";
    range.style.right = 100 - percentAlphaRight + "%";

    let maxAlpha = document.getElementsByClassName("max_value")[0];
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
        getChkMfeeValue();
        setLeftValue_age();
        setRightValue_age();
        setLeftValue();
        setRightValue();
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



////////////////////////////////
// 알파모델료 체크박스 상훈페이, 레디자동 선택 값 -> alpha input에 추가
function getChkMfeeValue()  {
    // 선택된 목록 가져오기
    const query = 'input[class="chk_alpha"]:checked';
    const selectedEls = 
        document.querySelectorAll(query);
    
    // 선택된 목록에서 value 찾기
    let result = '';
    selectedEls.forEach((el) => {
      result += el.value + ' ';
    });
    
    
    result = result.replace(' ', '%')

    console.log('알파모델료 체크 목록 :: ' , result)
    document.getElementById("alpha").value = result; 
  
  }


/////////////////////////////////////////////// 주석 체크 진행하기 



modalopen.addEventListener("click", clickmodal);
modalclose.addEventListener("click", closemodal);

chk_m.addEventListener("click", getChkGenderValue);
chk_w.addEventListener("click", getChkGenderValue);

chk_0100.addEventListener("click", getChkMfeeValue);
chk_alpha.addEventListener("click", getChkMfeeValue);




const setLeftValue_age = () => {

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

const setRightValue_age = () => {
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

inputLeft_age.addEventListener("input", setLeftValue_age);
inputRight_age.addEventListener("input", setRightValue_age);













const setLeftValue = () => {
    const _this = inputLeft;
    const [min, max] = [parseInt(_this.min), parseInt(_this.max)];
    

    var mfee = inputLeft.value + "%" + inputRight.value;
    // console.log(mfee);
    $('#mfee').val(mfee);


    // 교차되지 않게, 1을 빼준 건 완전히 겹치기보다는 어느 정도 간격을 남겨두기 위해.
    _this.value = Math.min(parseInt(_this.value), parseInt(inputRight.value) - 1);
    
    // input, thumb 같이 움직이도록
    const percent = ((_this.value - min) / (max - min)) * 100;
    thumbLeft.style.left = percent + "%";
    range.style.left = percent + "%";


    let x = document.getElementsByClassName("min_value")[0];
    x.innerText=_this.value; 

    // $(".min_value").text(_this.value);

};

const setRightValue = () => {
    const _this = inputRight;
    const [min, max] = [parseInt(_this.min), parseInt(_this.max)];
    
    var mfee = inputLeft.value + "%" + inputRight.value;
    // console.log(mfee);
    $('#mfee').val(mfee);

    // 교차되지 않게, 1을 더해준 건 완전히 겹치기보다는 어느 정도 간격을 남겨두기 위해.
    _this.value = Math.max(parseInt(_this.value), parseInt(inputLeft.value) + 1);
    
    // input, thumb 같이 움직이도록
    const percent = ((_this.value - min) / (max - min)) * 100;
    thumbRight.style.right = 100 - percent + "%";
    range.style.right = 100 - percent + "%";

    let x = document.getElementsByClassName("max_value")[0];
    x.innerText=_this.value; 
};

inputLeft.addEventListener("input", setLeftValue);
inputRight.addEventListener("input", setRightValue);





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

