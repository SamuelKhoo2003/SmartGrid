import React from 'react';

const ContactUs = () => {
  return (
    <div className="contact-us  text-white py-8" style={{ backgroundColor: '#1e1e1e' }}>
      <div className="max-w-6xl mx-auto px-4">
        <h2 className="text-3xl mb-4">Contact Us</h2>
        <p className="text-lg">For inquiries and more information:</p>
        <p className="text-lg">
          Email: <span className="italic">herecomesthesun@ic.ac.uk</span>
        </p>
        <p className="text-lg">
          Phone: <span className="italic">020 7589 5111</span>
        </p>
      </div>
    </div>
  );
};

export default ContactUs;
