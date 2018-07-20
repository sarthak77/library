function ValidateEmail(inputText,form)
{
	var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
	if(inputText.match(mailformat))
	{
		return true;
	}
	else
	{
		alert("You have entered an invalid email address!");
		return false;
	}
}

function password(input,form)
{
	var aaa=99;
	console.log(aaa);
	console.log(input);
	console.log(aaa);
	var flag=0;
	
	var lowercase = /[a-z]/g;
	if(!(input.match(lowercase)))
		flag=1;

	var uppercase = /[A-Z]/g;
	if(!(input.match(uppercase)))
		flag=1;

	var number = /[0-9]/g;
	if(!(input.match(number)))
		flag=1;

	if(input.length<8)
		flag=1;
	
	console.log(flag);
	if(flag==1)
	{
		alert("Password is not strong enough");
		return false;
	}
	else
		return true;

}

function phonenumber(inputtxt,form)
{
	var phoneno = /^\d{10}$/;
	if(inputtxt.match(phoneno))
	{
		return true;
	}
	else
	{
		alert("Not a valid Phone Number");
		return false;
	}
}

function Validatesignup()
{

	var aa;
	var ab;
	var ac;
	var x = document.getElementById("signupemail").value;
	console.log(x);
	aa=ValidateEmail(x,0);
	if(aa==false)
		return;
	

	var z = document.getElementById("signuppassword").value;
	console.log(z);
	ab=password(z,0);
	if(ab==false)
		return;
	
	
	
	var y = document.getElementById("signupphone").value;
	console.log(y);
	ac=phonenumber(y,0);
	if(ac==false)
		return;
	
	if(aa==ab==ac==true)
		check(1,0);
	else
		check(0,0);
	
}

function validateapply()
{
	var aa;
	var ab;
	var ac;
	var y = document.getElementById("applyphone").value;
	console.log(y);
	aa=phonenumber(y,1);
	console.log(aa);
	if(aa==false)
		return;
	
	console.log(aa);
	var x = document.getElementById("applypassword").value;
	console.log(x);
	ab=password(x,1);
	console.log(ab);
	if(ab==false)
		return;

	var z = document.getElementById("applyemail").value;
	ac=ValidateEmail(z,1)
	if(ac==false)
		return;

	
	var aaa=3;
	console.log(aaa);
	if(aa==ab==ac==true)
		check(1,1);
	else
		check(0,1);
}


function check(x,form)
{

	console.log(x,form);
	if(x==1)
	{
		if(form==0)
			document.getElementById("check1").style.display="inline";
		else
			document.getElementById("check0").style.display="inline";
	}
}
