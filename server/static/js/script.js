$(document).ready(function(){
	$('.btn').click(function(){
		var slotID = this.id;
		$.getJSON($SCRIPT_ROOT + '/_bookTime', {
			id : slotID,
		}, function(data) {
			alert("Slot Booked");
			window.location.replace("/");						
		}).fail(function (jqXHR, exception) {
			failError(jqXHR, exception)
		});
	})
	
	// Server Error
	function failError(jqXHR, exception) {
		var msg = '';
		if (jqXHR.status === 0) {
			msg = 'Not connected, Verify Network Connection.';
		} else if (jqXHR.status == 404) {
			msg = 'Requested page not found. [404]';
		} else if (jqXHR.status == 406) {
			msg = 'Please choose an appropriate date [406]';
		} else if (jqXHR.status == 500) {
			msg = 'Internal Server Error [500]';
		} else if (exception === 'parsererror') {
			msg = 'Requested JSON parse failed.';
		} else if (exception === 'timeout') {
			msg = 'Time out error.';
		} else if (exception === 'abort') {
			msg = 'Ajax request aborted.';
		} else {
			msg = jqXHR.responseText;
		}
		alert(msg)
	}
})
// 		// Hide input Date fields and slot table
// 		$("#OTDate, #RecDate, #TimeSlots").hide()
// 		$("#OTDateBtn").click(function(){
// 			$("#OTDate").toggle()
// 		})
// 		$("#RecDateBtn").click(function(){
// 			$("#RecDate").toggle();
// 		})
// 		$("#Close").click(function(){
// 			$("#TimeSlots").hide()
// 		})
// 	// Enable Tooltip
// 	$("body").tooltip({ selector: '[data-toggle=tooltip]' });
// 	// Provides table of available slots
// 	$("#OTTimeBtn").on("click", function() {
// 		$("#OTRadioBtn").prop("checked", true);
// 		$("#RecRadioBtn").prop("checked", false);
// 		$.getJSON($SCRIPT_ROOT + '/_getSlots', {
// 			date: $('input[name="Date"]').val()
// 		}).done(function(data) {				
// 			getTable(data)				
// 		}).fail(function (jqXHR, exception) {
// 			failError(jqXHR, exception)
// 		});
// 	})
// 	$("#RecTimeBtn").on("click", function() {
// 		$("#OTRadioBtn").prop("checked", false);
// 		$("#RecRadioBtn").prop("checked", true);
// 		$.getJSON($SCRIPT_ROOT + '/_getSlots', {
// 			date: $('input[name="RecDate"]').val(),
// 			type: $('#RecType option:selected').val()				
// 		}).done(function(data) {
// 			getTable(data)
// 		}).fail(function (jqXHR, exception) {
// 			failError(jqXHR, exception)
// 		})
// 	})
// 	// Handles When a slot is booked through cell click 
// 	$('#timeTable').on('click', 'td' , function(){
// 		var slotID = this.id;
// 		var Zone = $('#Zone option:selected').val()
// 		var Class =  $(this).attr('class')
// 		switch (Class){
// 			// If slot is available
// 			case "bg-info":
// 			case "bg-success":
// 			if($('#OTRadioBtn').is(':checked')) {
// 				$.getJSON($SCRIPT_ROOT + '/_bookTime', {
// 					date: $('input[name="Date"]').val(),
// 					id : slotID,
// 					zone: Zone
// 				}, function(data) {
// 					alert("Slot Booked");
// 					location.reload();						
// 				}).fail(function (jqXHR, exception) {
// 					failError(jqXHR, exception)
// 				});
// 			} else if ($('#RecRadioBtn').is(':checked')) {
// 				if (checkTime(slotID) == false) {
// 					break;
// 				} 
// 				$.getJSON($SCRIPT_ROOT + '/_bookTime', {
// 					date: $('input[name="RecDate"]').val(),
// 					id : slotID,
// 					type: $('#RecType option:selected').val(),
// 					zone: Zone
// 				}, function(data) {
// 					if(data){
// 						alert("Task could not be booked as, " +  data +  " was fully booked");
// 					} else{
// 						alert("Slot Booked");
// 						location.reload(); 	
// 					}
// 				}).fail(function (jqXHR, exception) {
// 					failError(jqXHR, exception)
// 				})	
// 			};
// 			break

// 			// If its too late to book the slot
// 			case "bg-secondary":
// 			alert("Grey slots cannot be booked");
// 			break;

// 			// If the slot is previously booked
// 			case "bg-warning":
// 			if ($('#OTRadioBtn').is(':checked')){
// 				// Confirm shifting the current slot
// 				var suggestedId = getSuggestedId()
// 				var Confirm = confirm("Tasks booked on this slot will be shifted to the closest available slot");
// 				if (Confirm == false) {
// 					break;
// 				} 
// 				$.getJSON($SCRIPT_ROOT + '/_bookTime', {
// 					date: $('input[name="Date"]').val(),
// 					id : slotID,
// 					suggestedId: suggestedId,
// 					zone: Zone
// 				}, function(data) {
// 					alert("Slot Booked");
// 					location.reload(); 						
// 				}).fail(function (jqXHR, exception) {
// 					failError(jqXHR, exception)
// 				})

