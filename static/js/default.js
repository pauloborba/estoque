function editItem(item_id){
  var csrftoken = Cookies.get('csrftoken');

  var promise = new Promise(function(resolve, reject){
    $.ajax({
      type: "POST",
      url: "/editItem/",
      data: {id: item_id, csrfmiddlewaretoken: csrftoken},
      success: function(data){
        resolve(data);
      },
      error: function(jqXHR, err){
        reject("fudeu");
      }
    });

  });
  var item = $('#item'+item_id);
  if(item.hasClass("label-success")){
    item.removeClass("label-success");
    item.addClass("label-danger");
    item.html("Ended up");
  }
  else {
    item.removeClass("label-danger");
    item.addClass("label-success");
    item.html("Enough");
  }


  promise.then(function(result){
    $('#userPoints').html("You've got "+result+" points.");
    $('#userPointsNav').html(result);
  }, function(error){
    alert("Some error ocurred. Sorry!");
    if(item.hasClass("label-success")){
      item.removeClass("label-success");
      item.addClass("label-danger");
      item.html("Ended up");
    }
    else {
      item.removeClass("label-danger");
      item.addClass("label-success");
      item.html("Enough");
    }
  });

}

function openItemModal(name, url){
  document.getElementById("itemName").innerHTML = "Atualizar " + name;
  document.modalForm.action = url;
}

function hideSideNav(){
  $("#test").addClass("hidden");
}

function isValid(strInp){
  return (strInp && strInp.length !== 0);
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
