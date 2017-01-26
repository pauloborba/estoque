$(document).ready(function() {
    Materialize.updateTextFields();
    $('select').material_select();
    $('.modal').modal();
});


function openItemModal(name, id){
  document.getElementById("itemName").innerHTML = "Atualizar " + name;
  document.modalForm.action = '/editItem/'+id+'/';
}
