let ws = require("nodejs-websocket")

let allUserData = new Array()
let historyMsg = new Array()
let historyAddFriendMsg = new Array()
let server = ws.createServer((conn) => {
    conn.on("text", function (message){
        let msgObj = JSON.parse(message)
        let isFriendOnline = false
        let friendIndex = 0
        switch (msgObj.type) {
            case 1:
                for (let userData in allUserData){
                    if (allUserData[userData].userID == msgObj.userID){
                        isFriendOnline = true
                        friendIndex = userData
                        break
                    }
                }
                if (isFriendOnline){
                    allUserData[friendIndex].conn.sendText(JSON.stringify(msgObj))
                }else{
                    msgObj.msgStatus = 1
                    historyMsg.push(msgObj)
                }
                break;
            case 2:
                for (let userData in allUserData){
                    if (allUserData[userData].userID == msgObj.userID){
                        if (allUserData[userData].userStatus === 1) {
                            isFriendOnline = true
                            friendIndex = userData
                        }
                    }
                }
                if (isFriendOnline){
                    allUserData[friendIndex].conn.sendText(JSON.stringify(msgObj))
                }else{
                    msgObj.msgStatus = 1
                    historyAddFriendMsg.push(msgObj)
                }
                break;
            case 3:
                let isHaveUser = false;
                let userIndex = 0
                for (let userData in allUserData){
                    if (allUserData[userData].userID === msgObj.userID){
                        isHaveUser = true
                        userIndex = userData
                    }
                }
                break;
            }
    })
})