$(function () {

    //单个选中
    $('.ann').click(function () {
        var cartid = $(this).attr('cartid')
        var $this = $(this)
        $.get('/changestatus/', {'cartid': cartid}, function (response) {
            console.log(response.isselect)
            $this.prop('checked', response.isselect)
            $('#total').html(response.paer)
        })
    })
    //全部选中
    $('.allchange').click(function () {
        var isselect = $(this).is(':checked')
        console.log(isselect)
        $.get('/allchange/', {'isselect': isselect}, function (response) {
            console.log(response.isselect)
            $(':checkbox').prop('checked',  response.isselect)
            $('#total').html(response.paer)
        })
    })
    
    //下单
    $('#generateorder').click(function () {
        $.get('/generateorder/',function (response) {
            console.log(response)
            if(response.status == 1){
                window.open('/orderinfo/'+response.identifier+'/',target='_self')
            }
        })
    })
})