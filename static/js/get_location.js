window.onload = function(){
            var form = document.getElementById('get-location-btn')

            form.addEventListener("click", 
                        function getLocation(){

                            if (navigator.geolocation) {
                                navigator.geolocation.getCurrentPosition(showPosition, showError);
                            } else {
                                alert("Geolocation is not supported by this browser.");
                            }
                                

                        function showPosition(position) {
                        var latitude = position.coords.latitude;
                        var longitude = position.coords.longitude;
                        var data = {
                                float_value_1: latitude,
                                float_value_2: longitude,
                            };
                        var json_data = JSON.stringify(data);
                        console.log(json_data)

                        $.ajax({
                            url: '/update_location/',
                            type: "POST",
                            contentType: 'application/json',
                            data: json_data,
                            success: function(response) {
                                console.log(response);
                                location.reload();
                            },
                            error: function(xhr) {
                                console.log(xhr.responseText);
                            }
                        });
                        }
                        

                                function showError(error) {
                                switch(error.code) {
                                    case error.PERMISSION_DENIED:
                                    alert("User denied the request for Geolocation.");
                                    break;
                                    case error.POSITION_UNAVAILABLE:
                                    alert("Location information is unavailable.");
                                    break;
                                    case error.TIMEOUT:
                                    alert("The request to get user location timed out.");
                                    break;
                                    case error.UNKNOWN_ERROR:
                                    alert("An unknown error occurred.");
                                    break;
                                }
                                }});

                }
