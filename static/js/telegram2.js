var tele_con = {
    token: "6369828560:AAHSgKJoC07OAmb1BP7Qq3luqlDV7vU0JGc", // Your bot's token that got from @BotFather
    chat_id: "867971529" // The user's(that you want to send a message) telegram chat id
 }


 async function sendMessage(text)
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