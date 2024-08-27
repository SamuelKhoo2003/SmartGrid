import React, { useEffect, useState } from 'react';
import TeamMembers from './TeamMembers';
import ContactUs from './ContactUs';
import abouttext from './abouttext.txt';

// Import headshot images from assets folder
import headshot1 from '../../assets/headshots/ilan.png';
import headshot2 from '../../assets/headshots/anson.JPG';
import headshot3 from '../../assets/headshots/samuel.jpg';
import headshot4 from '../../assets/headshots/lucas.png';
import headshot5 from '../../assets/headshots/eddie.png';
import headshot6 from '../../assets/headshots/justin.JPG';

const About = () => {
  const [projectDescription, setProjectDescription] = useState('');

  useEffect(() => {
    document.title = 'About | Smart Grid';

    const fetchProjectDescription = async () => {
      try {
        const response = await fetch(abouttext); // Adjust path as needed
        const text = await response.text();
        setProjectDescription(text);
      } catch (error) {
        console.error('Error fetching project description:', error);
      }
    };

    fetchProjectDescription();

  }, []);

  // Team members data
  const teamMembers = [
    {
      name: 'Ilan Iwumbwe',
      course: 'MEng EIE',
      description: "Ilan focused primarily on machine learning, designing the neural network architecture, and training models for our algorithm's machine learning component.",
      role: 'Machine Learning Engineer',
      image: headshot1,
    },
    {
      name: 'Anson Chin',
      course: 'MEng EIE',
      description: "Anson specialized in algorithm integration, combining both naive and optimized algorithms using concepts like linear programming and Model Predictive Control (MPC).",
      role: 'Algorithm Engineer',
      image: headshot2,
    },
    {
      name: 'Samuel Khoo',
      course: 'MEng EIE',
      description: "Samuel concentrated on cloud services, establishing API endpoints on AWS Lambda and developing the web application's user interface for data visualization and interaction.",
      role: 'Fullstack/Cloud Engineer',
      image: headshot3,
    },
    {
      name: 'Lucas Lasanta',
      course: 'MEng EEE',
      description: "Lucas managed the FMEA (Failure Modes and Effects Analysis) sheets for evaluating failure modes. He collaborated closely with Eddie and Justin in designing and implementing hardware circuits.",
      role: 'Hardware/Electrical Engineer',
      image: headshot4,
    },
    {
      name: 'Eddie Moualek',
      course: 'MEng EEE',
      description: "Eddie played a crucial role in circuit design and characterizing the PV array's performance. He collaborated closely with the team to ensure hardware functionality aligned with project requirements.",
      role: 'Hardware/Electrical Engineer',
      image: headshot5,
    },
    {
      name: 'Justin Lam',
      course: 'MEng EEE',
      description: "Justin collaborated with Eddie and Lucas in designing hardware circuits and adjusting SMPS (Switched-Mode Power Supply) modules to regulate voltage levels. He also contributed significantly to writing hardware code for Raspberry Pi modules.",
      role: 'Hardware/Electrical Engineer',
      image: headshot6,
    },
  ];

  return (
    <div className="about">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <h1 className="text-4xl text- font-semibold mb-4">About</h1>
        <p className="text-lg text-white mb-8">{projectDescription}</p>
        <TeamMembers members={teamMembers} />
      </div>
      <ContactUs />
    </div>
  );
};

export default About;

