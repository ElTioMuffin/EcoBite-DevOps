

document.addEventListener('DOMContentLoaded',function(){
    if ('geolocation' in navigator){
        navigator.geolocation.getCurrentPosition(
            function(position){
                saveUserCordinates(position)
            },
            function(error){
                console.error(error)
            },
            //Options
            {
                enableHighAccuracy:true,
                timeout: 5000,
                maximumAge: 0
            }
        )
    }
})
