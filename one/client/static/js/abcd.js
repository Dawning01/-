$('.setItem:eq(4)').css('display','block','background-color', 'aqua')
        $('.rightArrow:eq(4)').attr('src',"../../static/img/bottom.png")
        $('.setItem img').removeClass('setItemImg')
        // $('.setItem:eq(4) img:eq(1)').toggleClass('setItemImg')
        $('.setItem:eq(4) img:eq(2)').addClass('setItemImg').siblings().removeClass('setItemImg')
        $('.setItem:eq(4) .setItemA:eq(2)').addClass('setItemBackground')

        $('.directoryItem').on("click",function(){
        if(  $(this).children('.setItem').css('display')=='none' ){
            // 其他 都清除样式
            $('.setItem').css('display','none')
            $('.rightArrow').attr('src',"../../static/img/right.png")
             // 自己添加样式
            console.log('执行啦')
            $(this).children('.setItem').css('display','block')
            $(this).find('.rightArrow').attr('src',"../../static/img/bottom.png")

            console.log('.setItemImg执行前')

            $(this).children('.setItem img').addClass('setItemImg').siblings().removeClass('setItemImg')
            // console.log($(this).find('.rightArrow').length)
            // console.log( $(this).children('.rightArrow'))
            console.log('.setItemImg执行后')


        }else{
            $(this).children('.setItem').css('display','none')
            $(this).find('.rightArrow').attr('src',"../../static/img/right.png")
        }

        })