$(document).ready(function(){

    //Чтобы кнопка Enter не отправляла форму
    $('#products_table').on('keypress', 'input', function(event) {
        if (event.keyCode == 13 ) {
            event.preventDefault();
        }
    })

    function CalculateTotal() {
        let grandT = 0
        $("#myTable > TBODY > tr").each(function () {
            let tmp_sum = parseFloat($(this).find('.good_sum').html())
            if (!isNaN(tmp_sum)) {
                grandT += parseFloat(tmp_sum)
            }
        })
        $("#gTotal").html(grandT.toFixed(2))
    }

    function addRow(data){
        let found_sameId = false
        $("#myTable > TBODY > tr").each(function () {
            const tmp_idVal = $(this).find('.good_id').val()
            const tmp_qtyVal = $(this).find('.good_quantity')
            if(parseInt(tmp_idVal)===data.id){
                tmp_qtyVal.val(parseInt(tmp_qtyVal.val()) + 1)
                tmp_qtyVal.change()
                found_sameId = true
                return false
            }
        })
        if(!found_sameId){
            const my_tbody =  $("#myTable > TBODY")
            const my_tr = $("<tr></tr>")
            for (const [key, value] of Object.entries(data)) {
                if(key === 'name'){
                    my_tr.append($("<td></td>").attr({class: 'good_'+key}).text(value))
                    my_tr.append($("<td></td>").append($("<input>").attr({class: 'good_quantity', autocomplete: "off", name:'good_quantity', type: 'number', step: '1', min: '1', value: '1' })))
                }
                else{
                    my_tr.append($("<td></td>").append($("<input>").attr({class: 'good_'+key, name:'good_'+key, value: value}).prop('readonly', true)))
                }
            }
            my_tr.append($("<td></td>").attr({class: 'good_sum'}).text(data.price))
            my_tr.append($("<td></td>").append($("<button></button>").attr({class: 'good_delete', type: 'button'}).text('Удалить')))
            my_tbody.append(my_tr)
            found_sameId = false
            CalculateTotal()
        }
    }
    
    function myAjax(callback, my_url, my_data, my_type='POST', my_dataType='json') {
        $.ajax({
            url: my_url,
            type: my_type,
            data: my_data,
            dataType: my_dataType,
        }).then(function (resp) {
            callback(resp)
        }).fail(function () {
            $("#msg").text("Ошибка отправки")
            $("#msg").show('slow').delay(2000).hide('slow')
        })
    }

    $('#search_barcode_form').submit(function(e) {
        e.preventDefault()
        const form = $(this)
        myAjax(function(data) {
            if(data.id){
                addRow(data)
            }
            else{
                alert('Штрих-код не найден!')
            }
        }, form.attr('action'), form.serialize(), form.attr('method'))
    })

    $('#myTable').on('change', '.good_quantity', function(){
        const row = $(this).parent().closest("tr")
        const price = parseFloat(row.find('.good_price').val())
        const quantity = parseFloat(row.find('.good_quantity').val())
        const good_sum = row.find('.good_sum')
        let a = parseFloat(price*quantity).toFixed(2)
        good_sum.html(parseFloat(price*quantity).toFixed(2))
        good_sum.change()
        CalculateTotal()
    })

    $("#myTable").on("click", ".good_delete", function() {
        $(this).closest("tr").remove()
        CalculateTotal()
     });
})