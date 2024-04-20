var url="https://clapstation.herokuapp.com/home/";
function get_category_name(){
   // alert("hi")
    $.ajax ({
        url: url+"categorylist",
        type: "GET",
        contentType: 'application/json',
        // headers: {
        //           "Authorization": "Basic " + btoa(username + ":" + password)
        //           },
       
        success: function(result){
            var rowfirst = "";
            rowfirst+="<option>Select </option>";                                   
                     
                                                                       
            for (var i = 0; i < result.length; i++) {
                rowfirst += '<option value='+result[i]['name']+'>'+result[i]['name']+'</option>';

            }
            document.getElementById("signup").innerHTML=rowfirst;
       
        },               
     
       
       error: function(result) {

           alert("fail")
        
     }
   })

}


  function registration(){
   // alert("hi")
    //  var fname = document.getElementById('fname').value;
    //  var lname=document.getElementById('lname').value;
    //  var username = document.getElementById('username').value;
    //  var password=document.getElementById('password').value;
    var day=document.getElementById('day').value;
    var month=document.getElementById('month').value;
    var year=document.getElementById('year').value;
    var day1 = day.concat('-');
    var month1=day1.concat(month);
    var month2=month1.concat('-')
    var newdate=month2.concat(year)

    //var gendor=document.getElementById('gendor').value;
    var gendor=$('input[name="sex"]:checked').val();

    // alert(fname)
    // alert(newdate)

    var data = new FormData();
            data.append('first_name',document.getElementById('fname').value)
            data.append('last_name',document.getElementById('lname').value)
            data.append('username',document.getElementById('username').value)
            data.append('password',document.getElementById('password').value)
            data.append('gender',gendor)
            data.append('is_active',true)
            data.append('dob',newdate)
            data.append('user_category',document.getElementById('signup').value)
            
            
  
    //var myJSON = JSON.stringify(mainData);  
  $.ajax ({
        url: "https://clapstation.herokuapp.com/home/signup",
        type: "POST",
        enctype: 'multipart/form-data',
        
            data: data,
            processData: false,
            contentType: false,
      success: function(result){
          //var user=result['userid']
          //alert("success")
          if (result['massage']=="Data saved successfully"){
          Swal.fire({
              title: 'Congratulations!',
              text: "User registered successfully!",
              icon: 'success',
              confirmButtonText: 'Ok'
          }).then((result) => {
              if (result.value) {
                  location.reload();
                //   window.location.href="https://pharmaips.herokuapp.com/chemist/payment?userid="+user+"";

              }
          })
          }
          else if(result['massage']=="Username already register"){
              
              Swal.fire({
              title: 'Sorry!',
              text: "User with this username already registered!",
              icon: 'warning',
              confirmButtonText: 'Ok'
          }).then((result) => {
              if (result.value) {
                  location.reload();

              }
          })
          }
          else{
              alert("something went wrong")
          }
     },               
     
       
      error: function(result) {

          alert("fail")
        
     }
  })


  }


 function login() {
                 var username = document.getElementById("username").value;
				var password = document.getElementById("password").value;
				
               
               
			var mainData = {
                'username': username,
                'password':password     
             
            }
                var myJSON = JSON.stringify(mainData);  
                $.ajax ({
                url: url+"login",
                type: "POST",
                contentType: 'application/json',
                dataType: 'json',
                data: myJSON,
               success: function(result){
                   localStorage.setItem("userid", result['userid']);
                  localStorage.setItem("type", result['type']);
                  
                    Swal.fire({
              title: 'Congratulations!',
              text: "User login successfully!",
              icon: 'success',
              confirmButtonText: 'Ok'
          }).then((result) => {
              if (result.value) {
                  //location.reload
                  
                  //localStorage.setItem('userid',result['userid'])
window.location.href="http://nitd.in/clap-station/index.html";
              }
          })
      
               },
               error: function(result) {
                 
                    document.getElementById("error").innerHTML="Invalid Credentials!"

                
             }
           })
                
         
}



 function basicupdate() {
     //alert("asdf")
                 var category = document.getElementById("category1").value;
				var subcategory = document.getElementById("subcategory1").value;
				 var location = document.getElementById("location1").value;
				var budget = document.getElementById("budget1").value;
				
				
               
              // alert(budget)
			var mainData = {
                'budget': budget,
                'location':location  ,
                'category': category,
                'subcategory':subcategory  ,
                
             
            }
                var myJSON = JSON.stringify(mainData);  
                $.ajax ({
                url: url+"profilebasic?id="+  localStorage.getItem("userid")+"",
                type: "PUT",
                contentType: 'application/json',
                dataType: 'json',
                data: myJSON,
               success: function(result){
                  
                  
                    Swal.fire({
              title: 'Congratulations!',
              text: "Profile Updated successfully!",
              icon: 'success',
              confirmButtonText: 'Ok'
          }).then((result) => {
              if (result.value) {
                  location.reload()
                  
                  //localStorage.setItem('userid',result['userid'])
//window.location.href="http://nitd.in/clap-station/index.html";
              }
          })
               },
               error: function(result) {
                 
                    document.getElementById("error").innerHTML="Invalid Credentials!"

                
             }
           })
 }
 function uploadprofile()
 {
          var file=document.getElementById("file-1");
    console.log(file)
    var file = file.files[0];
    console.log(file['name'])
  
	var data = new FormData();
            data.append('profile',file)
               
                $.ajax ({
                url: url+"profilepic?id="+  localStorage.getItem("userid")+"",
                type: "PUT",
                contentType: 'multipart/form-data',
                  processData: false,
             contentType: false,
                data: data,
               success: function(result){
                  
                  
                    Swal.fire({
              title: 'Congratulations!',
              text: "Profile Updated successfully!",
              icon: 'success',
              confirmButtonText: 'Ok'
          }).then((result) => {
              if (result.value) {
                  location.reload()
                  
                 
                 
              }
          })
               },
               error: function(result) {
                   alert('faile')
                 
                    
                
             }
           })
 }
 
  function uploadphoto()
 {
//alert("asdf")
          var file=document.getElementById("file-2");
    console.log(file)
    var file = file.files[0];
    console.log(file['name'])
  
	var data = new FormData();
            data.append('photo',file),
            data.append('user',localStorage.getItem("userid"))
               
                $.ajax ({
                url: url+"profilephotos",
                type: "POST",
                contentType: 'multipart/form-data',
                  processData: false,
             contentType: false,
                data: data,
               success: function(result){
                  
                  
                    Swal.fire({
              title: 'Congratulations!',
              text: "Photo Uploaded successfully!",
              icon: 'success',
              confirmButtonText: 'Ok'
          }).then((result) => {
              if (result.value) {
                  location.reload()
                  
                 
                 
              }
          })
               },
               error: function(result) {
                   alert('faile')
                 
                    
                
             }
           })
 }
 
 
 function getartistlist(){
    //alert("hi")
    $.ajax ({
        url: url+"memberinfo?usercategory=Artist",
        type: "GET",
        contentType: 'application/json',
        // headers: {
        //           "Authorization": "Basic " + btoa(username + ":" + password)
        //           },
       
        success: function(result){
           // alert("success")
           // alert(result.length)
            
              var data="";                                                         
            for (var i = 0; i < result.length; i++) {
                	data+='<div class="col-lg-3 col-md-4 col-sm-12 col-xs-12 artist-title-col">';
					data+='	<div class="artist-box-wrap-in">';
						data+='	<div class="white-heading">';
				 		data+='		<h3>'+result[i]['first_name']+'</h3>	';
			 			data+='	</div>';
			 			data+='	<div class="admy-btn">';
				 		data+='		<button class="cmmn-btn top-left-book  slowHover" type="button" data-toggle="modal" data-target="#bookModal"><i class="fa fa-arrow-circle-right" aria-hidden="true"></i>Book</button>';
				 		data+='	</div>';
				 		
				 		data+='	<div class="posts-images artist-img">';
				 		if (result[i]['profile']==""){
				 		    data+='		<img src="images/artist.jpg">';
				 		}
				 		else{
				 		    data+='		<img src="https://res.cloudinary.com/dzdecrhc3/'+result[i]['profile']+'">';
				 		}
					 	
					 	//data+='		<p>Alienum phaedrum torquatos nec eu.</p>';
					 	data+='		    <ul>';
						 data+='			   	<li><a href="#"><i class="fa fa-thumbs-up" aria-hidden Namessss="true"></i> </a></li>';
						 data+='			   	<li><a href="#"><i class="fa fa-star" aria-hidden="true"></i></a></li>';
						 data+='			   	<li><a href="#"><i class="fa fa-commenting-o" aria-hidden="true"></i></a></li>';
						 data+='			   	<li><a href="#"><i class="fa fa-share-square-o" aria-hidden="true"></i></a></li>';
					 	data+='		    </ul>';
					 	data+='	</div>';
					 data+='	</div>	';
					data+='</div>';

            }
            document.getElementById("artist").innerHTML=data;
       
        },               
     
       
       error: function(result) {

           alert("fail")
        
     }
   })

}
function getacedmylist(){
    //alert("hi")
    $.ajax ({
        url: url+"memberinfo?usercategory=Academies",
        type: "GET",
        contentType: 'application/json',
        // headers: {
        //           "Authorization": "Basic " + btoa(username + ":" + password)
        //           },
       
        success: function(result){
            // alert("success")
            // alert(result.length)
            
              var data="";                                                         
            for (var i = 0; i < result.length; i++) {
                	data+='<div class="col-lg-3 col-md-4 col-sm-12 col-xs-12 artist-title-col">';
					data+='	<div class="artist-box-wrap-in">';
						data+='	<div class="white-heading">';
				 		data+='		<h3>'+result[i]['first_name']+'</h3>	';
			 			data+='	</div>';
			 			data+='	<div class="admy-btn">';
				 		data+='		<button class="cmmn-btn top-left-book  slowHover" type="button" data-toggle="modal" data-target="#bookModal"><i class="fa fa-arrow-circle-right" aria-hidden="true"></i>Book</button>';
				 		data+='	</div>';
				 		
				 		data+='	<div class="posts-images artist-img">';
				 		if (result[i]['profile']==""){
				 		    data+='		<img src="images/artist.jpg">';
				 		}
				 		else{
				 		    data+='		<img src="https://res.cloudinary.com/dzdecrhc3/'+result[i]['profile']+'">';
				 		}
					 	
					 	//data+='		<p>Alienum phaedrum torquatos nec eu.</p>';
					 	data+='		    <ul>';
						 data+='			   	<li><a href="#"><i class="fa fa-thumbs-up" aria-hidden Namessss="true"></i> </a></li>';
						 data+='			   	<li><a href="#"><i class="fa fa-star" aria-hidden="true"></i></a></li>';
						 data+='			   	<li><a href="#"><i class="fa fa-commenting-o" aria-hidden="true"></i></a></li>';
						 data+='			   	<li><a href="#"><i class="fa fa-share-square-o" aria-hidden="true"></i></a></li>';
					 	data+='		    </ul>';
					 	data+='	</div>';
					 data+='	</div>	';
					data+='</div>';

            }
            document.getElementById("acedmy").innerHTML=data;
       
        },               
     
       
       error: function(result) {

           alert("fail")
        
     }
   })

}

