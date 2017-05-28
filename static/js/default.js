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

function change_status(reference){
  if(reference.hasClass("green-text")){
    reference.removeClass("green-text");
    reference.addClass("red-text");
    reference.html("Comprar");
  }
  else {
    reference.removeClass("red-text");
    reference.addClass("green-text");
    reference.html("Suficiente");
  }
}

function editItem(item_id){
  var csrftoken = Cookies.get('csrftoken');
  $.ajax({
    type: "POST",
    url: "/editItem/",
    data: {id: item_id, csrfmiddlewaretoken: csrftoken},
    success: function(data){
      $('#userPoints').html(data);
      $('#userWelcome').html(' Você tem ' + data + ' pontos ');
    },
    error: function(jqXHR, err){
      change_status($('#item'+item_id));
    }
  });

  change_status($('#item'+item_id));

}

function validate_new_price(){
  price = document.getElementById("priceInput").value;
  category = document.getElementById("categoryInput").value;
  item = document.getElementById("itemInput").value;
  if(isValid(item) && isValid(category) && isValid(price.toString()))
    document.getElementById("newPriceForm").submit();
  else if(isValid(item_name))
    Materialize.toast('Escolha uma categoria!', 4000);
  else if(isValid(category))
    Materialize.toast('Escolha uma categoria!', 4000)
  else
    Materialize.toast('Preço é obrigatório!', 4000);
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

function check_no_stores(){
  if($("input:checkbox:checked").length > 0)
    $("#generateListForm").submit();
  else
    Materialize.toast('Nenhuma loja selecionada!', 4000);
}

function hidePanel(id){
  let ref = $('#'+id);
  if(ref.attr('hidden') === undefined || ref.attr === false)
    ref.attr('hidden', 'hidden');
  else
    ref.removeAttr('hidden');
}