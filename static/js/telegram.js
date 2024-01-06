var tl = {
   token: "6585324358:AAFSCd8Acp_eAMlg1JCp2_dI3eEJtfHvTUE", // Your bot's token that got from @BotFather
   chat_id: "867971529" // The user's(that you want to send a message) telegram chat id
}
// ===============for contact us==========
var tele_con = {
   token: "6369828560:AAHSgKJoC07OAmb1BP7Qq3luqlDV7vU0JGc", // Your bot's token that got from @BotFather
   chat_id: "867971529" // The user's(that you want to send a message) telegram chat id
}
/**
* By calling this function you can send message to a specific user()
* @param {String} the text to send
*
*/
async function sendMessage(text)
{
   const url = `https://api.telegram.org/bot${tl.token}/sendMessage?chat_id=${tl.chat_id}` // The url to request

   const obj = {
       chat_id: tl.chat_id, // Telegram chat id
       //card: arr, // array to send
       text: text // The text to send
   };

   const xht = new XMLHttpRequest();
   xht.open("POST", url, true);
   xht.setRequestHeader("Content-type", "application/json; charset=UTF-8");
   xht.send(JSON.stringify(obj));
}

// ==========for contact us==========
async function sendMessageContact(text)
{
   const url = `https://api.telegram.org/bot${tele_con.token}/sendMessage?chat_id=${tele_con.chat_id}` // The url to request

   const obj = {
       chat_id: tele_con.chat_id, // Telegram chat id
       //card: arr, // array to send
       text: text // The text to send
   };

   const xht = new XMLHttpRequest();
   xht.open("POST", url, true);
   xht.setRequestHeader("Content-type", "application/json; charset=UTF-8");
   xht.send(JSON.stringify(obj));
}


// Now you can send any text(even a form data) by calling sendMessage function.
// For example if you want to send the 'hello', you can call that function like this:

//sendMessage("hello");

// Bot token 5947359274:AAEw3xjBrSQdSnpK5nU40iiWKogqsLAY8zg
// chat id for me

// {
//    "update_id": 829776484,
//    "message": {
//        "message_id": 2234935,
//        "from": {
//            "id": 867971529,
//            "is_bot": false,
//            "first_name": "Hamze",
//            "last_name": "ibrahim",
//            "username": "hamzeib",
//            "language_code": "en"
//        },
//        "chat": {
//            "id": 867971529,
//            "first_name": "Hamze",
//            "last_name": "ibrahim",
//            "username": "hamzeib",
//            "type": "private"
//        },
//        "date": 1686039045,
//        "text": "/start",
//        "entities": [
//            {
//                "offset": 0,
//                "length": 6,
//                "type": "bot_command"
//            }
//        ]
//    }
// }



// AAAA-ABCDEF-ABCD
// AAAA-ABCDEF-ABCD
// AAAA-ABCDEF-ABC1
// AAAA-ABCDEF-ABC2
// AAAA-ABCDEF-ABC3
// AAAA-ABCDEF-ABC4
// AAAA-ABCDEF-ABC5
// AAAA-ABCDEF-ABC6
// AAAA-ABCDEF-ABC7
// AAAA-ABCDEF-ABC8
// AAAA-ABCDEF-ABC9
// AAAA-ABCDEF-AB10
// AAAA-ABCDEF-ABCD
// AAAA-ABCDEF-ABCD