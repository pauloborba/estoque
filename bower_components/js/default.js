$(document).ready(function() {
    Materialize.updateTextFields();
    $('select').material_select();
    $('.modal').modal();
});


function openItemModal(name, id){
  document.getElementById("itemName").innerHTML = "Atualizar " + name;
  document.modalForm.action = '/editItem/'+id+'/';
}

function isValid(strInp){
  return (strInp && strInp.length !== 0);
}

function validate_login(){
  username = document.getElementById("usernameInput").value;
  pwd = document.getElementById("pwdInput").value;
  if(isValid(username) && isValid(pwd))
    document.getElementById("loginForm").submit();
  else
    Materialize.toast('Senha ou Nome vazios!', 4000);
}

function validate_new_item(){
  item_name = document.getElementById("itemNameInput").value;
  if(isValid(item_name))
    document.getElementById("newItemForm").submit();
  else
    Materialize.toast('Nome é obrigatório!', 4000);
}
