$(document).ready(function(){

    $('#myTable').on('keypress', 'input', function(event) {
        if (event.keyCode == 13 ) {
            event.preventDefault();
        }
    })

    function calculateSum(myThis){
        const row = myThis.parent().closest("tr")
        const price = parseFloat(row.find('.good_supp_price').val())
        const quantity = parseFloat(row.find('.good_quantity').val())
        const good_sum = row.find('.good_sum')
        good_sum.html(parseFloat(price*quantity).toFixed(2))
        good_sum.change()
        CalculateTotal()
    }

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
            my_tr.append($("<td></td>").append($("<input>").attr({class: 'good_id', name:'good_id', value: data['id']}).prop('readonly', true)))
            my_tr.append($("<td></td>").attr({class: 'good_name'}).text(data['name']))
            my_tr.append($("<td></td>").append($("<input>").attr({class: 'good_quantity', autocomplete: "off", name:'good_quantity', type: 'number', step: '1', min: '1', value: '1' }).prop('required', true)))
            my_tr.append($("<td></td>").append($("<input>").attr({type: 'number', step: '0.01', min: '1.00', class: 'good_supp_price', name:'good_supp_price', value: data['supp_price']}).prop('required', true)))
            my_tr.append($("<td></td>").append($("<input>").attr({type: 'number', step: '0.01', min: '1.00', class: 'good_price', name:'good_price', value: data['price']}).prop('required', true)))
            my_tr.append($("<td></td>").attr({class: 'good_sum'}).text(parseFloat(data.supp_price).toFixed(2)))
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

    function send_barcode(){
        const my_url = $('#search_book_btn').attr("data-url")
        const mydata = {
            'search_book': $('#search_book').val(),
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
        }
        myAjax(function(data) {
            if(data.id){
                addRow(data)
            }
            else{
                alert('Штрих-код не найден!')
            }
        }, my_url, mydata)
    }

    $('#search_book').on('keypress', function(event) {
        if (event.keyCode == 13 ) {
            event.preventDefault()
            send_barcode()
        }
    })

    $('#search_book_btn').click(function(e) {
        send_barcode()
    })

    $('#documentForm').submit(function(e) {
        e.preventDefault()
        let data = []
        $('#myTable > tbody > tr').each(function() {
            data.push(
                {'id' : $(this).find(".good_id").val(), 'qty': $(this).find(".good_quantity").val(), 'supp_price': $(this).find(".good_supp_price").val(), 'sell_price': $(this).find(".good_price").val()}
            )
        })
        const jsonData = JSON.stringify(data);
        const myArray = {
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
            'doc_date': $("#id_doc_date").val(),
            'supplier': $("#id_supplier").val(),
            'data': jsonData,
        }
        const form = $(this)
        myAjax(function(data) {
            if(data.id){
                $('#doc_id').val(data.id)
                $('#doc_id').change()
            }
            else{
                console.log(data)
            }
        }, form.attr('action'), myArray, form.attr('method'))
    })
    
    $('#doc_id').change(function(){
        const myUrl = '/acceptance_detail/' + $('#doc_id').val() + '/'
        $('#documentForm').attr('action', myUrl)
    })

    $('#myTable').on('change', '.good_quantity', function(){
        const myThis = $(this)
        calculateSum(myThis)
    })
    
    $('#myTable').on('change', '.good_supp_price', function(){
        const myThis = $(this)
        calculateSum(myThis)
    })

    $("#myTable").on("click", ".good_delete", function() {
        $(this).closest("tr").remove()
        CalculateTotal()
    })

})