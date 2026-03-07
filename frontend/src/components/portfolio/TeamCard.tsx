import { motion } from 'framer-motion';
import { Instagram, Linkedin, Globe } from 'lucide-react';
import type { TeamMember } from '../../types';

export default function TeamCard({ member }: { member: TeamMember }) {
  return (
    <motion.div whileHover={{ y: -4 }} className="text-center group">
      <div className="w-32 h-32 mx-auto mb-4 rounded-full overflow-hidden neon-border">
        <img src={member.photo} alt={member.name} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
      </div>
      <h3 className="font-semibold text-lg">{member.name}</h3>
      <p className="text-sm text-[var(--color-neon-cyan)] mb-2">{member.role}</p>
      <p className="text-xs text-[var(--color-text-secondary)] line-clamp-3 mb-3 max-w-xs mx-auto">{member.bio}</p>
      <div className="flex items-center justify-center gap-3">
        {member.instagram && <a href={member.instagram} target="_blank" rel="noopener noreferrer" className="text-[var(--color-text-secondary)] hover:text-[var(--color-neon-pink)]"><Instagram className="w-4 h-4" /></a>}
        {member.linkedin && <a href={member.linkedin} target="_blank" rel="noopener noreferrer" className="text-[var(--color-text-secondary)] hover:text-[var(--color-neon-cyan)]"><Linkedin className="w-4 h-4" /></a>}
        {member.behance && <a href={member.behance} target="_blank" rel="noopener noreferrer" className="text-[var(--color-text-secondary)] hover:text-[var(--color-neon-purple)]"><Globe className="w-4 h-4" /></a>}
      </div>
    </motion.div>
  );
}