function getbandslist(){
    //alert("hi")
    $.ajax ({
        url: url+"memberinfo?usercategory=Bands",
        type: "GET",
        contentType: 'application/json',
        // headers: {
        //           "Authorization": "Basic " + btoa(username + ":" + password)
        //           },
       
        success: function(result){
            // alert("success")
            // alert(result.length)
            
              var data="";                                                         
            for (var i = 0; i < result.length; i++) {
                	data+='<div class="col-lg-3 col-md-4 col-sm-12 col-xs-12 artist-title-col">';
					data+='	<div class="artist-box-wrap-in">';
						data+='	<div class="white-heading">';
				 		data+='		<h3>'+result[i]['first_name']+'</h3>	';
			 			data+='	</div>';
			 			data+='	<div class="admy-btn">';
				 		data+='		<button class="cmmn-btn top-left-book  slowHover" type="button" data-toggle="modal" data-target="#bookModal"><i class="fa fa-arrow-circle-right" aria-hidden="true"></i>Book</button>';
				 		data+='	</div>';
				 		
				 		data+='	<div class="posts-images artist-img">';
				 		if (result[i]['profile']==""){
				 		    data+='		<img src="images/artist.jpg">';
				 		}
				 		else{
				 		    data+='		<img src="https://res.cloudinary.com/dzdecrhc3/'+result[i]['profile']+'">';
				 		}
					 	
				// 	 	data+='		<p>Alienum phaedrum torquatos nec eu.</p>';
					 	data+='		    <ul>';
						 data+='			   	<li><a href="#"><i class="fa fa-thumbs-up" aria-hidden Namessss="true"></i> </a></li>';
						 data+='			   	<li><a href="#"><i class="fa fa-star" aria-hidden="true"></i></a></li>';
						 data+='			   	<li><a href="#"><i class="fa fa-commenting-o" aria-hidden="true"></i></a></li>';
						 data+='			   	<li><a href="#"><i class="fa fa-share-square-o" aria-hidden="true"></i></a></li>';
					 	data+='		    </ul>';
					 	data+='	</div>';
					 data+='	</div>	';
					data+='</div>';

            }
            document.getElementById("bands").innerHTML=data;
       
        },               
     
       
       error: function(result) {

           alert("fail")
        
     }
   })

}
