const $toggle = document.querySelector(".toggleSwitch");
const $toggleCf = document.querySelector(".toggleSwitch_cf");
const $toggleMemo = document.querySelector(".toggleSwitch_memo");

const $contractTable = document.querySelector("#contract-table");
const $cfTable = document.querySelector("#cf-table");
const $memoDiv = document.querySelector("#memo-div");



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


$toggleMemo.onclick = () => {
    $toggleMemo.classList.toggle('active');
  
  
    if(!$toggleMemo.classList.contains('active')){
      $memoDiv.style.display = "none";
    }
    else{
      $memoDiv.style.display = "block";
    }
  
  
}



telMemo = (clickedId) => {


    console.log('ssiibb', clickedId);


    var lenButton = $("input[name=telButton]").length;
  
    //배열 생성
    var telMemoarr = new Array(lenButton);


    console.log(lenButton, typeof(lenButton))
    //배열에 값 주입
    for(var i=0; i<lenButton; i++){                          
        // telMemoarr[i] = $("input[name=telButton]").eq(i).val();

        console.log(i);
        console.log($("input[name=telButton]").eq(i).attr('id'));
          // console.log(document.getElementsByName("telButton")[0].id)

        if($("input[name=telButton]").eq(i).attr('id') == clickedId){
            document.getElementById("_" + clickedId).style.display = "block" ;
        }
        else{
            document.getElementById("_" + $("input[name=telButton]").eq(i).attr('id')).style.display = "none" ;
        }


    }

    
}