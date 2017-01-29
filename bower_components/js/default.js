$(document).ready(function() {
    Materialize.updateTextFields();
    $('select').material_select();
    $('.modal').modal();
});


function openItemModal(name, url){
  document.getElementById("itemName").innerHTML = "Atualizar " + name;
  document.modalForm.action = url;
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
  category = document.getElementById("categoryInput").value;
  if(isValid(item_name) && isValid(category))
    document.getElementById("newItemForm").submit();
  else if(isValid(item_name))
    Materialize.toast('Escolha uma categoria!', 4000);
  else
    Materialize.toast('Nome é obrigatório!', 4000);
}

function validate_new_category(){
  category_name = document.getElementById("categoryNameInput").value;
  if(isValid(category_name))
    document.getElementById("newCategoryForm").submit();
  else
    Materialize.toast('Nome é obrigatório!', 4000);
}
