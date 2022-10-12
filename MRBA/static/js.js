//Function to disable previous date selection 
document.getElementById("datePicker").min = new Date().toISOString().slice(0, 10);
//#####

//Function GrantMeet (INITIAL)
function grantmeet(){
var value = document.getElementsByClassName('roomIdValue');
var id = document.getElementsByClassName('labels');
var toggleID = document.getElementsByClassName('toggle');
btnSubmit = document.getElementsByClassName('btnSubmitId')
btnCancel = document.getElementsByClassName('btnCancelId')
btnCancelConfirm = document.getElementsByClassName('btnCancelIdConfirm')
var grantMeetValue = document.getElementsByClassName('grantMeetingValue')
for (n=0, length = value.length; n<length; n++){
  var Id = value[n].value
    id[n].id = Id;
    toggleID[n].id = Id + 'tgl';
    btnSubmit[n].id = Id +'submitID';
    btnCancel[n].id = Id + 'CancelBtn';
    btnCancelConfirm[n].id = Id + 'CancelBtnConfirm';
    if (grantMeetValue[n].value == 'True'){
      document.getElementById(Id).style.display = 'none';
      document.getElementById(Id+'tgl').style.display = 'none';
      document.getElementById(Id+'CancelBtn').style.display = "inline-block";
    }  
  }
}
//#####

//Function after Span Clicked
var switchStatus = false;
function spanClick(clicked_id)
{
if (!switchStatus) {
  var approve = window.confirm("Approve this Meeting ?");
  if (approve){
  document.getElementById(clicked_id+'submitID').style.display = "inline-block";
  switchStatus = true;
  } 
  else{
    location.reload()
  }
}
else if (switchStatus) {
  var approve = window.confirm("this Meeting ?");
  if (approve){
  location.reload()
  }
}
}
function btnCancelClick(clicked_id){
  var approve = window.confirm(clicked_id);
  if (approve){
  alert(document.getElementById(clicked_id+'CancelBtn'))
  }
}
//#####


//Function to display Meeting CountDown Time
// var countDownDate = new Date("Jan 5, 2024 15:37:25").getTime();
// var x = setInterval(function() {
//   var now = new Date().getTime();
//   var distance = countDownDate - now;
//   var days = Math.floor(distance / (1000 * 60 * 60 * 24));
//   var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
//   var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
//   var seconds = Math.floor((distance % (1000 * 60)) / 1000);
//   document.getElementById("meetingTimeDisplay").innerHTML = days + "d " + hours + "h "
//   + minutes + "m " + seconds + "s ";
//   if (distance < 0) {
//     clearInterval(x);
//     document.getElementById("meetingTimeDisplay").innerHTML = "Your Meeting is Now";
//   }
// }, 1000);
//
