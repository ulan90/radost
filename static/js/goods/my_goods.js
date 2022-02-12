$(document).ready(function(){

    $("#myTable > tbody").on("click", ".btn-del", function(){
        const id = $(this).attr("data-gid")
        const csrf = $("input[name=csrfmiddlewaretoken]").val()
        mydata = { gid: id, 'csrfmiddlewaretoken': csrf }
        mythis = this
        $.ajax({
            url: "delete_good/",
            method: 'POST',
            data: mydata,
            dataType: 'json',
            success: function(data){
                if(data.status == 1){
                    $(mythis).closest('tr').fadeOut();
                    $("#msg").text("Товар успешно удален!")
                }
                if(data.status == 0){
                    $("#msg").text("Возникла ошибка при удалении!")
                }
                $("#msg").show()
            }
        })
    })

})