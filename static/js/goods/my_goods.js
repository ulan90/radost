$(document).ready(function(){

    //Чтобы кнопка Enter не отправляла форму
    $('#create_container').on('keypress', 'input', function(event) {
        if (event.keyCode == 13 ) {
            event.preventDefault();
        }
    })

    //многофункциональная ajax функция
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

    //функция добавления input для штрихкода
	function addBarcode() {
        let count = $('.barcode_class').length
		if(count<5){
			let input = $('<div class="barcode_div"><p><input type="text" name="barcode" data-bar="'+(count+1)+'"class="barcode_class" maxlength="200" required><button type="button" class="removeRow">Удалить</button></p></div>')
			$('#create_good_form > .barcodes').append(input);
			++count
		}
	}

    //при нажатии кнопки добавить вызывается функция добавления штрихкода
    $('#create_container').on('click', '#add_barcode', function(){
        addBarcode()
    })
    
    //удаление input для штрихкода
    $('#create_container').on('click', '.removeRow', function () {
        $(this).closest('.barcode_div').remove();
    });

    //эта функция нужна для сравнения дублированных штрихкодов в input, дает понять какой из input пользователь нажал
    let focused_barcode = null
	let focused_bar_attr = null
	$('#create_container').on('mousedown', '.barcode_class', function(){
		focused_barcode = $(this).val()
		focused_bar_attr = $(this).attr("data-bar")
	})

    //Проверка одинаковых штрихкодов в input, если их нет то проверка дублирования в базе с помощью ajax
    let timeout = null
    let barcode_duplicate = null
    $('#create_container').on('keyup', '.barcode_class', function() {
        clearTimeout(timeout)
        const myThis = $(this)
        
        timeout = setTimeout(function() {
            const barcode = myThis.val() 
            let count = 0

            $('.barcode_class').each(function(){
                const next_barcode = $(this).val()
                const bar_attr = $(this).attr("data-bar")
                if (barcode === next_barcode && barcode !== '' && bar_attr !== focused_bar_attr){
                    count++
                    myThis.val(focused_barcode)
                    $("#msg").text("Нельзя вносить одинаковые штрих-коды!")
                    $("#msg").show('slow').delay(2000).hide('slow')
                    return false
                }
            })
            
            if(count == 0){
                const id = $("#good_id").val()
                const csrf = $("input[name=csrfmiddlewaretoken]").val()
                const mydata = { 'gid': id, 'barcode': barcode, 'csrfmiddlewaretoken': csrf }
                myAjax(function(data) {
                    //processing the response data
                    if(data.status === 1){
                        barcode_duplicate = data.good
                        $("#msg").text("Дублирование штрихкодов = " + barcode_duplicate)
                        $("#msg").show('slow').delay(2000).hide('slow')
                    }
                    else{
                        barcode_duplicate = null
                    }
                }, 'check_barcode/', mydata)
            }

        }, 500)
    })

    //чтобы кнопка сохранить не срабатывала при дублировании штрихкодов
    $('#create_container').on('submit', '#create_good_form', function( event ) {
        if( barcode_duplicate !== null){
            event.preventDefault(); // don't submit this
            $("#msg").text("Дублирование штрихкодов = " + barcode_duplicate)
            $("#msg").show('slow').delay(2000).hide('slow')
        }
    })

})