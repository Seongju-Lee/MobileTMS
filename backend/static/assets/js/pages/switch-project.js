const $toggleTel = document.querySelector(".toggleSwitch_tel");
const $toggleFiles = document.querySelector(".toggleSwitch_files");
const $toggleContract = document.querySelector(".toggleSwitch-contract");
const $toggleMemo = document.querySelector(".toggleSwitch_memo");

const $telTable = document.querySelector("#table_tel");
const $fileTable = document.querySelector("#ul_files");
const $contractTable = document.querySelector("#table-contract");
const $memoDiv = document.querySelector("#div_memo");



$toggleTel.onclick = () => {
  $toggleTel.classList.toggle('active');

  if(!$toggleTel.classList.contains('active')){
    $telTable.style.display = "none";
  }
  else{
    $telTable.style.display = "block";
  }


}



$toggleFiles.onclick = () => {

    $toggleFiles.classList.toggle('active');
  
  
    if(!$toggleFiles.classList.contains('active')){
      $fileTable.style.display = "none";
    }
    else{
      $fileTable.style.display = "block";
    }
  
  
}


$toggleContract.onclick = () => {
    $toggleContract.classList.toggle('active');
  
  
    if(!$toggleContract.classList.contains('active')){
      $contractTable.style.display = "none";
    }
    else{
      $contractTable.style.display = "block";
    }
  
  
}


$toggleMemo.onclick = () => {
  $toggleMemo.classList.toggle('active');


  if(!$toggleMemo.classList.contains('active')){
    $memoDiv.style.display = "none";
  }
  else{
    $memoDiv.style.display = "block";
  }


}


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