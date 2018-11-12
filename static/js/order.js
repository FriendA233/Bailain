$(function () {
    $('#pay').click(function () {
        console.log('支付')

        var identifier=$(this).attr('identifier')
        $.get('/pay/',{'identifier':identifier},function (response) {
            window.open(response.alipay,target='_self')
        })
    })
})