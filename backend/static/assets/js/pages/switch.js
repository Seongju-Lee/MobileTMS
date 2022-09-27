const $toggle = document.querySelector(".toggleSwitch");
const $toggleCf = document.querySelector(".toggleSwitch_cf");
const $contractTable = document.querySelector("#contract-table");
const $cfTable = document.querySelector("#cf-table");

$toggle.onclick = () => {
  $toggle.classList.toggle('active');

  if(!$toggle.classList.contains('active')){
    $contractTable.style.display = "none";
  }
  else{
    $contractTable.style.display = "block";
  }


}



$toggleCf.onclick = () => {
    $toggleCf.classList.toggle('active');
  
  
    if(!$toggleCf.classList.contains('active')){
      $cfTable.style.display = "none";
    }
    else{
      $cfTable.style.display = "block";
    }
  
  
  }