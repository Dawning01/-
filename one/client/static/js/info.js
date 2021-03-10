

//        $('.setItem:eq(4)').css('display','block','background-color', 'aqua')
//        $('.rightArrow:eq(4)').attr('src',"../static/images/bottom.png")
//        $('.setItem img').removeClass('setItemImg')
//        // $('.setItem:eq(4) img:eq(1)').toggleClass('setItemImg')
//        $('.setItem:eq(4) img:eq(0)').addClass('setItemImg').siblings().removeClass('setItemImg')
//        $('.setItem:eq(4) .setItemA:eq(0)').addClass('setItemBackground')
//        console.log('在setItem后面')
        $('.directoryItem').on("click",function(){
        if(  $(this).children('.setItem').css('display')=='none' ){
            // 其他 都清除样式
            $('.setItem').css('display','none')
            $('.rightArrow').attr('src',"../static/images/right.png")
             // 自己添加样式
            console.log('执行啦')
            $(this).children('.setItem').css('display','block')
            $(this).find('.rightArrow').attr('src',"../static/images/bottom.png")



        }else{
            $(this).children('.setItem').css('display','none')
            $(this).find('.rightArrow').attr('src',"../static/images/right.png")
        }

        })




$(document).on("mouseover",'.progressRightChaDiv',function(){
 $(this).find('img').attr('src',"../static/images/cha2.png")

})
$(document).on("mouseout",'.progressRightChaDiv',function(){
  $(this).find('img').attr('src',"../static/images/cha1.png")

})

//        $('.progressRightChaDiv').mouseover(function(){
//            console.log('叉 开始啦')
//            $(this).find('img').attr('src',"../static/images/cha2.png")
//
//        })
//        $('.progressRightChaDiv').mouseout(function(){
//            console.log('叉 开始啦')
//            $(this).find('img').attr('src',"../static/images/cha1.png")
//
//        })
$(document).on("mouseover",'.text-c:eq(1) a',function(){
  $('.text-c:eq(1) a').css({'color':'#3899dd','text-decoration':'underline'})

})
$(document).on("mouseout",'.text-c:eq(1) a',function(){
   $('.text-c:eq(1) a').css({'color':'#333',
                                        'text-decoration':'none'} )

})

//        $('.text-c:eq(1) a').mouseover(function(){
//
//            $('.text-c:eq(1) a').css({'color':'#3899dd','text-decoration':'underline'})
//
//        })
//        $('.text-c:eq(1) a').mouseout(function(){
//
//            $('.text-c:eq(1) a').css({'color':'#333',
//                                        'text-decoration':'none'}
//
//            )
//
//        })

  // 添加选中状态
        $('.VBiAdd').click(function(){
            // $(this).toggleClass('Hook')
            $(this).addClass('Hook').siblings().removeClass('Hook')
        })
        $('.VBipaymentFashion').click(function(){
            $(this).addClass('Hook').siblings().removeClass('Hook')
        })

        $('.jumpPayment').click(function(){
            $('.orderFormMostDiv').css('display','block')

        })

        $('.cancelPayment').click(function(){
//            var obj=document.getE


//                var clearOrderForm= document.getElementsByClassName("clearOrderForm")
//                clearOrderForm

            $('.orderFormMostDiv').css('display','none')
        }

        )

 $(document).on("click",".phoneSave",function(){
            $('.formerlyPhoneMostDiv').css('display','none');
            $('#phoneForm').css('display','block');

        })

function fullNoneBox(){
        var htmlss='';

        var chooseName=$('#VBiuserVerifyInput').val()
        //充值的钱
        var chooseViLiB=$('.VBiAdd.Hook b').html()
        //充值的v币
        var chooseViLiSpan=$('.VBiAdd.Hook span').html()

        console.log(chooseViLiB)
        console.log(chooseViLiSpan)

        console.log("已经开始")

         htmlss=`
        <li style="padding-left:30px"><b>充值用户:</b><p class="">${chooseName}</p></li>
        <li style="padding-left:30px ;border-top: 1px solid #e5e5e5"><b>充值V币:</b><p class="">${chooseViLiSpan}</p>V币</li>

        <li style="padding-left:30px"><b>实付金额:</b><p class="">${chooseViLiB}</p>  </li>
        <input onclick="blackPayment()" class="blackPayment" type="button" value="支付宝支付">
        `
        $('.clearOrderForm').text('')
        $('.clearOrderForm').append(htmlss);

        }