$(document).ready(function(){
	$('#BatteryCharge').slider({
		formatter: function(value) {
			return 'Charge until: ' + value + "%";
		}
	});
	$('.btn-success').click(function(){
		var slotID = this.id;
		$('#bookingModal').modal('toggle');
		$('#SaveBtn').click(function(){
			$('#bookingModal').modal('toggle');
			$.getJSON($SCRIPT_ROOT + '/_bookTime', {
				id : slotID,
			}, function(data) {
				alert("Slot Booked");
				window.location.replace("/timing");						
			}).fail(function (jqXHR, exception) {
				failError(jqXHR, exception)
			});
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