// 			} else if ($('#RecRadioBtn').is(':checked')) { 
// 				if (checkTime(slotID) == false) {
// 					break;
// 				} 
// 				// Since it is a recurrent Task, multiple clashes may exist
// 				var Confirm = confirm("Tasks booked on this slot will be shifted to the closest available slot");
// 				if (Confirm == false) {
// 					break;
// 				} 
// 				$.getJSON($SCRIPT_ROOT + '/_bookTime', {
// 					date: $('input[name="RecDate"]').val(),
// 					id : slotID,
// 					type: $('#RecType option:selected').val(),
// 					zone: Zone
// 				}, function(data) {
// 					if(data){
// 						alert("Task could not be booked as, " +  data +  " was fully booked");
// 					} else{
// 						alert("Slot Booked");
// 						location.reload(); 	
// 					}
// 				}).fail(function (jqXHR, exception) {
// 					failError(jqXHR, exception)
// 				})	
// 			}
// 			break;
// 			default:
// 			alert("Slot Color Error, please try again")
// 		}
// 	});

// 	// Confirm Slot Button is clicked
// 	$("#ConfirmSlot").click(function(){
// 		var Zone = $('#Zone option:selected').val()
// 		var suggestedId = getSuggestedId()
// 		if (suggestedId == -1 ){
// 			alert("No suitable slots available, Please click a Slot");
// 		} 
// 		else if ($('#OTRadioBtn').is(':checked')) {
// 			$.getJSON($SCRIPT_ROOT + '/_bookTime', {
// 				date: $('input[name="Date"]').val(),
// 				id : suggestedId,
// 				zone: Zone
// 			}, function(data) {
// 				alert("Slot Booked");
// 				location.reload();						
// 			}).fail(function (jqXHR, exception) {
// 				failError(jqXHR, exception)
// 			})
// 		}			
// 		else if ($('#RecRadioBtn').is(':checked')) {
// 			if (checkTime(suggestedId) == true) {				
// 				$.getJSON($SCRIPT_ROOT + '/_bookTime', {
// 					date: $('input[name="RecDate"]').val(),
// 					type: $('#RecType option:selected').val(),
// 					id: suggestedId,
// 					zone: Zone
// 				}, function(data) {
// 					alert("Slot Booked");
// 					location.reload(); 	
// 				}).fail(function (jqXHR, exception) {
// 					failError(jqXHR, exception)
// 				})
// 			}	
// 		}
// 	})
// 	function checkTime(slotID) {
// 		var fullDate  = new Date();
// 		var twoDigitMonth = ((fullDate.getMonth().length+1) === 1)? (fullDate.getMonth()+1) : '0' 
// 		+ (fullDate.getMonth()+1);
// 		var twoDigitDate = ((fullDate.getDate().length+1) === 1)? (fullDate.getDate()) : '0' 
// 		+ (fullDate.getDate());
// 		var currentDate = fullDate.getFullYear()  + "-" + twoDigitMonth + "-" + twoDigitDate;
// 		if ($('input[name="RecDate"]').val() == currentDate){
// 			bookTime = slotID * 60
// 			currentTime = fullDate.getHours() * 60 + fullDate.getMinutes()
// 			if (currentTime > bookTime){
// 				var Confirm = confirm("Can't book slot Today, book remaining slots?");
// 				if (Confirm == false) {
// 					return false
// 				}
// 			}
// 		}
// 		return true
// 	}
// 	function getTable(data){
// 		var table = ''
// 		var id=0
// 		$.each(data, function(key, value){
// 			table += '<td id = '+ id +' class=' + value[0] + ' data-toggle="tooltip" title="' 
// 			+ value[1] + '" ></td>';
// 			id += 1;
// 		})
// 		var tableRow = '<tr id="myTableRow">' + table + '</tr>'
// 		$("#myTableRow").replaceWith(tableRow);
// 		$("#TimeSlots").show()
// 	}
// 	function getSuggestedId(){
// 		var suggestedId = -1
// 		var i = 0
// 			// Get the suggested Slot
// 			$("td").each(function() {
// 				tdClass = $(this).attr('class');
// 				if (tdClass == "bg-info"){
// 					suggestedId = i;
// 					return suggestedId;
// 				}					
// 				i+= 1;
// 			});
// 			return suggestedId
// 		}
// 	// Server Error
// 	function failError(jqXHR, exception) {
// 		var msg = '';
// 		if (jqXHR.status === 0) {
// 			msg = 'Not connected, Verify Network Connection.';
// 		} else if (jqXHR.status == 404) {
// 			msg = 'Requested page not found. [404]';
// 		} else if (jqXHR.status == 406) {
// 			msg = 'Please choose an appropriate date [406]';
// 		} else if (jqXHR.status == 500) {
// 			msg = 'Internal Server Error [500]';
// 		} else if (exception === 'parsererror') {
// 			msg = 'Requested JSON parse failed.';
// 		} else if (exception === 'timeout') {
// 			msg = 'Time out error.';
// 		} else if (exception === 'abort') {
// 			msg = 'Ajax request aborted.';
// 		} else {
// 			msg = jqXHR.responseText;
// 		}
// 		alert(msg)
// 	}
// });