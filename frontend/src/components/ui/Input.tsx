import { forwardRef, type InputHTMLAttributes } from 'react';
import { clsx } from 'clsx';

interface Props extends InputHTMLAttributes<HTMLInputElement> { label?: string; error?: string; }

const Input = forwardRef<HTMLInputElement, Props>(({ label, error, className, ...p }, ref) => (
  <div className="space-y-1">
    {label && <label className="block text-sm font-medium text-[var(--color-text-secondary)]">{label}</label>}
    <input ref={ref} className={clsx('w-full px-4 py-2.5 bg-[var(--color-dark-bg)] border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-neon-green)] focus:ring-opacity-50 placeholder:text-[var(--color-text-secondary)]', error ? 'border-[var(--color-neon-pink)]' : 'border-[var(--color-dark-border)]', className)} {...p} />
    {error && <p className="text-xs text-[var(--color-neon-pink)]">{error}</p>}
  </div>
));
Input.displayName = 'Input';
export default Input;
