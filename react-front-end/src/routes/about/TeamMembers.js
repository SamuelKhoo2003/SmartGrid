import React from 'react';

const TeamMembers = ({ members }) => {
  return (
    <div className="team-members">
      <h2 className="text-white font-semibold text-3xl mb-4">Our Team</h2>
      <div className="grid grid-cols-3 gap-4">
        {members.map((member, index) => (
          <div key={index} className="bg-gray-500 bg-opacity-50 p-4 rounded-lg">
            <img
              src={member.image}
              alt={member.name}
              className="rounded-full w-24 h-24 object-cover mx-auto mb-4 border-2 border-gray-800"
            />
            <h3 className="text-white text-xl mb-2">{member.name}</h3>
            <p className="text-gray-300 text-sm mb-1 font-semibold">{member.course}</p>
            <p className="text-gray-300"><i>{member.role}</i></p>
            <p className="text-gray-400">{member.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TeamMembers;
