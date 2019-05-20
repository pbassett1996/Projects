//Name: Peter Bassett
//Date: 20.05.2019
//Description: The following code integrates google sheets with my google calendar in order to create an itemised to do list. 

function sheetIntegration() {
  
  var sheet = SpreadsheetApp.getActiveSheet();

  
  //Find Headings
  var Headings = ["Life", "Study", "Fitness", "Work"];
  var EntryRows = [0, 0, 0, 0];
  
  var startRow = 1;
  var endRow = 100;
  var data = sheet.getRange("A1:A100").getValues();
  for(var j = 0; j < Headings.length; j++) {
    for (var i = 0; i < data.length; i++) {
      if(String(data[i]) == Headings[j]) {
        EntryRows[j] = i+2;
        j++
      }
    }
  }
 

  //Get Dates
  var beginDate = new Date();
  var weDate = new Date(String(sheet.getRange("H2").getValue()));  
  weDate.setDate(weDate.getDate()+1);
  beginDate.setDate(weDate.getDate() - 8);
  
  
  //Import events from calendar
  var cal = CalendarApp.getCalendarById("petermarkbassett@gmail.com") 
  var eventArray = cal.getEvents(beginDate, weDate); 
  for(var i = 0; i < eventArray.length; i++) {
    
    //Retreive information from calendar entries
    var name = eventArray[i].getTitle();
    var st = eventArray[i].getStartTime();
    var et = eventArray[i].getEndTime();
    var des = eventArray[i].getDescription();
    var color = eventArray[i].getColor();
    var hours = (et-st)/(360*10000);
    
    var Event = [name, st, hours, des]
    
    //Categorise events under calendar depending on colour
    switch(color){
      case "10": //10 = green (Life events)
        for(var k = 1; k <= 4; k++) {
          sheet.getRange(EntryRows[0],k).setValue(Event[k-1]);
        }
        EntryRows[0]++;
        break;
      case "5": //5 = Yellow (Study Events)
        for(var k = 1; k <= 4; k++) {
          sheet.getRange(EntryRows[1],k).setValue(Event[k-1]);
        }
        EntryRows[1]++;
        break;
      case "6": //6 = Orange (Fitness Events)
        for(var k = 1; k <= 4; k++) {
          sheet.getRange(EntryRows[2],k).setValue(Event[k-1]);
        }
        EntryRows[2]++;
        break;
      case "3": //3 = Purple (Work events)
        for(var k = 1; k <= 4; k++) {
          if (k == 3 | k == 4) {
            sheet.getRange(EntryRows[3],k+1).setValue(Event[k-1]);
          } else {
            sheet.getRange(EntryRows[3],k).setValue(Event[k-1]);
          }
        }
        
        var day = st.getDay();
        var minutes = st.getMinutes();  
        var hrs = st.getHours() + (minutes/60);
        var pay = 0;
        
        Logger.log(day)
        
        //Calculate pay depending on penalty rates
        for(var k = 0; k <= hours; k = k + 0.5) {
          if(day == 6) { //Saturday
            pay = pay + 0.5*31.37;
          } else if (day == 0) { //Sunday
            pay = pay+ 0.5*36.59;
          } else if(hrs + k < 19.0) {
            pay = pay + 0.5*26.14;
          } else if(hrs + k < 24.0) {
            pay = pay + 0.5*28.34;
          } else {
            pay = pay + 0.5*29.45;
          }
        }
        
        sheet.getRange(EntryRows[3], 5).setValue(pay);
        EntryRows[3]++;
        break;


    }
    
    
  }
  
  sheet.autoResizeColumns(1, 3)
  
}
