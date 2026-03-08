interface Props {
  iconName: string;
  color?: string;
  size?: number;
  className?: string;
}

export default function ModuleIcon({ iconName, color = '#00ff88', size = 24, className = '' }: Props) {
  const s = size;
  const style = { filter: `drop-shadow(0 0 4px ${color})` };

  switch (iconName) {
    case 'ufo':
      return (
        <svg width={s} height={s} viewBox="0 0 24 24" className={className} style={style}>
          <ellipse cx="12" cy="14" rx="10" ry="4" fill="none" stroke={color} strokeWidth="1.5" />
          <ellipse cx="12" cy="12" rx="6" ry="6" fill="none" stroke={color} strokeWidth="1.5" />
          <circle cx="12" cy="10" r="2" fill={color} opacity="0.6" />
          <line x1="8" y1="18" x2="6" y2="22" stroke={color} strokeWidth="1" opacity="0.4" />
          <line x1="16" y1="18" x2="18" y2="22" stroke={color} strokeWidth="1" opacity="0.4" />
          <line x1="12" y1="18" x2="12" y2="22" stroke={color} strokeWidth="1" opacity="0.4" />
        </svg>
      );
    case 'tree':
      return (
        <svg width={s} height={s} viewBox="0 0 24 24" className={className} style={style}>
          <polygon points="12,2 4,12 8,12 5,18 19,18 16,12 20,12" fill="none" stroke={color} strokeWidth="1.5" />
          <rect x="10" y="18" width="4" height="4" fill={color} opacity="0.5" />
          <circle cx="12" cy="8" r="1" fill={color} opacity="0.6" />
          <circle cx="9" cy="12" r="0.8" fill={color} opacity="0.4" />
          <circle cx="15" cy="11" r="0.8" fill={color} opacity="0.4" />
        </svg>
      );
    case 'laser':
      return (
        <svg width={s} height={s} viewBox="0 0 24 24" className={className} style={style}>
          <rect x="8" y="14" width="8" height="6" rx="1" fill="none" stroke={color} strokeWidth="1.5" />
          <line x1="12" y1="14" x2="4" y2="2" stroke={color} strokeWidth="1.5" opacity="0.8" />
          <line x1="12" y1="14" x2="20" y2="2" stroke={color} strokeWidth="1.5" opacity="0.8" />
          <line x1="12" y1="14" x2="12" y2="2" stroke={color} strokeWidth="1.5" opacity="0.6" />
          <line x1="12" y1="14" x2="2" y2="6" stroke={color} strokeWidth="1" opacity="0.4" />
          <line x1="12" y1="14" x2="22" y2="6" stroke={color} strokeWidth="1" opacity="0.4" />
        </svg>
      );
    case 'led-panel':
      return (
        <svg width={s} height={s} viewBox="0 0 24 24" className={className} style={style}>
          <rect x="3" y="3" width="18" height="18" rx="2" fill="none" stroke={color} strokeWidth="1.5" />
          {[0,1,2].map(r => [0,1,2].map(c => (
            <rect key={`${r}-${c}`} x={5+c*6} y={5+r*6} width="4" height="4" rx="0.5" fill={color} opacity={0.3 + (r+c) * 0.1} />
          )))}
        </svg>
      );
    case 'led-wash':
      return (
        <svg width={s} height={s} viewBox="0 0 24 24" className={className} style={style}>
          <circle cx="12" cy="12" r="5" fill="none" stroke={color} strokeWidth="1.5" />
          <circle cx="12" cy="12" r="2" fill={color} opacity="0.5" />
          {[0,60,120,180,240,300].map(a => (
            <line key={a} x1={12+Math.cos(a*Math.PI/180)*6} y1={12+Math.sin(a*Math.PI/180)*6} x2={12+Math.cos(a*Math.PI/180)*10} y2={12+Math.sin(a*Math.PI/180)*10} stroke={color} strokeWidth="1.5" opacity="0.5" />
          ))}
        </svg>
      );
    case 'pixel-tube':
      return (
        <svg width={s} height={s} viewBox="0 0 24 24" className={className} style={style}>
          <rect x="10" y="2" width="4" height="20" rx="2" fill="none" stroke={color} strokeWidth="1.5" />
          {[4,8,12,16].map(y => (
            <rect key={y} x="11" y={y} width="2" height="2" rx="0.5" fill={color} opacity={0.4 + (y/20) * 0.5} />
          ))}
        </svg>
      );
    case 'led-strip':
      return (
        <svg width={s} height={s} viewBox="0 0 24 24" className={className} style={style}>
          <rect x="2" y="10" width="20" height="4" rx="2" fill="none" stroke={color} strokeWidth="1.5" />
          {[4,8,12,16,20].map(x => (
            <circle key={x} cx={x} cy="12" r="1" fill={color} opacity="0.6" />
          ))}
        </svg>
      );
    case 'truss':
      return (
        <svg width={s} height={s} viewBox="0 0 24 24" className={className} style={style}>
          <rect x="3" y="3" width="18" height="18" fill="none" stroke={color} strokeWidth="1.5" />
          <line x1="3" y1="3" x2="21" y2="21" stroke={color} strokeWidth="1" opacity="0.4" />
          <line x1="21" y1="3" x2="3" y2="21" stroke={color} strokeWidth="1" opacity="0.4" />
          <line x1="12" y1="3" x2="12" y2="21" stroke={color} strokeWidth="1" opacity="0.3" />
          <line x1="3" y1="12" x2="21" y2="12" stroke={color} strokeWidth="1" opacity="0.3" />
        </svg>
      );
    case 'truss-arch':
      return (
        <svg width={s} height={s} viewBox="0 0 24 24" className={className} style={style}>
          <path d="M4 22 L4 10 Q4 2 12 2 Q20 2 20 10 L20 22" fill="none" stroke={color} strokeWidth="1.5" />
          <path d="M7 22 L7 11 Q7 5 12 5 Q17 5 17 11 L17 22" fill="none" stroke={color} strokeWidth="1" opacity="0.5" />
        </svg>
      );
    case 'totem':
      return (
        <svg width={s} height={s} viewBox="0 0 24 24" className={className} style={style}>
          <rect x="8" y="2" width="8" height="20" rx="1" fill="none" stroke={color} strokeWidth="1.5" />
          <rect x="9" y="4" width="6" height="4" rx="0.5" fill={color} opacity="0.3" />
          <rect x="9" y="10" width="6" height="4" rx="0.5" fill={color} opacity="0.4" />
          <rect x="9" y="16" width="6" height="4" rx="0.5" fill={color} opacity="0.5" />
        </svg>
      );
    case 'fog':
      return (
        <svg width={s} height={s} viewBox="0 0 24 24" className={className} style={style}>
          <path d="M3 16 Q6 12 9 16 Q12 20 15 16 Q18 12 21 16" fill="none" stroke={color} strokeWidth="1.5" opacity="0.7" />
          <path d="M3 12 Q6 8 9 12 Q12 16 15 12 Q18 8 21 12" fill="none" stroke={color} strokeWidth="1.5" opacity="0.5" />
          <path d="M5 8 Q8 4 11 8 Q14 12 17 8" fill="none" stroke={color} strokeWidth="1" opacity="0.3" />
        </svg>
      );
    case 'low-fog':
      return (
        <svg width={s} height={s} viewBox="0 0 24 24" className={className} style={style}>
          <rect x="4" y="6" width="16" height="8" rx="2" fill="none" stroke={color} strokeWidth="1.5" />
          <path d="M2 18 Q5 16 8 18 Q11 20 14 18 Q17 16 20 18 Q22 20 24 18" fill="none" stroke={color} strokeWidth="1.5" opacity="0.6" />
          <path d="M0 21 Q4 19 8 21 Q12 23 16 21 Q20 19 24 21" fill="none" stroke={color} strokeWidth="1" opacity="0.3" />
        </svg>
      );
    case 'co2':
      return (
        <svg width={s} height={s} viewBox="0 0 24 24" className={className} style={style}>
          <rect x="9" y="16" width="6" height="6" rx="1" fill="none" stroke={color} strokeWidth="1.5" />
          <line x1="12" y1="16" x2="12" y2="2" stroke={color} strokeWidth="2" opacity="0.7" />
          <circle cx="12" cy="4" r="2" fill={color} opacity="0.3" />
          <circle cx="10" cy="6" r="1.5" fill={color} opacity="0.2" />
          <circle cx="14" cy="5" r="1" fill={color} opacity="0.2" />
        </svg>
      );
    case 'confetti':
      return (
        <svg width={s} height={s} viewBox="0 0 24 24" className={className} style={style}>
          <rect x="9" y="14" width="6" height="8" rx="1" fill="none" stroke={color} strokeWidth="1.5" />
          <line x1="6" y1="12" x2="4" y2="4" stroke={color} strokeWidth="1.5" opacity="0.6" />
          <line x1="12" y1="14" x2="12" y2="2" stroke={color} strokeWidth="1.5" opacity="0.6" />
          <line x1="18" y1="12" x2="20" y2="4" stroke={color} strokeWidth="1.5" opacity="0.6" />
          <rect x="3" y="3" width="2" height="1" fill={color} opacity="0.5" transform="rotate(30 4 3.5)" />
          <rect x="11" y="1" width="2" height="1" fill={color} opacity="0.5" transform="rotate(-20 12 1.5)" />
          <rect x="19" y="3" width="2" height="1" fill={color} opacity="0.5" transform="rotate(45 20 3.5)" />
        </svg>
      );
    default:
      return (
        <svg width={s} height={s} viewBox="0 0 24 24" className={className} style={style}>
          <circle cx="12" cy="12" r="8" fill="none" stroke={color} strokeWidth="1.5" />
          <circle cx="12" cy="12" r="3" fill={color} opacity="0.5" />
        </svg>
      );
  }
}
