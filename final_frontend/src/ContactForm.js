import React from 'react';
import './contactForm.css'; 

function Contact() {
  return (
    <div className="contact" id="contact">
      <h2 className="heading">Contact <span>Us</span></h2>
      <form action="https://api.web3forms.com/submit" method="POST">
        <input type="hidden" name="access_key" value="25a2de12-4ad0-4587-b4a0-dfe4e2167d3c" />

        <div className="input-box">
          <input type="text" name="full_name" placeholder="Full Name" required />
          <input type="email" name="email" placeholder="Email" required />
        </div>

        <div className="input-box">
          <input type="tel" name="phone_number" placeholder="Phone Number" required />
          <input type="text" name="subject" placeholder="Subject" required />
        </div>

        <textarea name="message" cols="30" rows="10" placeholder="Your Message" required></textarea>

        <div className="h-captcha" data-captcha="true"></div>

        <input type="submit" value="Send Message" className="btn" />
      </form>
    </div>
  );
}
<script src="https://web3forms.com/client/script.js" async defer></script>
export default Contact;
