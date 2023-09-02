async function joinPlan(){

    let button = document.getElementById('joinButton')
    let planID = button.getAttribute('data-planID');
    let userID = button.getAttribute('data-userID');
    
    let serverReq = new Request(`${window.origin}/tasks`,
                                 {'headers': {"Content-type": "application/json; charset=UTF-8",
                                              "Task": "add-user-to-plan"},
                                  'method': 'POST',
                                  'body' : JSON.stringify({'planID':planID, 'userID':userID})}
                                );
    let returnData = await fetch(serverReq);
    let jsondata = await returnData.json();

    if (jsondata['success']){
        button.remove();
        document.getElementById('joinInfo').textContent = 'You were successfully added to the plan!'
    }
    
}

