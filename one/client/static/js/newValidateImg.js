$(document).on("click",".newValidateMostDiv",function(){
var newCanvas = document.getElementById("newCanvas");//演员
var newcontext = newCanvas.getContext("2d");//舞台，getContext() 方法可返回一个对象，该对象提供了用于在画布上绘图的方法和属性。
var newbutton = document.getElementById("phoneNotePutIn");//获取按钮
var newinput = document.getElementById ("newPhoneInput");//获取输入框
var newValidateMostDiv = document.getElementById("newValidateMostDiv"); //获取图片验证码跟换一下总盒子


newcontext.clearRect(0, 0, 120, 40);
newDraw();
newValidateMostDiv.onclick = function () {
    newcontext.clearRect(0, 0, 120, 40);//在给定的矩形内清除指定的像素
        newDraw();
        }

// 随机颜色函数
function getColor() {
    var r = Math.floor(Math.random() * 256);
    var g = Math.floor(Math.random() * 256);
    var b = Math.floor(Math.random() * 256);
    return "rgb(" + r + "," + g + "," + b + ")";
}
function newDraw() {
    newcontext.strokeRect(0, 0, 120, 40);//绘制矩形（无填充）
    var aCode = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"];
    // 绘制字母
    var newArr = [] //定义一个数组用来接收产生的随机数
    var newNum //定义容器接收验证码
    for (var i = 0; i < 4; i++) {
        var x = 20 + i * 20;//每个字母之间间隔20
        var y = 20 + 10 * Math.random();//y轴方向位置为20-30随机
        var index = Math.floor(Math.random() * aCode.length);//随机索引值
        var newTxt = aCode[index];
        newcontext.font = "bold 20px 微软雅黑";//设置或返回文本内容的当前字体属性
        newcontext.fillStyle=getColor();//设置或返回用于填充绘画的颜色、渐变或模式，随机
        newcontext.translate(x,y);//重新映射画布上的 (0,0) 位置，字母不可以旋转移动，所以移动容器
        var deg=90*Math.random()*Math.PI/180;//0-90度随机旋转
        newcontext.rotate(deg);// 	旋转当前绘图
        newcontext.fillText(newTxt, 0, 0);//在画布上绘制“被填充的”文本
        newcontext.rotate(-deg);//将画布旋转回初始状态
        newcontext.translate(-x,-y);//将画布移动回初始状态
        newArr[i] = newTxt //接收产生的随机数
    }
    newNum = newArr[0] + newArr[1] + newArr[2] + newArr[3] //将产生的验证码放入newNum
    console.log('验证码 ',newNum)
    // 绘制干扰线条
    for (var i = 0; i < 8; i++) {
        newcontext.beginPath();//起始一条路径，或重置当前路径
        newcontext.moveTo(Math.random() * 120, Math.random() * 40);//把路径移动到画布中的随机点，不创建线条
        newcontext.lineTo(Math.random() * 120, Math.random() * 40);//添加一个新点，然后在画布中创建从该点到最后指定点的线条
        newcontext.strokeStyle=getColor();//随机线条颜色
        newcontext.stroke();// 	绘制已定义的路径
    }
    // 绘制干扰点，和上述步骤一样，此处用长度为1的线代替点
    for (var i = 0; i < 20; i++) {
        newcontext.beginPath();
        var x = Math.random() * 120;
        var y = Math.random() * 40;
        newcontext.moveTo(x, y);
        newcontext.lineTo(x + 1, y + 1);
        newcontext.strokeStyle=getColor();
        newcontext.stroke();
    }

    //点击按钮验证
    newbutton.onclick = function () { 
        
    var newText = newinput.value //获取输入框的值
    if (newText === newNum) {
//        alert('验证通过')
        // alert('验证通过')
       newPhone()
        

    } else {
        alert('验证失败')
    }
    }
    
}

})