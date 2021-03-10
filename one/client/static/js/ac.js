var countdown=60;
	function settime(obj) {
    	if (countdown == 0) {
        	obj.removeAttribute("disabled");
        	obj.value="免费获取验证码";
			countdown = 60;
			return;
    	} else {
        	obj.setAttribute("disabled", true);
        	obj.value="重新发送(" + countdown + ")";
        	countdown--;
    	}
		setTimeout(function() {
    		settime(obj) }
    	,1000)
	}
var	qu=[
	{
			'cityId': 1001, 'cityName': '你父亲的名字',
	}
	,
	{
			'cityId': 1002, 'cityName': '你母亲的名字',	
	}
	,
	{
			'cityId': 1003, 'cityName': '你的爱好',	
	}
	,
	{
			'cityId': 1004, 'cityName': '你毕业于那个学校',	
	}
	,
	{
			'cityId': 1005, 'cityName': '你喜欢看的电影',	
	}
	,
	{
			'cityId': 1006, 'cityName': '你喜欢玩的游戏',	
	}
	,
	{
			'cityId': 1007, 'cityName': '你的幸运数字是什么',	
	}
	,
	{
			'cityId': 1008, 'cityName': '你梦想的职业是什么',	
	}
	]
$.each(qu,function(i,o){
		// console.log(city);
		$('#question').append(`<option value="${o.cityId}">${o.cityName}</option>`)
	  })
	  console.log($('#city').val())
