function addCookieItem(prdid , action){
    console.log("not loged in")
    if (action == 'add'){//وقت المستخدم يلي مانو مسجل دخول يضغط على اضافة منشوف بالكوكيز يلي عنا اذا مانو معرف الاي دي تبع المنتج منضيفو واذا معرف منزيد الكمية
        if (cart[prdid] == undefined){
            cart[prdid] = {'quantity' : 1}
        }
        else{
            cart[prdid]['quantity'] += 1
        }
    }

    if (action == 'remove'){
        cart[prdid]['quantity'] -= 1

        if (cart[prdid]['quantity'] <= 0){//بعد ما ننقص بدنا نحط شرط مشان نشوف اذا المنتج بدنا نحذفو ولا لا

            console.log('remove item')
            delete cart[prdid]
        }
    }

    console.log("cart:" , cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

    location.reload()
}

function updateuserorder(prdid , action){
    console.log('user is auth, sending data')

    var url = '/updateitem/'

    fetch(url , {
        method:'POST',
        headers:{
            'Content_Type':'application/json',
            'X-CSRFToken': csrftoken,//هي الطريقة بالجافا سكريبت لنحل مشكلة التوكن وفينا نوصل لهي القيمة لان موجودة بسكريبت الماين كمان كل التيمبلت تورث من الماين
        },
        body:JSON.stringify({'prdid':prdid,'action':action})//بعتنا المعلومات لاب ديت ايتم بالفيو بس مدري ليش خلاه سترينغ
    })
    .then((response) => {//بعد مانخلص ارسال الداتا رح يجينا ريسبونس من الفيو سماه بروميس ,,انو كلشي صار تمام وارسلها الفيو كجيسن
        return response.json()

    })

    .then((data) => {//هلق بدنا نعرض الداتا يلي اجت بعد الريسبونس
        console.log('data:',data)
        location.reload()//هاي لتحديث الصفحة مشان قيم الكارت تتحدث
        
    })
}
///////////////////////////////////////////////this 
var user = '{{request.user}}'
function getToken(name) {
let cookieValue = null;
if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
return cookieValue;
}
const csrftoken = getToken('csrftoken');

/////////////////////////////////////////////////////////////////////////
//المهم بهاد التابع انو بيجيب الكوكيز يلي عنا بالمتصفح عن طريق اسما منمررو واذا مافي كوكيز بهاد الاسم بيرجع نول هاد الكود غير يل ذاكرو بالكورس يلي بالكورس بيضل يانشئ كوكيز جديدة
function getCookie(name) {
var nameEQ = name + "=";
var ca = document.cookie.split(';');
for (var i = 0; i < ca.length; i++) {
var c = ca[i];
while (c.charAt(0) == ' ') c = c.substring(1, c.length);
if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
}
return null;
}
var cart = JSON.parse(getCookie('cart'))//جبنا الكوكيز عن طريق اسمها وحطيناها بمتحول
console.log(cart)

if (cart == undefined){// اذا ماكان عنا كوكيز منحليها فاضية ومنبعتا للمتصفح بعد مانقصرها لسترينغ لان لازم تكون قيمة وحيدة مو اوبجكت
cart = {}
console.log('cart created')
document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
//هاي الطريقة لنبعت كوكيز للمتصفح فيك تشوفها هلق بالمتصفح من الابليكيشن واخر قيمة مشان نخلي الكوكيز للدومين تبع الموقع مشان مايضل يانشئ كوكيز جديدة بكل صفحة
}

console.log('cart:' , cart)
