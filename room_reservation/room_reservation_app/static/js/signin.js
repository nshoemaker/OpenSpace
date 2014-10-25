function onSubmitForm()
{
if(document.pressed == 'log in')
{
 document.signinForm.action ="my_reservations.html";
}
else if(document.pressed == 'sign up')
{
  document.signinForm.action ="profile-edit.html";
}
else if(document.pressed == 'reset password')
{
  document.signinForm.action ="password-reset.html";
}
return true;
}