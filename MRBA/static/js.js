//Function to disable previous date selection 
document.getElementById("datePicker").min = new Date().toISOString().slice(0, 10);
//#####

//Function GrantMeet (INITIAL)
function grantmeet(){
var deleteId = document.getElementsByClassName('btnDelId');
var deleteConfirm = document.getElementsByClassName('btnDelConfirm');
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
    deleteConfirm[n].id = Id + 'delIDConfirm';
    deleteId[n].id = Id + 'delID';
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

function userRoomFunct() {
  bool = document.getElementsByClassName('grantMeetBool');
  EditId = document.getElementsByClassName('EditButtonUser')
  for(i in bool){
    bool[i].id = i + 'Bool'
    EditId[i].id = i + 'Edit'
    if (bool[i].value == 'True'){
      document.getElementById(i+'Edit').style.display = 'none';
    }
  }
  
}

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
  var approve = window.confirm("Cancel The Process ?");
  if (approve){
  location.reload()
  }
}
}
//
var cancelSwitchStatus = false;
function btnCancelClick(clicked_id)
{
if (!cancelSwitchStatus) {
  var approve = window.confirm("Cancel this Meeting ?");
  if (approve){
  document.getElementById(clicked_id).style.display = 'none';
  document.getElementById(clicked_id+'Confirm').style.display = "inline-block";
  cancelSwitchStatus = true;
  } 
  else{
    location.reload()
  }
}
else if (cancelSwitchStatus) {
  var approve = window.confirm("Cancel The Process ?");
  if (approve){
  location.reload()
  }
}
}

//#####
//Function after Delete Clicked
deleteClicked = false;
function btnDelClick(clicked_id){
  var approve = window.confirm('Do You Want To Delete This Meeing ?')
  if (approve){
    document.getElementById(clicked_id).style.display = 'none';
    document.getElementById(clicked_id+'Confirm').style.display = 'inline-block';
  }
}

//EMAIL VALIDATION IN JS
function emailValid(){
  email = document.getElementById('email').value
  if (!email.includes('@')){
    document.getElementById('error').style.display ='inline-block';
    document.getElementById('error').innerHTML = ' ! ';
  }
  else{
    document.getElementById('error').innerHTML = '';
    document.getElementById('error').style.display ='none';
  }
}

//###############################


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
